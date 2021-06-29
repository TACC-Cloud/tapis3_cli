from ..client import AuthFormatMany
from ...mixins import StringIdentifier


class RowsShow(AuthFormatMany, StringIdentifier):
    """Show contents of a row in a collection
    """
    DISPLAY_FIELDS = []

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(parser,
                                        name='Table Root URL',
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

        resp = self.tapis3_client.pgrest.list_in_collection(
            collection=root_url, item=pkid)
        filt_resp = self.filter_tapis_result(resp, parsed_args.formatter)

        headers = self.headers_from_result(filt_resp)
        data = []
        for item in filt_resp:
            data.append(item.values())

        return (headers, data)
