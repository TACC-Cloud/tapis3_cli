from tapis3_cli.cache.direct import TapisDirectClient
from ..client import Oauth2FormatOne
from ...mixins import StringIdentifier

__all__ = ["NoncesCreate"]


class NoncesCreate(Oauth2FormatOne, StringIdentifier):
    """Create a Nonce for an Actor."""

    def get_parser(self, prog_name):
        parser = super(NoncesCreate, self).get_parser(prog_name)
        parser = super().add_identifier(
            parser, name="Actor ID or Alias", destination="actor_id", optional=False
        )
        parser.add_argument(
            "-A", dest="is_alias", action="store_true", help="Identifier is an Alias"
        )

        parser.add_argument(
            "--level",
            metavar="LEVEL",
            type=str,
            required=False,
            default="EXECUTE",
            help="Optional Permission level [EXECUTE]",
        )
        parser.add_argument(
            "--max-uses",
            metavar="INT",
            type=int,
            required=False,
            default=-1,
            help="Optional Max number of redemptions [-1])",
        )
        return parser

    def take_action(self, parsed_args):
        super(NoncesCreate, self).take_action(parsed_args)
        self.load_client(parsed_args)
        actor_id = parsed_args.actor_id
        body = {"level": parsed_args.level, "maxUses": parsed_args.max_uses}

        if parsed_args.is_alias:
            requests_client = TapisDirectClient(self.tapis3_client)
            api_path = "aliases/" + actor_id + "/nonces"
            requests_client.setup("actors", api_path=api_path)
            resp = requests_client.post(data=body)
        else:
            resp = self.tapis3_client.actors.createNonce(actor_id=actor_id, body=body)

        # This is the singular form for handling ONE TapisResult

        #        filt_resp = self.filter_record_dict(resp.__dict__, parsed_args)
        filt_resp = self.filter_tapis_result(resp, parsed_args)
        headers = [k for k in filt_resp.keys()]
        data = filt_resp.values()

        return (tuple(headers), tuple(data))
