import configparser
import logging
import os
import pathlib
import sys


def user_config_path_get():
    """Configuration folder path depending on OS"""

    if sys.platform == "linux":
        return os.path.expanduser("~/.config/batchpynamer/")
    elif sys.platform == "win32":
        return os.path.expanduser("~/AppData/Roaming/batchpynamer/")
    elif sys.platform == "darwin":  # macOS
        return os.path.expanduser("~/Library/Preferences/batchpynamer/")
    else:
        return None


def create_config_folder(path):
    """Creates the config folder if it doesn't exist already"""
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def user_config_commands_get(command_conf_file):
    """Configuration Object get"""

    if command_conf_file is not None:
        command_conf = configparser.ConfigParser()
        command_conf.read(command_conf_file)
        logging.info("Loaded command configuration")
        logging.debug(f'from "{command_conf_file}"')
        return command_conf
    else:
        return None
