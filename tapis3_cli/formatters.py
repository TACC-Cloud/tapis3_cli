"""Baseline formatters
"""
import argparse
import logging
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

__all__ = ['FormatOne', 'FormatMany', 'FormatNone']


class FormatNone(Command):
    """Unformatted command
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(FormatNone, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        pass


class FormatOne(ShowOne):
    """Generic Record Display
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(FormatOne, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        return ((), ())


class FormatMany(Lister):
    """Generic Records Listing
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(FormatMany, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        return ((), ())
