from tapis3_cli import cache
from tapis3_cli.cache.client import TapisLocalCache
from tapis3_cli.formatters import FormatOne, FormatMany

__all__ = ['NoAuthFormatOne', 'NoAuthFormatMany']


class NoAuthFormatOne(FormatOne):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        # parser.add_argument('-C',
        #                     '--client',
        #                     dest='client',
        #                     type=str,
        #                     metavar='str',
        #                     help="Tapis client config")
        return parser

    def load_client(self, parsed_args):
        """Initialize a Tapis client from local config and/or command args

        This should be called at the top of take_action()
        """
        self.tapis3_client = TapisLocalCache.restore()


class NoAuthFormatMany(FormatMany):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        # parser.add_argument('-C',
        #                     '--client',
        #                     dest='client',
        #                     type=str,
        #                     metavar='str',
        #                     help="Tapis client config")
        return parser

    def load_client(self, parsed_args):
        """Initialize a Tapis client from local config and/or command args

        This should be called at the top of take_action()
        """
        self.tapis3_client = TapisLocalCache.restore()
