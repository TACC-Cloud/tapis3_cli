import sys

from tapis3_cli.utils import nrlist, split_string

from ...mixins import StringIdentifier
from ..client import Oauth2FormatOne

__all__ = ["ActorsExecsLogs"]


class ActorsExecsLogs(Oauth2FormatOne, StringIdentifier):
    """Get logs for an Execution."""

    def get_parser(self, prog_name):
        parser = super(ActorsExecsLogs, self).get_parser(prog_name)
        parser = self.extend_parser(parser)
        return parser

    def extend_parser(self, parser):

        parser = super().add_identifier(
            parser, name="Actor ID", destination="actor_id", optional=False
        )
        parser = super().add_identifier(
            parser, name="Execution ID", destination="exec_id", optional=False
        )
        return parser

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        self.config = {}
        self.config["actor_id"] = parsed_args.actor_id
        self.config["execution_id"] = parsed_args.exec_id
        resp = self.tapis3_client.actors.get_execution_logs(**self.config)
        logs_result = resp.get("logs")
        print("Logs for execution", self.config["execution_id"], "\n", logs_result)
        sys.exit(0)
