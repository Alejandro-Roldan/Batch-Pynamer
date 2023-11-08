import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn
from batchpynamer.gui import utils as bpn_gui_utils
from batchpynamer.gui.basewidgets import (
    BaseNamingWidget,
    BpnBoolVar,
    BpnComboVar,
    BpnIntVar,
    BpnStrVar,
)
from batchpynamer.gui.notebook.rename.utils import spin_box_lower_limit_update


class Remove(BaseNamingWidget, ttk.LabelFrame):  # (5)
    """
    Draws the Remove widget. Inside rename notebook. 5th thing to change.
    It has:
        - ttk.Spinbox to remove the first n char(s)
        - ttk.Spinbox to remove the last n char(s)
        - ttk.Spinbox to choose what char to remove from
        - ttk.Spinbox to choose what char to remove up to
        - Entry for char(s) to remove
        - Entry for word(s) to remove
        - Combobox to crop (before, after)
        - Entry for what to remove before/after
        - Checkbutton to remove digits
        - Checkbutton to remove D/S
        - Checkbutton to remove accents
        - Checkbutton to remove chars
        - Checkbutton to remove sym
        - Combobox to remove lead dots (None,...)
        - Reset button
    """

    def __init__(self):
        self.fields = self.Fields(
            remove_first_n=BpnIntVar(0),
            remove_last_n=BpnIntVar(0),
            remove_from_n=BpnIntVar(0),
            remove_to_n=BpnIntVar(0),
            remove_rm_words=BpnStrVar(""),
            remove_rm_chars=BpnStrVar(""),
            remove_crop_pos=BpnComboVar(("Before", "After", "Special")),
            remove_crop_this=BpnStrVar(""),
            remove_digits=BpnBoolVar(False),
            remove_d_s=BpnBoolVar(True),
            remove_accents=BpnBoolVar(False),
            remove_chars=BpnBoolVar(False),
            remove_sym=BpnBoolVar(False),
            remove_lead_dots=BpnComboVar(("None", ".", "..")),
        )

    def tk_init(self, master):
        super().__init__(
            master,
            column=3,
            row=0,
            rowspan=2,
            text="Remove (5)",
        )
        super().tk_init(reset_column_row=(4, 7))

        # Remove first n characters, spinbox
        ttk.Label(self, text="First n").grid(column=0, row=0, sticky="ew")
        self.first_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn_gui_utils.drive_max_name_len(),
            textvariable=self.fields.remove_first_n,
        )
        self.first_n_spin.grid(column=1, row=0)

        # Remove las n characters, spinbox
        ttk.Label(self, text="Last n").grid(column=2, row=0, sticky="ew")
        self.last_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn_gui_utils.drive_max_name_len(),
            textvariable=self.fields.remove_last_n,
        )
        self.last_n_spin.grid(column=3, row=0)

        # Remove from this char position, spinbox
        ttk.Label(self, text="From").grid(column=0, row=1, sticky="ew")
        self.from_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn_gui_utils.drive_max_name_len(),
            textvariable=self.fields.remove_from_n,
        )
        self.from_n_spin.grid(column=1, row=1)

        # Remove to this char position, spinbox
        ttk.Label(self, text="To").grid(column=2, row=1, sticky="ew")
        self.to_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn_gui_utils.drive_max_name_len(),
            textvariable=self.fields.remove_to_n,
        )
        self.to_n_spin.grid(column=3, row=1)

        # Remove word(s), entry
        ttk.Label(self, text="Words").grid(column=0, row=2, sticky="ew")
        self.rm_words_entry = ttk.Entry(
            self,
            width=5,
            textvariable=self.fields.remove_rm_words,
        )
        self.rm_words_entry.grid(column=1, row=2, sticky="ew")

        # Remove character(s), entry
        ttk.Label(self, text="Chars.").grid(column=2, row=2, sticky="ew")
        self.rm_chars_entry = ttk.Entry(
            self,
            width=5,
            textvariable=self.fields.remove_rm_chars,
        )
        self.rm_chars_entry.grid(column=3, row=2, sticky="ew")

        # Choose where to crop, combobox
        ttk.Label(self, text="Crop").grid(column=0, row=3, sticky="w")
        self.crop_combo = ttk.Combobox(
            self,
            width=5,
            state="readonly",
            values=self.fields.remove_crop_pos.options,
            textvariable=self.fields.remove_crop_pos,
        )
        self.crop_combo.grid(column=1, row=3, sticky="ew")

        # Crop, entry
        self.crop_this_entry = ttk.Entry(
            self,
            width=5,
            textvariable=self.fields.remove_crop_this,
        )
        self.crop_this_entry.grid(column=2, row=3, columnspan=2, sticky="ew")

        # Remove digits, checkbutton
        self.digits_check = ttk.Checkbutton(
            self,
            text="Digits",
            variable=self.fields.remove_digits,
        )
        self.digits_check.grid(column=0, row=4)

        # Remove chars, checkbutton
        self.chars_check = ttk.Checkbutton(
            self,
            text="Chars.",
            variable=self.fields.remove_chars,
        )
        self.chars_check.grid(column=1, row=4)

        # Remove sym, checkbutton
        self.sym_check = ttk.Checkbutton(
            self,
            text="Sym.",
            variable=self.fields.remove_sym,
        )
        self.sym_check.grid(column=2, row=4)

        # Remove D/S, checkbutton
        self.d_s_check = ttk.Checkbutton(
            self,
            text="D/S",
            variable=self.fields.remove_d_s,
        )
        self.d_s_check.grid(column=0, row=5)

        # Remove accents, checkbutton
        self.accents_check = ttk.Checkbutton(
            self,
            text="Accents",
            variable=self.fields.remove_accents,
        )
        self.accents_check.grid(column=1, row=5)

        # Remove Leading Dots, combobox
        ttk.Label(self, text="Lead Dots").grid(column=0, row=6, sticky="w")
        self.lead_dots_combo = ttk.Combobox(
            self,
            width=5,
            state="readonly",
            values=self.fields.remove_lead_dots.options,
            textvariable=self.fields.remove_lead_dots,
        )
        self.lead_dots_combo.grid(column=1, row=6, sticky="ew")

        self.bindings()

    def bindings(self):
        """What to execute when the bindings happen."""
        super().bindings()
        # When updating from_n value makes sure its not bigger than remove_to_n
        self.fields.remove_from_n.trace_add("write", self.limit_to_n)
        self.fields.remove_to_n.trace_add("write", self.limit_to_n)

    def limit_to_n(self, var=None, index=None, mode=None):
        """Limits remove_to_n (b) with from_n (a)"""
        spin_box_lower_limit_update(
            self.fields.remove_from_n, self.fields.remove_to_n
        )
