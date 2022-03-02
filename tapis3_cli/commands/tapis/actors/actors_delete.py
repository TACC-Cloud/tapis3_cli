from ...mixins import StringIdentifier
from ..client import Oauth2Common

__all__ = ["ActorsDelete"]


class ActorsDelete(Oauth2Common, StringIdentifier):
    """Delete an Actor."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(
            parser, name="Actor ID", destination="actor_id", optional=False
        )
        return parser

    def take_action(self, parsed_args):
        super(ActorsDelete, self).take_action(parsed_args)
        self.load_client(parsed_args)
        self.config = {}
        self.config["actor_id"] = parsed_args.actor_id
        resp = self.tapis3_client.actors.delete_actor(**self.config)
        # No return since this is Oauth2Common
