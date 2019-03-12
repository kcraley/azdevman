import click


@click.group('delete')
@click.pass_obj
def delete(ctx):
    """Delete Azure DevOps resources"""


@delete.command('repo')
@click.option('-p', '--project', 'project',
              help='Project name or id the repository in')
@click.argument('repository_names', nargs=-1, required=True)
@click.pass_obj
def create_repo(ctx, project, repository_names):
    """Delete an Azure DevOps repository"""
    try:
        click.confirm('Are you sure you want to delete these repositories?',
                      default=False, abort=True)
        _git_client = ctx.connection.clients.get_git_client()
        if not project:
            project = ctx._azure_devops_project
        for repo_name in repository_names:
            repository = _git_client.get_repository(repo_name, project)
            _git_client.delete_repository(repository.id, repository.project.name)
            click.echo('Deleted repository ' + repo_name + ' within project ' + project)
    except Exception as err:
        raise click.UsageError(err)


@delete.command('build-definition')
@click.option('-p', '--project', 'project',
              help='Project name or id the build definition in')
@click.argument('build_definitions', nargs=-1, required=True)
@click.pass_obj
def delete_build_definition(ctx, project, build_definitions):
    """Delete an Azure DevOps build definition"""
    try:
        click.confirm('Are you sure you want to delete these build definitions?',
                      default=False, abort=True)
        _build_client = ctx.connection.clients.get_build_client()
        if not project:
            project = ctx._azure_devops_project
        for build_definition in build_definitions:
            definition = _build_client.get_definitions(project, build_definition)
            _build_client.delete_definition(project, definition[0].id)
    except Exception as err:
        raise err
