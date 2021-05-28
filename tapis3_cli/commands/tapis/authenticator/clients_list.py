from ..client import BasicFormatMany


class ClientsList(BasicFormatMany):
    """List available Oauth2 clients
    """
    DISPLAY_FIELDS = [
        'client_id', 'create_time', 'last_update_time', 'display_name'
    ]

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        resp = self.tapis3_client.authenticator.list_clients()
        filt_resp = [
            self.filter_record_dict(o.__dict__, parsed_args.formatter)
            for o in resp
        ]
        headers = [k for k in filt_resp[0].keys()]
        data = []
        for item in filt_resp:
            data.append(item.values())
        self.save_client()
        return (headers, data)
