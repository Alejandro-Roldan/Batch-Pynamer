import tkinter as tk
from tkinter import ttk

import batchpynamer
from . import basewidgets, menubar
from .rename import rename


class SaveCommandNameWindow(basewidgets.PopUpWindow):
    """
    Opens a window to save a command.
    It has:
        - A Name entry
        - A Previous command dropdown. Lists all the already saved commads
    """

    def __init__(self, master):
        super().__init__(master, title="Choose Name for Command")

        # Variable defs
        self.command_name = tk.StringVar()
        self.prev_step = tk.StringVar()

        # Extended Replace, entry
        txt = "Choose a Name for The New Command"
        ttk.Label(self, text=txt).grid(
            column=0, row=0, columnspan=2, sticky="w"
        )
        self.name_entry = ttk.Entry(self, textvariable=self.command_name)
        self.name_entry.grid(column=0, row=1, columnspan=2, sticky="ew")
        self.name_entry.focus()

        # Previous Step, combobox
        steps_list = batchpynamer.COMMAND_CONF.sections()
        steps_list.insert(0, "")
        txt = "Select Previous Step"
        ttk.Label(self, text=txt).grid(column=0, row=2, sticky="w")
        self.steps_combo = ttk.Combobox(
            self,
            width=10,
            state="readonly",
            values=steps_list,
            textvariable=self.prev_step,
        )
        self.steps_combo.grid(column=1, row=2, sticky="ew")
        self.steps_combo.current(0)

        # Cancel, button
        self.cancel_button = ttk.Button(
            self, text="Cancel", command=self.destroy
        )
        self.cancel_button.grid(column=0, row=3)

        # Save and exit Window, Button
        self.save_button = ttk.Button(self, text="Save", command=self.saveExit)
        self.save_button.grid(column=1, row=3)

        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=2)

        self.bindEntries()

    def bindEntries(self, *args, **kwargs):
        """Defines the binded actions"""
        self.steps_combo.bind("<<ComboboxSelected>>", self.defocus)

    def defocus(self, *args, **kwargs):
        """
        Clears the highlightning of the comboboxes inside this frame
        whenever any of them changes value.
        """
        self.steps_combo.selection_clear()

    def saveExit(self, *args, **kwargs):
        """
        Saves the command to the configuration file and exits the window
        """
        command_name = self.command_name.get()
        prev_step = self.prev_step.get()

        # Check the command name is valid (alphanumeric)
        if not command_name.isalnum():
            basewidgets.ErrorFrame("Invalid Name")
        # Check its not already in use
        elif command_name in batchpynamer.COMMAND_CONF:
            basewidgets.ErrorFrame("Name Already in Use")
        # Save command and edit the previous step
        else:
            save_to_command_file(command_name, prev_step)
            self.destroy()


def save_to_command_file(command_name, prev_step=""):
    """Saves the current entries variables configuration as a command"""
    # Get the current variable config
    # command_dict = create_var_val_dict()
    command_dict = rename.all_fields_get()

    # Added to the configparser object
    batchpynamer.COMMAND_CONF[command_name] = command_dict
    # If a previous step was selected modify the previous step adding the
    # next_step
    if prev_step:
        batchpynamer.COMMAND_CONF[prev_step]["next_step"] = command_name

    # Save changes
    with open(batchpynamer.COMMAND_CONF_FILE, "w") as conf_file:
        batchpynamer.COMMAND_CONF.write(conf_file)

    # Update command menu list and show info msg
    batchpynamer.menu_bar.updateCommandListMenu()
    inf_msg = 'Saved Field States as Command "{}"'.format(command_name)
    batchpynamer.info_bar.lastActionRefresh(inf_msg)


def delete_command(*args, **kwargs):
    """Deletes selected command from the command configuration file"""
    # Get selected command
    command_name = batchpynamer.menu_bar.selectedCommandGet()
    # Pop it
    batchpynamer.COMMAND_CONF.pop(command_name)

    # Save changes
    with open(batchpynamer.COMMAND_CONF_FILE, "w") as conf_file:
        batchpynamer.COMMAND_CONF.write(conf_file)

    # Update the command list in the menu and show info msg
    batchpynamer.menu_bar.updateCommandListMenu()
    inf_msg = 'Deleted "{}" Command'.format(command_name)
    batchpynamer.info_bar.lastActionRefresh(inf_msg)


def load_command_call(*args, **kwargs):
    """Loads the selected command to the entries fields"""
    command_name = batchpynamer.menu_bar.selectedCommandGet()

    # If the selected command isn't the default loads the dictionary from the
    # configuration file
    if command_name != "DEFAULT":
        var_val_dict = dict(batchpynamer.COMMAND_CONF.items(command_name))

        # Call to set the dictionary
        set_command_call(var_val_dict)

        # Show info msg
        inf_msg = 'Loaded "{}" Fields Configuration'.format(command_name)
        batchpynamer.info_bar.lastActionRefresh(inf_msg)

    # Else show an error info msg
    else:
        batchpynamer.info_bar.lastActionRefresh("No selected Command")


def set_command_call(fields_dict):
    """Call each widget to set the entries values from the given dict"""
    batchpynamer.rename_from_file.setCommand(fields_dict)
    batchpynamer.rename_from_reg_exp.setCommand(fields_dict)
    batchpynamer.name_basic.setCommand(fields_dict)
    batchpynamer.replace.setCommand(fields_dict)
    batchpynamer.case.setCommand(fields_dict)
    batchpynamer.remove.setCommand(fields_dict)
    batchpynamer.move_parts.setCommand(fields_dict)
    batchpynamer.add_to_str.setCommand(fields_dict)
    batchpynamer.add_folder_name.setCommand(fields_dict)
    batchpynamer.numbering.setCommand(fields_dict)
    batchpynamer.ext_replace.setCommand(fields_dict)
