from tapis3_cli import cache, settings
#from tapipy.tapis import Tapis
from tapis3_cli.cache.client import TapisLocalCache
from tapis3_cli.utils import prompt, prompt_accept, prompt_boolean, get_hostname
from prettytable import PrettyTable
from ..client import NoAuthFormatOne
from ....formatters import FormatNone


class AuthInit(FormatNone):
    """Configure a Tapis client on this host
    """

    interactive = False

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('-C',
                            '--config',
                            dest='client_config',
                            type=str,
                            metavar='str',
                            default='client',
                            help="Tapis client config")

        parser.add_argument('--interactive',
                            action='store_true',
                            help='Prompt for all values')

        parser.add_argument('--base-url',
                            dest='base_url',
                            help='Tapis platform base URL')

        parser.add_argument('--site-id', dest='site_id', help='Tapis site id')
        parser.add_argument('--tenant-id',
                            dest='tenant_id',
                            help='Tapis tenant id')

        parser.add_argument('--username',
                            dest='username',
                            help='Tapis username')
        parser.add_argument('--password',
                            dest='password',
                            help='Tapis password')

        parser.add_argument('--client-id',
                            dest='client_id',
                            help='Tapis client id')
        parser.add_argument('--client-key',
                            dest='client_key',
                            help='Tapis client key')

        return parser

    def take_action(self, parsed_args):

        api_base_url = None
        context = {}
        if parsed_args.client_config is not None:
            config_filename = parsed_args.client_config
        else:
            config_filename = None
        self.interactive = parsed_args.interactive

        if self.interactive:
            print('Configure Tapis API access:')
            print('===========================')

        # Load from client
        try:
            cl = TapisLocalCache.restore(cache=config_filename)
            #            cl = cache.load_client(filename=config_filename)
            disk_client = {
                'base_url': cl.base_url,
                'client_id': cl.client_id,
                'client_key': cl.client_key,
                'username': cl.username,
                'tenant_id': cl.tenant_id
            }
        except FileNotFoundError:
            disk_client = {}

        # Platform base URL
        if parsed_args.base_url is not None:
            api_base_url = parsed_args.base_url
        else:
            api_base_url = settings.TAPIS3_CLI_DEFAULT_BASE_URL

        if self.interactive:
            api_base_url = prompt('Tapis Platform URL: ',
                                  default=api_base_url,
                                  secret=False,
                                  allow_empty=False)
        self.log.debug('api_base_url: ' + api_base_url)

        # SITE ID
        # Was it provided via parsed_arg? If so.. use it
        # Is it available from current client? If so.. use it
        # Is it available as an ENV? If so... use it
        # Are we interactive? If so... prompt with value if we have it
        #   List sites into a dict
        #   Stache site base URL from dict[site_id]
        if parsed_args.site_id is not None:
            context['site_id'] = parsed_args.site_id
        else:
            context['site_id'] = settings.TAPIS3_CLI_DEFAULT_SITE_ID

        t = TapisLocalCache(base_url=api_base_url)
        if self.interactive:
            th = ['Site ID', 'URL']
            tr = [[t.site_id, t.base_url] for t in t.tenants.list_sites()]
            tl = [t[0] for t in tr]
            pt = PrettyTable()
            pt.field_names = ['Site ID', 'Base URL']
            for rec in tr:
                pt.add_row(rec)

            print('Choose a site')
            print(pt)
            context['site_id'] = prompt('Site ID',
                                        default=context['site_id'],
                                        secret=False,
                                        allow_empty=False)

        # Set site URL to specific site
        api_site_url = t.tenants.get_site(site_id=context['site_id']).base_url
        self.log.debug('site_id: ' + context['site_id'])
        self.log.debug('site_base_url: ' + api_site_url)

        # TENANT ID
        if parsed_args.tenant_id is not None:
            context['tenant_id'] = parsed_args.tenant_id
        elif disk_client.get('tenant_id', None) is not None:
            context['tenant_id'] = disk_client.get('tenant_id')
        else:
            context['tenant_id'] = settings.TAPIS3_CLI_DEFAULT_TENANT_ID

        t = TapisLocalCache(base_url=api_base_url)
        if self.interactive:
            th = ['Tenant ID', 'Description', 'API URL']
            tr = [[t.tenant_id, t.description, t.base_url]
                  for t in t.tenants.list_tenants()]
            tl = [t[0] for t in tr]
            pt = PrettyTable()
            pt.field_names = ['Tenant ID', 'Description', 'API URL']
            for rec in tr:
                pt.add_row(rec)

            print('Choose a tenant')
            print(pt)
            context['tenant_id'] = prompt('Tenant ID',
                                          default=context['tenant_id'],
                                          secret=False,
                                          allow_empty=False)

        context['base_url'] = t.tenants.get_tenant(
            tenant_id=context['tenant_id']).base_url
        self.log.debug('tenant_id: ' + context['tenant_id'])
        self.log.debug('base_url: ' + context['base_url'])

        # Username
        if parsed_args.username is not None:
            context['username'] = parsed_args.username
        elif disk_client.get('username', None) is not None:
            context['username'] = disk_client.get('username')
        else:
            context['username'] = None
        if self.interactive:
            context['username'] = prompt('Username',
                                         default=context['username'],
                                         secret=False,
                                         allow_empty=False)
        self.log.debug('username: ' + context['username'])

        # Password
        if parsed_args.password is not None:
            context['password'] = parsed_args.password
        else:
            context['password'] = None
        if self.interactive:
            context['password'] = prompt('Password',
                                         secret=True,
                                         allow_empty=False)
        self.log.debug('password: ' + context['password'])

        # Prepare to accept or fetch client
        #
        # t is a new Tapis client - it has basic credentials so we can take
        # authenticated actions such as listing, getting, and managing clients
        t = TapisLocalCache(base_url=context['base_url'],
                            username=context['username'],
                            password=context['password'])
        # If credentials are wrong, this will throw
        # tapipy.errors.InvalidInputError: message: Invalid username/password combination
        t.get_tokens()

        # Client ID
        if parsed_args.client_id is not None:
            context['client_id'] = parsed_args.client_id
        elif disk_client.get('client_id', None) is not None:
            context['client_id'] = disk_client.get('client_id')
        else:
            context['client_id'] = '{0}-{1}-{1}'.format(
                context['tenant_id'], context['username'], get_hostname())
        if self.interactive:
            context['client_id'] = prompt('Oauth2 Client Id',
                                          default=context['client_id'],
                                          secret=False,
                                          allow_empty=False)

        # Retrieve or create client
        try:
            oauth_client = t.authenticator.get_client(
                client_id=context['client_id'])
        except Exception:
            oauth_client = t.authenticator.create_client(
                client_id=context['client_id'])
        context['client_id'] = oauth_client.client_id
        self.log.debug('client_id: ' + context['client_id'])

        # Client Key
        if parsed_args.client_id is not None:
            context['client_key'] = parsed_args.client_key
        elif disk_client.get('client_key', None) is not None:
            context['client_key'] = disk_client.get('client_key')
        else:
            context['client_key'] = oauth_client.client_key
        if self.interactive:
            context['client_key'] = prompt('Oauth2 Client Key',
                                           default=context['client_key'],
                                           secret=False,
                                           allow_empty=False)
        self.log.debug('client_key: ' + context['client_key'])

        # Access/refresh tokens (Do not accept from CLI)
        # t is a new Tapis client, this time configured with
        # OAuth2 client id/key allowing issuance of auth/refresh
        t = TapisLocalCache(base_url=context['base_url'],
                            username=context['username'],
                            password=context['password'],
                            client_id=context['client_id'],
                            client_key=context['client_key'],
                            cache=config_filename)
        t.get_tokens()
        # This should automatically save to disk
        t.refresh_tokens()
