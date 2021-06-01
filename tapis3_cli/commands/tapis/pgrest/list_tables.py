from ..client import AuthFormatMany


class TablesList(AuthFormatMany):
    """List available PgREST tables
    """
    DISPLAY_FIELDS = ['table_name', 'root_url', 'table_id']

    def take_action(self, parsed_args):

        self.load_client(parsed_args)
        resp = self.tapis3_client.pgrest.list_tables()
        filt_resp = [
            self.filter_record_dict(o.__dict__, parsed_args.formatter)
            for o in resp
        ]
        headers = [k for k in filt_resp[0].keys()]
        data = []
        for item in filt_resp:
            data.append(item.values())
        return (headers, data)
