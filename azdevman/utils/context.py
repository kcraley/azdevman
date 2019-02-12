import json
import os
import click
from vsts.vss_connection import VssConnection
from msrest.authentication import BasicAuthentication

class Context(object):

    def __init__(self):
        self._azure_devops_organization = ''
        self._personal_access_token = ''
        self._project = ''
        self._config_dir = '.azdevman'
        self._config_file = 'config.json'
        self._config_path = os.path.join(os.getenv('HOME'), self._config_dir, self._config_file)
        self.config = self._get_config()
        self.connection = self._create_connection()

    def _get_config(self):
        if os.path.isfile(self._config_path):
            with open(self._config_path, 'r') as file:
                contents = json.load(file)
                self._azure_devops_organization = contents['Azure DevOps Organization']
                self._personal_access_token = contents['Personal Access Token']
                self._project = contents['Project']

        else:
            self._init_config()

    def _init_config(self):
        if os.path.exists(os.path.dirname(self._config_path)):
            pass
        else:
            os.mkdir(os.path.dirname(self._config_path))
        with open(self._config_path, 'w') as contents:
            contents.write('')
            return contents

    def _create_connection(self):
        _credentials = BasicAuthentication('', self._personal_access_token)
        _connection_string = 'https://dev.azure.com/' + self._azure_devops_organization
        _connection = VssConnection(base_url=_connection_string, creds=_credentials)
        return _connection

pass_context = click.make_pass_decorator(Context, ensure=True)
