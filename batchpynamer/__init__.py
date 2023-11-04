import os
import sys
import configparser

import batchpynamer

from .info_bar import Info_Bar
from .notebook import Changes_Notebook
from .rename.rename import LastRename
from .rename.a_from_file import RenameFromFile
from .rename.b_reg_exp import RenameFromRegExp
from .rename.c_name_basic import NameBasic
from .rename.d_replace import Replace
from .rename.e_case import Case
from .rename.f_remove import Remove
from .rename.g_move import MoveParts
from .rename.h_add_to_str import AddToStr
from .rename.i_add_folder_name import AddFolderName
from .rename.j_numbering import Numbering
from .rename.k_ext_replace import ExtReplace
from .trees.trees import (
    Directory_Entry_Frame,
    Directory_Navigator,
    File_Navigator,
)
from .trees.filtering import FiltersWidget

# Information
__license__ = "GPL3"
__version__ = "8.0.0"
__release__ = True
__author__ = __maintainer__ = "Alejandro Roldán"
__email__ = "alej.roldan.trabajos@gmail.com"

# name_basic = NameBasic()
__all__ = ["batchpynamer", "hook_init"]

TITLE = f"{__name__}-V{__version__}"

OG_PATH = os.path.expanduser("~")

# URLS
PROJECT_URL = "https://github.com/Alejandro-Roldan/Batch-Pynamer"
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


# TODO: this can probably be moved outside and get rid of the hook by having
# the rename classes init Fields vars inside tk_init
def tk_init_hook():
    """Hook to call AFTER the tk root has been created

    Globalizes the widget to be able to access their methods and vars from
    other widgets without caring for widget creation order
    """

    # Last Rename Object
    global last_rename
    last_rename = LastRename()

    # Main Window Widgets
    global info_bar
    info_bar = Info_Bar()
    global fn_treeview
    fn_treeview = File_Navigator()
    global folder_treeview
    folder_treeview = Directory_Navigator()
    global dir_entry_frame
    dir_entry_frame = Directory_Entry_Frame()
    global changes_notebook
    changes_notebook = Changes_Notebook()
    global menu_bar
    menu_bar = menubar.TopMenu()

    # Search Filters
    global filters_widget
    filters_widget = FiltersWidget()

    # Rename Widgets
    global rename_from_file
    rename_from_file = RenameFromFile()
    global rename_from_reg_exp
    rename_from_reg_exp = RenameFromRegExp()
    global name_basic
    name_basic = NameBasic()
    global replace
    replace = Replace()
    global case
    case = Case()
    global remove
    remove = Remove()
    global move_parts
    move_parts = MoveParts()
    global add_to_str
    add_to_str = AddToStr()
    global add_folder_name
    add_folder_name = AddFolderName()
    global numbering
    numbering = Numbering()
    global ext_replace
    ext_replace = ExtReplace()
