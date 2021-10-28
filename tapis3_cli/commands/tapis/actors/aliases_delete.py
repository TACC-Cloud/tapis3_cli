from ..client import Oauth2Common
from ...mixins import StringIdentifier

__all__ = ['AliasesDelete']


class AliasesDelete(Oauth2Common, StringIdentifier):
    """Delete an Alias
    """
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(parser,
                                        name='Alias',
                                        destination='alias',
                                        optional=False)
        return parser

    def take_action(self, parsed_args):
        super(AliasesDelete, self).take_action(parsed_args)
        self.load_client(parsed_args)
        self.config = {}
        self.config['alias'] = parsed_args.alias
        resp = self.tapis3_client.actors.deleteAlias(**self.config)
        # No return since this is Oauth2Common
