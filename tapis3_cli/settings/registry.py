"""Container registry settings
"""
import os

from .helpers import int_or_none, parse_boolean

__all__ = [
    "TAPIS3_CLI_REGISTRY_URL",
    "TAPIS3_CLI_REGISTRY_USERNAME",
    "TAPIS3_CLI_REGISTRY_PASSWORD",
    "TAPIS3_CLI_REGISTRY_NAMESPACE",
]

# Default to public Dockerhub
TAPIS3_CLI_REGISTRY_URL = os.environ.get(
    "TAPIS3_CLI_REGISTRY_URL", "https://index.docker.io"
)

TAPIS3_CLI_REGISTRY_USERNAME = os.environ.get("TAPIS3_CLI_REGISTRY_USERNAME", None)
TAPIS3_CLI_REGISTRY_PASSWORD = os.environ.get("TAPIS3_CLI_REGISTRY_PASSWORD", None)
# Default to container registry username if not specified
TAPIS3_CLI_REGISTRY_NAMESPACE = os.environ.get(
    "TAPIS3_CLI_REGISTRY_NAMESPACE", TAPIS3_CLI_REGISTRY_USERNAME
)
