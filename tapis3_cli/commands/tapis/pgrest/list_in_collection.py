from ..client import AuthFormatMany
from .mixins import TableRootUrl

class RowsList(AuthFormatMany, TableRootUrl):
    """List rows in a collection
    """
    DISPLAY_FIELDS = []

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super(TableRootUrl, self).extend_parser(parser)
        return parser

    def take_action(self, parsed_args):

        self.load_client(parsed_args)

        root_url = table_id=super(
            TableRootUrl, self).get_identifier(parsed_args)
        resp = self.tapis3_client.pgrest.list_in_collection(collection=root_url)
        filt_resp = self.filter_tapis_results(resp, parsed_args.formatter)

        headers = self.headers_from_result(filt_resp)
        data = []
        for item in filt_resp:
            data.append(item.values())

        return (headers, data)
