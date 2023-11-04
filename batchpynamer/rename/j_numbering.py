import string
import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn

from ..basewidgets import BaseNamingWidget, BpnComboVar, BpnIntVar, BpnStrVar


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
        pass

    def tk_init(self, master):
        super().__init__(
            master,
            column=5,
            row=0,
            rowspan=2,
            text="Numbering (9)",
        )
        super().tk_init(reset_column_row=(4, 5))

        # Variable defs
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

        self.bindEntries()


def numbering_rename(name, idx, fields_dict):
    """Calls to create the numbering and then sets it up inplace"""

    def numbering_create(n, base, padding):
        """
        Creates the final numbering to add as a str

        Changes the number to the the chosen base, removes the part of the
        string that specifies that its a number in such a base and then
        adds the padding 0s.
        For the letter cases transforms the number to what letter it would
        correspond and adds the padding As
        """
        padding_char = "0"
        # Number cases
        if base == "Base 10":
            n = str(n)
        elif base == "Base 2":
            n = bin(n)
            n = n[2:]
        elif base == "Base 8":
            n = oct(n)
            n = n[2:]
        elif base == "Base 16":
            n = hex(n)
            n = n[2:]

        # Letter cases
        else:
            # Uses a cycle variable to know how many times it has to loop
            # ex: 1 -> A, 27 -> AA, 53 -> BA
            cycle = n // 26
            letter_n = ""
            for a in range(0, cycle + 1):
                letter_n = letter_n + string.ascii_lowercase[n - 26 * cycle]

            padding_char = "a"
            n = letter_n

            if base == "Upper Case Letters":
                padding_char = "A"
                n = n.upper()

        # Add right padding
        n = n.rjust(padding, padding_char)

        return n

    numbering_mode = fields_dict.get("numbering_mode")
    numbering_at_n = fields_dict.get("numbering_at_n")
    numbering_start_num = fields_dict.get("numbering_start_num")
    numbering_incr_num = fields_dict.get("numbering_incr_num")
    numbering_sep = fields_dict.get("numbering_sep")
    numbering_type_base = fields_dict.get("numbering_type_base")
    numbering_pad = fields_dict.get("numbering_pad")

    # Calculate what number we are in taking into account the step and
    # the starting number
    n = idx + numbering_start_num + (numbering_incr_num - 1) * idx
    # Change the number to string in whatever base
    n = numbering_create(n, numbering_type_base, numbering_pad)

    if numbering_mode == "Prefix":
        name = n + numbering_sep + name
    elif numbering_mode == "Suffix":
        name = name + numbering_sep + n
    elif numbering_mode == "Both":
        name = n + numbering_sep + name + numbering_sep + n
    elif numbering_mode == "Position":
        # If blocks to determine where to write the separators and how to
        # act depending on where we have to write it to make it seem
        # seamless
        if numbering_at_n == 0:
            name = n + numbering_sep + name
        elif numbering_at_n == -1 or numbering_at_n >= len(name):
            name = name + numbering_sep + n
        elif numbering_at_n > 0:
            name = (
                name[:numbering_at_n]
                + numbering_sep
                + n
                + numbering_sep
                + name[numbering_at_n:]
            )
        elif numbering_at_n < -1:
            numbering_at_n += 1
            name = (
                name[:numbering_at_n]
                + numbering_sep
                + n
                + numbering_sep
                + name[numbering_at_n:]
            )

    return name
