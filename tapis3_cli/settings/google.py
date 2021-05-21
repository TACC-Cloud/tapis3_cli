"""Google Analytics settings
"""
import os
from hashlib import sha1

from tapis3_cli.utils import get_hostname

from .helpers import parse_boolean

__all__ = ['TAPIS3_CLI_GA_VISITOR', 'TAPIS3_CLI_GA_DISABLE']

TAPIS3_CLI_GA_VISITOR = str(
    int(
        "0x%s" % sha1(
            os.environ.get('TAPIS3_CLI_GA_VISITOR',
                           get_hostname()).encode('utf-8')).hexdigest(),
        0))[:10]

TAPIS3_CLI_GA_DISABLE = parse_boolean(
    os.environ.get('TAPIS3_CLI_GA_DISABLE', 'false'))
