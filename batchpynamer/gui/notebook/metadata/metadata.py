from tkinter import ttk

import batchpynamer.gui as bpn_gui
from batchpynamer.data import metadata_data_tools
from batchpynamer.gui import infobar
from batchpynamer.gui.basewidgets import BaseWidget
from batchpynamer.gui.notebook import notebook


class MetadataApplyChanges(BaseWidget, ttk.Frame):
    """
    Apply chnages widget. Inside the metadata notebook.
    It has:
        - Button to apply the metadata changes
        - Button to apply the image changes
        - Button to apply both
    """

    def __init__(self):
        pass

    def tk_init(self, master):
        super().__init__(master, column=2, row=0, sticky="se")

        self.apply_meta_button = ttk.Button(
            self,
            width=10,
            text="Apply Meta",
            command=meta_gui_audio_changes_call,
        )
        self.apply_meta_button.grid(column=0, row=0, sticky="e")

        self.apply_img_button = ttk.Button(
            self,
            width=10,
            text="Apply Img",
            command=meta_gui_img_changes_call,
        )
        self.apply_img_button.grid(column=0, row=1, sticky="e")

        self.apply_all_button = ttk.Button(
            self,
            width=10,
            text="Apply All",
            command=meta_gui_all_changes_call,
        )
        self.apply_all_button.grid(column=0, row=2, sticky="e")


def meta_gui_audio_changes_call():
    """Call for metadata audio changes"""
    _meta_gui_changes_action(
        meta_change=True, img_change=False, inf_msg="Metadata Changed"
    )


def meta_gui_img_changes_call():
    """Call for metadata image changes"""
    _meta_gui_changes_action(
        meta_change=False, img_change=True, inf_msg="Image Changed"
    )


def meta_gui_all_changes_call():
    """Call for metadata audio and image changes"""
    _meta_gui_changes_action(
        meta_change=True,
        img_change=True,
        inf_msg="Metadata and Image Changed",
    )


def _meta_gui_changes_action(
    meta_change=False,
    img_change=False,
    inf_msg: str = "No msg defined",
):
    """Action for the GUI to apply metadata changes"""
    # Show that its in the process
    infobar.show_working()
    selection = bpn_gui.fn_treeview.selection_get()

    if meta_change:
        meta_dict = bpn_gui.metadata_list_entries.fields.get_all()
    if img_change:
        img_path = bpn_gui.metadata_img.fields.image_path.get()
        img, apic = metadata_data_tools.meta_img_create(img_path)

    for item in selection:
        if meta_change:
            meta_audio = metadata_data_tools.meta_audio_get(item)
            metadata_data_tools.meta_audio_save(meta_audio, meta_dict)

        if img_change:
            metadata_data_tools.meta_img_save(item, img, apic)

    # Reload after the changes
    notebook.populate_fields()
    # Show that its finish
    infobar.finish_show_working(inf_msg=inf_msg)
