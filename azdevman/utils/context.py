import base64
import json
import os
import click
from azdevman.utils._const import (
    AZ_BASE_URL,
    AZ_DEFAULT_ORG,
    AZ_DEFAULT_PAT,
    AZ_DEFAULT_PROJECT,
    CONFIG_DIR,
    CONFIG_FILE_NAME,
    CONFIG_FILE_DEFAULT_CONTENT,
    CONFIG_FILE_DEFAULT_PROFILE
)
from vsts.vss_connection import VssConnection
from msrest.authentication import BasicAuthentication


class Context(object):
    """
    Click Context

    The context object which is passed to each commamnd when executed
    """

    def __init__(self):
        self._azure_base_url = AZ_BASE_URL
        self._azure_devops_organization = AZ_DEFAULT_ORG
        self._azure_devops_pat = AZ_DEFAULT_PAT
        self._azure_devops_project = AZ_DEFAULT_PROJECT
        self._config_dir = CONFIG_DIR
        self._config_file = CONFIG_FILE_NAME
        self._config_path = os.path.join(os.path.expanduser("~"), self._config_dir, self._config_file)
        self._init_config()
        self._set_current_context()
        self.config = self._get_config()
        self.connection = self._create_connection()

    def _init_config(self):
        if not os.path.exists(os.path.dirname(self._config_path)):
            os.mkdir(os.path.dirname(self._config_path))
        if not os.path.exists(self._config_path):
            with open(self._config_path, 'w') as file:
                json.dump(CONFIG_FILE_DEFAULT_CONTENT, file, sort_keys=True, indent=2)

    def _get_config(self):
        try:
            with open(self._config_path, 'r') as file:
                contents = json.load(file)
                return contents
        except KeyError:
            raise click.UsageError('Your configuration is not set. Execute `azdevman config set-context` first.')

    def _get_current_context(self):
        with open(self._config_path, 'r') as file:
            _config_contents = json.load(file)
            try:
                return _config_contents['CurrentContext']
            except KeyError as err:
                raise click.UsageError('The current context is not properly configured: ' + str(err))

    def _get_current_context_obj(self):
        _current_context = self._get_current_context()
        with open(self._config_path, 'r') as file:
            _config_contents = json.load(file)
            return _config_contents["Profiles"][_current_context]

    def _set_current_context(self):
        _current_context_obj = self._get_current_context_obj()
        self._azure_devops_organization = _current_context_obj["Azure DevOps Organization"]
        self._azure_devops_pat = _current_context_obj["Personal Access Token"]
        self._azure_devops_project = _current_context_obj["Project"]

    def _create_connection(self):
        _credentials = BasicAuthentication('', self._azure_devops_pat)
        _connection_string = self._azure_base_url + self._azure_devops_organization
        _connection = VssConnection(base_url=_connection_string, creds=_credentials)
        return _connection


pass_context = click.make_pass_decorator(Context, ensure=True)
