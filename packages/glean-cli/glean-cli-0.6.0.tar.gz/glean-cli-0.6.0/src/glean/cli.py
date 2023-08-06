from contextlib import suppress
from itertools import count
import logging
import os
import string
from typing import Optional, List
from uuid import UUID, uuid3
import webbrowser
from pathlib import Path, PurePath, PurePosixPath

import click
import git
from requests import Session
import ruamel.yaml as yaml
from yaspin import yaspin

from glean import VERSION

from glean.filesystem import local_resources
from glean.credentials import get_credentials
from glean.glean_api import (
    build_details_uri,
    clear_model_cache,
    create_build_from_git_revision,
    create_build_from_local_files,
    login,
    preview_model_uri,
    get_datasources,
    get_tables,
    get_model_and_build_summary,
    export_query,
    pull_resource,
)
from glean.utils.cli import cli_error_boundary, getenv_bool
from glean.utils.grn import GRN_TYPE_KEY_MODEL, GRNComponents, parse_grn
from glean.utils.resource import Resource


GLEAN_DEBUG = getenv_bool("GLEAN_DEBUG")

# Turning this on will result in secrets getting logged to stdout.
GLEAN_VERBOSE_DEBUG_UNSAFE = getenv_bool("GLEAN_VERBOSE_DEBUG_UNSAFE")


MAX_COLUMN_REGEX_LENGTH = 30
MAX_COLUMN_FILTER_CHARS = 1000


def main():
    with cli_error_boundary(debug=GLEAN_DEBUG):
        if not _check_version():
            logging.warn(
                "There is a newer version of the Glean CLI available on PyPI. Upgrade your glean-cli package for the latest features.\n"
            )

        cli()


git_revision_option = click.option(
    "--git-revision",
    type=str,
    required=False,
    help="""
    If specified, Glean will pull configuration files from your configured git repository at the provided commit,
    instead of using local files.
    """,
)
git_path_option = click.option(
    "--git-path",
    type=str,
    required=False,
    help="""
    A path within your git repo that will be used as the top-level directory for the Build.
    Only applicable when also using the `--git-revision` flag.
    """,
)
dbt_manifest_option = click.option(
    "--dbt-manifest",
    "dbt_manifest_path",
    required=False,
    # TODO(meyer): unhide when feature is stable
    hidden=True,
    help="Path to dbt manifest JSON file (if using Glean dbt integration).",
    type=click.Path(exists=True, readable=True, file_okay=True, dir_okay=False),
)
local_path_argument = click.argument(
    "filepath", type=click.Path(exists=True), default="."
)


@click.group(context_settings=dict(max_content_width=130))
@click.version_option(version=VERSION, prog_name="Glean")
@click.option(
    "--credentials-filepath",
    type=str,
    default="~/.glean/glean_access_key.json",
    show_default=True,
    help="Path to your Glean access key credentials. You can also control this by setting a "
    "GLEAN_CREDENTIALS_FILEPATH environment variable.",
    envvar="GLEAN_CREDENTIALS_FILEPATH",
)
@click.option(
    "--allow-dangerous-empty-build",
    is_flag=True,
    default=False,
    help="Allow builds with no config files. WARNING: this will allow a build to delete all of your resources, including non-dataops resources that depend on your dataops resources!",
)
@click.pass_context
def cli(ctx, credentials_filepath, allow_dangerous_empty_build=False):
    """A command-line interface for interacting with Glean."""
    if GLEAN_DEBUG or GLEAN_VERBOSE_DEBUG_UNSAFE:
        _enable_http_logging()

    ctx.ensure_object(dict)
    ctx.obj["allow_dangerous_empty_build"] = allow_dangerous_empty_build
    ctx.obj["credentials"] = get_credentials(os.path.expanduser(credentials_filepath))


@cli.command()
@git_revision_option
@git_path_option
@dbt_manifest_option
@local_path_argument
@click.pass_context
def preview(ctx, git_revision, git_path, dbt_manifest_path, filepath):
    """Validates resource configurations and generates a preview link."""
    click.echo("🏗️  Creating preview build...")
    build_results = _create_build_using_options(
        ctx,
        filepath,
        git_revision=git_revision,
        git_path=git_path,
        deploy=False,
        dbt_manifest_path=dbt_manifest_path,
    )
    _echo_build_results(build_results, False)


