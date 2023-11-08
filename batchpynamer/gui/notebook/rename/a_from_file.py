from tkinter import ttk

from batchpynamer.gui.basewidgets import (
    BaseNamingWidget,
    BpnBoolVar,
    BpnStrVar,
)


class RenameFromFile(BaseNamingWidget, ttk.LabelFrame):  # (0)
    """
    Draws the Rename from file widget. Inside the rename notebook.
    This takes priority over anything else
    It has:
        - An entry to enter the path to the text file to rename from
        - A checkbutton to select if you want to wrap around once the end
        of the file is reached
    """

    def __init__(self):
        self.fields = self.Fields(
            rename_from_file_file=BpnStrVar(""),
            rename_from_file_wrap=BpnBoolVar(False),
        )

    def tk_init(self, master):
        super().__init__(
            master,
            column=0,
            row=0,
            text="Rename From File (0)",
        )
        super().tk_init()

        # Filename, entry
        ttk.Label(self, text="Filename").grid(column=0, row=0, sticky="w")
        self.file_entry = ttk.Entry(
            self,
            width=10,
            textvariable=self.fields.rename_from_file_file,
        )
        self.file_entry.grid(column=1, row=0, sticky="ew")

        # Wrap, checkbutton
        self.wrap_check = ttk.Checkbutton(
            self,
            text="Wrap",
            variable=self.fields.rename_from_file_wrap,
        )
        self.wrap_check.grid(column=0, row=1)

        self.bindings()
