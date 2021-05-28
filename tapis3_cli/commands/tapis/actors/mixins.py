from tapis3_cli.commands.mixins import StringIdentifier

__all__ = ['ActorId']


class ActorId(StringIdentifier):
    service_id_type = 'actor'
    optional = False
    dest = 'actor_identifier'
