import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn

from . import basewidgets, info_bar, menubar, notebook
from .trees import trees


def windowInitialization():
    # Create the Tkinter window
    bpn.init_tk_root()
    # Set title
    bpn.root.title(bpn.TITLE)
    # Set window type to dialog to make it floating
    bpn.root.attributes("-type", "dialog")  # makes the window a pop up/dialog
    bpn.tk_init_post_hook()

    # Mainframe
    mainframe = ttk.Frame(bpn.root, padding="5 5 5 5")
    mainframe.grid(column=0, row=0, sticky="nwes")
    bpn.root.columnconfigure(0, weight=1)
    bpn.root.rowconfigure(0, weight=1)

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
    bpn.menu_bar.tk_init(bpn.root)
    bpn.root.config(menu=bpn.menu_bar)

    # Set Padding around the window
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Initialize the treeview
    bpn.folder_treeview.refreshView()
    # Initialize the global key bindings
    # Root_Binds()

    bpn.root.mainloop()
