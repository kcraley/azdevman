"""
Azdevman Consts

This module contains constant variables that will not change
"""

# Environment Variables
AZDEVMAN_ENV_PREFIX = 'AZDEVMAN_'

# Config file
CONFIG_DIR = ".azdevman"
CONFIG_FILE_NAME = "config.json"
CONFIG_FILE_DEFAULT = {
    "CurrentContext": "default",
    "Profiles": [
        {
            "Name": "default"
        }
    ]
}

# Azure Devops
AZ_BASE_URL = 'https://dev.azure.com/'
AZ_DEFAULT_ORG = 'ORGANIZATION'
AZ_DEFAULT_PAT = 'PAT'
AZ_DEFAULT_PROJECT = 'PROJECT'
