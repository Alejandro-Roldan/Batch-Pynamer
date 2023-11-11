import tkinter as tk
from tkinter import ttk

import batchpynamer.gui as bpn_gui
from batchpynamer.gui.basewidgets import BaseNamingWidget, BpnStrVar


class RenameFromRegExp(BaseNamingWidget, ttk.LabelFrame):  # (1)
    """
    Draws the Regular Expressions widget. Inside the rename notebook.
    1st thing to change.
    It has:
        - An entry to write the regular expression to match
        - An entry to write what the name should be
        - A button to extend the fields in a new window, which has:
            - A writeable text field for the regular expression to match
            - A writable text field for what the name should be
            - A button to close that window and write the content of the
            text fields to the entries.
    """

    def __init__(self):
        self.fields = self.Fields(
            reg_exp_match_reg=BpnStrVar(""),
            reg_exp_replace_with=BpnStrVar(""),
        )

    def tk_init(self, master):
        super().tk_init(
            master,
            column=1,
            row=0,
            text="Regular Expressions (1)",
        )

        # Match, entry
        ttk.Label(self, text="Match").grid(column=0, row=0, sticky="w")
        self.match_reg_entry = ttk.Entry(
            self,
            width=10,
            textvariable=self.fields.reg_exp_match_reg,
        )
        self.match_reg_entry.grid(column=1, row=0, sticky="ew")

        # Replace with, entry
        ttk.Label(self, text="Replace").grid(column=0, row=1, sticky="w")
        self.replace_with_entry = ttk.Entry(
            self,
            width=10,
            textvariable=self.fields.reg_exp_replace_with,
        )
        self.replace_with_entry.grid(column=1, row=1, sticky="ew")

        # Extended, button
        extended_button = ttk.Button(
            self,
            text="Extend",
            command=self.extended_reg_ex_window,
        )
        extended_button.grid(column=1, row=2, sticky="w")

        self.bindings()

    def extended_reg_ex_window(self):
        """
        Create a pop up window with extended entries for the
        regular expressions and a button 'Done' that saves the changes
        """
        self.ex_w_frame = tk.Toplevel(bpn_gui.root, bg="gray85")
        self.ex_w_frame.title("Extended Regular Expression Window")
        self.ex_w_frame.attributes("-type", "dialog")

        # Extended Match, text
        ttk.Label(self.ex_w_frame, text="Match").grid(
            column=0, row=0, sticky="w"
        )
        self.ex_match_reg_text = tk.Text(
            self.ex_w_frame, bg="white", fg="black", relief="sunken"
        )
        self.ex_match_reg_text.grid(column=0, row=1, sticky="ew")
        self.ex_match_reg_text.insert(
            "end", self.fields.reg_exp_match_reg.get()
        )

        # Extended Replace, text
        ttk.Label(self.ex_w_frame, text="Replace").grid(
            column=0, row=2, sticky="w"
        )
        self.ex_replace_with_text = tk.Text(
            self.ex_w_frame, bg="white", fg="black", relief="sunken"
        )
        self.ex_replace_with_text.grid(column=0, row=3, sticky="ew")
        self.ex_replace_with_text.insert(
            "end", self.fields.reg_exp_replace_with.get()
        )

        # Close window, button
        self.done_button = ttk.Button(
            self.ex_w_frame, text="Done", command=self.save_and_exit
        )
        self.done_button.grid(column=0, row=4, sticky="e")

    def save_and_exit(self):
        """
        Gets the values of the text widgets and saves it to the variables.
        Then kills the window.
        """
        ex_match_reg = self.ex_match_reg_text.get("1.0", "end")
        ex_replace_with = self.ex_replace_with_text.get("1.0", "end")

        # Remove the newline char
        ex_match_reg = ex_match_reg[:-1]
        ex_replace_with = ex_replace_with[:-1]

        # Save to variable
        self.fields.reg_exp_match_reg.set(ex_match_reg)
        self.fields.reg_exp_replace_with.set(ex_replace_with)

        # Kill window
        self.ex_w_frame.destroy()
