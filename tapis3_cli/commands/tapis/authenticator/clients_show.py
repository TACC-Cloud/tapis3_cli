from ..client import BasicAuthFormatOne
from .mixins import ClientId


class ClientsShow(BasicAuthFormatOne, ClientId):
    """Show details for one Oauth2 client
    """
    DISPLAY_FIELDS = [
        'client_id', 'client_key', 'callback_url', 'create_time',
        'last_update_time', 'display_name'
    ]

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super(ClientId, self).extend_parser(parser)
        return parser

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        resp = self.tapis3_client.authenticator.get_client(
            client_id=super(ClientId, self).get_identifier(parsed_args))

        # This is the singular form for handling ONE TapisResult
        filt_resp = self.filter_record_dict(resp.__dict__,
                                            parsed_args.formatter)
        headers = [k for k in filt_resp.keys()]
        data = filt_resp.values()
        return (headers, data)
