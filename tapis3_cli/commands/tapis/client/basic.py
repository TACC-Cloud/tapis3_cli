from tapis3_cli.formatters import FormatOne, FormatMany
from tapis3_cli.settings.config import config_directory
from tapis3_cli import cache
from tapis3_cli.cache.client import TapisLocalCache
from tapipy.tapis import Tapis
import warnings

__all__ = ['BasicFormatOne', 'BasicFormatMany']


class BasicCommon(object):
    DISPLAY_FIELDS = []

    tapis3_client = None
    tapis3_client_cache = None

    def add_common_arguments(self, parser):

        parser.add_argument('-H',
                            '--base-url',
                            dest='base_url',
                            type=str,
                            metavar='URL',
                            help="Tapis Base URL")

        parser.add_argument('--username',
                            type=str,
                            metavar='username',
                            help="Tapis Username")

        parser.add_argument('--password',
                            type=str,
                            metavar='password',
                            help="Tapis Password")

        return parser

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = self.add_common_arguments(parser)
        return parser

    def load_client(self, parsed_args):
        """Initialize a Tapis client from local config and/or command args

        This should be called at the top of take_action()
        """
        self.tapis3_client = TapisLocalCache(base_url=parsed_args.base_url,
                                             username=parsed_args.username,
                                             password=parsed_args.password)
        try:
            self.tapis3_client.get_tokens()
            self.tapis3_client.refresh_tokens()
        except Exception as exc:
            warnings.warn(str(exc))

    def take_action(self, parsed_args):
        pass

    def filter_record_dict(self, record, formatter='table'):
        if len(self.DISPLAY_FIELDS) == 0 or formatter != 'table':
            return record
        else:
            new_record = {}
            for k, v in record.items():
                if k in self.DISPLAY_FIELDS:
                    new_record[k] = v
            return new_record


class BasicFormatOne(BasicCommon, FormatOne):
    pass


class BasicFormatMany(BasicCommon, FormatMany):
    pass
