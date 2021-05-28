from ..client import NoAuthFormatOne


class TokensShow(NoAuthFormatOne):
    """Show current OAuth2 tokens
    """
    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        headers = ['access_token', 'refresh_token', 'expires_at']
        data = [
            self.tapis3_client.access_token.access_token,
            self.tapis3_client.refresh_token.refresh_token,
            self.tapis3_client.access_token.expires_at
        ]
        return (headers, data)
