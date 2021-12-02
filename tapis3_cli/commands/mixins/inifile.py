from ... import project_ini
from .extender import ParserExtender

__all__ = ["IniLoader"]

DEFAULT_FILENAME = "project.ini"


class IniLoader(ParserExtender):
    def extend_parser(self, parser):
        parser = super(IniLoader, self).extend_parser(parser)
        parser.add_argument(
            "--ini",
            dest="ini_file_name",
            metavar="FILEPATH",
            type=str,
            help=".ini file ({0})".format(DEFAULT_FILENAME),
        )
        return parser

    def get_ini_path(self, filename):
        return project_ini.config_path(filename, self.getwd())

    def get_ini_contents(self, parsed_args):
        ini_path = self.get_ini_path(parsed_args.ini_file_name)
        p = project_ini.key_values(ini_path)
        return p
