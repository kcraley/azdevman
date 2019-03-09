import click
import json
from azdevman.utils.context import pass_context


@click.group('config')
@click.pass_obj
def config(ctx):
    """Configure azdevman local options"""


@config.command('current-context')
@click.pass_obj
def get_current_context(ctx):
    """Return the current context from the config file"""
    _current_context = ctx._get_current_context()
    click.echo(_current_context)


@config.command('get-context')
@click.pass_obj
def get_contexts(ctx):
    """Get the current configuration"""
    try:
        with open(ctx._config_path, 'r') as file:
            _config_contents = json.load(file)
            click.echo(json.dumps(_config_contents, sort_keys=True, indent=2))
    except json.decoder.JSONDecodeError:
        raise click.ClickException('No configuration exists.  Please run `azdevman config set-context`.')


@config.command('set-context')
@click.option('--profile', 'profile',
              help='Profile to use within the configuration')
@click.pass_obj
def set_context(ctx, profile):
    """Set a property within the configuration"""
    with open(ctx._config_path, 'r') as file:
        _config_contents = json.load(file)
    if profile:
        _config_contents['Profiles'][profile] = {}
    else:
        profile = "default"
    _config_contents['Profiles'][profile]['Azure DevOps Organization'] = click.prompt('Azure DevOps Organization')
    _config_contents['Profiles'][profile]['Personal Access Token'] = ctx._base64_encoder(click.prompt('Personal Access Token'))
    _config_contents['Profiles'][profile]['Project'] = click.prompt('Project')
    with open(ctx._config_path, 'w') as file:
        json.dump(_config_contents, file, sort_keys=True, indent=2)


@config.command('delete-context')
@click.argument('context', nargs=-1)
@click.pass_obj
def delete_context(ctx, context):
    """Delete an existing context from the config file"""
    try:
        with open(ctx._config_path, 'r') as file:
            _config_contents = json.load(file)
        for profile in context:
            _config_contents["Profiles"].pop(profile, None)
        with open(ctx._config_path, 'w') as file:
            json.dump(_config_contents, file, sort_keys=True, indent=2)
            click.echo('Deleted context: ' + profile)
    except KeyError as err:
        raise click.UsageError("The profile " + err + " does not exist.")
