"""Code for managing cached Tapis3 credentials
"""
import datetime
import json
import os

from tapipy.tapis import Tapis

from tapis3_cli.settings.config import TAPIS3_CLI_CONFIG_DIR

from . import direct

DEFAULT_CACHE_FILE = "client"
DEFAULT_TTL = 14400


class DateTimeEncoder(json.JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def cache_path(filename=None):
    if filename is None:
        filename = DEFAULT_CACHE_FILE
    return os.path.join(TAPIS3_CLI_CONFIG_DIR, filename)


def load_client(filename=None):
    """Load client from disk"""
    with open(cache_path(filename), "r") as c:
        data = json.load(c)
        try:
            t = Tapis(
                base_url=data["base_url"],
                username=data["username"],
                client_id=data["client_id"],
                client_key=data["client_key"],
                access_token=data["access_token"],
                refresh_token=data["refresh_token"],
            )
            t.get_tokens()
        except Exception:
            t = Tapis(
                base_url=data["base_url"],
                client_id=data["client_id"],
                client_key=data["client_key"],
                username=data["username"],
            )
        # Confirm - do we REALLY need this?
        # t.get_tokens()
        return t


def save_client(client, filename=None):
    """Persist a Tapis client to disk"""
    data = {
        "base_url": client.base_url,
        "username": client.username,
        "client_id": client.client_id,
        "client_key": client.client_key,
        "access_token": client.access_token.access_token,
        "refresh_token": client.refresh_token.refresh_token,
        "expires_at": client.access_token.expires_at,
        "expires_in": client.access_token.expires_in().seconds,
        "jti": client.access_token.jti,
        "tenant_id": client.tenant_id,
    }
    with open(cache_path(filename), "w") as c:
        json.dump(data, c, sort_keys=True, indent=4, cls=DateTimeEncoder)


def refresh_client(client, force=False, filename=None):
    """Update access and refresh tokens then save to disk"""
    # TODO - check expiration time and try to skip refresh cycle
    # if token is not in danger of expiring
    client.get_tokens()
    client.refresh_tokens()
    save_client(client, filename)
    return client
