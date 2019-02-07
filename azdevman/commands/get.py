import click
from pprint import pprint
from vsts.vss_connection import VssConnection
import vsts.exceptions
from msrest.authentication import BasicAuthentication
from azdevman.utils.context import pass_context

@click.group('get')
@click.help_option('-h', '--help')
@click.pass_obj
def get(ctx):
    """Get Azure DevOps resources"""

@get.command('projects')
@click.help_option('-h', '--help')
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
@click.help_option('-h', '--help')
@click.option('-b', '--build-id', 'build_id', type=int, default=None, required=True,
            help='Build id used to search for build')
# @click.option('-f', '--filters', 'filters', default=None,
#             help='Properties to be returned')
@click.option('-p', '--project', 'project', required=True,
            help='Project name or id to scope the search')
@click.pass_context
def get_build(ctx, project, build_id):
    """Get a single build instance or list of build instances within a project"""
    _build_client = ctx.obj.connection.get_client('vsts.build.v4_1.build_client.BuildClient')
    try:
        build = _build_client.get_build(build_id, project)
        print(build.requested_by.__dict__)
    except vsts.exceptions.VstsServiceError:
        raise click.BadParameter('a build does not exist with id: ' + str(build_id), ctx=ctx,
                                param=build_id, param_hint='--build-id')

# @get.command('builds')
# @click.help_option('-h', '--help')
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
@click.help_option('-h', '--help')
@click.option('-d', '--definition-id', 'definition_id',
                help='Definition id used to search build definitions')
@click.option('-p', '--project', 'project', required=True,
                help='Project name or id to scope the search')
@click.pass_obj
def get_build_definition(ctx, definition_id, project):
    """Get a single build definition or a list of build definitions within a project"""
    _build_client = ctx.connection.get_client('vsts.build.v4_1.build_client.BuildClient')
    try:
        build_definition = _build_client.get_definition(definition_id, project)
        print(build_definition.__dict__)
    except vsts.exceptions.VstsServiceError:
        raise click.BadParameter('a build definition does not exist with id: ' + str(definition_id), ctx=ctx,
                                param=definition_id, param_hint='--definition-id')

# @get.command('build-definitions')
# @click.help_option('-h', '--help')
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
@click.option('-r', '--release-id', 'release_id', type=int,
            help='Get a single release instance of a list of release')
@click.option('-p', '--project', 'project',
            help='Project name or id to scope the search')
@click.pass_context
def get_release(ctx, project, release_id):
    """Get a single release instance or a list of release instances within a project"""
    pass

@get.command('release-definition')
@click.option('-d', '--definition-id', 'definition_id', type=int,
            help='Get a single release instance of a list of release')
@click.option('-p', '--project', 'project',
            help='Project name or id to scope the search')
@click.pass_context
def get_release_def(ctx, project, definition_id):
    """Get a single release definition or a list of release definitions within a project"""
    pass