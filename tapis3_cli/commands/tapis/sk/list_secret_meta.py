from ..client import Oauth2FormatOne
from .common import SKCommonArgs


class SecretsList(Oauth2FormatOne, SKCommonArgs):
    """List user Secrets.
    """
    DISPLAY_FIELDS = ['keys', 'secretPath']

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        SKCommonArgs.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        self.process_secret_common_args(parsed_args)

        resp = self.tapis3_client.sk.listSecretMeta(
            secretType=self.secret_type,
            user=self.secret_user,
            tenant=self.secret_tenant)

        headers = self.DISPLAY_FIELDS
        data = [resp.get(h) for h in self.DISPLAY_FIELDS]

        return (headers, data)
