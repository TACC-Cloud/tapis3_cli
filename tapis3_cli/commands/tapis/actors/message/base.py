import argparse
import json

from tapis3_cli.utils import nrlist, split_string

from ....mixins import StringIdentifier
from ...client import Oauth2FormatOne

__all__ = ["ActorsMessage"]


class ActorsMessage(Oauth2FormatOne, StringIdentifier):
    """Base class for messaging an Actor"""

    SYNCHRONOUS_EXECUTION = False
    DISPLAY_FIELDS = ["execution_id"]

    def get_parser(self, prog_name):
        parser = super(ActorsMessage, self).get_parser(prog_name)
        parser = self.extend_parser(parser)

        mg = parser.add_mutually_exclusive_group()
        mg.add_argument(
            "-M",
            "--message",
            metavar="STRING",
            type=str,
            dest="message_str",
            help="Message Data (String)",
        )
        mg.add_argument(
            "-F",
            "--file",
            type=argparse.FileType("r"),
            metavar="FILENAME",
            dest="message_file",
            help="Message Data (JSON file)",
        )
        return parser

    def extend_parser(self, parser):

        parser = super().add_identifier(
            parser, name="Actor ID", destination="actor_id", optional=False
        )
        return parser

    def prepare_message(self, parsed_args):
        if parsed_args.message_str:
            # Load from text message
            body = parsed_args.message_str
        elif parsed_args.message_file:
            # Load from file
            file_descriptor = getattr(parsed_args, "message_file")
            # NOTE: This is the constructor for sendJSONMessage. Not using it.
            # body = {'message': json.load(file_descriptor)}
            #
            # Insted, load, stringify, and compact JSON
            body = json.dumps(
                json.load(file_descriptor), sort_keys=True, separators=(",", ":")
            )
        else:
            # Empty message
            body = ""
        return body

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        self.config = {}
        self.config["actor_id"] = parsed_args.actor_id
        self.config["_abaco_synchronous"] = self.SYNCHRONOUS_EXECUTION
        # NOTE: The OAPI spec says this is supposed to be request_body
        self.config["message"] = self.prepare_message(parsed_args)
        return [(), ()]