@cli.command()
@git_revision_option
@git_path_option
@dbt_manifest_option
@local_path_argument
@click.option(
    "--preview / --no-preview",
    default=True,
    help="Whether to generate a Preview Build before deploying.",
)
@click.pass_context
def deploy(
    ctx: click.Context,
    git_revision: Optional[str],
    git_path: Optional[str],
    dbt_manifest_path: Optional[PurePath],
    filepath: str,
    preview: bool,
):
    """Validates and deploys resource configurations to your project."""

    if preview:
        click.echo("🏗️  Creating preview build...")
        build_results = _create_build_using_options(
            ctx,
            filepath,
            git_revision=git_revision,
            git_path=git_path,
            deploy=False,
            dbt_manifest_path=dbt_manifest_path,
        )
        _echo_build_results(build_results, False)
        click.echo("")
        if not click.confirm("Continue with deploy?"):
            exit(1)

    click.echo("🚀 Creating deploy build...")
    build_results = _create_build_using_options(
        ctx,
        filepath,
        git_revision=git_revision,
        git_path=git_path,
        deploy=True,
        dbt_manifest_path=dbt_manifest_path,
    )
    _echo_build_results(build_results, True)
    click.echo("")
    click.echo(click.style("✅ Deploy complete.", fg="bright_green"))


@cli.command()
@click.pass_context
def databases(ctx):
    """See your available database connections.

    A database connection can be added in the Settings tab on glean.io."""
    s = Session()
    project_id = login(s, ctx.obj["credentials"])

    datasources = get_datasources(s, project_id)
    _echo_datasources(datasources)


@cli.command()
@click.argument("database")
@click.pass_context
def tables(ctx, database):
    """Specify a database connection and see its available tables."""
    s = Session()
    project_id = login(s, ctx.obj["credentials"])

    datasources = get_datasources(s, project_id)
    if database not in datasources:
        _echo_datasource_not_found(database, datasources)
        exit(1)

    datasource_id = datasources[database]

    tables = get_tables(s, datasource_id)
    table_names = list(tables.keys())
    _echo_tables(table_names, database)


@cli.group()
@click.pass_context
def cache(ctx):
    """Glean stores the results of queries in a cache so that users don't have
    to access the database again."""
    pass


@cache.command("clear")
@click.argument("resource_grn")
@click.pass_context
def cache_clear(ctx, resource_grn):
    """Clears the cache for the associated resource."""
    s = Session()
    login(s, ctx.obj["credentials"])

    grn = parse_grn(resource_grn)
    if not grn.gluid:
        click.echo("GRN must specify an id when clearing cache.")
        exit(1)
    if grn.resource_type != GRN_TYPE_KEY_MODEL:
        click.echo("Cache can only be cleared for models.")
        exit(1)

    clear_model_cache(s, grn.gluid)
    click.echo(f"Successfully cleared cache for {resource_grn}.")


