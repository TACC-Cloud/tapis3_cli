from ..client import Oauth2FormatMany
from ...mixins import LimitsArgs


class AliasesList(Oauth2FormatMany, LimitsArgs):
    """List available Aliases
    """
    def get_parser(self, prog_name):
        parser = super(AliasesList, self).get_parser(prog_name)
        # TODO - reenable this once limit and offset are supported by V3 Abaco
        # parser = LimitsArgs.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        super(AliasesList, self).take_action(parsed_args)
        self.load_client(parsed_args)

        self.config = {}
        # if self.get_limit(parsed_args) is not None:
        #     self.config['limit'] = self.get_limit(parsed_args)
        # if self.get_offset(parsed_args) is not None:
        #     self.config['offset'] = self.get_offset(parsed_args)

        resp = self.tapis3_client.actors.listAliases(**self.config)

        filt_resp = self.filter_tapis_results(resp, parsed_args)

        headers = self.headers_from_result(filt_resp)

        data = []
        for item in filt_resp:
            data.append(item.values())

        return (tuple(headers), tuple(data))
