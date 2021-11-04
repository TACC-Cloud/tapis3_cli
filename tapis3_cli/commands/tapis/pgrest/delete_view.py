from ..client import Oauth2Common
from ...mixins import StringIdentifier


class ViewsDelete(Oauth2Common, StringIdentifier):
    """Delete a View (requires view admin role)."""

    DISPLAY_FIELDS = ["view_name", "root_url", "view_id", "manage_view_id", "comments"]

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_identifier(
            parser, name="View ID", destination="view_id", optional=False
        )
        return parser

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        view_id = self.get_identifier(parsed_args, "view_id")
        resp = self.tapis3_client.pgrest.delete_view(view_name=view_id)
        print(resp.get("message", None))
