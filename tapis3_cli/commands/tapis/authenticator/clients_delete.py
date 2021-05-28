from ..client import BasicFormatOne
from .mixins import ClientId


class ClientsDelete(BasicFormatOne, ClientId):
    """Delete an Oauth2 client
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
        resp = self.tapis3_client.authenticator.delete_client(
            client_id=super(ClientId, self).get_identifier(parsed_args))

        self.app.stdout.write('Client deleted')
        return ((), ())
