from ..client import AuthCommon
from .mixins import TableId


class TablesManageDelete(AuthCommon, TableId):
    """Delete one PgREST table
    """
    DISPLAY_FIELDS = ['table_name', 'root_url', 'table_id', 'columns']

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super(TableId, self).extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        resp = self.tapis3_client.pgrest.delete_table(table_id=super(
            TableId, self).get_identifier(parsed_args))
        print(resp.message)
