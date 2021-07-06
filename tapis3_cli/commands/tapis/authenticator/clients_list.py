from ..client import BasicAuthFormatMany


class ClientsList(BasicAuthFormatMany):
    """List available Oauth2 clients
    """
    DISPLAY_FIELDS = [
        'client_id', 'create_time', 'description', 'display_name'
    ]

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        resp = self.tapis3_client.authenticator.list_clients()

        filt_resp = self.filter_tapis_results(resp, parsed_args)
        headers = self.headers_from_result(filt_resp)
        data = []
        for item in filt_resp:
            data.append(item.values())

        return (headers, data)
