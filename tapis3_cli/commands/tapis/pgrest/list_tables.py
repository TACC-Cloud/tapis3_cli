from ..client import Oauth2FormatMany


class TablesList(Oauth2FormatMany):
    """List available tables
    """
    DISPLAY_FIELDS = ['table_name', 'root_url', 'table_id']

    def take_action(self, parsed_args):

        self.load_client(parsed_args)
        resp = self.tapis3_client.pgrest.list_tables()
        filt_resp = self.filter_tapis_results(resp, parsed_args.formatter)

        headers = self.headers_from_result(filt_resp)

        data = []
        for item in filt_resp:
            data.append(item.values())

        return (headers, data)