@cli.command()
@click.argument("grn", required=False, type=str)
@click.option(
    "--allow-dirty",
    is_flag=True,
    default=False,
    help="Overwrite resources even if the working directory has changes",
)
@click.pass_context
def pull(
    ctx: click.Context,
    grn: str,
    allow_dirty: bool = False,
):
    """Pull the latest DataOps resource configuration from Glean into the working directory.

    GRN is the Glean resource name of the target resource. If the resource has DataOps dependencies, they will also be
    retrieved. If no GRN is specified, all resources for the project are pulled.
    """

    try:
        repo = git.Repo(Path("."), search_parent_directories=True)
        if repo.is_dirty() and not allow_dirty:
            raise click.ClickException(
                "️🚩 The working directory has uncommitted changes that might be overwritten. (Skip this check with --allow-dirty.)"
            )
    except git.InvalidGitRepositoryError:
        click.confirm(
            "The working directory is not a Git repository; this operation may irreversibly change files. Proceed?",
            default=False,
            abort=True,
            show_default=True,
        )

    s = Session()
    project_id = login(s, ctx.obj["credentials"])

    resource_type = None
    resource_id = None

    # map the GRN resource type abbreviation to the full name
    RESOURCE_TYPE_FROM_ABBREV = {
        "dsb": "dashboard",
        "sv": "savedView",
        "m": "model",
        "palette": "colorPalette"
        # todo: support for launch config, collections...
    }
    if grn:
        grn_components = parse_grn(grn)

        # TODO(meyer): add support for aliases
        try:
            resource_type = RESOURCE_TYPE_FROM_ABBREV[grn_components.resource_type]
        except:
            raise click.ClickException(
                "Glean pull currently only supports models, saved views, dashboards, and color palettes"
            )
        resource_id = grn_components.gluid

    SUPPORTED_TYPES = ["dashboard", "saved_view", "model", "color_palette"]
    local_by_path = {
        k: v for k, v in local_resources(Path(".")).items() if v.type in SUPPORTED_TYPES
    }

    def get_grn(path: PurePosixPath, resource: Resource) -> GRNComponents:
        RESOURCE_TYPE_TO_ABBREV = {
            "model": "m",
            "saved_view": "sv",
            "dashboard": "dsb",
            "color_palette": "palette",
            # TODO(meyer): support for the other resources
        }
        if resource.grn is not None:
            return resource.grn

        elif resource.type == "saved_view":
            # terrible special case logic for saved views to maintain backwards compatibility,
            # since saved view IDs include a hash of the model ID

            model_ref: str = resource.raw["model"]
            model_grn = None
            try:
                # resolve model references by file paths to their project-local path
                model_path = (
                    Path(path.parent / model_ref).resolve().relative_to(Path.cwd())
                )
                if model_path.exists():
                    model = local_by_path[PurePosixPath(model_path)]
                    assert model is not None
                    model_grn = get_grn(PurePosixPath(model_path), model)
            except OSError:  # python 3.7, Path.exists can throw if the path is invalid
                pass
            except ValueError:
                pass

            # if model is not a local path, it must be a GRN
            if not model_grn:
                model_grn = parse_grn(model_ref)

            model_id = model_grn.gluid
            assert model_id is not None

            default_namespace = UUID("{00000000-0000-0000-0000-000000000000}")
            initial_id = GRNComponents.generate("sv", project_id, path).gluid
            assert initial_id is not None
            sv_id = str(uuid3(default_namespace, model_id + initial_id))

            return GRNComponents("sv", sv_id)

        else:
            return GRNComponents.generate(
                RESOURCE_TYPE_TO_ABBREV[resource.type], project_id, path
            )

    # Can't use a map here because we actually _do_ want to compare GRNs that hash to different values!
    # In particular, if they have the same type/alias but different guid (because local hasn't received a guid),
    # they should be considered equal.
    local_by_grn = list(
        (get_grn(path, resource), path, resource)
        for (path, resource) in local_by_path.items()
    )
    local_grns = list(local_grn for (local_grn, _, _) in local_by_grn)

    result = pull_resource(s, project_id, resource_type, resource_id)
    if result.get("errors"):
        _echo_pull_errors_and_exit(result["errors"])
        return

    remote: list[Resource] = result["configs"]

    updated_files = []
    for resource in remote:
        assert resource.grn is not None
        with suppress(ValueError):
            index = local_grns.index(resource.grn)
            # we've matched the resource to a local file
            (_, path, local_resource) = local_by_grn[index]
            if local_resource.raw == resource.raw:
                continue

            updated_files.append(Path(path))
            # the resource has changed!
            with open(Path(path), "w") as f:
                yaml.dump(resource.raw, f, Dumper=yaml.RoundTripDumper)

            continue

        # not present locally, so we need to make a new file
        name = "".join(
            filter(
                lambda x: x in string.ascii_letters or x in string.digits,
                resource.raw.get("name", "untitled").lower().replace(" ", "_"),
            )
        )
        name = resource.grn.resource_type + "_" + name
        for i in count(0):
            if i > 0:
                path = Path(f"{name}_{i}.yml")
            else:
                path = Path(f"{name}.yml")
            if path.exists():
                continue

            updated_files.append(path)
            with open(path, "w") as f:
                yaml.dump(resource.raw, f, Dumper=yaml.RoundTripDumper)

            break

    click.echo()
    if updated_files:
        click.echo("✅ Done. Files created or modified:")
        _echo_list([str(p) for p in updated_files])
    else:
        click.echo("✅ Done. No files were updated.")


