import os

from .helpers import (array_from_string, fix_assets_path, int_or_none,
                      ns_os_environ_get, parse_boolean, set_from_string)

__all__ = [
    "TAPIS3_CLI_DEFAULT_BASE_URL",
    "TAPIS3_CLI_BASE_URL",
    "TAPIS3_CLI_DEFAULT_SITE_ID",
    "TAPIS3_CLI_DEFAULT_TENANT_ID",
]

# Defaults are provided for use in tapis auth init workflow
# Using environment vars allows site operators to customize default
# behavior on naive installations of the CLI
TAPIS3_CLI_DEFAULT_BASE_URL = os.environ.get(
    "TAPIS3_CLI_DEFAULT_BASE_URL", "https://tacc.tapis.io"
)

TAPIS3_CLI_DEFAULT_SITE_ID = os.environ.get("TAPIS3_CLI_DEFAULT_SITE_ID", "tacc")
TAPIS3_CLI_DEFAULT_TENANT_ID = os.environ.get("TAPIS3_CLI_DEFAULT_TENANT_ID", "tacc")

TAPIS3_CLI_BASE_URL = os.environ.get("TAPIS3_CLI_BASE_URL", TAPIS3_CLI_DEFAULT_BASE_URL)
