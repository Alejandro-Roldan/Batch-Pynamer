import os
import tkinter as tk
from tkinter import ttk

from scandirrecursive.scandirrecursive import scandir_recursive_sorted

import batchpynamer as bpn
from batchpynamer.basewidgets import BaseWidget
from batchpynamer.notebook.rename import rename


class DirectoryNavigator(BaseWidget, ttk.Frame):
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

        self.bindings()

    def bindings(self):
        """Defines the binded actions"""
        # Tree navigation bindings
        self.tree_nav.bind("<<TreeviewOpen>>", self.openNode)
        self.tree_nav.bind(
            "<<TreeviewSelect>>",
            lambda x: bpn.fn_treeview.refreshView(path=self.selectedItem()),
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
            hidden = bpn.filters_widget.fields.hidden.get()
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
        hidden = bpn.filters_widget.fields.hidden.get()

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