@cli.command()
@click.argument("database")
@click.argument("table")
@click.option(
    "--exclude",
    "-e",
    help="A comma-separated list of columns to exclude from the preview.",
)
@click.option(
    "--include",
    "-i",
    help="A comma-separated list of columns to include in the preview.",
)
@click.option(
    "--regex",
    "-r",
    help="A regular expression to filter column names by. You can use this along with the --include and/or --exclude options to include columns regardless of the regex result.",
)
@click.option(
    "--skip-confirmation",
    is_flag=True,
    help="If set, the generated model configuration file will silently overwrite any existing files with the same name in your current directory.",
)
@click.pass_context
def explore(
    ctx: click.Context,
    database: str,
    table: str,
    exclude: str = "",
    include: str = "",
    regex: str = "",
    skip_confirmation: bool = False,
):
    """Explore your data! Specify a database and table to generate a Glean preview for it.

    DATABASE is the name of a Glean database connection you want to explore.
    TABLE is the name of a table within your DATABASE. Alternatively, it can be a SQL query wrapped in quotes.

    Usage examples:

    $ glean explore database_connection_name table_name

    $ glean explore database_connection_name "SELECT * FROM table_name"

    $ glean explore database_connection_name table_name --regex "[^date]$" --include important_date --exclude extra_info

    """
    s = Session()
    project_id = login(s, ctx.obj["credentials"])

    datasources = get_datasources(s, project_id)
    if database not in datasources:
        _echo_datasource_not_found(database, datasources)
        exit(1)
    datasource_id = datasources[database]

    _limit_column_filters(exclude, include, regex)

    model_spec = {
        "columnsToExclude": exclude.split(",") if exclude else [],
        "columnsToInclude": include.split(",") if include else [],
        "columnsRegex": regex if regex else "",
    }

    if not _infer_if_sql(table):
        tables = get_tables(s, datasource_id)
        if table not in tables:
            _echo_table_not_found(table, tables, database)
            exit(1)

        with yaspin(text="Generating your data model...", color="yellow") as spinner:
            model_spec["schema"] = tables[table]["schema"]
            model_spec["tableName"] = tables[table]["name"]
            model, build_summary = get_model_and_build_summary(
                s, datasource_id, project_id, **model_spec
            )
    else:
        with yaspin(text="Generating your data model...", color="yellow") as spinner:
            model_spec["sqlStatement"] = table
            model, build_summary = get_model_and_build_summary(
                s, datasource_id, project_id, **model_spec
            )

    config = export_query(
        s, "model", model, additional_headers={"Content-Type": "yaml"}
    )
    model_yaml = yaml.load(config, Loader=yaml.RoundTripLoader)
    if "grn" in model_yaml:
        del model_yaml["grn"]
    config = yaml.dump(model_yaml, Dumper=yaml.RoundTripDumper)

    filename = model["name"]
    _save_config(config, filename, skip_confirmation=skip_confirmation)

    _echo_build_results(build_summary, False, query_name="modelPreviewBuildFromGleanDb")
    webbrowser.open(preview_model_uri(model["id"], build_summary))


def _infer_if_sql(table: str) -> bool:
    """
    Guesses if the table input is a table or a SQL query.
    """
    return bool(table.count(" ") >= 3 and "select" in table.lower())


def _limit_column_filters(
    exclude: Optional[str], include: Optional[str], regex: Optional[str]
) -> None:
    """
    This limits column filter inputs to a reasonable size.
    There are the same checks server-side; this is for better user error messaging.
    """
    if exclude and include and not regex:
        click.secho(
            "Can't specify both columns to include and columns to exclude without a regex.",
            fg="red",
        )
        exit(1)
    if regex and len(regex) > MAX_COLUMN_REGEX_LENGTH:
        click.secho(
            f"Regex input is too long — it should be {MAX_COLUMN_REGEX_LENGTH} characters or less.",
            fg="red",
        )
        exit(1)
    if include and len(include) > MAX_COLUMN_FILTER_CHARS:
        click.secho(
            f"The list of columns to include should be less than {MAX_COLUMN_FILTER_CHARS} characters.",
            fg="red",
        )
        exit(1)
    if exclude and len(exclude) > MAX_COLUMN_FILTER_CHARS:
        click.secho(
            f"The list of columns to exclude should be less than {MAX_COLUMN_FILTER_CHARS} characters.",
            fg="red",
        )
        exit(1)


