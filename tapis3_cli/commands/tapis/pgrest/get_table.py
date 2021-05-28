from ..client import AuthFormatOne
from .mixins import TableId


class TablesShow(AuthFormatOne, TableId):
    """Show details for one PgREST table
    """
    DISPLAY_FIELDS = ['table_name', 'root_url', 'table_id', 'columns']

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser = super(TableId, self).extend_parser(parser)
        return parser

    def take_action(self, parsed_args):

        self.load_client(parsed_args)
        resp = self.tapis3_client.pgrest.get_table(table_id=super(
            TableId, self).get_identifier(parsed_args),
                                                   details=True)

        # This is the singular form for handling ONE TapisResult
        filt_resp = self.filter_record_dict(resp.__dict__,
                                            parsed_args.formatter)
        # TODO - process columns for pretty printing if formatter == 'table'
        headers = [k for k in filt_resp.keys()]
        data = filt_resp.values()

        self.save_client()
        return (headers, data)
