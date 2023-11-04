import tkinter as tk
from tkinter import BooleanVar as tkBooleanVar
from tkinter import StringVar as tkStringVar
from tkinter import ttk

import batchpynamer as bpn


class PopUpWindow(tk.Toplevel):
    def __init__(self, title=""):
        # Pop Up windows always are children of root
        super().__init__(bpn.root, bg="gray85")
        self.title(title)
        self.attributes("-type", "dialog")


class ErrorFrame(PopUpWindow):
    """Error frame with an error message and an "Okay" button"""

    def __init__(self, error_desc="Non-descript"):
        # Create a new window
        super().__init__(title="ERROR")

        # Label with error description
        ttk.Label(self, text=f"ERROR: {error_desc}").grid(
            column=0, row=0, padx=5, pady=5
        )

        # Okay button destroys the window
        ttk.Button(self, text="Okay", command=self.destroy).grid(
            column=0, row=1, padx=5, pady=5
        )


class BaseWidget:
    def __init__(
        self,
        master,
        column=0,
        row=0,
        columnspan=1,
        rowspan=1,
        sticky="nsew",
        **kwargs,
    ):
        # Create TTK Frame with parent master
        super().__init__(master, **kwargs)
        # And set Frame on grid
        self.grid(
            column=column,
            row=row,
            columnspan=columnspan,
            rowspan=rowspan,
            sticky=sticky,
        )

    def tk_init(self):
        raise NotImplementedError


class BaseFieldsWidget(BaseWidget):
    fields = None

    class Fields:
        def __init__(self, **fields):
            self.__dict__.update(fields)

        def get_all(self):
            return {
                field: self.__dict__[field].get() for field in self.__dict__
            }

        def reset_all(self):
            for field in self.__dict__:
                self.__dict__[field].reset()

    def bindEntries(self):
        """Defines the binded actions"""
        # Call defocus when combo boxes have items selected
        for var in self.__dict__:
            if isinstance(self.__dict__[var], ttk.Combobox):
                self.__dict__[var].bind("<<ComboboxSelected>>", self.defocus)

    def defocus(self, event=None):
        """
        Clears the highlightning of the comboboxes inside the instance
        whenever any of them changes value.
        """
        for var in self.__dict__:
            if isinstance(self.__dict__[var], ttk.Combobox):
                self.__dict__[var].selection_clear()


class BaseNamingWidget(BaseFieldsWidget):
    def tk_init(self, reset_column_row: tuple = (2, 2)):
        """Creates the reset button"""
        self.reset_button = ttk.Button(
            self,
            width=2,
            text="R",
            command=self.resetWidget,
        )
        self.reset_button.grid(
            column=reset_column_row[0],
            row=reset_column_row[1],
            sticky="se",
            padx=2,
            pady=2,
        )

    def bindEntries(self):
        super().bindEntries()

        # Call update new name when each fields are written on
        for field in self.fields.__dict__:
            self.fields.__dict__[field].trace_add(
                "write", bpn.fn_treeview.showNewName
            )

    def resetWidget(self):
        """Resets fields to defined default value"""
        self.fields.reset_all()

    def setCommand(self, var_dict):
        """Sets the proper rename class child fields from the whole dict"""
        for field in self.fields.__dict__:
            self.fields.__dict__[field].set(var_dict[field])

    def appendVarValToDict(dict_={}, *args, **kwargs):
        raise NotImplementedError


class BpnVar:
    def __init__(self, default_val):
        self.default = default_val
        super().__init__(bpn.root, default_val)

    def reset(self):
        self.set(self.default)


class BpnIntVar(BpnVar, tk.IntVar):
    def __init__(self, default_val: int):
        super().__init__(default_val)


class BpnStrVar(BpnVar, tk.StringVar):
    def __init__(self, default_val: str):
        super().__init__(default_val)


class BpnComboVar(BpnStrVar):
    def __init__(self, default_val: tuple):
        self.options = default_val
        super().__init__(default_val[0])


class BpnBoolVar(BpnVar, tk.BooleanVar):
    def __init__(self, default_val: bool):
        super().__init__(default_val)
