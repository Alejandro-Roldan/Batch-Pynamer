import configparser
import logging
import os
import pathlib
import sys

from batchpynamer import data


class CommandsConfig(configparser.ConfigParser):
    def __init__(self, command_conf_file):
        super().__init__()
        if command_conf_file is not None:
            self.read(command_conf_file)
            logging.info("Loaded command configuration")
            logging.debug(f'from "{command_conf_file}"')

    def command_conf_fields_get(self, command_name):
        """Fields get that handles types"""
        command_dict = data.ALL_RENAME_FIELDS.copy()
        for key, value in self.items(command_name):
            try:
                default = command_dict[key]
            # Handle "next_step" value
            except KeyError:
                default = ""

            if isinstance(default, bool):
                command_dict[key] = self.getboolean(command_name, key)
            elif isinstance(default, int):
                command_dict[key] = self.getint(command_name, key)
            else:
                command_dict[key] = self.get(command_name, key)

        return command_dict


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
