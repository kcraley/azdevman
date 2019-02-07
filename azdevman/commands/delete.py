import click
from azdevman.utils.context import pass_context

@click.group('delete')
@pass_context
def delete():
    """Delete Azure DevOps resources"""
    pass
