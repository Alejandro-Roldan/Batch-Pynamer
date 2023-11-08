"""Graphic User Interface related code"""

import logging


def init_tk_root():
    from batchpynamer.gui.mainwindow import WindowRoot

    global root
    root = WindowRoot()

    logging.debug("Initialized window root with global")


def tk_init_post_hook():
    """Hook to call AFTER the tk root has been created

    Globalizes the widget to be able to access their methods and vars from
    other widgets without caring for widget creation order
    """

    from batchpynamer.gui.infobar import Info_Bar
    from batchpynamer.gui.menubar import TopMenu
    from batchpynamer.gui.notebook.metadata.a_text import MetadataListEntries
    from batchpynamer.gui.notebook.metadata.b_image import MetadataImg
    from batchpynamer.gui.notebook.notebook import ChangesNotebook
    from batchpynamer.gui.notebook.rename.a_from_file import RenameFromFile
    from batchpynamer.gui.notebook.rename.b_reg_exp import RenameFromRegExp
    from batchpynamer.gui.notebook.rename.c_name_basic import NameBasic
    from batchpynamer.gui.notebook.rename.d_replace import Replace
    from batchpynamer.gui.notebook.rename.e_case import Case
    from batchpynamer.gui.notebook.rename.f_remove import Remove
    from batchpynamer.gui.notebook.rename.g_move import MoveParts
    from batchpynamer.gui.notebook.rename.h_add_to_str import AddToStr
    from batchpynamer.gui.notebook.rename.i_add_folder_name import (
        AddFolderName,
    )
    from batchpynamer.gui.notebook.rename.j_numbering import Numbering
    from batchpynamer.gui.notebook.rename.k_ext_replace import ExtReplace
    from batchpynamer.gui.notebook.rename.rename import LastRename
    from batchpynamer.gui.trees.a_directory_navigator import DirectoryNavigator
    from batchpynamer.gui.trees.b_file_navigator import FileNavigator
    from batchpynamer.gui.trees.c_directory_entry import DirectoryEntryFrame
    from batchpynamer.gui.trees.filtering import FiltersWidget

    # Last Rename Object
    global last_rename
    last_rename = LastRename()

    # Main Window Widgets
    global info_bar
    info_bar = Info_Bar()
    global folder_treeview
    folder_treeview = DirectoryNavigator()
    global fn_treeview
    fn_treeview = FileNavigator()
    global dir_entry_frame
    dir_entry_frame = DirectoryEntryFrame()
    global changes_notebook
    changes_notebook = ChangesNotebook()
    global menu_bar
    menu_bar = TopMenu()

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

    logging.debug("Initialized window sub fields with global")
