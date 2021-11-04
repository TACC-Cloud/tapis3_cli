from ...mixins import LimitsArgs, StringIdentifier
from ..client import Oauth2FormatMany


class ViewsRowsList(Oauth2FormatMany, LimitsArgs, StringIdentifier):
    """List Rows in a View."""

    DISPLAY_FIELDS = []

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(
            parser, name="View root URL", destination="root_url", optional=False
        )
        parser = LimitsArgs.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):

        self.load_client(parsed_args)
        root_url = self.get_identifier(parsed_args, "root_url")
        resp = self.tapis3_client.pgrest.get_view(
            view_name=root_url, limit=parsed_args.limit, offset=parsed_args.offset
        )
        filt_resp = self.filter_tapis_results(resp, parsed_args)

        headers = self.headers_from_result(filt_resp)
        data = []
        for item in filt_resp:
            data.append(item.values())

        return (headers, data)
