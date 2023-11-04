import os
import re
import tkinter as tk
from tkinter import ttk

from scandirrecursive.scandirrecursive import scandir_recursive_sorted

import batchpynamer
from batchpynamer import mainwindow

from .. import basewidgets
from ..rename import rename


class Directory_Navigator(basewidgets.BaseWidget, ttk.Frame):
    def __init__(self):
        pass

    def tk_init(self, master, path, **kwargs):
        """
        Draws the treeview of the file navigation:
            It exclusively shows folders.
            You can only select one item at a time.
            It creates a temporary child node (empty) inside the folders to be
            able to open them without having to load the directories inside.
            If this wasn't done the app would have to load the whole system
            at starup.
        """
        super().__init__(master=master, column=0, row=1, **kwargs)

        self.path = path

        # Create a dict of what nodes exist. Used to load the placeholder nodes
        self.nodes = {}

        # Directory navigator, treeview
        self.tree_nav = ttk.Treeview(self, selectmode="browse")
        # Scroll bars tree file navigation
        ysb_tree_nav = ttk.Scrollbar(
            self, orient="vertical", command=self.tree_nav.yview
        )
        xsb_tree_nav = ttk.Scrollbar(
            self, orient="horizontal", command=self.tree_nav.xview
        )
        self.tree_nav.configure(
            yscroll=ysb_tree_nav.set, xscroll=xsb_tree_nav.set
        )
        # Title of the Treeview
        self.tree_nav.heading("#0", text="Directory Browser", anchor="w")
        self.tree_nav.column("#0", width=280)
        # Treeview and the scrollbars placing
        self.tree_nav.grid(row=0, column=0)
        ysb_tree_nav.grid(row=0, column=1, sticky="ns")
        xsb_tree_nav.grid(row=1, column=0, sticky="ew")

        self.bindEntries()

    def bindEntries(self):
        """Defines the binded actions"""
        # Tree navigation bindings
        self.tree_nav.bind("<<TreeviewOpen>>", self.openNode)
        self.tree_nav.bind(
            "<<TreeviewSelect>>",
            lambda x: batchpynamer.fn_treeview.refreshView(
                path=self.selectedItem()
            ),
        )

    def selectedItem(self):
        # Since this tree can only select 1 item at a time we just pass
        # the index instead of doing a for loop
        return self.tree_nav.focus()

    def deleteChildren(self, path=""):
        """Delete all existing nodes in the folder view"""
        for child in self.tree_nav.get_children(path):
            self.tree_nav.delete(child)

    def insertNode(self, entry):
        """Create nodes for the tree file navigation."""
        parent = os.path.dirname(entry.path)

        # Uses the absolute path to the folder as the iid
        node = self.tree_nav.insert(
            parent=parent,
            index="end",
            iid=entry.path,
            text=entry.name,
            open=False,
        )

        # Make dirs openable without loading children by creating an empty
        # node inside
        self.nodes[node] = entry.path
        self.tree_nav.insert(parent=node, index="end")

    def openNode(self, event=None):
        """Open Node action. Only avaible to the tree file navigation."""
        # Get active node
        path = self.tree_nav.focus()

        # Get the path to the directory of the opening node and only act when
        # it finds it in the dictionary (which means the node hasn't been
        # opened previously, if it where then there would be no need to reload
        # the contents)
        if self.nodes.pop(path, None):
            # Delete the placeholder node that was created previously
            self.tree_nav.delete(self.tree_nav.get_children(path))

            # Get if we need to show hidden folders
            hidden = batchpynamer.filters_widget.fields.hidden.get()
            # hidden = False
            # Get folders and sort them
            scanned_dir = scandir_recursive_sorted(
                path=path, folders=True, files=False, hidden=hidden, depth=0
            )
            # Insert the entries
            for entry in scanned_dir:
                self.insertNode(entry)

    def refreshView(self, *args):
        path = self.path
        # Get if hidden folders are active
        hidden = batchpynamer.filters_widget.fields.hidden.get()
        # hidden = False

        # Delete all children and reset Treeview
        self.deleteChildren()
        # Insert the original node
        self.tree_nav.insert(
            parent="", index="end", iid=self.path, text=self.path, open=True
        )

        scanned_dir = scandir_recursive_sorted(
            path=path, folders=True, files=False, hidden=hidden, depth=0
        )

        for entry in scanned_dir:
            self.insertNode(entry)

    def updateNode(self):
        """
        Updates the focused node.
        Close focused node, deletes all children and inserts an empty node
        """
        path = self.tree_nav.focus()
        if path:
            # Close focused node
            self.tree_nav.item(path, open=False)
            # Delete children nodes of the focused node
            self.deleteChildren(path)

            # Reinsert an empty node
            self.tree_nav.insert(path, "end")
            self.nodes[path] = path


