import os

from .helpers import (array_from_string, fix_assets_path, int_or_none,
                      ns_os_environ_get, parse_boolean, set_from_string)

__all__ = ['TAPIS3_CLI_DEBUG_MODE']

TAPIS3_CLI_DEBUG_MODE = parse_boolean(
    os.environ.get('TAPIS3_CLI_DEBUG_MODE', 'false'))
