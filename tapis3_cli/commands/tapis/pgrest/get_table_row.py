from ...mixins import StringIdentifier
from ..client import Oauth2FormatOne


class RowsShow(Oauth2FormatOne, StringIdentifier):
    """Show contents of a Row in a Table."""

    DISPLAY_FIELDS = []

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(
            parser, name="Table root URL", destination="root_url", optional=False
        )
        parser = super().add_identifier(
            parser, name="Row ID", destination="_pkid", optional=False
        )

        return parser

    def take_action(self, parsed_args):

        self.load_client(parsed_args)

        root_url = self.get_identifier(parsed_args, "root_url")
        pkid = self.get_identifier(parsed_args, "_pkid")

        resp = self.tapis3_client.pgrest.get_table_row(root_url=root_url, item=pkid)

        # NOTE: get_in_collection returns a list - grab first and only item
        filt_resp = self.filter_tapis_result(resp[0], parsed_args)
        headers = self.headers_from_result(filt_resp)
        data = filt_resp.values()

        return (headers, data)
