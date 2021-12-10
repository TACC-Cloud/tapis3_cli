from ..client import NoAuthFormatOne


class AuthShow(NoAuthFormatOne):
    """Show current Tapis client configuration on this host."""

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        headers = [
            "base_url",
            "tenant_id",
            "client_id",
            "client_key",
            "access_token",
            "refresh_token",
        ]
        data = [
            self.tapis3_client.base_url,
            self.tapis3_client.tenant_id,
            self.tapis3_client.client_id,
            self.tapis3_client.client_key,
            self.tapis3_client.access_token.access_token,
            self.tapis3_client.refresh_token.refresh_token,
        ]
        return (headers, data)
