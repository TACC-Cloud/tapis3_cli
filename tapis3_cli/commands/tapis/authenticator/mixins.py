from tapis3_cli.commands.mixins import StringIdentifier

__all__ = ['ClientId']


class ClientId(StringIdentifier):
    service_id_type = 'client'
    optional = False
    dest = 'client_identifier'
