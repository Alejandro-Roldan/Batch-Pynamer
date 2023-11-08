from tkinter import ttk

import batchpynamer as bpn
import batchpynamer.gui as bpn_gui
from batchpynamer.gui.basewidgets import BaseWidget
from batchpynamer.gui.notebook.metadata import metadata
from batchpynamer.gui.notebook.rename import rename


class ChangesNotebook(BaseWidget, ttk.Notebook):
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

    def tk_init(self, master):
        # Create TTK Notebook with parent master
        super().__init__(master, column=0, row=1)

        # Add the rename page and call the widgets that go inside
        self.nb_rename = ttk.Frame(self)
        self.nb_rename.columnconfigure(0, weight=1)
        self.nb_rename.rowconfigure(0, weight=1)
        self.add(self.nb_rename, text="Rename")
        self.initialize_rename_nb_page(self.nb_rename)

        # Add the metadata page
        self.nb_metadata = ttk.Frame(self, padding="5 5 5 5")
        self.nb_metadata.columnconfigure(0, weight=1)
        self.nb_metadata.rowconfigure(0, weight=1)
        self.add(self.nb_metadata, text="Metadata")
        # Call the widgets that go inside only if the modules were
        # installed and imported properly
        if bpn.METADATA_IMPORT:
            self.initialize_metadata_nb_page(self.nb_metadata)
        else:
            self.tab(1, state="disable")
            bpn_gui.info_bar.last_action_set(bpn.metadata_import_error_msg)

        # Bindings
        self.bindings()

    def initialize_rename_nb_page(self, master):
        """Calls to draw the rename widgets"""
        # Rename from File (0)
        bpn_gui.rename_from_file.tk_init(master)
        # # Regular Expressions (1)
        bpn_gui.rename_from_reg_exp.tk_init(master)
        # Name (2)
        bpn_gui.name_basic.tk_init(master)
        # Replace (3)
        bpn_gui.replace.tk_init(master)
        # Case (4)
        bpn_gui.case.tk_init(master)
        # Remove (5)
        bpn_gui.remove.tk_init(master)
        # Move Parts (6)
        bpn_gui.move_parts.tk_init(master)
        # Add (7)
        bpn_gui.add_to_str.tk_init(master)
        # Append Folder Name (8)
        bpn_gui.add_folder_name.tk_init(master)
        # Numbering (9)
        bpn_gui.numbering.tk_init(master)
        # Extension (10)
        bpn_gui.ext_replace.tk_init(master)

        # Bottom Frame for Filters and Rename buttons
        self.nb_bottom_frame = ttk.Frame(master)
        self.nb_bottom_frame.grid(
            column=0, row=3, columnspan=6, sticky="w" + "e"
        )
        self.nb_bottom_frame.columnconfigure(0, weight=1)
        # Filters
        bpn_gui.filters_widget.tk_init(self.nb_bottom_frame)
        # Rename
        rename.Rename(self.nb_bottom_frame)

        # Add a little bit of padding between each widget
        for child in master.winfo_children():
            child.grid_configure(padx=2, pady=2)

    def initialize_metadata_nb_page(self, master):
        """Calls to draw the matadata widgets"""
        # Entries with the Metadata
        bpn_gui.metadata_list_entries.tk_init(master)
        # Attached Image
        bpn_gui.metadata_img.tk_init(master)
        # Apply buttons
        bpn_gui.metadata_apply_changes.tk_init(master)

    def nb_active_tab_get(self):
        return self.tab(self.select(), "text")

    def bindings(self):
        self.bind("<<NotebookTabChanged>>", populate_fields)


def populate_fields(event=None):
    """
    What to show and what to have active when each notebook tab is active.
    """
    # Get active tab
    tab = bpn_gui.changes_notebook.nb_active_tab_get()

    if tab == "Rename":
        # Shows new naming
        bpn_gui.fn_treeview.reset_new_name()
        bpn_gui.fn_treeview.show_new_name()
        # Enables the menu options for renaming
        bpn_gui.menu_bar.menu_opts_rename_enable()
        # Disables the menu options for metadata
        bpn_gui.menu_bar.menu_opts_metadata_disable()
        bpn_gui.root.rename_binds()

    elif tab == "Metadata":
        # Stops showing new name
        bpn_gui.fn_treeview.reset_new_name()
        # Enables loading metadata
        bpn_gui.metadata_list_entries.metadata_gui_show()
        bpn_gui.metadata_img.image_gui_show()
        # Enables the menu options for metadata
        bpn_gui.menu_bar.menu_opts_metadata_enable()
        # Disables the menu options for renaming
        bpn_gui.menu_bar.menu_opts_rename_disable()
        bpn_gui.root.rename_unbinds()
