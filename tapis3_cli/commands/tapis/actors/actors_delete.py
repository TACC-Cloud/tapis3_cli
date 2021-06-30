from ..client import Oauth2Common
from ...mixins import StringIdentifier

__all__ = ['ActorsDelete']


class ActorsDelete(Oauth2Common, StringIdentifier):
    """Delete an Actor
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(parser,
                                        name='Actor ID',
                                        destination='actor_id',
                                        optional=False)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
