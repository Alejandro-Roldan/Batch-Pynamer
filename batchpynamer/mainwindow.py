import tkinter as tk
from tkinter import ttk

import batchpynamer

# from . import constants
from . import basewidgets, info_bar, menubar, notebook

# from . import trees
from .trees import trees


def windowInitialization():
    # Create the Tkinter window
    global root
    root = tk.Tk()
    # Set title
    root.title(batchpynamer.TITLE)
    # Set window type to dialog to make it floating
    root.attributes("-type", "dialog")  # makes the window a pop up/dialog
    batchpynamer.tk_init_hook()

    # Mainframe
    mainframe = ttk.Frame(root, padding="5 5 5 5")
    mainframe.grid(column=0, row=0, sticky="nwes")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Extra Information Bar
    batchpynamer.info_bar.tk_init(mainframe)

    # Tree view & File view
    # Frame Creation for the folder treeview, file view and the directory entry
    f_t_view_frame = ttk.Frame(mainframe)
    f_t_view_frame.grid(column=0, row=0, sticky="we")
    f_t_view_frame.columnconfigure(1, weight=1)

    batchpynamer.fn_treeview.tk_init(f_t_view_frame)
    batchpynamer.folder_treeview.tk_init(
        f_t_view_frame, path=batchpynamer.OG_PATH
    )
    batchpynamer.dir_entry_frame.tk_init(f_t_view_frame)

    # Notebook
    batchpynamer.changes_notebook.tk_init(mainframe)

    # Menubar
    batchpynamer.menu_bar.tk_init(root)
    root.config(menu=batchpynamer.menu_bar)

    # Set Padding around the window
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Initialize the treeview
    batchpynamer.folder_treeview.refreshView()
    # Initialize the global key bindings
    # Root_Binds()

    root.mainloop()
