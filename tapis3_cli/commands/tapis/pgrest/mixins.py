from tapis3_cli.commands.mixins import StringIdentifier

__all__ = ['TableIdentifier', 'TableName']


class TableId(StringIdentifier):
    service_id_type = 'table'
    optional = False
    dest = 'table_identifier'


class TableName(StringIdentifier):
    service_id_type = 'table'
    optional = False
    dest = 'table_name'
