import os

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .helpers import (
    array_from_string,
    fix_assets_path,
    int_or_none,
    ns_os_environ_get,
    parse_boolean,
    set_from_string,
)

__all__ = [
    "TAPIS3_CLI_VERIFY_SSL",
    "TAPIS3_CLI_WARN_INSECURE_SSL",
    "TAPIS3_CLI_CLIENT_FILE",
]

# Whether Tapis API calls should verify SSL certificates. Inherits default
# from current TapisPy setting. Depends on agavepy==1.0.0a9
TAPIS3_CLI_VERIFY_SSL = parse_boolean(os.environ.get("TAPIS3_CLI_VERIFY_SSL", True))

# Disable InsecureRequestWarning
TAPIS3_CLI_WARN_INSECURE_SSL = parse_boolean(
    os.environ.get("TAPIS3_CLI_WARN_INSECURE_SSL", False)
)
if not TAPIS3_CLI_WARN_INSECURE_SSL:
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Default filename for Oauth2 client
TAPIS3_CLI_CLIENT_FILE = os.environ.get("TAPIS3_CLI_CLIENT_FILE", "client")
