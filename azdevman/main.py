"""
Azure DevOps Manager

"""

import os
import json
import click
from azdevman.utils._const import AZDEVMAN_ENV_PREFIX
from azdevman.utils import context

__version__ = "0.0.1"
CONTEXT_SETTINGS = dict(auto_envvar_prefix=AZDEVMAN_ENV_PREFIX,
                        help_option_names=['-h', '--help'],
                        terminal_width=125)
command_plugins = os.path.join(os.path.dirname(__file__), 'commands')


class AzDevMan(click.MultiCommand):

    def list_commands(self, ctx):
        commands = []
        for filename in os.listdir(command_plugins):
            if filename.endswith('.py'):
                commands.append(filename[:-3])
        commands.sort()
        return commands

    def get_command(self, ctx, name):
        try:
            ns = {}
            fn = os.path.join(command_plugins, name + '.py')
            with open(fn) as file:
                code = compile(file.read(), fn, 'exec')
                eval(code, ns, ns)
            return ns[name]
        except FileNotFoundError:
            raise click.UsageError('`' + name + '`' + ' command does not exist.  Run `azdevman -h` for help',
                                   ctx=ctx)


# MAIN CLI GROUP
@click.command(cls=AzDevMan, context_settings=CONTEXT_SETTINGS)
@click.help_option('-h', '--help')
@click.version_option(version=__version__, prog_name='Azure DevOps Manager')
@click.pass_context
def cli(ctx):
    """Azure DevOps Manager\n

    Azdevman is a CLI tool that assists in managing resources within an Azure DevOps organization."""
    ctx.obj = context.Context()
    ctx.obj._init_config()
