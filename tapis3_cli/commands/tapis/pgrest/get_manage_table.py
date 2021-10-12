from ..client import Oauth2FormatOne
from ...mixins import StringIdentifier


class TablesShow(Oauth2FormatOne, StringIdentifier):
    """Show details for a table (requires table admin role)
    """
    DISPLAY_FIELDS = ['table_name', 'comments', 'root_url', 'table_id', 'columns']

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(parser,
                                        name='Table ID',
                                        destination='table_id',
                                        optional=False)
        return parser

    def take_action(self, parsed_args):

        self.load_client(parsed_args)
        table_id = self.get_identifier(parsed_args, 'table_id')
        resp = self.tapis3_client.pgrest.get_manage_table(table_id=table_id,
                                                          details=True)

        filt_resp = self.filter_tapis_result(resp, parsed_args)
        headers = self.headers_from_result(filt_resp)
        data = filt_resp.values()

        return (headers, data)
