from .extender import ParserExtender

__all__ = ["LimitsArgs"]


class LimitsArgs(ParserExtender):
    def extend_parser(self, parser):
        parser.add_argument(
            "--limit", dest="limit", type=int, help="Limit to <n> records"
        )
        parser.add_argument(
            "--offset", dest="offset", type=int, help="Offset by <n> records"
        )
        return parser

    def get_limit(self, parsed_args):
        return parsed_args.limit

    def get_offset(self, parsed_args):
        return parsed_args.offset
