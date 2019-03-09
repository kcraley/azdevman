import json
from pprint import pprint
import click
from vsts.vss_connection import VssConnection
import vsts.exceptions
from msrest.authentication import BasicAuthentication
from azdevman.utils.context import pass_context


@click.group('get')
@click.pass_obj
def get(ctx):
    """Get Azure DevOps resources"""


@get.command('projects')
@click.pass_obj
def get_projects(ctx):
    """Get all projects within an Azure DevOps organization"""
    _core_client = ctx.connection.get_client('vsts.core.v4_1.core_client.CoreClient')
    projects = _core_client.get_projects()
    print('{:<38} {:<38} {:<60}'.format('Project ID:', 'Project Name:', 'Description'))
    print('-' * 150)
    for project in projects:
        print("{!s:<38} {!s:<38} {!s:<.120}".format(project.id, project.name, project.description))


@get.command('build')
@click.option('-p', '--project', 'project',
              help='Project name or id to scope the search')
@click.argument('build_ids', nargs=-1, type=int, default=None, required=True)
@click.pass_context
def get_build(ctx, project, build_ids):
    """Get a single build instance or list of build instances within a project"""
    _build_client = ctx.obj.connection.get_client('vsts.build.v4_1.build_client.BuildClient')
    try:
        from azdevman.utils._format import transform_build_table_output
        if not project:
            project = ctx.obj._azure_devops_project
        for build_id in build_ids:
            build = _build_client.get_build(build_id, project)
            output = transform_build_table_output(build)
            click.echo(json.dumps(output, indent=2))
    except vsts.exceptions.VstsServiceError as err:
        raise click.BadArgumentUsage(err, ctx=ctx)


# @get.command('builds')
# @click.option('-d', '--definition-id', 'definition',
#                 help='Retrieve builds by definition id')
# @click.option('-p', '--project', 'project', required=True,
#                 help='Project to get builds from')
# @click.pass_obj
# def get_builds(ctx, definition, project):
#     """Get a list of builds from within a project"""
#     _build_client = ctx.connection.get_client('vsts.build.v4_1.build_client.BuildClient')
#     if definition:
#         builds = _build_client.get_definitions(project)
#     else:
#         builds = _build_client.get_builds(project)
#     for build in builds:
#         print(build)


@get.command('build-definition')
@click.option('-p', '--project', 'project',
              help='Project name or id to scope the search')
@click.option('-s', '--show-tasks', 'show_tasks', required=False, is_flag=True,
              help='Show build definition tasks as part of the output')
@click.argument('definition_ids', nargs=-1, type=int, default=None, required=True)
@click.pass_context
def get_build_definition(ctx, definition_ids, project, show_tasks):
    """Get a single build definition or a list of build definitions within a project"""
    _build_client = ctx.obj.connection.get_client('vsts.build.v4_1.build_client.BuildClient')
    try:
        from azdevman.utils._format import transform_definition_table_output
        if not project:
            project = ctx.obj._azure_devops_project
        for definition_id in definition_ids:
            build_definition = _build_client.get_definition(definition_id, project)
            # pprint(build_definition.__dict__)
            output = transform_definition_table_output(build_definition)
            click.echo(json.dumps(output, indent=2))
    except vsts.exceptions.VstsServiceError as err:
        raise click.BadArgumentUsage(err, ctx=ctx)


# @get.command('build-definitions')
# @click.option('-p', '--project', 'project', required=True,
#                 help='Project name or id to scope the search')
# @click.pass_obj
# def get_build_definitions(ctx, project):
#     """Get a single build definition from within a project"""
#     _build_client = ctx.connection.get_client('vsts.build.v4_1.build_client.BuildClient')
#     try:
#         build_definitions = _build_client.get_definitions(project)
#         for build_definition in build_definitions:
#             print(build_definition.__dict__)
#     except:
#         return


@get.command('release')
@click.option('-r', '--release-id', 'release_id',
              type=int, required=False,
              help='Get a single release instance of a list of release')
@click.option('-p', '--project', 'project',
              help='Project name or id to scope the search')
@click.pass_context
def get_release(ctx, project, release_id):
    """Get a single release instance or a list of release instances within a project"""
    _release_client = ctx.obj.connection.get_client('vsts.release.v4_1.release_client.ReleaseClient')
    try:
        release = _release_client.get_release(project, release_id)
        pprint(release.__dict__)
    except vsts.exceptions.VstsServiceError:
        raise click.BadParameter('a release definition does not exist with id: ' + str(release_id),
                                 ctx=ctx, param=release_id, param_hint='--release-id')


@get.command('release-definition')
@click.option('-d', '--definition-id', 'definition_id',
              type=int,
              help='Get a single release instance of a list of release')
@click.option('-p', '--project', 'project',
              help='Project name or id to scope the search')
@click.pass_context
def get_release_def(ctx, project, definition_id):
    """Get a single release definition or a list of release definitions within a project"""
    pass
