import logging
import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn
import batchpynamer.gui as bpn_gui
from batchpynamer.gui import commands
from batchpynamer.gui.notebook.rename import rename
from batchpynamer.gui.trees import trees


class WindowRoot(tk.Tk):
    """Tkinter Root Window is created by __init__"""

    def tk_init(self, og_path):
        # Set title
        self.title(bpn.TITLE)
        # Set window type to dialog to make it floating
        self.attributes("-type", "dialog")  # makes the window a pop up/dialog
        bpn_gui.tk_init_post_hook()

        # Mainframe
        mainframe = ttk.Frame(self, padding="5 5 5 5")
        mainframe.grid(column=0, row=0, sticky="nwes")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Extra Information Bar
        bpn_gui.info_bar.tk_init(mainframe)

        # Tree view & File view
        trees.TreesFrame(mainframe, og_path, column=0, row=0, sticky="ew")

        # Notebook
        bpn_gui.changes_notebook.tk_init(mainframe)

        # Menubar
        bpn_gui.menu_bar.tk_init(self)
        self.config(menu=bpn_gui.menu_bar)

        # Set Padding around the window
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Initialize the global key bindings
        self.root_binds()

        self.mainloop()

    def root_binds(self):
        """Key bindings for the whole program

        "A" and "a" are different keys
        """

        # Refresh
        self.bind("<F5>", bpn_gui.dir_entry_frame.active_path_set)
        self.bind("<Control-F5>", trees.refresh_folderview_focus_node)
        self.bind("<Control-Shift-F5>", trees.refresh_folderview_full_tree)

        # Selection
        self.bind("<Control-a>", bpn_gui.fn_treeview.select_all)
        self.bind("<Control-A>", bpn_gui.fn_treeview.select_all)
        self.bind("<Control-d>", bpn_gui.fn_treeview.deselect_all)
        self.bind("<Control-D>", bpn_gui.fn_treeview.deselect_all)
        self.bind("<Control-i>", bpn_gui.fn_treeview.invert_selection)
        self.bind("<Control-I>", bpn_gui.fn_treeview.invert_selection)

        # Command
        self.bind("<Control-e>", commands.command_gui_load_command_call)
        self.bind("<Control-E>", commands.command_gui_load_command_call)
        self.bind("<Control-y>", commands.command_gui_apply_command_call)
        self.bind("<Control-Y>", commands.command_gui_apply_command_call)

        # Exit
        self.bind("<Control-Escape>", lambda event: self.quit())
        logging.debug("GUI- root binds")

    def rename_binds(self):
        # Entries Reset
        self.bind("<Control-t>", rename.rename_gui_all_fields_reset)
        self.bind("<Control-T>", rename.rename_gui_all_fields_reset)

        # Rename
        self.bind("<Control-r>", rename.rename_gui_apply_rename_call)
        self.bind("<Control-R>", rename.rename_gui_apply_rename_call)
        self.bind("<Control-z>", rename.rename_gui_undo_rename_call)
        self.bind("<Control-Z>", rename.rename_gui_undo_rename_call)

    def rename_unbinds(self):
        # Entries Reset
        self.unbind("<Control-t>")
        self.unbind("<Control-T>")

        # Rename
        self.unbind("<Control-r>")
        self.unbind("<Control-R>")
        self.unbind("<Control-z>")
        self.unbind("<Control-Z>")
