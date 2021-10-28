from tapis3_cli.cache.direct import TapisDirectClient
from ..client import Oauth2FormatMany
from ...mixins import LimitsArgs, StringIdentifier


class NoncesList(Oauth2FormatMany, LimitsArgs, StringIdentifier):
    """List active Nonces for an Actor
    """
    DISPLAY_FIELDS = [
        'actorId', 'id', 'lastUseTime', 'level', 'remainingUses', 'owner'
    ]

    def get_parser(self, prog_name):
        parser = super(NoncesList, self).get_parser(prog_name)
        parser = super().add_identifier(parser,
                                        name='Actor ID or Alias',
                                        destination='actor_id',
                                        optional=False)
        parser.add_argument('-A',
                            dest='is_alias',
                            action='store_true',
                            help='Identifier is an Alias')
        # TODO - reenable this once limit and offset are supported by V3 Abaco
        # parser = LimitsArgs.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        super(NoncesList, self).take_action(parsed_args)
        self.load_client(parsed_args)
        self.config = {}
        self.config['actor_id'] = parsed_args.actor_id
        if parsed_args.is_alias:
            requests_client = TapisDirectClient(self.tapis3_client)
            api_path = 'aliases/' + self.config['actor_id'] + '/nonces'
            requests_client.setup('actors', api_path=api_path)
            resp = requests_client.get()
        else:
            resp = self.tapis3_client.actors.listNonces(**self.config)

        filt_resp = self.filter_tapis_results(resp, parsed_args)
        headers = self.headers_from_result(filt_resp)
        data = []
        for item in filt_resp:
            data.append(item.values())

        return (tuple(headers), tuple(data))
