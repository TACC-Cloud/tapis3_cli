from tapis3_cli.cache.client import TapisLocalCache
from tapis3_cli.formatters import FormatMany, FormatNone, FormatOne
from tapis3_cli.settings.auth import TAPIS3_CLI_CLIENT_FILE

from .filter import TapisResultsDisplay

__all__ = ["NoAuthCommon", "NoAuthFormatOne", "NoAuthFormatMany"]


class NoAuthCommon(FormatNone, TapisResultsDisplay):

    tapis3_client = None
    tapis3_client_cache = None

    def add_common_arguments(self, parser):
        # configuration -C, --ccnfig [default]
        # base URL -H --base-url [https://tacc.tapis.io]
        # access_token -Z, --token
        g = parser.add_argument_group("authentication options")

        g.add_argument(
            "-C",
            "--client",
            dest="client",
            default=TAPIS3_CLI_CLIENT_FILE,
            type=str,
            metavar="str",
            help="Tapis client config",
        )

        g.add_argument(
            "-H",
            "--base-url",
            dest="base_url",
            type=str,
            metavar="URL",
            help="Tapis Base URL",
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

        if parsed_args.base_url is not None:
            self.tapis3_client = TapisLocalCache(base_url=parsed_args.base_url)
        else:
            try:
                self.tapis3_client = TapisLocalCache.restore(cache=parsed_args.client)
            except Exception:
                self.tapis3_client = TapisLocalCache()

    def take_action(self, parsed_args):
        pass


class NoAuthFormatOne(NoAuthCommon, FormatOne):
    pass


class NoAuthFormatMany(NoAuthCommon, FormatMany):
    pass
