__all__ = ["ParserExtender"]


class ParserExtender(object):

    working_dir = "."

    def getwd(self):
        return getattr(self, "working_dir")

    def extend_parser(self, parser):
        # When sublcassing: DO NOT FORGET TO RETURN PARSER
        return parser

    def preprocess_args(self, parsed_args):
        # When sublcassing: DO NOT FORGET TO RETURN PARSED_ARGS
        return parsed_args

    def render_extended_parser_value(self, key, value, formatter=None):
        return key, value

    def validate(self, value, permissive=True):
        """Placeholder to implement validation of a value passed
        via a ParserExtender
        """
        if value is not None:
            return True
        else:
            return False
