from ..client import Oauth2Common
from ...mixins import StringIdentifier


class TablesDelete(Oauth2Common, StringIdentifier):
    """Delete a table (requires table admin role)
    """
    DISPLAY_FIELDS = ['table_name', 'root_url', 'table_id', 'columns']

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
        resp = self.tapis3_client.pgrest.delete_table(table_id=table_id)
        print(resp.get('message', None))
