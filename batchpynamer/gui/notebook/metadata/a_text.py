import tkinter as tk
from tkinter import ttk

import batchpynamer.gui as bpn_gui
from batchpynamer.data import metadata_data_tools
from batchpynamer.gui.basewidgets import (
    BaseFieldsWidget,
    BpnStrVar,
    VerticalScrolledFrame,
)
from batchpynamer.gui.notebook.metadata.utils import no_duplicate_list


class MetadataListEntries(BaseFieldsWidget, ttk.Frame):
    """
    Draws the Metadata List entries. Inside metadata notebook.
    It has:
        - A Vertical Scrollable Frame with the list of metadata entries
        - A New Tag name entry
        - An Add button to add the new tag
    """

    def __init__(self):
        self.metadata_fields_reset()

    def tk_init(self, master):
        super().__init__(master, column=0, row=0, sticky="nsw")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.field_frame = VerticalScrolledFrame(self)
        self.field_frame.grid(
            column=0, row=0, columnspan=3, pady=3, sticky="nsw"
        )

        self.new_tag_name = tk.StringVar()

        ttk.Label(self, text="New Tag Name").grid(
            column=0,
            row=1,
        )
        self.new_tag_name_entry = ttk.Entry(
            self,
            textvariable=self.new_tag_name,
        )
        self.new_tag_name_entry.grid(column=1, row=1, sticky="w" + "e")

        # Add new tag, button
        self.add_field_button = ttk.Button(
            self, width=5, text="Add", command=self.add_new_tag_to_entries
        )
        self.add_field_button.grid(column=2, row=1, sticky="se")

        self.metadata_entries_create()

    def metadata_fields_reset(self):
        try:
            del self.fields
        except AttributeError:
            pass

        self.fields = self.Fields(
            title=BpnStrVar(""),
            tracknumber=BpnStrVar(""),
            artist=BpnStrVar(""),
            album=BpnStrVar(""),
            date=BpnStrVar(""),
            genre=BpnStrVar(""),
        )

    def add_new_tag_to_entries(self):
        """
        Adds a new tag to the metadata tags entries list if the tag
        name is not empty.
        """
        tag_name = self.new_tag_name.get()

        if tag_name:
            self.fields.__dict__[tag_name] = BpnStrVar("")
            # For last position
            n = len(self.fields.__dict__)

            ttk.Label(
                self.field_frame.interior, text=tag_name, width=25, anchor="e"
            ).grid(column=0, row=n)
            ttk.Entry(
                self.field_frame.interior,
                width=55,
                textvariable=self.fields.__dict__[tag_name],
            ).grid(column=1, row=n, sticky="e")

        else:
            msg = "No name for the new tag. Please type a name"
            bpn_gui.info_bar.last_action_set(msg)

    def metadata_gui_show(self):
        """
        Resets the frame and repopulates with all the entries and
        their corresponding labels
        """
        selection = bpn_gui.fn_treeview.selection_get()
        self.metadata_entry_frame_reset()
        self.metadata_get_for_gui(selection)
        self.metadata_entries_create()

    def metadata_get_for_gui(self, selection, *args, **kwargs):
        """
        Create a dictionary that has all the same keys than the metadata
        and the values are all the values together of all selected items.
        Then removes duplicate values
        Ex:
            Item1 = {1:'a', 2:'b'}
            Item2 = {1:'a', 2:'c', 3:'d'}

            Result = {1:['a'], 2:['b', 'c'], 3:'d'}

        Finally it transforms each value key to a tkinter.tk.StringVar()
        with a default value thats the list transformed into a string with
        each item separated by "; ".
        Error handling for when the selected items don't have metadata.
        """

        def meta_values_list_to_str(list_):
            """Transforms a list into a string separating values with ";" """
            return "; ".join(list_)

        self.meta_dict = {
            "title": [],
            "tracknumber": [],
            "artist": [],
            "album": [],
            "date": [],
            "genre": [],
        }
        self.metadata_fields_reset()
        try:
            for file in selection:
                meta_audio = metadata_data_tools.meta_audio_get(file)

                for meta_item in meta_audio:
                    meta_value = meta_audio.get(meta_item)

                    # Adds to each key the value for this selected item
                    self.meta_dict[meta_item] = (
                        self.meta_dict.get(meta_item, list()) + meta_value
                    )

            for key in self.meta_dict:
                # Remove duplicates
                self.meta_dict[key] = no_duplicate_list(self.meta_dict[key])
                # List to string
                str_value = meta_values_list_to_str(self.meta_dict[key])

                # Add new fields to self.fields
                self.fields.__dict__[key] = BpnStrVar(str_value)

        except TypeError:
            pass

    def metadata_entry_frame_reset(self):
        """
        Reset the entry list by deleting all widgets inside
        the entry widget
        """
        for child in self.field_frame.interior.winfo_children():
            child.destroy()

    def metadata_entries_create(self, *args, **kwargs):
        """Create the metadata list entries with their values"""
        for n, key in enumerate(self.fields.__dict__):
            ttk.Label(
                self.field_frame.interior, text=key, width=25, anchor="e"
            ).grid(column=0, row=n)

            ttk.Entry(
                self.field_frame.interior,
                width=55,
                textvariable=self.fields.__dict__[key],
            ).grid(column=1, row=n, sticky="e")
