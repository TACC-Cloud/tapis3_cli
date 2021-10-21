from ..client import Oauth2FormatMany


class ViewsList(Oauth2FormatMany):
    """List available views (requires views admin role)
    """
    DISPLAY_FIELDS = [
        'view_name', 'root_url', 'view_id', 'manage_view_id', 'comments'
    ]

    def take_action(self, parsed_args):

        self.load_client(parsed_args)
        resp = self.tapis3_client.pgrest.list_views()
        filt_resp = self.filter_tapis_results(resp, parsed_args)

        headers = self.headers_from_result(filt_resp)

        data = []
        for item in filt_resp:
            data.append(item.values())

        return (headers, data)
