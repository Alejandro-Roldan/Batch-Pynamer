import re  # regular expressions
import string
import tkinter as tk
import unicodedata
from tkinter import ttk

import batchpynamer as bpn
from batchpynamer.basewidgets import (
    BaseNamingWidget,
    BpnBoolVar,
    BpnComboVar,
    BpnIntVar,
    BpnStrVar,
)


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
        pass

    def tk_init(self, master):
        super().__init__(
            master,
            column=3,
            row=0,
            rowspan=2,
            text="Remove (5)",
        )
        super().tk_init(reset_column_row=(4, 7))

        # Variable defs
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

        # Remove first n characters, spinbox
        ttk.Label(self, text="First n").grid(column=0, row=0, sticky="ew")
        self.first_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.remove_first_n,
        )
        self.first_n_spin.grid(column=1, row=0)

        # Remove las n characters, spinbox
        ttk.Label(self, text="Last n").grid(column=2, row=0, sticky="ew")
        self.last_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.remove_last_n,
        )
        self.last_n_spin.grid(column=3, row=0)

        # Remove from this char position, spinbox
        ttk.Label(self, text="From").grid(column=0, row=1, sticky="ew")
        self.from_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.remove_from_n,
        )
        self.from_n_spin.grid(column=1, row=1)

        # Remove to this char position, spinbox
        ttk.Label(self, text="To").grid(column=2, row=1, sticky="ew")
        self.to_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn.MAX_NAME_LEN,
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
        self.fields.remove_from_n.trace_add("write", self.fromAddTo)
        self.fields.remove_to_n.trace_add("write", self.fromAddTo)

    def fromAddTo(self, *args, **kwargs):
        """
        Checks if the from_n value is bigger than the remove_to_n value,
        If so raises the remove_to_n value accordingly.
        """
        a = self.fields.remove_from_n.get()
        b = self.fields.remove_to_n.get()

        if a > b:
            self.fields.remove_to_n.set(a)


def remove_rename(name, fields_dict):
    """Main remove function. It's been broken down into simpler parts"""

    def remove_n_chars(name):
        """Removes chars depending on their index"""
        remove_first_n = fields_dict.get("remove_first_n")
        # Need this to be a negative number
        remove_last_n = -fields_dict.get("remove_last_n")
        # Need this to be one less of the displayed number
        remove_from_n = fields_dict.get("remove_from_n") - 1
        remove_to_n = fields_dict.get("remove_to_n")

        name = name[remove_first_n:]
        # Only act when the index is not 0
        if remove_last_n != 0:
            name = name[:remove_last_n]
        # Only act when the index is not -1
        if remove_from_n != -1:
            # Doing it with str slices is faster than transforming it to a list
            name = name[:remove_from_n] + name[remove_to_n:]

        return name

    def remove_words_chars(name):
        """
        Firstly removes the apparition of a word (must be between spaces).
        Secondly removes every apparition of any of the chars that were
        input in the entry.
        """
        remove_rm_words = fields_dict.get("remove_rm_words")
        remove_rm_chars = fields_dict.get("remove_rm_chars")

        # Only try this if theres somethin in remove_rm_words, otherwise it would
        # have to transform the string into lists and loop through the whole
        # name of each selected item everytime
        if remove_rm_words:
            # Create list of words to remove, splitted spaces
            remove_rm_words = remove_rm_words.split()
            # Create a list out of the name string, splitted spaces
            name_list = name.split()

            # Use list comprehension to loop trough the name (as a list) and
            # create an output list with the words that are Not inside the
            # remove_rm_words list, then join the list into a str with
            # spaces inbetween
            name = " ".join(
                [word for word in name_list if word not in remove_rm_words]
            )

        # Removes every apparition of all chars in the str by themselves
        for chara in remove_rm_chars:
            name = name.replace(chara, "")

        return name

    def crop_remove(name):
        """
        Crops before or after the specified char(s).
        It can also crop inbetween 2 char(s), ex:
        a*b (for cropping between the first ocurrence of a and b)
        \[*\] (for cropping between [ and ])
        """
        remove_crop_pos = fields_dict.get("remove_crop_pos")
        remove_crop_this = fields_dict.get("remove_crop_this")

        # If this field is empty do nothing
        if remove_crop_this:
            # If the combobox is not in 'Special' do the regular crops
            if remove_crop_pos != "Special":
                name_tuple = name.partition(remove_crop_this)
                if remove_crop_pos == "Before" and name_tuple[2]:
                    name = name_tuple[2]
                elif remove_crop_pos == "After" and name_tuple[0]:
                    name = name_tuple[0]
            else:
                # Create a regular expresion from the given string
                reg_exp = remove_crop_this.replace("*", ".+?", 1)
                reg_exp = re.compile(reg_exp)
                name = re.sub(reg_exp, "", name)

        return name

    def remove_checkbuttons(name):
        """Checks what checkbuttons are active and removes accordingly"""
        remove_digits = fields_dict.get("remove_digits")
        remove_d_s = fields_dict.get("remove_d_s")
        remove_accents = fields_dict.get("remove_accents")
        remove_chars = fields_dict.get("remove_chars")
        remove_sym = fields_dict.get("remove_sym")

        if remove_digits:
            for char in string.digits:
                name = name.replace(char, "")
        # Remove double spaces for single space
        if remove_d_s:
            name = name.replace("  ", " ")
        # Replace accents for their no accented counterpart
        if remove_accents:
            # Not sure how this thing works (from stackoverflow)
            nfkd_form = unicodedata.normalize("NFKD", name)
            name = "".join(
                [c for c in nfkd_form if not unicodedata.combining(c)]
            )
        if remove_chars:
            for char in string.ascii_letters:
                name = name.replace(char, "")
        if remove_sym:
            for char in string.punctuation:
                name = name.replace(char, "")

        return name

    def lead_dots(name):
        """Removes either '.' or '..' right at the begining"""
        remove_lead_dots = fields_dict.get("remove_lead_dots")
        if remove_lead_dots != "None":
            name = name.replace(remove_lead_dots, "", 1)

        return name

    name = remove_n_chars(name)
    name = remove_words_chars(name)
    name = crop_remove(name)
    name = remove_checkbuttons(name)
    name = lead_dots(name)

    return name
