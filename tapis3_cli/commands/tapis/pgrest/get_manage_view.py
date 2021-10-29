from ..client import Oauth2FormatOne
from ...mixins import StringIdentifier
from tapis3_cli.utils import flatten


class ViewsShow(Oauth2FormatOne, StringIdentifier):
    """Show details for a View (requires view admin role).
    """
    DISPLAY_FIELDS = []

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(parser,
                                        name='View ID',
                                        destination='view_id',
                                        optional=False)
        return parser

    def take_action(self, parsed_args):

        self.load_client(parsed_args)
        view_id = self.get_identifier(parsed_args, 'view_id')
        resp = self.tapis3_client.pgrest.get_manage_view(view_name=view_id,
                                                         details=True)

        # flatten() is a special TapisResult-aware dictionary flattener
        resp = flatten(resp.__dict__)
        headers = list(resp.keys())
        data = list(resp.values())

        return (headers, data)
