from .extender import ParserExtender

__all__ = ['StringIdentifier']


class StringIdentifier(ParserExtender):
    """Configures a Command to require a mandatory 'identifier' positional param
    Adds a positional parameter to the Command parser. The value for the
    parameter's 'metavar' is set by the Command.service_id_type property.
    """
    # Stem for naming the identifier
    service_id_type = 'Service'
    # Leaf for naming the identifier
    id_type = 'identifier'
    # If True, the argument is optional
    optional = False
    # argparse destination
    dest = id_type

    def arg_display(self, id_value):
        return '{0}_id'.format(id_value).lower()

    def arg_metavar(self, id_value):
        return self.arg_display(id_value)

    def arg_help(self, id_value):
        if not self.optional:
            return '{0} {1}'.format(id_value, self.id_type)
        else:
            return 'Optional {0} {1}'.format(id_value, self.id_type)

    def extend_parser(self, parser):
        id_value = getattr(self, 'service_id_type')
        if id_value is not None:
            arg_display = '{0}_id'.format(id_value).lower()
        if self.optional:
            nargs = '?'
        else:
            nargs = None
        if id_value is not None:
            parser.add_argument(self.dest,
                                type=str,
                                nargs=nargs,
                                metavar=self.arg_metavar(id_value).upper(),
                                help=self.arg_help(id_value))
        return parser

    def validate_identifier(self, identifier, permissive=True):
        return True

    def get_identifier(self, parsed_args, validate=False, permissive=False):
        identifier = None
        try:
            identifier = getattr(parsed_args, self.dest)
            # identifier = parsed_args.identifier
            self.validate_identifier(identifier)
        except Exception:
            if permissive:
                return None
            else:
                raise
        return identifier


class TapisEntityUUID(StringIdentifier):
    service_id_type = 'Tapis Entity'
    id_type = 'unique identifer'

    @classmethod
    def arg_display(cls, id_value):
        return '{0}_uuid'.format(id_value).lower()
