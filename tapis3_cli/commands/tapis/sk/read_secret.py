from ..client import Oauth2FormatOne
# from ...mixins import JSONArg
from .common import SKCommonArgs, SKSecretNameArg, SKSecretJSONFileArg


class SecretsRead(Oauth2FormatOne, SKCommonArgs, SKSecretNameArg,
                  SKSecretJSONFileArg):
    """Read a user secret
    """
    DISPLAY_FIELDS = ['secretMap']

    # TODO - Let user can retrieve either whole secret as dict-like or individual entries in secretMap
    # TODO - Make disiplay of secret metadata optional via --metadata flag
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        SKSecretNameArg.extend_parser(self, parser)
        SKCommonArgs.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        self.process_secret_common_args(parsed_args)
        secret_name = parsed_args.secret_name

        resp = self.tapis3_client.sk.readSecret(secretType=self.secret_type,
                                                user=self.secret_user,
                                                tenant=self.secret_tenant,
                                                secretName=secret_name)

        headers = self.DISPLAY_FIELDS
        data = [resp.get(h) for h in self.DISPLAY_FIELDS]

        return (headers, data)
