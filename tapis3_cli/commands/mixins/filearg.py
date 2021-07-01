import argparse
import json
import sys
from .extender import ParserExtender

__all__ = ['FileArg', 'JSONArg']


class FileArg(ParserExtender):
    """Accept a file from file system or STDIN
    """
    def add_file_arg(self,
                     parser,
                     name='File',
                     destination='file_arg',
                     metavar=None,
                     optional=True):

        dest = destination.lower()
        python_type = argparse.FileType('r')

        if metavar is None:
            arg_display = dest.upper()
        else:
            arg_display = metavar

        arg_help = '{0}'.format(name)
        if optional:
            nargs = '?'
        else:
            nargs = None

        parser.add_argument('-F',
                            default=sys.stdin,
                            dest=dest,
                            type=python_type,
                            nargs=nargs,
                            metavar=arg_display,
                            help=arg_help)

        return parser

    def get_file_data(self,
                      parsed_args,
                      destination='file_arg',
                      validate=False,
                      permissive=False):
        file_descriptor = getattr(parsed_args, destination)
        with file_descriptor as f:
            return f.read()

    def validate_file_data(self, data):
        return True


class JSONArg(ParserExtender):
    """Accept a JSON file from file system or STDIN
    """
    def add_file_arg(self,
                     parser,
                     name='JSON File',
                     destination='json_arg',
                     metavar=None,
                     optional=True):

        dest = destination.lower()
        python_type = argparse.FileType('r')

        if metavar is None:
            arg_display = dest.upper()
        else:
            arg_display = metavar

        arg_help = '{0}'.format(name)
        if optional:
            nargs = '?'
        else:
            nargs = None


        parser.add_argument('-F',
                            default=sys.stdin,
                            dest=dest,
                            type=python_type,
                            nargs=nargs,
                            metavar=arg_display,
                            help=arg_help)

        return parser

    def get_file_data(self,
                      parsed_args,
                      destination='json_arg',
                      validate=False,
                      permissive=False):
        file_descriptor = getattr(parsed_args, destination)
        return json.load(file_descriptor)
