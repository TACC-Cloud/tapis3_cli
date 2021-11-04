from ..client import Oauth2FormatOne

# from ...mixins import JSONArg
from .common import SKCommonArgs, SKSecretNameArg, SKSecretJSONFileArg


class SecretsWrite(Oauth2FormatOne, SKCommonArgs, SKSecretNameArg, SKSecretJSONFileArg):
    """Write a user Secret."""

    DISPLAY_FIELDS = ["created_time", "deletion_time", "destroyed", "version"]

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        # parser = super().add_file_arg(parser,
        #                               name='Secret data (JSON dict)',
        #                               metavar='FILE/STDIN',
        #                               destination='json_arg')
        SKSecretNameArg.extend_parser(self, parser)
        SKSecretJSONFileArg.extend_parser(self, parser)
        SKCommonArgs.extend_parser(self, parser)

        return parser

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        self.process_secret_common_args(parsed_args)

        secret_name = parsed_args.secret_name
        secret_data = self.get_file_data(parsed_args, destination="json_arg")

        resp = self.tapis3_client.sk.writeSecret(
            secretType=self.secret_type,
            user=self.secret_user,
            tenant=self.secret_tenant,
            secretName=secret_name,
            data=secret_data,
        )

        headers = self.DISPLAY_FIELDS
        data = [resp.get(h) for h in self.DISPLAY_FIELDS]

        return (headers, data)
