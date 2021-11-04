import os

from dotenv import set_key
from tapis3_cli import settings
from tapis3_cli.formatters import FormatOne

from .mixins import SettingName

__all__ = ["SettingsSet", "settings_set"]


def settings_set(setting_name, setting_value):
    env_file = settings.config.find_config()
    # Create an empty env file since dotenv.set_key fails
    # if it does not exist
    if not os.path.exists(env_file):
        try:
            open(env_file, "a").close()
        except Exception:
            raise
    set_key(env_file, setting_name, setting_value)
    return True


class SettingsSet(FormatOne, SettingName):
    """Set a Tapis CLI setting"""

    def get_parser(self, prog_name):
        parser = super(SettingsSet, self).get_parser(prog_name)
        parser = super().add_identifier(
            parser,
            name="Setting Name",
            metavar="SETTING",
            destination="setting_name",
            optional=False,
        )
        parser.add_argument(
            "settings_value", metavar="VALUE", help="New value for setting"
        )
        return parser

    def take_action(self, parsed_args):
        setting_name = self.get_identifier(parsed_args, "setting_name")
        setting_value = parsed_args.settings_value
        self.validate_identifier(setting_name, allow_private=True)

        settings_set(setting_name, setting_value)
        headers = [setting_name]
        records = [setting_value]

        return (tuple(headers), tuple(records))
