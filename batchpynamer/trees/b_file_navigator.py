import os
import re
import tkinter as tk
from tkinter import ttk

from scandirrecursive.scandirrecursive import scandir_recursive_sorted

import batchpynamer as bpn
from batchpynamer.basewidgets import BaseWidget
from batchpynamer.notebook.rename import rename


class FileNavigator(BaseWidget, ttk.Frame):
    """
    Draws the treeview of the files and folders inside the selected folder.
    """

    def __init__(self):
        pass

    def tk_init(self, master, **kwargs):
        super().__init__(master=master, column=1, row=1, sticky="we", **kwargs)
        self.columnconfigure(2, weight=1)

        self.active_path = ""

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

        # Bindings
        self.bindings()

    def oldNameGet(self, item):
        return self.tree_folder.item(item)["text"]

    def bindings(self):
        """Defines the binded actions"""
        # File Navigation bindings
        self.tree_folder.bind(
            "<<TreeviewSelect>>", bpn.changes_notebook.populate_fields
        )
        # add='+' to not just rebind the action but to make it so both happen
        self.tree_folder.bind("<<TreeviewSelect>>", self.infoBarCall, add="+")
        self.tree_folder.bind("<Button-3>", self.rightClickPathToClip)

    def infoBarCall(self, event=None):
        """Refresh the number of items in the info bar"""
        # self.info_bar.numItemsRefresh(
        bpn.info_bar.numItemsRefresh(
            num_items=len(self.tree_folder.get_children()),
            num_sel_items=len(self.selectedItems()),
        )

    def selectionSet(self, items, *args, **kwargs):
        """Sets the selection of the tree_folder to the list of items"""
        self.tree_folder.selection_set(items)

    def selectAll(self, *args, **kwargs):
        """Select all children items"""
        self.tree_folder.selection_set(self.tree_folder.get_children())

    def deselectAll(self, *args, **kwargs):
        """Deselect all selected items"""
        self.tree_folder.selection_set()

    def invertSelection(self, *args, **kwargs):
        """Inverts the selection"""
        # Get all children
        all_items = self.tree_folder.get_children()

        # Get current selection
        selected = set(self.selectedItems())
        # Create a list of items from all_items that aren't in selected
        inverted = [item for item in all_items if item not in selected]

        # Set inverted as the new selection
        self.selectionSet(inverted)

    def deleteChildren(self, *args, **kwargs):
        """Delete already existing nodes in the folder view"""
        for item in self.tree_folder.get_children():
            self.tree_folder.delete(item)

    def setNewName(self, path, new_name, old_name, *args, **kwargs):
        return self.tree_folder.set(path, "#1", new_name)

    def selectedItems(self, *args, **kwargs):
        return self.tree_folder.selection()

    def showNewName(self, *args, **kwargs):
        """
        Iterates over each selected item and recreates each new name
        following the renaming rules given inside the rename page of
        the notebook.
        """
        # Get list of selected items iids
        selection = self.selectedItems()
        for idx, path in enumerate(selection):
            # Get the old name
            old_name = self.oldNameGet(path)
            # Transform the old name to the new name
            new_name = rename.new_naming_visual(old_name, idx, path)
            # Changes the new name column
            self.setNewName(path, new_name, old_name)

    def resetNewName(self, *args, **kwargs):
        """
        Renames every item to their old name, so if you change selection
        they dont still show the new name.
        """
        all_nodes = self.tree_folder.get_children()
        for item in all_nodes:
            old_name = self.oldNameGet(item)
            self.setNewName(item, old_name, old_name)

    def rightClickPathToClip(self, event, *args, **kwargs):
        """
        When you right click over an item in the folder treeview gets the
        path to that item and puts it in the clipboard so you can paste it
        somewhere elese.
        """
        # Get the path of the item in the row under the cursor position
        path = self.tree_folder.identify_row(event.y)
        # Clear the clipboard
        bpn.root.clipboard_clear()
        # Copy path to clipboard
        bpn.root.clipboard_append(path)
        # Get the file/directory name to use in info msg
        name = os.path.basename(path)

        # Set info msg
        bpn.info_bar.lastActionRefresh(f'Copied "{name}" Path to Clipboard')

    def insertNode(self, entry, tag="", *args, **kwargs):
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

    def refreshView(self, event=None, path="", tree=[], *args, **kwargs):
        """Get the folder path and update the treeview"""
        # If the path hasn't been given in the function call
        # if not path:
        #     # Get selected folder's path
        #     path = folder_treeview.selectedItem()
        # When the path is still not set use the active_path
        if not path:
            path = self.active_path

        # If after that the path is still empty (when a folder hasn't been
        # selected) don't try to load it
        if path:
            # Get the filters values
            filters_dict = bpn.filters_widget.fields.get_all()

            # Transform the list of extensions into a tuple and add a . before the
            # extension to make sure that its an extension and not just that the
            # filename ends in that
            exts = filters_dict.pop("ext")
            filters_dict["ext_tuple"] = [
                i for i in re.split(r";\s?|,\s?", exts)
            ]

            # Delete the children, load the new ones and sort them
            self.deleteChildren()

            scanned_dir = scandir_recursive_sorted(path, **filters_dict)

            for entry in scanned_dir:
                self.insertNode(entry)

            # Call info set actions
            self.active_path = path
            bpn.info_bar.numItemsRefresh(
                num_items=len(self.tree_folder.get_children()),
                num_sel_items=len(self.selectedItems()),
            )
            bpn.dir_entry_frame.folderDirSet()
            bpn.info_bar.lastActionRefresh("Refreshed File View")
