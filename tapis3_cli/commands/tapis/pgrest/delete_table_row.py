from ..client import Oauth2Common
from ...mixins import StringIdentifier

__all__ = ['RowsDelete']


class RowsDelete(Oauth2Common, StringIdentifier):
    """Delete a Row from a Table.
    """
    DISPLAY_FIELDS = []

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(parser,
                                        name='Table root URL',
                                        destination='root_url',
                                        optional=False)
        parser = super().add_identifier(parser,
                                        name='Row ID',
                                        destination='_pkid',
                                        optional=False)
        return parser

    def take_action(self, parsed_args):

        self.load_client(parsed_args)
        root_url = self.get_identifier(parsed_args, 'root_url')
        pkid = self.get_identifier(parsed_args, '_pkid')

        resp = self.tapis3_client.pgrest.delete_table_row(collection=root_url,
                                                          item=pkid)
        print(resp.get('message', None))
