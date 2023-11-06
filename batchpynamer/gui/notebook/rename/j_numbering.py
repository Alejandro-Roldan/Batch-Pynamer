# import string
import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn
from batchpynamer.gui.basewidgets import (
    BaseNamingWidget,
    BpnComboVar,
    BpnIntVar,
    BpnStrVar,
)


class Numbering(BaseNamingWidget, ttk.LabelFrame):  # (9)
    """
    Draws the numbering widget. Inside the rename notebook. 9th thing
    to change.
    It has:
        - Dropdown that lets you shoose position
        - ttk.Spinbox to choose at what place in the middle of the name
        - ttk.Spinbox to choose from what number to start numbering
        - ttk.Spinbox to choose the numbering step
        - ttk.Spinbox for how many 0 to use
        - Entry for a separator
        - Dropdown to choose the type of numbering
            - Base 10
            - Base 2
            - Base 8
            - Base 16
            - Uppercase letters
            - Lowercase letter
    """

    def __init__(self):
        self.fields = self.Fields(
            numbering_mode=BpnComboVar(
                ("None", "Prefix", "Suffix", "Both", "Position")
            ),
            numbering_at_n=BpnIntVar(0),
            numbering_start_num=BpnIntVar(0),
            numbering_incr_num=BpnIntVar(1),
            numbering_pad=BpnIntVar(1),
            numbering_sep=BpnStrVar(""),
            numbering_type_base=BpnComboVar(
                (
                    "Base 10",
                    "Base 2",
                    "Base 8",
                    "Base 16",
                    "Upper Case Letters",
                    "Lower Case Letters",
                )
            ),
        )

    def tk_init(self, master):
        super().__init__(
            master,
            column=5,
            row=0,
            rowspan=2,
            text="Numbering (9)",
        )
        super().tk_init(reset_column_row=(4, 5))

        # Mode, combobox
        ttk.Label(self, text="Mode").grid(column=0, row=0, sticky="ew")
        self.mode_combo = ttk.Combobox(
            self,
            width=5,
            state="readonly",
            values=self.fields.numbering_mode.options,
            textvariable=self.fields.numbering_mode,
        )
        self.mode_combo.grid(column=1, row=0, sticky="ew")

        # At position, spinbox
        ttk.Label(self, text="At").grid(column=2, row=0, sticky="ew")
        self.at_n_spin = ttk.Spinbox(
            self,
            width=3,
            from_=-bpn.MAX_NAME_LEN,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.numbering_at_n,
        )
        self.at_n_spin.grid(column=3, row=0)

        # Start from this number, spinbox
        ttk.Label(self, text="Start").grid(column=0, row=1, sticky="ew")
        self.start_num_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.numbering_start_num,
        )
        self.start_num_spin.grid(column=1, row=1)

        # Step, spinbox
        ttk.Label(self, text="Incr.").grid(column=2, row=1, sticky="ew")
        self.incr_num_spin = ttk.Spinbox(
            self,
            width=3,
            from_=1,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.numbering_incr_num,
        )
        self.incr_num_spin.grid(column=3, row=1)

        # Padding of possible 0s, spinbox
        ttk.Label(self, text="Pad.").grid(column=0, row=2, sticky="ew")
        self.pad_spin = ttk.Spinbox(
            self,
            width=3,
            from_=1,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.numbering_pad,
        )
        self.pad_spin.grid(column=1, row=2)

        # Separator, entry
        ttk.Label(self, text="Sep.").grid(column=2, row=2, sticky="ew")
        self.sep_entry = ttk.Entry(
            self, width=5, textvariable=self.fields.numbering_sep
        )
        self.sep_entry.grid(column=3, row=2, sticky="ew")

        # Type of enumeration/Base, combobox
        ttk.Label(self, text="Type").grid(column=0, row=3, sticky="w")
        self.type_base_combo = ttk.Combobox(
            self,
            width=5,
            state="readonly",
            values=self.fields.numbering_type_base.options,
            textvariable=self.fields.numbering_type_base,
        )
        self.type_base_combo.grid(column=1, row=3, columnspan=3, sticky="ew")

        self.bindings()
