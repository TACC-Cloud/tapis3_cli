"""Settings-specfic mixins
"""

from tapis3_cli.commands.mixins import StringIdentifier, InvalidIdentifier
from tapis3_cli.settings import all_settings

__all__ = ["SettingName"]


class UnknownSetting(InvalidIdentifier):
    pass


class SettingName(StringIdentifier):
    """Adds validation of the identifier as a CLI setting"""

    def validate_identifier(self, identifier, allow_private=False, permissive=False):
        if identifier.startswith("_") and allow_private is not True:
            raise ValueError("{0} is a private setting".format(identifier))
        if identifier in list(all_settings().keys()):
            return True
        else:
            if permissive:
                return False
            else:
                raise UnknownSetting("{0} not a known setting".format(identifier))
