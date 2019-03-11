import click


@click.group('delete')
@click.pass_obj
def delete(ctx):
    """Delete Azure DevOps resources"""


@delete.command('repo')
@click.option('-p', '--project', 'project',
              help='Project name or id to create the repository in')
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
