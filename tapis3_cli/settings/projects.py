"""Project configuration and build settings
"""
import os

from .helpers import int_or_none, parse_boolean

__all__ = [
    'TAPIS3_CLI_PROJECT_GIT_INIT', 'TAPIS3_CLI_PROJECT_GIT_FIRST_COMMIT',
    'TAPIS3_CLI_PROJECT_GIT_CREATE_REMOTE'
]

# Automatically init a project as a git repo
TAPIS3_CLI_PROJECT_GIT_INIT = parse_boolean(
    os.environ.get('TAPIS3_CLI_PROJECT_GIT_INIT', 'true'))

# Automatically commit initial files
#
# Defaults to TAPIS3_CLI_PROJECT_GIT_INIT
TAPIS3_CLI_PROJECT_GIT_FIRST_COMMIT = parse_boolean(
    os.environ.get('TAPIS3_CLI_PROJECT_GIT_FIRST_COMMIT', 'false'))

# Automatically create a remote for the repo
# assuming git server and credentials are available
TAPIS3_CLI_PROJECT_GIT_CREATE_REMOTE = parse_boolean(
    os.environ.get('TAPIS3_CLI_PROJECT_GIT_CREATE_REMOTE', 'false'))
