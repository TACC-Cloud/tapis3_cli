from ..client import BasicAuthFormatOne
from ...mixins import StringIdentifier


class ClientsShow(BasicAuthFormatOne, StringIdentifier):
    """Show details for a Tapis Oauth2 client."""

    DISPLAY_FIELDS = [
        "client_id",
        "client_key",
        "callback_url",
        "create_time",
        "last_update_time",
        "display_name",
    ]

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(
            parser, name="Client ID", destination="client_id", optional=False
        )
        return parser

    def take_action(self, parsed_args):
        self.load_client(parsed_args)

        client_id = self.get_identifier(parsed_args, "client_id")
        resp = self.tapis3_client.authenticator.get_client(client_id=client_id)

        filt_resp = self.filter_tapis_result(resp, parsed_args)
        headers = self.headers_from_result(filt_resp)
        data = filt_resp.values()

        return (headers, data)
