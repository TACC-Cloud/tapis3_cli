from tapipy.tapis import Tapis
from ..client import Oauth2FormatMany


class SitesList(Oauth2FormatMany):
    """List available Tapis sites
    """
    DISPLAY_FIELDS = ['site_id', 'primary', 'base_url']

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.load_client(parsed_args)

        resp = self.tapis3_client.tenants.list_sites()
        filt_resp = [
            self.filter_record_dict(o.__dict__, parsed_args.formatter)
            for o in resp
        ]
        headers = [k for k in filt_resp[0].keys()]
        data = []
        for item in filt_resp:
            data.append(item.values())

        return (headers, data)
