from .mixins import ActorId
from ..client import AuthCommon

__all__ = ['ActorsDelete']


class ActorsDelete(AuthCommon, ActorId):
    """Delete an Actor
    """
    pass
    # def get_parser(self, prog_name):
    #     parser = super(ActorsDelete, self).get_parser(prog_name)
    #     parser = super(ActorId, self).extend_parser(parser)
    #     return parser
