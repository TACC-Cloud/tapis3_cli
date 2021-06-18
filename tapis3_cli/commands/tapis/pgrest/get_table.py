from ..client import AuthFormatOne
from .mixins import TableId


class TablesManageShow(AuthFormatOne, TableId):
    """Show details for one PgREST table
    """
    DISPLAY_FIELDS = ['table_name', 'root_url', 'table_id', 'columns']

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super(TableId, self).extend_parser(parser)
        return parser

    def take_action(self, parsed_args):

        self.load_client(parsed_args)
        resp = self.tapis3_client.pgrest.get_table(table_id=super(
            TableId, self).get_identifier(parsed_args),
                                                   details=True)

        filt_resp = self.filter_tapis_result(resp, parsed_args.formatter)
        headers = self.headers_from_result(filt_resp)
        data = filt_resp.values()

        return (headers, data)
