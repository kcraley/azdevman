import click
from azdevman.utils.context import pass_context

@click.group('compare')
@pass_context
def compare():
    """Compare similar Azure DevOps resources"""
    pass
