from genericpath import exists
from tapipy.tapis import Tapis
import datetime
import json
import os

__all__ = ['TapisLocalCache']

DEFAULT_CACHE_FILE = 'client'
DEFAULT_TTL = 14400


def cache_dir():
    os.environ.get('TAPIS3_CACHE_DIR', os.path.expanduser('~/.tapis3'))


def cache_path(filename=None):
    if filename is None:
        filename = DEFAULT_CACHE_FILE
    return os.path.join(cache_dir(), filename)


class DateTimeEncoder(json.JSONEncoder):
    #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class TapisLocalCache(Tapis):
    def __init__(self, cache_dir=None, cache=None, **kwargs):
        setattr(self, 'user_tokens_cache_path',
                self.path_to_cache(cache_dir, cache))
        super().__init__(**kwargs)

    @classmethod
    def path_to_cache(cls, cache_dir=None, cache=None):
        # Cache directory resolves as:
        # 1. Provided value 2. TAPIS3_CACHE_DIR 3. ~/.tapis3
        if cache_dir is None:
            cache_dir = os.environ.get('TAPIS3_CACHE_DIR',
                                       os.path.expanduser('~/.tapis3'))
        if cache is None:
            cache = DEFAULT_CACHE_FILE
        return os.path.join(cache_dir, cache)

    @classmethod
    def restore(cls, cache_dir=None, cache=None, password=None):
        """Load Tapis from a cached client
        """
        cache_path = cls.path_to_cache(cache_dir, cache)
        with open(cache_path, 'r') as cl:
            data = json.load(cl)
        try:
            return TapisLocalCache(base_url=data['base_url'],
                                   tenant_id=data['tenant_id'],
                                   access_token=data['access_token'],
                                   refresh_token=data['refresh_token'],
                                   client_id=data['client_id'],
                                   client_key=data['client_key'],
                                   username=data['username'],
                                   verify=True)
        except Exception:
            return TapisLocalCache(base_url=data['base_url'],
                                   tenant_id=data['tenant_id'],
                                   access_token=data['access_token'],
                                   refresh_token=data['refresh_token'],
                                   client_id=data['client_id'],
                                   client_key=data['client_key'],
                                   username=data['username'],
                                   password=password,
                                   verify=True)

    def refresh_user_tokens(self):
        """Refresh access and refresh tokens then save to cache
        """
        resp = super().refresh_user_tokens()
        data = {
            'base_url': self.base_url,
            'tenant_id': self.tenant_id,
            'username': self.username,
            'client_id': self.client_id,
            'client_key': self.client_key,
            'access_token': self.access_token.access_token,
            'refresh_token': self.refresh_token.refresh_token,
            'expires_at': self.access_token.expires_at
        }
        cache_dir = os.path.dirname(self.user_tokens_cache_path)
        if not os.path.isdir(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
        with open(self.user_tokens_cache_path, 'w') as cl:
            json.dump(data, cl, cls=DateTimeEncoder, indent=4)
        return resp
