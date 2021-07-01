from tapis3_cli import settings
from tapis3_cli.formatters import FormatOne

from .mixins import SettingName

__all__ = ['SettingsGet']


class SettingsGet(FormatOne, SettingName):
    """Get a Tapis CLI setting
    """
    def get_parser(self, prog_name):
        parser = super(SettingsGet, self).get_parser(prog_name)
        parser = super().add_identifier(parser,
                                        name='Setting Name',
                                        metavar='SETTING',
                                        destination='setting_name',
                                        optional=False)
        return parser

    def take_action(self, parsed_args):
        # super(SettingsGet, self).take_action(parsed_args)
        setting_name = self.get_identifier(parsed_args, 'setting_name')
        self.validate_identifier(setting_name, allow_private=True)

        headers = []
        records = []
        for s, v in settings.all_settings().items():
            if s == setting_name.upper():
                headers.append(s)
                records.append(v)
        return (tuple(headers), tuple(records))
