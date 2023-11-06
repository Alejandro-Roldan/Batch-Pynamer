"""Batch-Pynamer"""


__license__ = "GPL3"
__version__ = "8.0.3"
__release__ = True
__author__ = __maintainer__ = "Alejandro Roldán"
__email__ = "alej.roldan.trabajos@gmail.com"
__url__ = "https://github.com/Alejandro-Roldan/Batch-Pynamer"

import configparser
import os
import sys

import batchpynamer

TITLE = f"{__name__}-V{__version__}"

OG_PATH = os.path.expanduser("~")

# URLS
PROJECT_URL = __url__
WIKI_URL = "https://github.com/Alejandro-Roldan/Batch-Pynamer/wiki"

# Configuration folder path depending on OS
if sys.platform == "linux":
    CONFIG_FOLDER_PATH = os.path.expanduser("~/.config/batchpynamer/")
elif sys.platform == "win32":
    CONFIG_FOLDER_PATH = os.path.expanduser("~/AppData/Roaming/batchpynamer/")
elif sys.platform == "darwin":  # macOS
    CONFIG_FOLDER_PATH = os.path.expanduser(
        "~/Library/Preferences/batchpynamer/"
    )
else:
    CONFIG_FOLDER_PATH = None

# Configparser object for loading the commands
if CONFIG_FOLDER_PATH is not None:
    COMMAND_CONF_FILE = CONFIG_FOLDER_PATH + "commands.conf"
    COMMAND_CONF = configparser.ConfigParser()
    COMMAND_CONF.read(COMMAND_CONF_FILE)

# Metadata availabe flag
try:
    import mutagen
    import PIL

    # If succesful set flag
    METADATA_IMPORT = True
except ImportError:
    METADATA_IMPORT = False

MAX_NAME_LEN = 99999


def __init__():
    pass
