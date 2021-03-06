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
    """Get the current context configuration"""
    try:
        with open(ctx._config_path, 'r') as file:
            _config_contents = json.load(file)
            click.echo(json.dumps(_config_contents, sort_keys=True, indent=2))
    except json.decoder.JSONDecodeError:
        raise click.ClickException('No configuration exists.  Please run `azdevman config set-context`.')


@config.command('create-context')
@click.option('--profile', 'profile',
              help='Profile to use within the configuration')
@click.pass_obj
def create_context(ctx, profile):
    """Create a new context or update the default within the configuration"""
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


@config.command('set-context')
@click.argument('context', nargs=1, required=True)
@click.pass_context
def set_context(ctx, context):
    """Change the current context to a new one"""
    try:
        with open(ctx.obj._config_path, 'r') as file:
            _config_contents = json.load(file)
        if context in _config_contents["Profiles"]:
            _config_contents["CurrentContext"] = context
            click.echo('Set the current context to: ' + context)
        else:
            click.echo('The context does not exist in the configuration: ' + context)
        with open(ctx.obj._config_path, 'w') as file:
            json.dump(_config_contents, file, sort_keys=True, indent=2)
    except KeyError as err:
        raise click.BadArgumentUsage('The context does not exist' + err, ctx=ctx)


@config.command('delete-context')
@click.argument('context', nargs=-1)
@click.pass_obj
def delete_context(ctx, context):
    """Delete an existing context from the config file"""
    try:
        with open(ctx._config_path, 'r') as file:
            _config_contents = json.load(file)
        for profile in context:
            if _config_contents["CurrentContext"] == profile:
                _config_contents["CurrentContext"] = "default"
                click.echo('Setting current context to default')
            _config_contents["Profiles"].pop(profile, None)
            click.echo('Deleted context: ' + profile)
        with open(ctx._config_path, 'w') as file:
            json.dump(_config_contents, file, sort_keys=True, indent=2)
    except KeyError as err:
        raise click.UsageError("The profile " + err + " does not exist.")