class File_Navigator(basewidgets.BaseWidget, ttk.Frame):
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
        self.bindEntries()

    def oldNameGet(self, item):
        return self.tree_folder.item(item)["text"]

    def bindEntries(self):
        """Defines the binded actions"""
        # File Navigation bindings
        self.tree_folder.bind(
            "<<TreeviewSelect>>", batchpynamer.changes_notebook.populate_fields
        )
        # add='+' to not just rebind the action but to make it so both happen
        self.tree_folder.bind("<<TreeviewSelect>>", self.infoBarCall, add="+")
        self.tree_folder.bind("<Button-3>", self.rightClickPathToClip)

    def infoBarCall(self, event=None):
        """Refresh the number of items in the info bar"""
        # self.info_bar.numItemsRefresh(
        batchpynamer.info_bar.numItemsRefresh(
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
        root.clipboard_clear()
        # Copy path to clipboard
        root.clipboard_append(path)
        # Get the file/directory name to use in info msg
        name = os.path.basename(path)

        # Set info msg
        inf_bar.lastActionRefresh('Copied "{}" Path to Clipboard'.format(name))

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
            filters_dict = batchpynamer.filters_widget.fields.get_all()

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
            batchpynamer.info_bar.numItemsRefresh(
                num_items=len(self.tree_folder.get_children()),
                num_sel_items=len(self.selectedItems()),
            )
            batchpynamer.dir_entry_frame.folderDirSet()
            batchpynamer.info_bar.lastActionRefresh("Refreshed File View")


class Directory_Entry_Frame(basewidgets.BaseWidget, ttk.Frame):
    """
    Draws a entry field that has the active directory path, and that can
    be used to go to an specific directory directly by writing on it and
    using ENTER.
    It also has a R button to refresh the directory navigator.
    One click refreshes the active node, two the whole tree.
    """

    def __init__(self):
        pass

    def tk_init(self, master, **kwargs):
        super().__init__(
            master=master,
            column=0,
            row=0,
            columnspan=2,
            sticky="we",
            **kwargs,
        )
        # Set the weight of the entry column so it extends the whole frame
        self.columnconfigure(1, weight=1)

        self.folder_dir = tk.StringVar()

        # Folder Navigation Refresh, button
        self.folder_nav_refresh_button = ttk.Button(self, width=2, text="R")
        self.folder_nav_refresh_button.grid(column=0, row=0, sticky="w")

        # Folder path, entry
        self.folder_dir_entry = ttk.Entry(self, textvariable=self.folder_dir)
        self.folder_dir_entry.grid(column=1, row=0, sticky="w" + "e")

        # self.folder_treeview = folder_treeview
        # self.fn_treeview = fn_treeview
        # self.fn_treeview.directory_entry_frame = self

        # self.info_bar = info_bar

        self.bindEntries()

    def folderDirGet(self, *args, **kwargs):
        return self.folder_dir.get()

    def bindEntries(self, *args, **kwargs):
        self.folder_dir_entry.bind("<Return>", self.openFolderTreeNav)
        self.folder_nav_refresh_button.bind(
            "<Button-1>", self.focusFolderRefresh
        )
        self.folder_nav_refresh_button.bind(
            "<Double-1>", self.folderNavRefresh
        )

    def folderNavRefresh(self, *args, **kwargs):
        """Refreshes the folder navigation treeview"""
        # self.folder_treeview.refreshView()
        batchpynamer.folder_treeview.refreshView()
        # self.info_bar.lastActionRefresh("Refreshed Browse Files Treeview")
        batchpynamer.info_bar.lastActionRefresh(
            "Refreshed Browse Files Treeview"
        )

    def focusFolderRefresh(self, *args, **kwargs):
        """Refreshes the focused folder in the navigation treeview"""
        # self.folder_treeview.updateNode()
        batchpynamer.folder_treeview.updateNode()
        # self.info_bar.lastActionRefresh(
        batchpynamer.info_bar.lastActionRefresh(
            "Refreshed Focused Directory in Treeview"
        )

    def folderDirSet(self, *args, **kwargs):
        # folder_path = self.fn_treeview.active_path
        folder_path = batchpynamer.fn_treeview.active_path
        self.folder_dir.set(folder_path)

    def openFolderTreeNav(self, *args, **kwags):
        """Loads the writen path to the file navigator treeview"""
        folder_path = self.folderDirGet()
        # Check if the path is a valid directory
        if os.path.isdir(folder_path):
            # self.fn_treeview.refreshView(path=folder_path)
            batchpynamer.fn_treeview.refreshView(path=folder_path)
        else:
            # self.info_bar.lastActionRefresh("Not a Valid Directory")
            batchpynamer.info_bar.lastActionRefresh("Not a Valid Directory")
            self.folderDirSet()


def Refresh_Treeviews(*args, **kwargs):
    """Refreshes Both Treeviews"""
    # Update the file view
    batchpynamer.fn_treeview.refreshView()
    # Update the folder view
    batchpynamer.folder_treeview.updateNode()

    batchpynamer.info_bar.lastActionRefresh("Refreshed Both Treeviews")
