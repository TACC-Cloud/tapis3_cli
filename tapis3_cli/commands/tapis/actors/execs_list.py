import sys

from tapis3_cli.utils import nrlist, split_string

from ...mixins import LimitsArgs, StringIdentifier
from ..client import Oauth2FormatMany

__all__ = ["ActorsExecsList"]


class ActorsExecsList(Oauth2FormatMany, StringIdentifier, LimitsArgs):
    """List Executions for an Actor."""

    def get_parser(self, prog_name):
        parser = super(ActorsExecsList, self).get_parser(prog_name)
        parser = super().add_identifier(
            parser, name="Actor ID", destination="actor_id", optional=False
        )
        # TODO - reenable this once limit and offset are supported by V3 Abaco
        # parser = LimitsArgs.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        super(ActorsExecsList, self).take_action(parsed_args)
        self.load_client(parsed_args)
        self.config = {}
        self.config["actor_id"] = parsed_args.actor_id
        # if self.get_limit(parsed_args) is not None:
        #     self.config['limit'] = self.get_limit(parsed_args)
        # if self.get_offset(parsed_args) is not None:
        #     self.config['offset'] = self.get_offset(parsed_args)

        resp = self.tapis3_client.actors.listExecutions(**self.config).get("executions")

        filt_resp = self.filter_tapis_results(resp, parsed_args)
        headers = self.headers_from_result(filt_resp)
        data = []
        for item in filt_resp:
            data.append(item.values())

        return (tuple(headers), tuple(data))
