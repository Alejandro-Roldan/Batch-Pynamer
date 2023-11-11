import logging
from tkinter import ttk

import batchpynamer.config as bpn_config
import batchpynamer.gui as bpn_gui
from batchpynamer.data.rename_data_tools import rename_create_new_name_action
from batchpynamer.gui import infobar
from batchpynamer.gui.basewidgets import (
    BaseFieldsWidget,
    BpnComboVar,
    BpnStrVar,
    ErrorFrame,
    PopUpWindow,
)
from batchpynamer.gui.notebook.rename import rename


class SaveCommandWindow(PopUpWindow, BaseFieldsWidget):
    """
    Opens a window to save a command.
    It has:
        - A Name entry
        - A Previous command dropdown. Lists all the already saved commads
    """

    def __init__(self):
        super().__init__(title="Choose Name for Command")

        # Get the command list
        steps_list = bpn_config.command_conf.sections()
        # Insert an empty one at the top
        steps_list.insert(0, "")
        # Variable defs
        self.fields = self.Fields(
            command_name=BpnStrVar(""),
            prev_step=BpnComboVar(steps_list),
        )

        # Extended Replace, entry
        txt = "Choose a Name for The New Command"
        ttk.Label(self, text=txt).grid(
            column=0, row=0, columnspan=2, sticky="w"
        )
        self.name_entry = ttk.Entry(
            self, textvariable=self.fields.command_name
        )
        self.name_entry.grid(column=0, row=1, columnspan=2, sticky="ew")
        self.name_entry.focus()

        # Previous Step, combobox
        txt = "Select Previous Step"
        ttk.Label(self, text=txt).grid(column=0, row=2, sticky="w")
        self.steps_combo = ttk.Combobox(
            self,
            width=10,
            state="readonly",
            values=self.fields.prev_step.options,
            textvariable=self.fields.prev_step,
        )
        self.steps_combo.grid(column=1, row=2, sticky="ew")

        # Cancel, button
        self.cancel_button = ttk.Button(
            self, text="Cancel", command=self.destroy
        )
        self.cancel_button.grid(column=0, row=3)

        # Save and exit Window, Button
        self.save_button = ttk.Button(
            self, text="Save", command=self.save_and_exit
        )
        self.save_button.grid(column=1, row=3)

        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=2)

        self.bindings()

    def save_and_exit(self):
        """
        Saves the command to the configuration file and exits the window
        """
        command_name = self.fields.command_name.get()
        prev_step = self.fields.prev_step.get()

        # Check the command name is valid (alphanumeric)
        if not command_name.isalnum():
            inf_msg = f'Invalid Name: "{command_name}"'
            ErrorFrame(inf_msg)
            logging.error("GUI- command- " + inf_msg)
        # Check its not already in use
        elif command_name in bpn_config.command_conf:
            inf_msg = "Name Already in Use"
            ErrorFrame(inf_msg)
            logging.error("GUI- command- " + inf_msg)
        # Save command and edit the previous step
        else:
            command_gui_save_command_action(command_name, prev_step)
            self.destroy()


def command_gui_save_command_action(command_name, prev_step=""):
    """Saves the current entries variables configuration as a command"""
    # Get the current variable config
    command_dict = rename.all_fields_get()

    # Added to the configparser object
    bpn_config.command_conf[command_name] = command_dict
    # If a previous step was selected modify the previous step adding the
    # next_step
    if prev_step:
        bpn_config.command_conf[prev_step]["next_step"] = command_name

    # Save changes
    with open(bpn_config.command_conf_file, "w") as conf_file:
        bpn_config.command_conf.write(conf_file)

    # Update command menu list and show info msg
    bpn_gui.menu_bar.update_command_list_menu()
    inf_msg = f'Saved Field States as Command "{command_name}"'
    bpn_gui.info_bar.last_action_set(inf_msg)
    logging.info("GUI- command- " + inf_msg)


