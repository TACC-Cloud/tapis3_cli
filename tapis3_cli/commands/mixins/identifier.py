from .extender import ParserExtender

__all__ = ['StringIdentifier']


class StringIdentifier(ParserExtender):
    def add_identifier(self,
                       parser,
                       name='Service Identifer',
                       destination='identifier',
                       metavar=None,
                       optional=False):

        dest = destination.lower()
        python_type = str

        if metavar is None:
            arg_display = dest.upper()

        if optional:
            nargs = '?'
            arg_help = 'Optional {0}'.format(name)
        else:
            nargs = None
            arg_help = '{0}'.format(name)

        parser.add_argument(dest,
                            type=python_type,
                            nargs=nargs,
                            metavar=arg_display,
                            help=arg_help)

        return parser

    def get_identifier(self,
                       parsed_args,
                       destination='identifier',
                       validate=False,
                       permissive=False):
        return getattr(parsed_args, destination, None)
