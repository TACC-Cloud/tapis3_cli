__all__ = ["InvalidValue", "InvalidIdentifier", "OptionNotImplemented"]


class InvalidValue(ValueError):
    pass


class InvalidIdentifier(InvalidValue):
    """Raised when an invalid identifier is encountered"""

    pass


class OptionNotImplemented(ValueError):
    """Raised when an option that is only a placeholder is specified"""

    pass
