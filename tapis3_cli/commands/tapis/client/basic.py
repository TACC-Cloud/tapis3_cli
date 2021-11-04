import warnings

from tapipy.tapis import Tapis

from tapis3_cli import cache
from tapis3_cli.cache.client import TapisLocalCache
from tapis3_cli.formatters import FormatMany, FormatNone, FormatOne
from tapis3_cli.settings.config import config_directory

from .filter import TapisResultsDisplay

__all__ = ["BasicAuthFormatOne", "BasicAuthFormatMany", "BasicAuthCommon"]


class BasicAuthCommon(FormatNone, TapisResultsDisplay):

    tapis3_client = None
    tapis3_client_cache = None

    def add_common_arguments(self, parser):

        g = parser.add_argument_group("authentication options")

        g.add_argument(
            "-H",
            "--base-url",
            dest="base_url",
            type=str,
            metavar="URL",
            help="Tapis Base URL",
        )

        g.add_argument(
            "--username", type=str, metavar="username", help="Tapis Username"
        )

        g.add_argument(
            "--password", type=str, metavar="password", help="Tapis Password"
        )

        return parser

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = self.add_common_arguments(parser)
        return parser

    def load_client(self, parsed_args):
        """Initialize a Tapis client from local config and/or command args

        This should be called at the top of take_action()
        """
        self.tapis3_client = TapisLocalCache(
            base_url=parsed_args.base_url,
            username=parsed_args.username,
            password=parsed_args.password,
        )
        try:
            self.tapis3_client.get_tokens()
            # self.tapis3_client.refresh_tokens()
        except Exception as exc:
            warnings.warn(str(exc))

    def take_action(self, parsed_args):
        pass


class BasicAuthFormatOne(BasicAuthCommon, FormatOne):
    pass


class BasicAuthFormatMany(BasicAuthCommon, FormatMany):
    pass
