import click
from azdevman.utils._const import (
    AZ_DEFAULT_BUILD_DEF_PROCESS,
    AZ_DEFAULT_BUILD_DEF_QUEUE
)


@click.group('create')
@click.pass_obj
def create(ctx):
    """Create Azure DevOps resources"""


@create.command('repo')
@click.option('-p', '--project', 'project',
              help='Project name or id to create the repository in')
@click.argument('repository_names', nargs=-1, required=True)
@click.pass_obj
def create_repo(ctx, project, repository_names):
    """Create an Azure DevOps repository"""
    try:
        _git_client = ctx.connection.clients.get_git_client()
        if not project:
            project = ctx._azure_devops_project
        for repo_name in repository_names:
            _git_create_options = ctx.models.git_models.GitRepositoryCreateOptions(repo_name)
            _git_client.create_repository(_git_create_options, project)
            click.echo('Created repository ' + repo_name + ' within project ' + project)
    except Exception as err:
        raise click.UsageError(err)


@create.command('build-definition')
@click.option('-f', '--copy-from', 'copy_from',
              help='Build definition to copy from')
@click.option('-r', '--repo', 'repo_name', required=True,
              help='The repository to build from')
@click.option('-p', '--project', 'project',
              help='Project name or id to create the build-definition in')
@click.argument('definition_name', nargs=1, required=True)
@click.pass_obj
def create_build_definition(ctx, definition_name, repo_name, copy_from, project):
    """Create an Azure DevOps build definition"""
    try:
        _git_client = ctx.connection.clients.get_git_client()
        _build_client = ctx.connection.clients.get_build_client()
        if not project:
            project = ctx._azure_devops_project
        try:
            # Get repository information to build BuildRepository model
            _repo = _git_client.get_repository(repo_name, project)
            _build_repo_model = ctx.models.build_models.BuildRepository(
                default_branch=_repo.default_branch,
                id=_repo.id,
                name=_repo.name,
                url=_repo.remote_url,
                type='TfsGit'
            )

            # Set default values
            _build_process = AZ_DEFAULT_BUILD_DEF_PROCESS
            _build_queue = AZ_DEFAULT_BUILD_DEF_QUEUE

            # Create base BuildDefinition model from defaults
            _build_def_model = ctx.models.build_models.BuildDefinition(
                name=definition_name,
                process=_build_process,
                repository=_build_repo_model,
                queue=_build_queue
            )

            if copy_from:
                # Get BuildDefinition properties from copied location
                _build_def = _build_client.get_definitions(project, copy_from)
                _build_def = _build_client.get_definition(project, _build_def[0].id)
                _build_process = _build_def.process
                _build_options_model = _build_def.options
                _build_queue_models = _build_def.queue
                _build_retention_model = _build_def.retention_rules
                _build_triggers = _build_def.triggers

                _build_def_model.process = _build_process
                _build_def_model.options = _build_options_model
                _build_def_model.queue = _build_queue_models
                _build_def_model.retention_rules = _build_retention_model
                _build_def_model.triggers = _build_triggers

            _new_definition = _build_client.create_definition(_build_def_model, project)
            click.echo('Created new definition: ' + _new_definition.name)
            click.echo('Link: ' + _new_definition._links.additional_properties.get('editor').get('href'))
        except Exception as err:
            raise click.UsageError(err)
    except Exception as err:
        raise click.UsageError(err)
