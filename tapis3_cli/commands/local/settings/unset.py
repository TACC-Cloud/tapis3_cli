from dotenv import unset_key

from tapis3_cli import settings
from tapis3_cli.formatters import FormatOne

from .mixins import SettingName

__all__ = ["SettingsUnset"]


class SettingsUnset(FormatOne, SettingName):
    """Unset a Tapis CLI setting"""

    def get_parser(self, prog_name):
        parser = super(SettingsUnset, self).get_parser(prog_name)
        parser = super().add_identifier(
            parser,
            name="Setting Name",
            metavar="SETTING",
            destination="setting_name",
            optional=False,
        )
        return parser

    def take_action(self, parsed_args):
        setting_name = self.get_identifier(parsed_args, "setting_name")
        self.validate_identifier(setting_name, allow_private=True)

        env_file = settings.config.find_config()
        unset_key(env_file, setting_name)

        headers = [setting_name]
        records = [
            'Run "tapis3 config get {0}" to see current value'.format(setting_name)
        ]

        return (tuple(headers), tuple(records))
