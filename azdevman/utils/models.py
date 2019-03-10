

class Models(object):

    def __init__(self):
        self.build_models = self._return_build_modles()
        self.core_models = self._return_core_models()
        self.git_models = self._return_git_models()
        self.release_models = self._return_release_models

    def _return_build_modles(self):
        """Return Azure DevOps Build models"""
        from azure.devops.v5_1.build import models
        return models

    def _return_core_models(self):
        """Return Azure DevOps Project models"""
        from azure.devops.v5_1.core import models
        return models

    def _return_git_models(self):
        """Return Azure DevOps Git models"""
        from azure.devops.v5_1.git import models
        return models

    def _return_release_models(self):
        """Return Azure DevOps release models"""
        from azure.devops.v5_1.release import models
        return models
