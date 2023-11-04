import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn

from batchpynamer import basewidgets, info_bar, menubar, commands
from batchpynamer.trees import trees
from batchpynamer.notebook import notebook
from batchpynamer.notebook.rename import rename


class WindowRoot(tk.Tk):
    """Tkinter Root Window is created by __init__"""

    def tk_init(self):
        # Set title
        self.title(bpn.TITLE)
        # Set window type to dialog to make it floating
        self.attributes("-type", "dialog")  # makes the window a pop up/dialog
        bpn.tk_init_post_hook()

        # Mainframe
        mainframe = ttk.Frame(self, padding="5 5 5 5")
        mainframe.grid(column=0, row=0, sticky="nwes")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Extra Information Bar
        bpn.info_bar.tk_init(mainframe)

        # Tree view & File view
        # Frame Creation for the folder treeview, file view and the directory entry
        f_t_view_frame = ttk.Frame(mainframe)
        f_t_view_frame.grid(column=0, row=0, sticky="we")
        f_t_view_frame.columnconfigure(1, weight=1)

        bpn.fn_treeview.tk_init(f_t_view_frame)
        bpn.folder_treeview.tk_init(f_t_view_frame, path=bpn.OG_PATH)
        bpn.dir_entry_frame.tk_init(f_t_view_frame)

        # Notebook
        bpn.changes_notebook.tk_init(mainframe)

        # Menubar
        bpn.menu_bar.tk_init(self)
        self.config(menu=bpn.menu_bar)

        # Set Padding around the window
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # Initialize the treeview
        bpn.folder_treeview.refreshView()

        # Initialize the global key bindings
        self.root_binds()

        self.mainloop()

    def root_binds(self):
        """Key bindings for the whole program

        "A" and "a" are different keys
        """

        # Entries Reset
        self.bind("<Control-t>", rename.full_reset)
        self.bind("<Control-T>", rename.full_reset)

        # Rename
        self.bind("<Control-r>", rename.final_rename)
        self.bind("<Control-R>", rename.final_rename)
        self.bind("<Control-z>", rename.undo_rename)
        self.bind("<Control-Z>", rename.undo_rename)

        # Refresh
        self.bind("<F5>", bpn.fn_treeview.refreshView)
        self.bind("<Control-F5>", bpn.folder_treeview.updateNode)
        self.bind("<Control-Shift-F5>", bpn.folder_treeview.refreshView)

        # Selection
        self.bind("<Control-a>", bpn.fn_treeview.selectAll)
        self.bind("<Control-A>", bpn.fn_treeview.selectAll)
        self.bind("<Control-d>", bpn.fn_treeview.deselectAll)
        self.bind("<Control-D>", bpn.fn_treeview.deselectAll)
        self.bind("<Control-i>", bpn.fn_treeview.invertSelection)
        self.bind("<Control-I>", bpn.fn_treeview.invertSelection)

        # Command
        self.bind("<Control-e>", commands.load_command_call)
        self.bind("<Control-E>", commands.load_command_call)
        self.bind("<Control-y>", rename.apply_command)
        self.bind("<Control-Y>", rename.apply_command)

        # Exit
        self.bind("<Control-Escape>", lambda event: self.quit())
