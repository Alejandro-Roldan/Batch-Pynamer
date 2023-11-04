import tkinter as tk
from tkinter import ttk

import batchpynamer
from . import basewidgets
from . import mainwindow


class Info_Bar(basewidgets.BaseWidget, ttk.Frame):
    """
    A bar that displays information at the bottom of the window:
    - Number of items displayed in the File Navigator, and selected items
    - Relevant information messages (errors, last completed action...)
    """

    def __init__(self):
        pass

    def tk_init(self, master, **kwargs):
        super().__init__(master=master, column=0, row=2, sticky="we", **kwargs)
        self.columnconfigure(1, weight=1)

        self.items_text_var = tk.StringVar()
        self.action_text_var = tk.StringVar()

        # Items, label
        self.items_label = ttk.Label(
            self, textvariable=self.items_text_var, relief="sunken"
        )
        self.items_label.grid(column=0, row=0, ipadx=50, ipady=2, padx=4)

        # Last completed action, label
        self.action_label = ttk.Label(
            self, textvariable=self.action_text_var, relief="sunken"
        )
        self.action_label.grid(column=1, row=0, sticky="we", ipady=2, padx=4)

        self.numItemsRefresh()

    def numItemsRefresh(self, num_items=0, num_sel_items=0):
        """Number of items refresher"""
        # Message to display
        items_text = f"{num_items} items ({num_sel_items} selected)"
        # Set the text variable with the message
        self.items_text_var.set(items_text)

    def lastActionRefresh(self, action):
        """Display a message, passed in the action variable"""
        # Set the text variable with the message
        self.action_text_var.set(action)


def show_working(inf_msg="Working..."):
    """
    Sets the cursor to "watch" and empties the info msg to show that
    you have to wait.
    Remember calling Finish_Show_Working() after the work is done.
    """

    # Set mouse pointer to watch
    mainwindow.root.config(cursor="watch")
    # Delete the last action text from the info bar
    batchpynamer.info_bar.lastActionRefresh(inf_msg)
    # Needs the update call so the window can apply this changes
    mainwindow.root.update()


def finish_show_working(inf_msg="Done"):
    """Sets cursor to arrow and sets the info msg."""

    # Set mouse pointer back to arrow
    mainwindow.root.config(cursor="arrow")
    # Show that its finish by setting the info bar message.
    batchpynamer.info_bar.lastActionRefresh(inf_msg)
