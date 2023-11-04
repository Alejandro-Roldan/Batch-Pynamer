from tkinter import BooleanVar as tkBooleanVar
from tkinter import StringVar as tkStringVar
from tkinter import ttk
import tkinter as tk


class PopUpWindow(tk.Toplevel):
    def __init__(self, master, title=""):
        super().__init__(master, bg="gray85")
        self.title(title)
        self.attributes("-type", "dialog")


class ErrorFrame(PopUpWindow):
    """Error frame with an error message and an "Okay" button"""

    def __init__(self, master, title="", error_desc="ERROR"):
        # Create a new window
        super().__init__(master, title=title)

        # Label with error description
        ttk.Label(self, text="Error: {}".format(error_desc)).grid(
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

    def bindEntries(self):
        """Default function for binded actions"""
        raise NotImplementedError


class BaseNamingWidget(BaseWidget):
    class Fields:
        def __init__(self, **fields):
            for field in fields:
                # When accessing the var_name return the tk_var
                self.__dict__[field] = fields[field][0]
                # And have var_name.default for the default values
                self.__dict__[field].default = fields[field][1]

        def get_all(self):
            return {
                field: self.__dict__[field].get() for field in self.__dict__
            }

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

    def resetWidget(self):
        """Resets fields to defined default value"""
        for field in self.fields.__dict__:
            # Extract default value and if its a tuple, its first element
            val = (
                self.fields.__dict__[field].default[0]
                if isinstance(self.fields.__dict__[field].default, tuple)
                else self.fields.__dict__[field].default
            )
            self.fields.__dict__[field].set(val)

    def setCommand(self, var_dict):
        """Sets the proper rename class child fields from the whole dict"""
        for field in self.fields.__dict__:
            self.fields.__dict__[field].set(var_dict[field])

    def appendVarValToDict(dict_={}, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def appendVarValToDict(dict_: dict = {}):
        raise NotImplementedError
