from ...mixins import StringIdentifier
from ..client import BasicAuthCommon


class ClientsDelete(BasicAuthCommon, StringIdentifier):
    """Delete a Tapis Oauth2 client."""

    DISPLAY_FIELDS = []

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(
            parser, name="Client ID", destination="client_id", optional=False
        )
        return parser

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        client_id = self.get_identifier(parsed_args, "client_id")
        try:
            resp = self.tapis3_client.authenticator.delete_client(client_id=client_id)
            print("Client deleted")
        except Exception as exc:
            raise
