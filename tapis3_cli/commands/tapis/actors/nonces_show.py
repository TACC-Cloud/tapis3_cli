from tapis3_cli.cache.direct import TapisDirectClient
from ..client import Oauth2FormatOne
from ...mixins import LimitsArgs, StringIdentifier


class NoncesShow(Oauth2FormatOne, StringIdentifier):
    """Display details for a Nonce."""

    def get_parser(self, prog_name):
        parser = super(NoncesShow, self).get_parser(prog_name)
        parser = super().add_identifier(
            parser, name="Actor ID or Alias", destination="actor_id", optional=False
        )
        parser = super().add_identifier(
            parser, name="Nonce", destination="nonce_id", optional=False
        )
        parser.add_argument(
            "-A", dest="is_alias", action="store_true", help="Identifier is an Alias"
        )

        parser.add_argument(
            "--url", dest="show_url", action="store_true", help="Show redemption URL"
        )

        return parser

    def take_action(self, parsed_args):
        super(NoncesShow, self).take_action(parsed_args)
        self.load_client(parsed_args)
        actor_id = parsed_args.actor_id
        nonce_id = parsed_args.nonce_id

        if parsed_args.is_alias:
            requests_client = TapisDirectClient(self.tapis3_client)
            api_path = "aliases/" + actor_id + "/nonces/" + nonce_id
            requests_client.setup("actors", api_path=api_path)
            resp = requests_client.get()
        else:
            resp = self.tapis3_client.actors.getNonce(
                actor_id=actor_id, nonce_id=nonce_id
            )

        filt_resp = self.filter_tapis_result(resp, parsed_args)
        headers = [k for k in filt_resp.keys()]
        data = list(filt_resp.values())

        # Display the redemption URL. Helpful for building 3rd party
        # integrations that use Actors + their Nonces
        if parsed_args.show_url:
            headers.append("url")
            data.append(
                self.tapis3_client.base_url
                + "/v3/actors/"
                + actor_id
                + "/messages?x-nonce="
                + nonce_id
            )

        return (tuple(headers), tuple(data))
