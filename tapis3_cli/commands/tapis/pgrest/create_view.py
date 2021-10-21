from ..client import Oauth2FormatOne
from ...mixins import JSONArg


class ViewsCreate(Oauth2FormatOne, JSONArg):
    """Create a new view (requires view admin role)
    """
    DISPLAY_FIELDS = ['view_name', 'root_url', 'view_id', 'columns']

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super().add_file_arg(parser,
                                      name='New view data (JSON)',
                                      metavar='FILE/STDIN',
                                      destination='json_arg')
        return parser

    def take_action(self, parsed_args):
        self.load_client(parsed_args)
        data = self.get_file_data(parsed_args, destination='json_arg')

        # By my reckoning the signature here should be data=data
        resp = self.tapis3_client.pgrest.create_view(**data)
        print(resp)
        raise SystemError()

        filt_resp = self.filter_tapis_result(resp, parsed_args)
        headers = self.headers_from_result(filt_resp)
        data = filt_resp.values()

        return (headers, data)
