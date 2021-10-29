from ..client import Oauth2FormatOne
from ...mixins import JSONArg, StringIdentifier

__all__ = ['RowsCreate']


class RowsCreate(Oauth2FormatOne, JSONArg, StringIdentifier):
    """Create a Row in a Table.
    """
    DISPLAY_FIELDS = []

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(parser,
                                        name='Table root URL',
                                        destination='root_url',
                                        optional=False)
        parser = super().add_file_arg(parser,
                                      name='New row data (JSON)',
                                      metavar='FILE/STDIN',
                                      destination='json_arg')

        return parser

    def take_action(self, parsed_args):

        self.load_client(parsed_args)
        root_url = self.get_identifier(parsed_args, 'root_url')
        data = self.get_file_data(parsed_args, destination='json_arg')

        resp = self.tapis3_client.pgrest.add_table_row(collection=root_url,
                                                       data=data)

        # NOTE: get_in_collection returns a list - grab first and only item
        filt_resp = self.filter_tapis_result(resp[0], parsed_args)
        headers = self.headers_from_result(filt_resp)
        data = filt_resp.values()

        return (headers, data)
