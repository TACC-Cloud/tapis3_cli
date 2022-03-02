from ...mixins import LimitsArgs
from ..client import Oauth2FormatMany


class ActorsList(Oauth2FormatMany, LimitsArgs):
    """List Actors."""

    DISPLAY_FIELDS = ["id", "name", "owner", "image", "lastUpdateTime", "status"]

    def get_parser(self, prog_name):
        parser = super(ActorsList, self).get_parser(prog_name)
        # TODO - reenable this once limit and offset are supported by V3 Abaco
        # parser = LimitsArgs.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        # TapisResult
        self.load_client(parsed_args)

        cmdargs = {}
        # if self.get_limit(parsed_args) is not None:
        #     cmdargs['limit'] = self.get_limit(parsed_args)
        # if self.get_offset(parsed_args) is not None:
        #     cmdargs['offset'] = self.get_offset(parsed_args)

        # TODO - add support for limit and offset
        # https://github.com/tapis-project/tapipy/blob/a62c5e9bece9e829919b1f2d0f56f25334dcc0f1/tapipy/resources/openapi_v3-actors.yml#L42
        resp = self.tapis3_client.actors.list_actors(**cmdargs)
        filt_resp = self.filter_tapis_results(resp, parsed_args)

        headers = self.headers_from_result(filt_resp)
        data = []
        for item in filt_resp:
            data.append(item.values())

        return (tuple(headers), tuple(data))