def command_gui_load_command_call(event=None):
    """Loads the selected command to the entries fields"""
    command_name = bpn_gui.menu_bar.selected_command.get()

    # If the selected command isn't the default loads the dictionary from the
    # configuration file
    if command_name != "DEFAULT":
        fields_dict = bpn_config.command_conf.command_conf_fields_get(
            command_name
        )

        # Call to set the dictionary
        set_command_action(fields_dict)

        # Show info msg
        inf_msg = f'Loaded "{command_name}" Fields Configuration'
        bpn_gui.info_bar.last_action_set(inf_msg)
        logging.info("GUI- command- " + inf_msg)

    # Else show an error info msg
    else:
        inf_msg = "No selected Command"
        bpn_gui.info_bar.last_action_set(inf_msg)
        logging.info("GUI- command- " + inf_msg)


def command_gui_apply_command_call(event=None):
    # Gets the selected command
    command_name = bpn_gui.menu_bar.selected_command.get()

    # Apply only if the selected command isn't the default (no changes)
    if command_name != "DEFAULT":
        rename.rename_gui_apply_rename_action(command_rename=command_name)

        # Show that it finished
        inf_msg = 'Applied "{}" Command'.format(command_name)
        infobar.finish_show_working(inf_msg=inf_msg)
        logging.info("GUI- command- " + inf_msg)

    # If the selected command was the default show msg
    else:
        inf_msg = "No Command Selected"
        bpn_gui.info_bar.last_action_set(inf_msg)
        logging.info("GUI- command- " + inf_msg)


def command_gui_generate_name_action(
    command_name=None, old_name="", old_path="", idx=0
):
    """
    Directly applies a command or a chain of commands.
    """

    # Gets the selected command if a command_name wasn't provided
    if command_name is None or command_name == "DEFAULT":
        return ""

    # Get the variables values dict from the config command file under
    # the selected command name
    fields_dict = bpn_config.command_conf.command_conf_fields_get(command_name)

    new_name = rename_create_new_name_action(
        old_name, idx, old_path, fields_dict
    )

    # Get the next_step value from the command config, if there is one
    # call func recursevely with command_name=next_step
    next_step = fields_dict["next_step"]
    if next_step:
        # Select the items that were previously selected based on the
        # last_rename list to get what are the new names
        bpn_gui.fn_treeview.selection_set(
            bpn_gui.last_rename.new_name_list_get()
        )
        # Call command_gui_apply_action with next_step
        new_name = command_gui_generate_name_action(
            command_name=next_step,
            old_name=new_name,
            old_path=old_path,
            idx=idx,
        )

    return new_name


def command_gui_delete_command_action():
    """Deletes selected command from the command configuration file"""
    # Get selected command
    command_name = bpn_gui.menu_bar.selected_command.get()
    # Pop it
    bpn_config.command_conf.pop(command_name)

    # Save changes
    with open(bpn_config.command_conf_file, "w") as conf_file:
        bpn_config.command_conf.write(conf_file)

    # Update the command list in the menu and show info msg
    bpn_gui.menu_bar.update_command_list_menu()
    inf_msg = 'Deleted "{}" Command'.format(command_name)
    bpn_gui.info_bar.last_action_set(inf_msg)
    logging.info("GUI- command- " + inf_msg)


def set_command_action(fields_dict):
    """Call each widget to set the entries values from the given dict"""
    bpn_gui.rename_from_file.set_fields_from_command(fields_dict)
    bpn_gui.rename_from_reg_exp.set_fields_from_command(fields_dict)
    bpn_gui.name_basic.set_fields_from_command(fields_dict)
    bpn_gui.replace.set_fields_from_command(fields_dict)
    bpn_gui.case.set_fields_from_command(fields_dict)
    bpn_gui.remove.set_fields_from_command(fields_dict)
    bpn_gui.move_parts.set_fields_from_command(fields_dict)
    bpn_gui.add_to_str.set_fields_from_command(fields_dict)
    bpn_gui.add_folder_name.set_fields_from_command(fields_dict)
    bpn_gui.numbering.set_fields_from_command(fields_dict)
    bpn_gui.ext_replace.set_fields_from_command(fields_dict)
