import tkinter as tk
from tkinter import ttk

import batchpynamer
from . import basewidgets

# from . import constants
from . import info
from . import menubar
from . import notebook

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
    # info_bar = info.Info_Bar(mainframe)
    batchpynamer.info_bar.tk_init(mainframe)

    # Tree view & File view
    # Frame Creation for the folder treeview, file view and the directory entry
    f_t_view_frame = ttk.Frame(mainframe)
    f_t_view_frame.grid(column=0, row=0, sticky="we")
    f_t_view_frame.columnconfigure(1, weight=1)

    # fn_treeview = trees.File_Navigator(
    batchpynamer.fn_treeview.tk_init(
        f_t_view_frame,
        # brothers={"info_bar": info_bar},
    )
    # folder_treeview = trees.Directory_Navigator(
    batchpynamer.folder_treeview.tk_init(
        f_t_view_frame,
        path=batchpynamer.OG_PATH,
        # brothers={"fn_treeview": fn_treeview},
    )
    # dir_entry_frame = trees.Directory_Entry_Frame(
    batchpynamer.dir_entry_frame.tk_init(
        f_t_view_frame,
        # brothers={
        #     "folder_treeview": folder_treeview,
        #     "fn_treeview": fn_treeview,
        #     "info_bar": info_bar,
        # },
    )

    # Notebook
    # changes_notebook = notebook.Changes_Notebook(
    batchpynamer.changes_notebook.tk_init(
        mainframe,
        # brothers={
        #     "folder_treeview": folder_treeview,
        #     "fn_treeview": fn_treeview,
        #     "info_bar": info_bar,
        # },
    )

    # Menubar
    # menu_bar = menubar.Top_Menu(
    batchpynamer.menu_bar.tk_init(
        root,
        # brothers={
        #     "root": root,
        #     "folder_treeview": folder_treeview,
        #     "fn_treeview": fn_treeview,
        #     "dir_entry_frame": dir_entry_frame,
        #     "info_bar": info_bar,
        #     "changes_notebook": changes_notebook,
        # },
    )
    root.config(menu=batchpynamer.menu_bar.menubar)

    # Set Padding around the window
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Initialize the treeview
    batchpynamer.folder_treeview.refreshView()
    # # Initialize the global key bindings
    # Root_Binds()

    root.mainloop()
