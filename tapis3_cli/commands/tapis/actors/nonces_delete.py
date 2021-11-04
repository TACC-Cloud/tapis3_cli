from tapis3_cli.cache.direct import TapisDirectClient

from ...mixins import StringIdentifier
from ..client import Oauth2Common

__all__ = ["NoncesDelete"]


class NoncesDelete(Oauth2Common, StringIdentifier):
    """Delete a Nonce for an Actor."""

    def get_parser(self, prog_name):
        parser = super(NoncesDelete, self).get_parser(prog_name)
        parser = super().add_identifier(
            parser, name="Actor ID or Alias", destination="actor_id", optional=False
        )
        parser = super().add_identifier(
            parser, name="Nonce", destination="nonce_id", optional=False
        )
        parser.add_argument(
            "-A", dest="is_alias", action="store_true", help="Identifier is an Alias"
        )

        return parser

    def take_action(self, parsed_args):
        super(NoncesDelete, self).take_action(parsed_args)
        self.load_client(parsed_args)
        actor_id = parsed_args.actor_id
        nonce_id = parsed_args.nonce_id

        if parsed_args.is_alias:
            requests_client = TapisDirectClient(self.tapis3_client)
            api_path = "aliases/" + actor_id + "/nonces/" + nonce_id
            requests_client.setup("actors", api_path=api_path)
            resp = requests_client.delete()
        else:
            resp = self.tapis3_client.actors.deleteNonce(
                actor_id=actor_id, nonce_id=nonce_id
            )

        # No return as this is a delete operation
