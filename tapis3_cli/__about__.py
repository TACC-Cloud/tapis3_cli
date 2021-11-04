"""Exposes project and package metadata in a rationalized form
"""
import os.path
import re
from pkg_resources import get_distribution

MAPPINGS = [
    ("Name", "title"),
    ("Summary", "summary"),
    ("Home_page", "uri"),
    ("Author", "author"),
    ("Author_email", "email"),
    ("Maintainer_email", "help"),
]

OTHERS = [
    ("Copyright", "2021 Texas Advanced Computing Center"),
    ("License", "BSD-3"),
    ("Project", "Tapis v3 CLI"),
]

__all__ = ["About"]


class About(object):
    def __init__(self, name="tapis3_cli"):
        # Read from setup.cfg [metadata]
        dst = get_distribution(name)
        lines = dst.get_metadata_lines(dst.PKG_INFO)
        found = list()
        for line in lines:
            for metadata_name, attribute in MAPPINGS:
                if re.match("{}:".format(metadata_name), line):
                    name, value = line.split(":", 1)
                    setattr(self, attribute, value.strip())
                    found.append(metadata_name)
                    break
                elif metadata_name not in found:
                    setattr(self, attribute, None)
        # extension metadata
        for other_name, value in OTHERS:
            setattr(self, other_name.lower(), value)
