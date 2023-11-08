import logging
import os
import re
from tkinter import ttk

from scandirrecursive.scandirrecursive import scandir_recursive_sorted

import batchpynamer.gui as bpn_gui
from batchpynamer.gui.basewidgets import BaseWidget
from batchpynamer.gui.notebook import notebook
from batchpynamer.gui.notebook.rename import rename


class FileNavigator(BaseWidget, ttk.Frame):
    """
    Draws the treeview of the files and folders inside the selected folder
    """

    def __init__(self):
        pass

    def tk_init(self, master):
        super().__init__(master=master, column=1, row=1, sticky="we")
        self.columnconfigure(2, weight=1)

        # File selection, treeview
        self.tree_folder = ttk.Treeview(self, selectmode="extended")
        # Scroll bars tree selected folder
        ysb_tree_folder = ttk.Scrollbar(
            self, orient="vertical", command=self.tree_folder.yview
        )
        xsb_tree_folder = ttk.Scrollbar(
            self, orient="horizontal", command=self.tree_folder.xview
        )
        self.tree_folder.configure(
            yscroll=ysb_tree_folder.set, xscroll=xsb_tree_folder.set
        )

        # Name first column
        self.tree_folder.heading("#0", text="Old Name", anchor="w")
        # Create second column and name it
        self.tree_folder["columns"] = "#1"
        self.tree_folder.heading("#1", text="New name", anchor="w")
        # Treeview and the scrollbars placing
        self.tree_folder.grid(row=0, column=2, sticky="w" + "e")
        ysb_tree_folder.grid(row=0, column=3, sticky="ns")
        xsb_tree_folder.grid(row=1, column=2, sticky="ew")

        self.bindings()

    def bindings(self):
        """Defines the binded actions"""
        # File Navigation bindings
        self.tree_folder.bind("<<TreeviewSelect>>", notebook.populate_fields)
        # add='+' to not just rebind the action but to make it so both happen
        self.tree_folder.bind(
            "<<TreeviewSelect>>", self.num_items_info_bar_call, add="+"
        )
        self.tree_folder.bind("<Button-3>", self.right_click_path_to_clip)

    def old_name_get(self, item):
        return self.tree_folder.item(item)["text"]

    def new_name_set(self, path, new_name, old_name):
        return self.tree_folder.set(path, "#1", new_name)

    def selection_get(self):
        return self.tree_folder.selection()

    def selection_set(self, items):
        """Sets the selection of the tree_folder to the list of items"""
        self.tree_folder.selection_set(items)
        logging.debug("GUI- file navigator selection set")

    def select_all(self, event=None):
        """Select all children items"""
        self.tree_folder.selection_set(self.tree_folder.get_children())
        logging.debug("GUI- file navigator select all")

    def deselect_all(self, event=None):
        """Deselect all selected items"""
        self.tree_folder.selection_set()
        logging.debug("GUI- file navigator deselect all")

    def invert_selection(self, event=None):
        """Inverts the selection"""
        # Get all children
        all_items = self.tree_folder.get_children()

        # Get current selection
        selected = set(self.selection_get())
        # Create a list of items from all_items that aren't in selected
        inverted = [item for item in all_items if item not in selected]

        # Set inverted as the new selection
        self.selection_set(inverted)
        logging.debug("GUI- file navigator inverse selection")

    def show_new_name(self, var=None, index=None, mode=None):
        """
        Iterates over each selected item and recreates each new name
        following the renaming rules given inside the rename page of
        the notebook.
        """
        # Get list of selected items iids
        selection = self.selection_get()
        for idx, path in enumerate(selection):
            # Get the old name
            old_name = self.old_name_get(path)
            # Transform the old name to the new name
            new_name = rename.rename_gui_create_new_name_action(
                old_name, idx, path
            )
            # Changes the new name column
            self.new_name_set(path, new_name, old_name)
        logging.debug("GUI- file navigator show new name")

    def reset_new_name(self):
        """
        Renames every item to their old name, so if you change selection
        they dont still show the new name.
        """
        all_nodes = self.tree_folder.get_children()
        for item in all_nodes:
            old_name = self.old_name_get(item)
            self.new_name_set(item, old_name, old_name)

    def refresh_view_call(self, path=None):
        """Get the folder path and update the treeview"""

        def _insert_node(entry, tag=""):
            """Create nodes"""
            # uses the absolute path to the folder as the iid
            self.tree_folder.insert(
                parent="",
                index="end",
                iid=entry.path,
                text=entry.name,
                values=[entry.name],
                tags=tag,
                open=False,
            )

        def _delete_children():
            """Delete already existing nodes in the folder view"""
            for item in self.tree_folder.get_children():
                self.tree_folder.delete(item)

        # Delete the children, load the new ones and sort them
        _delete_children()

        # When the path is still not set use the active_path
        if path is None:
            return

        # If after that the path is still empty (when a folder hasn't been
        # selected) don't try to load it
        if path:
            # Get the filters values
            filters_dict = self.filters_widget_get()

            scanned_dir = scandir_recursive_sorted(path, **filters_dict)
            for entry in scanned_dir:
                _insert_node(entry)

            # Call info set actions
            # self.active_path = path
            bpn_gui.info_bar.items_count_set(
                num_items=len(self.tree_folder.get_children()),
                num_sel_items=len(self.selection_get()),
            )
            # bpn_gui.dir_entry_frame.folderDirSet()
            bpn_gui.info_bar.last_action_set("Refreshed File View")
            logging.debug("GUI- file navigator refreshed view")

    def filters_widget_get(self):
        """Get the filters values"""
        filters_dict = bpn_gui.filters_widget.fields.get_all()

        # Transform the list of extensions into a tuple
        exts = filters_dict.pop("ext")
        filters_dict["ext_tuple"] = [i for i in re.split(r";\s?|,\s?", exts)]

        return filters_dict

    def num_items_info_bar_call(self, event=None):
        """Refresh the number of items in the info bar"""
        bpn_gui.info_bar.items_count_set(
            num_items=len(self.tree_folder.get_children()),
            num_sel_items=len(self.selection_get()),
        )

    def right_click_path_to_clip(self, event=None):
        """
        When you right click over an item in the folder treeview gets the
        path to that item and puts it in the clipboard so you can paste it
        somewhere elese.
        """
        # Get the path of the item in the row under the cursor position
        path = self.tree_folder.identify_row(event.y)
        # Clear the clipboard
        bpn_gui.root.clipboard_clear()
        # Copy path to clipboard
        bpn_gui.root.clipboard_append(path)

        # Get the file/directory name to use in info msg
        name = os.path.basename(path)
        # Set info msg
        msg = f'Copied "{name}" Path to Clipboard'
        bpn_gui.info_bar.last_action_set(msg)
        logging.debug("GUI- " + msg)
