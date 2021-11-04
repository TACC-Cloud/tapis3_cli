"""Provides config file loading and management
"""
import os
import warnings

from dotenv import find_dotenv, load_dotenv

__all__ = ["find_config", "load_config", "TAPIS3_CLI_CONFIG_DIR"]

TAPIS3_CLI_CONFIG_DIRNAME = ".tapis3"
TAPIS3_CLI_CONFIG_FILE = os.environ.get("TAPIS3_CLI_CONFIG_FILE", "config")
TAPIS3_CLI_CONFIG_DIR = os.environ.get(
    "TAPIS3_CLI_CONFIG_DIR",
    os.path.join(os.path.expanduser("~"), TAPIS3_CLI_CONFIG_DIRNAME),
)


def config_directory():
    """Return the path to the CLI configs directory"""
    return TAPIS3_CLI_CONFIG_DIR


def config_file():
    """Return the path to the CLI configs directory"""
    return TAPIS3_CLI_CONFIG_FILE


def find_config(filename=None):
    """Wrapper for find_dotenv that searches module path, CWD, and HOME"""
    if filename is None:
        filename = config_file()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        confdir = config_directory()
        if not os.path.isdir(confdir):
            os.makedirs(confdir, exist_ok=True)
        # Default to $HOME
        env_file = os.path.join(config_directory(), filename)
        # But, try find_dotenv to find overrides
        try:
            # Search from __file__ up to /
            env_file = find_dotenv(filename, raise_error_if_not_found=True)
        except (IOError, OSError):
            pass
    return env_file


def load_config(filename=None, override=False):
    """Wrapper for load_env that considers module path, CWD, and HOME"""
    if filename is None:
        filename = config_file()
    abs_file_name = find_config(filename)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        # Load into environment
        try:
            load_dotenv(abs_file_name, override=override)
        except Exception:
            pass

    # Return path to env file so it can be displayed
    return abs_file_name
