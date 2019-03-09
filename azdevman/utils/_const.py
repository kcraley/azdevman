"""
Azdevman Consts

This module contains constant variables that will not change
"""

# Environment Variables
AZDEVMAN_ENV_PREFIX = 'AZDEVMAN_'

# Azure Devops
AZ_BASE_URL = 'https://dev.azure.com/'
AZ_DEFAULT_ORG = 'ORGANIZATION'
AZ_DEFAULT_PAT = 'UEFUCg=='
AZ_DEFAULT_PROJECT = 'PROJECT'

# Config file
CONFIG_DIR = ".azdevman"
CONFIG_FILE_NAME = "config.json"
CONFIG_FILE_DEFAULT_PROFILE = "default"
CONFIG_FILE_DEFAULT_CONTENT = {
    "CurrentContext": CONFIG_FILE_DEFAULT_PROFILE,
    "Profiles": {
        "default": {
            "Azure DevOps Organization": AZ_DEFAULT_ORG,
            "Personal Access Token": AZ_DEFAULT_PAT,
            "Project": AZ_DEFAULT_PROJECT
        }
    }
}
