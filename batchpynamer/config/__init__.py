"""Code related to the configuration"""

import os

from batchpynamer.config import config

config_folder_path = config.user_config_path_get()
plugins_folder_path = (
    os.path.join(config_folder_path, "plugins/")
    if config_folder_path
    else None
)
command_conf_file = (
    os.path.join(config_folder_path, "commands.conf")
    if config_folder_path
    else None
)
command_conf = config.CommandsConfig(command_conf_file)
