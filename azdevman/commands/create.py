import click


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
@click.pass_obj
def create_build_definition(ctx):
    """Create an Azure DevOps build definition"""
