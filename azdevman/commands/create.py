import click
from azdevman.utils.context import pass_context

@click.group('create')
@pass_context
def create():
    """Create Azure DevOps resources"""
    pass
