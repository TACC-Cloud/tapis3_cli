from tapis3_cli.cache.direct import TapisDirectClient

from ...mixins import LimitsArgs, StringIdentifier
from ..client import Oauth2FormatOne


class ActorsShow(Oauth2FormatOne, StringIdentifier):
    """Display details for a Actor."""

    def get_parser(self, prog_name):
        parser = super(ActorsShow, self).get_parser(prog_name)
        parser = super().add_identifier(
            parser, name="Actor ID or Alias", destination="actor_id", optional=False
        )
        return parser

    def take_action(self, parsed_args):
        super(ActorsShow, self).take_action(parsed_args)
        self.load_client(parsed_args)
        actor_id = parsed_args.actor_id
        resp = self.tapis3_client.actors.getActor(actor_id=actor_id)
        filt_resp = self.filter_tapis_result(resp, parsed_args)
        headers = [k for k in filt_resp.keys()]
        data = list(filt_resp.values())

        return (tuple(headers), tuple(data))
