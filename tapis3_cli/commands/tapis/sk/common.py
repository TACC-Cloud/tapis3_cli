from tapis3_cli.commands.mixins import ParserExtender
from ...mixins import JSONArg

__all__ = ['SKCommonArgs', 'SKSecretNameArg', 'SKSecretJSONFileArg']


class SKCommonArgs(ParserExtender):
    def extend_parser(self, parser):
        # parser.add_argument('--secret-type',
        #             type=str,
        #             default='user',
        #             dest='secret_type',
        #             help='Secret Type [user]')
        parser.add_argument('--secret-tenant',
                            type=str,
                            dest='secret_tenant',
                            help='Tenant [Tapis.tenant_id]')
        parser.add_argument('--secret-user',
                            type=str,
                            dest='secret_user',
                            help='User [Tapis.user]')
        return parser

    def process_secret_common_args(self, parsed_args):
        self.secret_type = 'user'
        self.secret_user = parsed_args.secret_user
        if self.secret_user is None:
            self.secret_user = self.tapis3_client.authenticator.get_userinfo(
            ).get('username')
        self.secret_tenant = parsed_args.secret_tenant
        if self.secret_tenant is None:
            self.secret_tenant = self.tapis3_client.tenant_id


class SKSecretNameArg(ParserExtender):
    def extend_parser(self, parser):
        parser.add_argument('secret_name',
                            metavar='SECRET_NAME',
                            type=str,
                            help='Secret Name')
        return parser


class SKSecretJSONFileArg(JSONArg):
    def extend_parser(self, parser):
        parser = super().add_file_arg(parser,
                                      name='Secret data (JSON dict)',
                                      metavar='FILE/STDIN',
                                      destination='json_arg')
        return parser
