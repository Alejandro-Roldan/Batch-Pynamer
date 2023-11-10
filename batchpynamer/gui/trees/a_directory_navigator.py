import logging
import os
from tkinter import TclError, ttk

from scandirrecursive.scandirrecursive import scandir_recursive_sorted

import batchpynamer.gui as bpn_gui
from batchpynamer.gui.basewidgets import BaseWidget


class DirectoryNavigator(BaseWidget, ttk.Frame):
    def __init__(self):
        # Create a dict of what nodes exist that are empty. Used to load the
        # placeholder nodes
        self.empty_nodes = {}

    def tk_init(self, master, path):
        """
        Draws the treeview of the file navigation:
            It exclusively shows folders.
            You can only select one item at a time.
            It creates a temporary child node (empty) inside the folders to be
            able to open them without having to load the directories inside.
            If this wasn't done the app would have to load the whole system
            at starup.
        """
        super().__init__(master=master, column=0, row=1)

        self.path = path
        # self.empty_nodes[path] = path

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

        self.tree_nav.insert(
            parent="",
            index="end",
            iid=self.path,
            text=self.path,
            open=True,
        )
        self.bindings()

        # Initialize the treeview
        self.refresh_full_tree_call()

    def bindings(self):
        """Defines the binded actions"""
        # Tree navigation bindings
        self.tree_nav.bind("<<TreeviewOpen>>", self.open_node_call)
        self.tree_nav.bind(
            "<<TreeviewSelect>>",
            lambda x: bpn_gui.dir_entry_frame.active_path_set(
                new_active_path=self.selected_item()
            ),
        )

    def selected_item(self):
        # Since this tree can only select 1 item at a time we just pass
        # the index instead of doing a for loop
        return self.tree_nav.focus()

    def refresh_full_tree_call(self, event=None):
        self.refresh_node(self.path)

    def update_active_node_call(self, event=None):
        """Updates the focused node.

        Close focused node, deletes all children and inserts an empty node
        """
        path = self.tree_nav.focus()
        self.refresh_node(path)

    def open_node_call(self, event=None):
        """Open Node action"""
        # Get active node
        path = self.selected_item()
        self.fill_node(path)

    def refresh_node(self, node):
        self.delete_node_children(node)
        self.empty_nodes[node] = node
        self.fill_node(node=node)
        logging.info(f"GUI- Refreshed directory view node: {node}")

    def delete_node_children(self, node):
        """Delete all existing nodes in the folder view"""
        try:
            # Delete sub-nodes
            for child in self.tree_nav.get_children(node):
                self.tree_nav.delete(child)
        except TclError:
            pass

    def fill_node(self, node):
        """Open Node action. Only avaible to the tree file navigation."""

        def _insert_node(entry):
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
            self.empty_nodes[node] = entry.path

            # Make dirs openable without loading children by creating an empty
            # node inside
            self.tree_nav.insert(parent=node, index="end")

        # Get the path to the directory of the opening node and only act when
        # it finds it in the dictionary (which means the node hasn't been
        # opened previously, if it where then there would be no need to reload
        # the contents)
        if self.empty_nodes.pop(node, None):
            # Delete the placeholder node that was created previously
            self.delete_node_children(node)

            # Get if we need to show hidden folders
            hidden = bpn_gui.filters_widget.fields.hidden.get()
            # Get folders and sort them
            try:
                scanned_dir = scandir_recursive_sorted(
                    path=node,
                    folders=True,
                    files=False,
                    hidden=hidden,
                    depth=0,
                )
            # When file not found refresh parent node
            except FileNotFoundError:
                self.refresh_node(self.tree_nav.parent(node))
            else:
                # Insert the entries
                for entry in scanned_dir:
                    _insert_node(entry)
