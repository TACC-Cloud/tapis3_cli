"""Git server settings
"""
import os

from .helpers import int_or_none, parse_boolean

__all__ = [
    'TAPIS3_CLI_GIT_USERNAME', 'TAPIS3_CLI_GIT_TOKEN',
    'TAPIS3_CLI_GIT_NAMESPACE'
]

# Default to public Github
# TAPIS3_CLI_GIT_URL = os.environ.get('TAPIS3_CLI_GIT_URL', 'https://github.com')

TAPIS3_CLI_GIT_USERNAME = os.environ.get('TAPIS3_CLI_GIT_USERNAME', None)
TAPIS3_CLI_GIT_TOKEN = os.environ.get('TAPIS3_CLI_GIT_TOKEN', None)
# Default to git server username if not specified
TAPIS3_CLI_GIT_NAMESPACE = os.environ.get('TAPIS3_CLI_GIT_NAMESPACE',
                                          TAPIS3_CLI_GIT_USERNAME)
