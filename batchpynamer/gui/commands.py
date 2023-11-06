from tkinter import ttk

import batchpynamer as bpn
import batchpynamer.gui as bpn_gui
from batchpynamer.gui.basewidgets import (
    BaseFieldsWidget,
    BpnComboVar,
    BpnStrVar,
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
        steps_list = bpn.COMMAND_CONF.sections()
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
            bw.ErrorFrame(f'Invalid Name: "{command_name}"')
        # Check its not already in use
        elif command_name in bpn.COMMAND_CONF:
            bw.ErrorFrame("Name Already in Use")
        # Save command and edit the previous step
        else:
            command_gui_save_command_action(command_name, prev_step)
            self.destroy()


def command_gui_save_command_action(command_name, prev_step=""):
    """Saves the current entries variables configuration as a command"""
    # Get the current variable config
    command_dict = rename.all_fields_get()

    # Added to the configparser object
    bpn.COMMAND_CONF[command_name] = command_dict
    # If a previous step was selected modify the previous step adding the
    # next_step
    if prev_step:
        bpn.COMMAND_CONF[prev_step]["next_step"] = command_name

    # Save changes
    with open(bpn.COMMAND_CONF_FILE, "w") as conf_file:
        bpn.COMMAND_CONF.write(conf_file)

    # Update command menu list and show info msg
    bpn_gui.menu_bar.update_command_list_menu()
    inf_msg = 'Saved Field States as Command "{}"'.format(command_name)
    bpn_gui.info_bar.last_action_set(inf_msg)


def command_gui_load_command_call(event=None):
    """Loads the selected command to the entries fields"""
    command_name = bpn_gui.menu_bar.selected_command.get()

    # If the selected command isn't the default loads the dictionary from the
    # configuration file
    if command_name != "DEFAULT":
        var_val_dict = dict(bpn.COMMAND_CONF.items(command_name))

        # Call to set the dictionary
        set_command_action(var_val_dict)

        # Show info msg
        inf_msg = 'Loaded "{}" Fields Configuration'.format(command_name)
        bpn_gui.info_bar.last_action_set(inf_msg)

    # Else show an error info msg
    else:
        bpn_gui.info_bar.last_action_set("No selected Command")


def command_gui_apply_action(event=None, command_name=None):
    """
    Directly applies a command or a chain of commands.
    """
    # Clear the last_rename list
    bpn_gui.last_rename.clear()
    # Save what the variable fields are right now
    var_val_dict_in_use = rename.all_fields_get()

    # Gets the selected command if a command_name wasn't provided
    if command_name is None:
        command_name = bpn_gui.menu_bar.selected_command.get()

    # Apply only if the selected command isn't the default (no changes)
    if command_name != "DEFAULT":
        # Show that it's in the process
        info_bar.show_working()

        # Get the variables values dict from the config command file under
        # the selected command name
        var_val_dict = dict(bpn_gui.COMMAND_CONF.items(command_name))

        # Set that variable values dict in the fields
        set_command_action(var_val_dict)
        # Call for a basic Rename
        rename.final_rename()

        # Get the next_step value from the command config, if there is one
        # call Apply_Command (this same function) but with command_name =
        # next_step
        next_step = var_val_dict["next_step"]
        if next_step:
            # Select the items that were previously selected based on the
            # last_rename list to get what are the new names
            bpn_gui.fn_treeview.selection_set(
                bpn_gui.last_rename.new_name_list_get()
            )
            # Call Apply_Command with next_step
            apply_command(event=None, command_name=next_step)

        # Show that it finished
        inf_msg = 'Applied "{}" Command'.format(command_name)
        info_bar.finish_show_working(inf_msg=inf_msg)

    # If the selected command was the default show msg
    else:
        bpn_gui.info_bar.last_action_set("No Command Selected")

    # Set the variable fields back to what you had prior to the command
    set_command_action(var_val_dict_in_use)


def command_gui_delete_command():
    """Deletes selected command from the command configuration file"""
    # Get selected command
    command_name = bpn_gui.menu_bar.selected_command.get()
    # Pop it
    bpn.COMMAND_CONF.pop(command_name)

    # Save changes
    with open(bpn.COMMAND_CONF_FILE, "w") as conf_file:
        bpn.COMMAND_CONF.write(conf_file)

    # Update the command list in the menu and show info msg
    bpn_gui.menu_bar.update_command_list_menu()
    inf_msg = 'Deleted "{}" Command'.format(command_name)
    bpn_gui.info_bar.last_action_set(inf_msg)


def set_command_action(fields_dict):
    """Call each widget to set the entries values from the given dict"""
    bpn_gui.rename_from_file.setCommand(fields_dict)
    bpn_gui.rename_from_reg_exp.setCommand(fields_dict)
    bpn_gui.name_basic.setCommand(fields_dict)
    bpn_gui.replace.setCommand(fields_dict)
    bpn_gui.case.setCommand(fields_dict)
    bpn_gui.remove.setCommand(fields_dict)
    bpn_gui.move_parts.setCommand(fields_dict)
    bpn_gui.add_to_str.setCommand(fields_dict)
    bpn_gui.add_folder_name.setCommand(fields_dict)
    bpn_gui.numbering.setCommand(fields_dict)
    bpn_gui.ext_replace.setCommand(fields_dict)
