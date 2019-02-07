import click
from azdevman.utils.context import pass_context

@click.group('update')
@click.help_option('-h', '--help')
@click.pass_obj
def update(ctx):
    """Update Azure DevOps resources"""

@update.command('release')
@click.help_option('-h', '--help')
@click.pass_obj
def update_release(ctx):
    """Update an Azure DevOps release resource"""
    print(ctx.__dict__)
