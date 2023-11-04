import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn

from batchpynamer.basewidgets import (
    BaseNamingWidget,
    BpnComboVar,
    BpnIntVar,
    BpnStrVar,
)


class MoveParts(BaseNamingWidget, ttk.LabelFrame):  # (6)
    """
    Draws the move/copy parts widget. Inside rename notebook.
    6th thing to change.
    It has:
        - Combobox to select where to select the text from (start, end)
        - ttk.Spinbox to select how many characters to select
        - Combobox to select where to paste the char(s) to
        (start, end, position)
        - ttk.Spinbox to select where to paste when 'position' is selected
        - Entry to write a separator
    """

    def __init__(self):
        pass

    def tk_init(self, master):
        super().__init__(
            master,
            column=0,
            row=2,
            columnspan=3,
            text="Move Parts (6)",
        )
        super().tk_init(reset_column_row=(10, 1))

        # Variable defs
        self.fields = self.Fields(
            move_parts_ori_pos=BpnComboVar(("None", "Start", "End")),
            move_parts_ori_n=BpnIntVar(0),
            move_parts_end_pos=BpnComboVar(("Start", "End", "Position")),
            move_parts_end_n=BpnIntVar(0),
            move_parts_sep=BpnStrVar(""),
        )

        # Copy from, combobox
        ttk.Label(self, text="Copy").grid(column=0, row=0)
        self.ori_pos_combo = ttk.Combobox(
            self,
            width=5,
            state="readonly",
            values=self.fields.move_parts_ori_pos.options,
            textvariable=self.fields.move_parts_ori_pos,
        )
        self.ori_pos_combo.grid(column=1, row=0, sticky="ew")

        # Copy n characters, spinbox
        ttk.Label(self, text="Chars.").grid(column=2, row=0)
        self.ori_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.move_parts_ori_n,
        )
        self.ori_n_spin.grid(column=3, row=0)

        # Paste to, combobox
        ttk.Label(self, text="Paste").grid(column=4, row=0)
        self.end_pos_combo = ttk.Combobox(
            self,
            width=5,
            state="readonly",
            values=self.fields.move_parts_end_pos.options,
            textvariable=self.fields.move_parts_end_pos,
        )
        self.end_pos_combo.grid(column=5, row=0, sticky="ew")

        # Paste in n position, spinbox
        ttk.Label(self, text="Pos.").grid(column=6, row=0)
        self.end_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.move_parts_end_n,
        )
        self.end_n_spin.grid(column=7, row=0)

        # Separator between pasted part and position, entry
        ttk.Label(self, text="Sep.").grid(column=8, row=0)
        self.sep_entry = ttk.Entry(
            self, width=5, textvariable=self.fields.move_parts_sep
        )
        self.sep_entry.grid(column=9, row=0)

        self.bindEntries()

    def bindEntries(self):
        """Defines the binded actions"""
        super().bindEntries()

        self.fields.move_parts_ori_n.trace_add("write", self.fromAddTo)
        self.fields.move_parts_end_n.trace_add("write", self.fromAddTo)

    def fromAddTo(self, *args, **kwargs):
        """
        Checks if the from_n value is bigger than the to_n value,
        If so raises the to_n value accordingly.
        """
        a = self.fields.move_parts_ori_n.get()
        b = self.fields.move_parts_end_n.get()

        if a > b:
            self.fields.move_parts_end_n.set(a)


def move_copy_action(name, fields_dict):
    """
    Copies and pastes the selected characters to the selected
    position.
    """
    move_parts_ori_pos = fields_dict.get("move_parts_ori_pos")
    move_parts_ori_n = fields_dict.get("move_parts_ori_n")
    move_parts_end_pos = fields_dict.get("move_parts_end_pos")
    move_parts_end_n = fields_dict.get("move_parts_end_n")
    move_parts_sep = fields_dict.get("move_parts_sep")

    if move_parts_ori_pos == "Start":
        if move_parts_end_pos == "End":
            name = (
                name[move_parts_ori_n:]
                + move_parts_sep
                + name[:move_parts_ori_n]
            )

        elif move_parts_end_pos == "Position":
            name = (
                name[move_parts_ori_n:move_parts_end_n]
                + move_parts_sep
                + name[:move_parts_ori_n]
                + move_parts_sep
                + name[move_parts_end_n:]
            )

    elif move_parts_ori_pos == "End":
        if move_parts_end_pos == "Start":
            name = (
                name[-move_parts_ori_n:]
                + move_parts_sep
                + name[:-move_parts_ori_n]
            )

        elif move_parts_end_pos == "Position":
            name = (
                name[:move_parts_end_n]
                + move_parts_sep
                + name[-move_parts_ori_n:]
                + move_parts_sep
                + name[move_parts_end_n:-move_parts_ori_n]
            )

    return name
