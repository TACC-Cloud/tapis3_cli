from tapis3_cli.commands.mixins import StringIdentifier

__all__ = ['TableIdentifier', 'TableName', 'TableRootUrl', 'RowPkid']


class TableId(StringIdentifier):
    service_id_type = 'table'
    optional = False
    dest = 'table_identifier'


class TableName(StringIdentifier):
    service_id_type = 'table'
    optional = False
    dest = 'table_name'

class TableRootUrl(StringIdentifier):
    service_id_type = 'root_url'
    optional = False
    dest = 'root_url'

class RowPkid(StringIdentifier):
    service_id_type = 'pkid'
    optional = False
    dest = 'pkid'