def _save_config(
    config: str, name: str, config_type: str = "yml", skip_confirmation: bool = False
) -> None:
    """Confirms with user and writes config file to user's local directory"""
    filename = f"{name}.{config_type}"
    click.echo("")
    click.echo(
        "Saving a model configuration file as "
        + click.style(f"{filename}", bold=True)
        + " in this directory."
    )

    write = True
    if os.path.exists(filename):
        if not skip_confirmation:
            if not click.confirm(
                "A file named "
                + click.style(f"{filename}", bold=True)
                + " already exists. Do you want to overwrite it?"
            ):
                write = False
                click.echo("")
                click.echo(
                    "Your preview build was generated, but a model configuration file was not saved."
                )

    if write:
        with open(filename, "w") as config_file:
            config_file.write(config)

    click.echo("")


def _create_build_using_options(
    ctx: click.Context,
    filepath: str,
    dbt_manifest_path: Optional[PurePath] = None,
    git_revision: Optional[str] = None,
    git_path: Optional[str] = None,
    deploy: bool = False,
    targets: Optional[set] = None,
):
    s = Session()
    project_id = login(s, ctx.obj["credentials"])
    allow_dangerous_empty_build = ctx.obj["allow_dangerous_empty_build"]
    if git_revision:
        return create_build_from_git_revision(
            s,
            project_id,
            git_revision,
            git_path,
            deploy,
            allow_dangerous_empty_build=allow_dangerous_empty_build,
            dbt_manifest_path=dbt_manifest_path,
        )
    else:
        return create_build_from_local_files(
            s,
            project_id,
            filepath,
            deploy,
            targets,
            allow_dangerous_empty_build=allow_dangerous_empty_build,
            dbt_manifest_path=dbt_manifest_path,
        )


def _echo_tables(table_names: list, datasource: str) -> None:
    click.secho(f"📂 Available Tables From {datasource}", fg="bright_green")
    _echo_list(table_names)


def _echo_table_not_found(table: str, tables: dict, datasource: str) -> None:
    """If table is not found in the available tables, output warning and display available tables."""
    click.echo("")
    click.secho(f"❗{table} was not found in {datasource}'s tables.", fg="red")
    click.echo("")
    _echo_tables(list(tables.keys()), datasource)
    click.echo("")


def _echo_datasources(datasources: dict) -> None:
    click.secho("🗒  Available Database Connections ", fg="bright_green")
    _echo_list(list(datasources.keys()))


def _echo_datasource_not_found(datasource: str, datasources: dict) -> None:
    """If datasource not found, output warning and available datasources."""
    click.echo("")
    click.secho(f"❗{datasource} was not found in your database connections.", fg="red")
    click.echo("")
    _echo_datasources(datasources)
    click.echo("")
    click.echo(
        "You can add another database connection in your Settings tab on glean.io."
    )
    click.echo("")


def _echo_build_results(build_results: dict, deploy: bool, query_name="createBuild"):
    """Outputs user-friendly build results."""
    if "errors" in build_results and build_results["errors"]:
        _echo_build_errors_and_exit(
            [
                e["extensions"]["userMessage"]
                for e in build_results["errors"]
                if "extensions" in e and "userMessage" in e["extensions"]
            ]
        )
    created_build_results = build_results["data"][query_name]

    if created_build_results["errors"]:
        _echo_build_errors_and_exit(created_build_results["errors"])

    click.echo(
        click.style("📦 Build ", fg="bright_green")
        + click.style(created_build_results["id"], bold=True)
        + click.style(" created successfully.", fg="bright_green")
    )
    click.echo("")

    if created_build_results["warnings"]:
        _echo_build_warnings(created_build_results["warnings"])

    _echo_build_resources(created_build_results["resources"], deploy)
    click.echo("")
    click.echo(f"Details: {build_details_uri(build_results, query_name=query_name)}")


def _echo_pull_errors_and_exit(errors: List[str]):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    click.echo("❗ Errors encountered when pulling resources")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    if not errors:
        errors = ["Something went wrong, please contact Glean for support."]
    _echo_list(errors, color="red")
    click.echo("")
    click.secho("Pull failed. No files were changed.", fg="red")
    exit(1)


