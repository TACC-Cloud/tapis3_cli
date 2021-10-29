from ..client import Oauth2FormatOne
from ...mixins import StringIdentifier

__all__ = ['AliasesCreate']


class AliasesCreate(Oauth2FormatOne, StringIdentifier):
    """Create an Alias for an Actor.
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(parser,
                                        name='Alias',
                                        destination='alias',
                                        optional=False)
        parser = super().add_identifier(parser,
                                        name='Actor ID',
                                        destination='actor_id',
                                        optional=False)
        return parser

    def take_action(self, parsed_args):
        super(AliasesCreate, self).take_action(parsed_args)
        self.load_client(parsed_args)
        self.config = {}
        self.config['alias'] = parsed_args.alias
        self.config['actorId'] = parsed_args.actor_id
        resp = self.tapis3_client.actors.createAlias(**self.config)

        filt_resp = self.filter_tapis_result(resp, parsed_args)
        headers = [k for k in filt_resp.keys()]
        data = filt_resp.values()

        return (tuple(headers), tuple(data))