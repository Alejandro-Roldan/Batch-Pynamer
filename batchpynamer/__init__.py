import configparser
import os
import sys

import batchpynamer

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


def init_tk_root():
    from batchpynamer.mainwindow import WindowRoot

    global root
    root = WindowRoot()


def tk_init_post_hook():
    """Hook to call AFTER the tk root has been created

    Globalizes the widget to be able to access their methods and vars from
    other widgets without caring for widget creation order
    """

    from batchpynamer.info_bar import Info_Bar
    from batchpynamer.notebook.metadata.a_text import MetadataListEntries
    from batchpynamer.notebook.metadata.b_image import MetadataImg
    from batchpynamer.notebook.metadata.metadata import MetadataApplyChanges
    from batchpynamer.notebook.notebook import Changes_Notebook
    from batchpynamer.notebook.rename.a_from_file import RenameFromFile
    from batchpynamer.notebook.rename.b_reg_exp import RenameFromRegExp
    from batchpynamer.notebook.rename.c_name_basic import NameBasic
    from batchpynamer.notebook.rename.d_replace import Replace
    from batchpynamer.notebook.rename.e_case import Case
    from batchpynamer.notebook.rename.f_remove import Remove
    from batchpynamer.notebook.rename.g_move import MoveParts
    from batchpynamer.notebook.rename.h_add_to_str import AddToStr
    from batchpynamer.notebook.rename.i_add_folder_name import AddFolderName
    from batchpynamer.notebook.rename.j_numbering import Numbering
    from batchpynamer.notebook.rename.k_ext_replace import ExtReplace
    from batchpynamer.notebook.rename.rename import LastRename
    from batchpynamer.trees.a_directory_navigator import DirectoryNavigator
    from batchpynamer.trees.b_file_navigator import FileNavigator
    from batchpynamer.trees.c_directory_entry import DirectoryEntryFrame
    from batchpynamer.trees.filtering import FiltersWidget

    # Last Rename Object
    global last_rename
    last_rename = LastRename()

    # Main Window Widgets
    global info_bar
    info_bar = Info_Bar()
    global fn_treeview
    fn_treeview = FileNavigator()
    global folder_treeview
    folder_treeview = DirectoryNavigator()
    global dir_entry_frame
    dir_entry_frame = DirectoryEntryFrame()
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

    # Metadata Widgets
    global metadata_list_entries
    metadata_list_entries = MetadataListEntries()
    global metadata_img
    metadata_img = MetadataImg()
    global metadata_apply_changes
    metadata_apply_changes = MetadataApplyChanges()
