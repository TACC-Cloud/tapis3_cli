from ..client import AuthFormatMany
from .mixins import TableRootUrl, RowPkid

class RowsShow(AuthFormatMany, TableRootUrl, RowPkid):
    """Show contents of a row in a collection
    """
    DISPLAY_FIELDS = []

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super(TableRootUrl, self).extend_parser(parser)
        parser = super(RowPkid, self).extend_parser(parser)
        return parser

    def take_action(self, parsed_args):

        self.load_client(parsed_args)

        root_url = super(
            TableRootUrl, self).get_identifier(parsed_args)
        pkid = super(
            RowPkid, self).get_identifier(parsed_args)
        resp = self.tapis3_client.pgrest.list_in_collection(
            collection=root_url, item=pkid)
        filt_resp = self.filter_tapis_result(resp, parsed_args.formatter)

        headers = self.headers_from_result(filt_resp)
        data = []
        for item in filt_resp:
            data.append(item.values())

        return (headers, data)
