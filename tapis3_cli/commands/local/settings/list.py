from tapis3_cli import settings
from tapis3_cli.formatters import FormatMany

__all__ = ["SettingsList"]


class SettingsList(FormatMany):
    """List current Tapis CLI settings"""

    def take_action(self, parsed_args):
        super(SettingsList, self).take_action(parsed_args)
        headers = ["Setting", "Value"]
        records = []
        for s, v in settings.all_settings().items():
            records.append([s, v])
        return (tuple(headers), tuple(records))
