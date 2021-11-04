import argparse
import logging
import os
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
from pbr.version import VersionInfo

from . import PKG_NAME
from .__about__ import About

about_info = About(PKG_NAME)
version_info = VersionInfo(PKG_NAME)


class Tapis_App(App):
    def __init__(self):
        super(Tapis_App, self).__init__(
            description="{0}: {1}. For support contact {2}".format(
                about_info.project, about_info.summary, about_info.help
            ),
            version=version_info.version_string(),
            command_manager=CommandManager("tapis3.cli"),
            deferred_help=True,
        )

        # Force fit width
        # TODO - allow this to be disabled
        # TODO - remove the option
        os.environ["CLIFF_FIT_WIDTH"] = "1"

    def clean_up(self, cmd, result, err):
        self.LOG.debug("clean_up %s", cmd.__class__.__name__)
        if err:
            self.LOG.debug("got an error: %s", err)


def main(argv=sys.argv[1:]):
    myapp = Tapis_App()
    return myapp.run(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
