from tkinter import ttk

import batchpynamer.gui as bpn_gui
from batchpynamer.gui.basewidgets import BaseFieldsWidget, BpnStrVar


class Info_Bar(BaseFieldsWidget, ttk.Frame):
    """
    A bar that displays information at the bottom of the window:
    - Number of items displayed in the File Navigator, and selected items
    - Relevant information messages (errors, last completed action...)
    """

    def __init__(self):
        self.fields = self.Fields(
            items_count=BpnStrVar(""),
            last_action=BpnStrVar(""),
        )

    def tk_init(self, master, **kwargs):
        super().__init__(master=master, column=0, row=2, sticky="we", **kwargs)
        self.columnconfigure(1, weight=1)

        # Items, label
        self.items_label = ttk.Label(
            self, textvariable=self.fields.items_count, relief="sunken"
        )
        self.items_label.grid(column=0, row=0, ipadx=50, ipady=2, padx=4)

        # Last completed action, label
        self.action_label = ttk.Label(
            self, textvariable=self.fields.last_action, relief="sunken"
        )
        self.action_label.grid(column=1, row=0, sticky="we", ipady=2, padx=4)

        self.items_count_set()

    def items_count_set(self, num_items=0, num_sel_items=0):
        """Number of items refresher"""
        # Message to display
        items_text = f"{num_items} items ({num_sel_items} selected)"
        # Set the text variable with the message
        self.fields.items_count.set(items_text)

    def last_action_set(self, action):
        """Display a message, passed in the action variable"""
        # Set the text variable with the message
        self.fields.last_action.set(action)


def show_working(inf_msg="Working..."):
    """
    Sets the cursor to "watch" and empties the info msg to show that
    you have to wait.
    Remember calling Finish_Show_Working() after the work is done.
    """

    # Set mouse pointer to watch
    bpn_gui.root.config(cursor="watch")
    # Delete the last action text from the info bar
    bpn_gui.info_bar.last_action_set(inf_msg)
    # Needs the update call so the window can apply this changes
    bpn_gui.root.update()


def finish_show_working(inf_msg="Done"):
    """Sets cursor to arrow and sets the info msg."""

    # Set mouse pointer back to arrow
    bpn_gui.root.config(cursor="arrow")
    # Show that its finish by setting the info bar message.
    bpn_gui.info_bar.last_action_set(inf_msg)
