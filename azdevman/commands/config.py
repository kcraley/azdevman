import click
import json
from azdevman.utils.context import pass_context

@click.group('config')
@click.help_option('-h', '--help')
@click.pass_obj
def config(ctx):
    """Configure azdevman local options"""

@config.command('get')
@click.help_option('-h', '--help')
@click.pass_obj
def get_config(ctx):
    """Get the current configuration"""
    with open(ctx._config_path, 'r') as file:
        contents = json.load(file)
        print(json.dumps(contents, indent=4))

@config.command('set')
@click.help_option('-h', '--help')
@click.pass_obj
def set_config(ctx):
    """Set a property within the configuration"""
    configuration = {}
    configuration['Azure DevOps Organization'] = click.prompt('Azure DevOps Organization')
    configuration['Personal Access Token'] = click.prompt('Personal Access Token')

    with open(ctx._config_path, 'w') as file:
        json.dump(configuration, file)
