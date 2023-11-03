import tkinter as tk
from tkinter import ttk

import batchpynamer
from . import basewidgets
from . import metadata
from .rename import rename


class Changes_Notebook(basewidgets.BaseWidget, ttk.Notebook):
    """
    Draws the Notebook.
    It has the following pages:
        - Rename:
            Has the widgets to change the name of the selected files.
        - Metadata:
            Has the widgets to change the metadata of the selected files.
    """

    def __init__(self):
        pass

    def tk_init(self, master, **kwargs):
        # Create TTK Notebook with parent master
        super().__init__(master, **kwargs)
        self.grid(column=0, row=1)

        self.nb_rename = ttk.Frame(self)
        self.nb_metadata = ttk.Frame(self, padding="5 5 5 5")
        self.nb_metadata.columnconfigure(0, weight=1)
        self.nb_metadata.rowconfigure(0, weight=1)

        # Add the rename page and call the widgets that go inside
        self.add(self.nb_rename, text="Rename")
        self.renameNbPage(self.nb_rename)

        # Add the metadata page
        self.add(self.nb_metadata, text="Metadata")
        # Call the widgets that go inside only if the modules were
        # installed and imported properly
        if batchpynamer.METADATA_IMPORT:
            self.metadataNbPage(self.nb_metadata)
        else:
            self.tab(1, state="disable")
            metadata_import_error_msg = (
                "No metadata modules available. This "
                "program is able to edit metadata tags if you install the mutagen "
                "and Pillow libraries"
            )
            inf_bar.lastActionRefresh(metadata_import_error_msg)

        # self.__dict__.update(brothers)

        # Bindings
        self.bindEntries()

    def renameNbPage(self, master, *args, **kwargs):
        """Calls to draw the rename widgets"""
        self.nb_rename_frame = ttk.Frame(master)
        self.nb_rename_frame.grid(sticky="nsew")

        # Rename from File (0)
        # self.rename_from_file = rename.Rename_From_File(
        #     self.nb_rename_frame, brothers={"fn_treeview": self.fn_treeview}
        # )
        batchpynamer.rename_from_file.tk_init(self.nb_rename_frame)
        # # Regular Expressions (1)
        # self.reg_exp = rename.Reg_Exp(self.nb_rename_frame)
        batchpynamer.rename_from_reg_exp.tk_init(self.nb_rename_frame)
        # Name (2)
        # self.name_basic = rename.c_name_basic.NameBasic(
        # self.name_basic = batchpynamer.name_basic.tk_init(
        batchpynamer.name_basic.tk_init(
            # self.nb_rename_frame, brothers={"fn_treeview": self.fn_treeview}
            self.nb_rename_frame
        )
        # # Replace (3)
        # self.replace = rename.Replace(self.nb_rename_frame)
        batchpynamer.replace.tk_init(self.nb_rename_frame)
        # # Case (4)
        # self.case = rename.Case(self.nb_rename_frame)
        batchpynamer.case.tk_init(self.nb_rename_frame)
        # # Remove (5)
        # self.remove = rename.Remove(self.nb_rename_frame)
        batchpynamer.remove.tk_init(self.nb_rename_frame)
        # # Move Parts (6)
        # self.Move_Parts = rename.Move_Parts(self.nb_rename_frame)
        batchpynamer.move_parts.tk_init(self.nb_rename_frame)
        # # Add (7)
        # self.add_to_string = rename.Add_To_String(self.nb_rename_frame)
        batchpynamer.add_to_str.tk_init(self.nb_rename_frame)
        # # Append Folder Name (8)
        # self.append_folder_name = rename.Append_Folder_Name(
        #     self.nb_rename_frame
        # )
        batchpynamer.add_folder_name.tk_init(self.nb_rename_frame)
        # # Numbering (9)
        # self.numbering = rename.Numbering(self.nb_rename_frame)
        batchpynamer.numbering.tk_init(self.nb_rename_frame)
        # # Extension (10)
        # self.extension_rep = rename.Extension_Rep(self.nb_rename_frame)
        batchpynamer.ext_replace.tk_init(self.nb_rename_frame)

        # # Bottom Frame for Filters and Rename buttons
        # self.nb_bottom_frame = ttk.Frame(self.nb_rename_frame)
        # self.nb_bottom_frame.grid(
        #     column=0, row=3, columnspan=6, sticky="w" + "e"
        # )
        # self.nb_bottom_frame.columnconfigure(0, weight=1)
        # # Filters
        # self.filters = Filters_Widget(self.nb_bottom_frame)
        # # Rename
        # self.rename = rename.Rename(self.nb_bottom_frame)

        # Add a little bit of padding between each widget
        for child in self.nb_rename_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)

    def metadataNbPage(self, master, *args, **kwargs):
        """Calls to draw the matadata widgets"""
        self.nb_metadata_frame = ttk.Frame(master)
        self.nb_metadata_frame.grid(sticky="nswe")
        self.nb_metadata_frame.columnconfigure(0, weight=1)
        self.nb_metadata_frame.columnconfigure(1, weight=1)
        self.nb_metadata_frame.rowconfigure(0, weight=1)

        # Entries with the Metadata
        # self.metadata_list_entries = Metadata_ListEntries(
        #     self.nb_metadata_frame
        # )
        # # Attached Image
        # self.metadata_img = Metadata_Img(self.nb_metadata_frame)
        # # Apply buttons
        # self.apply_changes = Apply_Changes(self.nb_metadata_frame)

    def nbTabGet(self, *args, **kwargs):
        return self.tab(self.select(), "text")

    def bindEntries(self, *args, **kwargs):
        self.bind("<<NotebookTabChanged>>", self.populate_fields)

    def populate_fields(self, tab):
        """
        What to show and what to have active when each notebook tab is active.
        """
        # Get active tab
        tab = self.nbTabGet()

        if tab == "Rename":
            # Shows new naming
            batchpynamer.fn_treeview.resetNewName()
            batchpynamer.fn_treeview.showNewName()
            # Enables the menu options for renaming
            batchpynamer.menu_bar.renameEnable()
            # Disables the menu options for metadata
            batchpynamer.menu_bar.metadataDisable()

        elif tab == "Metadata":
            # Stops showing new name
            batchpynamer.fn_treeview.resetNewName()
            # Enables loading metadata
            batchpynamer.metadata_list_entries.metadataSelect()
            batchpynamer.metadata_img.imageShow()
            # Enables the menu options for metadata
            batchpynamer.menu_bar.metadataEnable()
            # Disables the menu options for renaming
            batchpynamer.menu_bar.renameDisable()
