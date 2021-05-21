import os

from .helpers import int_or_none, parse_boolean

__all__ = [
    'TAPIS3_CLI_LOG_LEVEL',
    'TAPIS3_CLI_PAGE_SIZE',
    'TAPIS3_CLI_RESPONSE_FORMAT',
    'TAPIS3_CLI_FIT_WIDTH',
    'TAPIS3_CLI_DISPLAY_AUP',
    'TAPIS3_CLI_DISPLAY_COC',
]

TAPIS3_CLI_PAGE_SIZE = int_or_none(
    os.environ.get('TAPIS3_CLI_PAGE_SIZE', '100'))
TAPIS3_CLI_LOG_LEVEL = os.environ.get('TAPIS3_CLI_LOG_LEVEL', None)
TAPIS3_CLI_RESPONSE_FORMAT = os.environ.get('TAPIS3_CLI_RESPONSE_FORMAT',
                                            'table')
TAPIS3_CLI_FIT_WIDTH = parse_boolean(
    os.environ.get('TAPIS3_CLI_FIT_WIDTH', '1'))
TAPIS3_CLI_DISPLAY_AUP = parse_boolean(
    os.environ.get('TAPIS3_CLI_DISPLAY_AUP', '1'))
TAPIS3_CLI_DISPLAY_COC = parse_boolean(
    os.environ.get('TAPIS3_CLI_DISPLAY_COC', '1'))