def _echo_build_errors_and_exit(errors: List[str]):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    click.echo("❗ Errors encountered when creating your build")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="red")
    if not errors:
        errors = ["Something went wrong, please contact Glean for support."]
    _echo_list(errors, color="red")
    click.echo("")
    click.secho("Build failed.", fg="red")
    exit(1)


def _echo_build_warnings(warnings: List[str]):
    click.echo("")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="yellow")
    click.echo(" ⚠️  Warnings encountered when creating your build")
    click.secho("―――――――――――――――――――――――――――――――――――――――――――――――――", fg="yellow")
    if not warnings:
        warnings = ["Warning message missing, please contact Glean for support."]
    _echo_list(warnings, color="yellow")
    click.echo("")


def _echo_list(items: List[str], color="white"):
    for item in items:
        lines = item.split("\n")
        click.echo(click.style("*", fg=color) + "  " + lines[0])
        for line in lines[1:]:
            click.echo("   " + line)


def _echo_resources_with_status(resources: dict, status: str, title: str):
    models = resources[status]["models"]
    saved_views = resources[status]["savedViews"]
    dashboards = resources[status]["dashboards"]
    color_palettes = resources[status]["colorPalettes"]
    homepage_launchpads = resources[status]["homepageLaunchpads"]

    combinedResources = (
        models + saved_views + dashboards + color_palettes + homepage_launchpads
    )

    if combinedResources:
        click.echo(title)
        _echo_list(
            [
                click.style("Model - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in models
            ]
        )
        _echo_list(
            [
                click.style("View - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in saved_views
            ]
        )
        _echo_list(
            [
                click.style("Dashboard - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in dashboards
            ]
        )
        _echo_list(
            [
                click.style("Color Palette - ", fg="bright_black")
                + click.style(r["name"], fg="white")
                for r in color_palettes
            ]
        )
        _echo_list(
            [
                click.style("Homepage Launchpad", fg="bright_black")
                for _ in homepage_launchpads
            ]
        )
        click.echo()


def _echo_build_resources(resources: dict, deploy: bool):
    added = click.style("Added:" if deploy else "Will add:", bold=True, fg="green")
    _echo_resources_with_status(resources, "added", added)

    updated = click.style(
        "Updated:" if deploy else "Will update:", bold=True, fg="cyan"
    )
    _echo_resources_with_status(resources, "changed", updated)

    deleted = click.style("Deleted:" if deploy else "Will delete:", bold=True, fg="red")
    _echo_resources_with_status(resources, "deleted", deleted)

    not_modified = click.style("Unchanged:", bold=True)
    _echo_resources_with_status(resources, "unchanged", not_modified)


def _enable_http_logging():
    # From: https://docs.python-requests.org/en/master/api/#api-changes
    from http.client import HTTPConnection

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    if GLEAN_VERBOSE_DEBUG_UNSAFE:
        HTTPConnection.debuglevel = 1


def _check_version():
    from pathlib import Path
    import time, requests

    ttl = 24 * 60 * 60
    path = Path.home() / ".glean" / ".cache" / "version"

    try:
        os.makedirs(path.parent, exist_ok=True)
    except:
        # Could be a permissions issue, or hard drive full, or weird cosmic bit flip...
        # Just assume we're up-to-date.
        return True

    try:
        prev_mtime = os.path.getmtime(path)
    except Exception:
        prev_mtime = None

    if prev_mtime is None or time.time() - prev_mtime > ttl:
        # delete stale cache
        try:
            path.unlink()  # missing_ok not available in Python 3.7
        except:
            pass

    try:
        with open(path, "r") as f:
            return VERSION == f.readline().strip()
    except:
        pass

    # cache was stale or did not exist; fetch from pypi
    try:
        with open(path, "w+") as f:
            PACKAGE_JSON_URL = "https://pypi.org/pypi/glean-cli/json"
            resp = requests.get(PACKAGE_JSON_URL, timeout=1)
            data = resp.json()
            LATEST_VERSION: str = list(data["releases"].keys())[-1]
            f.write(LATEST_VERSION)
            return VERSION == LATEST_VERSION
    except Exception as e:
        logging.warn(
            f"Unable to check whether this is the latest version of the CLI: {e}."
        )
        # Unable to pull version information currently, just return true
        return True
