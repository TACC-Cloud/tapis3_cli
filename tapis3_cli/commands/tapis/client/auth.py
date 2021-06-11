from tapis3_cli.formatters import FormatNone, FormatOne, FormatMany
from tapis3_cli.settings.config import config_directory
from tapis3_cli import cache
from tapis3_cli.cache.client import TapisLocalCache
from tapipy.tapis import Tapis

__all__ = ['AuthCommon', 'AuthFormatOne', 'AuthFormatMany']


class AuthCommon(FormatNone):
    tapis3_client = None
    tapis3_client_cache = None

    def add_common_arguments(self, parser):
        # configuration -C, --ccnfig [default]
        # base URL -H --base-url [https://tacc.tapis.io]
        # access_token -Z, --token

        # parser.add_argument('-C',
        #                     '--client',
        #                     dest='client',
        #                     type=str,
        #                     metavar='str',
        #                     help="Tapis client config")

        parser.add_argument('-H',
                            '--base-url',
                            dest='base_url',
                            type=str,
                            metavar='URL',
                            help="Tapis Base URL")

        parser.add_argument('-Z',
                            '--token',
                            dest='access_token',
                            type=str,
                            metavar='token',
                            help="Tapis Access Token")

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
        # Did user provide an override?
        # URL and token
        if (parsed_args.base_url is not None
                and parsed_args.access_token is not None):
            self.tapis3_client = TapisLocalCache(
                base_url=parsed_args.base_url,
                access_token=parsed_args.access_token)
        # URL username password
        elif (parsed_args.base_url is not None
              and parsed_args.username is not None
              and parsed_args.password is not None):
            self.tapis3_client = TapisLocalCache(base_url=parsed_args.base_url,
                                                 username=parsed_args.username,
                                                 password=parsed_args.password)
        # TODO - support passing base_url and nonce
        else:
            self.tapis3_client = TapisLocalCache.restore(
                password=parsed_args.password)
            self.tapis3_client.get_tokens()
            self.tapis3_client.refresh_tokens()

    def filter_record_dict(self, record, formatter='table'):
        if len(self.DISPLAY_FIELDS) == 0 or formatter != 'table':
            return record
        else:
            new_record = {}
            for k, v in record.items():
                if k in self.DISPLAY_FIELDS:
                    new_record[k] = v
            return new_record

    def filter_tapis_result(self, tapis_response, formatter='table'):
        return self.filter_record_dict(tapis_response.__dict__, formatter)

    def filter_tapis_results(self, tapis_response, formatter='table'):
        try:
            filtered = [
                self.filter_record_dict(o.__dict__, formatter)
                for o in tapis_response
            ]
            return filtered
        except TypeError:
            # Tapipy can returns a single response from a limit/offset response if 
            # number of records == 1. This wraps it into a list
            return [self.filter_tapis_result(tapis_response, formatter)]

    def headers_from_result(self, tapis_data):
        if isinstance(tapis_data, list):
            if len(tapis_data) > 0:
                return [k for k in tapis_data[0].keys()]
            else:
                return []
        else:
            return [k for k in tapis_data.keys()]


class AuthFormatOne(AuthCommon, FormatOne):
    pass


class AuthFormatMany(AuthCommon, FormatMany):
    pass
