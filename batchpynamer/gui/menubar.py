import tkinter as tk
import webbrowser  # for the About menu

import batchpynamer as bpn
import batchpynamer.gui as bpn_gui
from batchpynamer.gui import commands
from batchpynamer.gui.notebook.metadata import metadata
from batchpynamer.gui.notebook.rename import rename
from batchpynamer.gui.trees import trees


class TopMenu(tk.Menu):
    def __init__(self):
        self.rename_order_bottom_to_top = tk.BooleanVar(value=False)

    def tk_init(self, master):
        super().__init__(master, bg="gray75", foreground="black")

        # Create the menus and add them to the main bar
        self.file_menu_init()
        self.add_cascade(label="File", menu=self.file_menu)

        self.selection_menu_init()
        self.add_cascade(label="Selection", menu=self.selection_menu)

        # Only create the command menu if there is a configuration folder
        self.command_menu_init()
        self.add_cascade(label="Commands", menu=self.command_menu)
        if not bpn.CONFIG_FOLDER_PATH:
            self.entryconfigure(index=3, state="disable")

        self.about_menu_init()
        self.add_cascade(label="About", menu=self.about_menu)

        # self.changes_notebook.menu_bar = self

        self.menu_opts_metadata_disable()

    def file_menu_init(self):
        """File Menu Dropdown"""

        # Create the menu
        self.file_menu = tk.Menu(
            self, tearoff=0, bg="gray75", foreground="black"
        )

        # Rename
        self.file_menu.add_command(
            label="Rename",
            command=rename.rename_gui_apply_rename_call,
            accelerator="Ctrl+R",
        )

        # Undo Rename
        self.file_menu.add_command(
            label="Undo Rename",
            command=rename.rename_gui_undo_rename_call,
            accelerator="Ctrl+Z",
        )

        # Reset Entry Fields
        self.file_menu.add_command(
            label="Reset Entry Fields",
            command=rename.rename_gui_all_fields_reset,
            accelerator="Ctrl+T",
        )

        # Rename from Bottom to Top
        self.file_menu.add_checkbutton(
            label="Activate renaming from Bottom to Top",
            variable=self.rename_order_bottom_to_top,
        )

        # Separator
        self.file_menu.add_separator()

        # Create the metadata menu options only if the metadata modification
        # is active (the dependencies have been exported)
        if bpn.METADATA_IMPORT:
            # Apply Metadata Changes
            self.file_menu.add_command(
                label="Apply Metadata Changes",
                command=metadata.meta_gui_audio_changes_call,
            )

            # Apply Image Metadata
            self.file_menu.add_command(
                label="Apply Image Metadata Change",
                command=metadata.meta_gui_img_changes_call,
            )

            # Apply Both Image & Metadata Changes
            self.file_menu.add_command(
                label="Apply Both Image & Metadata Changes",
                command=metadata.meta_gui_all_changes_call,
            )

            # Separator
            self.file_menu.add_separator()

        # Refresh Files
        self.file_menu.add_command(
            label="Refresh File View",
            command=bpn_gui.dir_entry_frame.active_path_set,
            accelerator="F5",
        )

        # Refresh Focused Node in Tree
        self.file_menu.add_command(
            label="Refresh Focused Node",
            command=trees.refresh_folderview_focus_node,
            accelerator="Ctrl+F5",
        )

        # Refresh Whole Tree
        self.file_menu.add_command(
            label="Refresh Full Directory Browser",
            command=trees.refresh_folderview_full_tree,
            accelerator="Ctrl+Shift+F5",
        )

        # Separator
        self.file_menu.add_separator()

        # Exit
        self.file_menu.add_command(
            label="Exit",
            command=bpn_gui.root.quit,
            accelerator="Ctrl+Esc",
        )

    def menu_opts_rename_enable(self):
        """Enable the rename menu options when on the rename page"""
        self.file_menu.entryconfigure(index=0, state="active")
        self.file_menu.entryconfigure(index=1, state="active")
        self.file_menu.entryconfigure(index=2, state="active")

    def menu_opts_rename_disable(self):
        """Disable the rename menu options when not in the rename page"""
        self.file_menu.entryconfigure(index=0, state="disable")
        self.file_menu.entryconfigure(index=1, state="disable")
        self.file_menu.entryconfigure(index=2, state="disable")

    def menu_opts_metadata_enable(self):
        """Enable the metadata menu options when on the metadata page"""
        if bpn.METADATA_IMPORT:
            self.file_menu.entryconfigure(index=5, state="active")
            self.file_menu.entryconfigure(index=6, state="active")
            self.file_menu.entryconfigure(index=7, state="active")

    def menu_opts_metadata_disable(self):
        """Disable the metadata menu options when not in the metadata page"""
        if bpn.METADATA_IMPORT:
            self.file_menu.entryconfigure(index=5, state="disable")
            self.file_menu.entryconfigure(index=6, state="disable")
            self.file_menu.entryconfigure(index=7, state="disable")

    def selection_menu_init(self):
        """Selection Menu Dropdown"""
        # Create the menu
        self.selection_menu = tk.Menu(
            self, tearoff=0, bg="gray75", foreground="black"
        )

        # Select All
        self.selection_menu.add_command(
            label="Select All",
            command=bpn_gui.fn_treeview.select_all,
            accelerator="Ctrl+A",
        )

        # Deselect All
        self.selection_menu.add_command(
            label="Deselect All",
            command=bpn_gui.fn_treeview.deselect_all,
            accelerator="Ctrl+D",
        )

        # Invert Selection
        self.selection_menu.add_command(
            label="Invert Selection",
            command=bpn_gui.fn_treeview.invert_selection,
            accelerator="Ctrl+I",
        )

    def command_menu_init(self):
        """Command Menu Dropdown"""
        # Variable defs
        self.selected_command = tk.StringVar(value="DEFAULT")

        # Create the menu
        self.command_menu = tk.Menu(
            self, tearoff=0, bg="gray75", foreground="black"
        )

        # Save current variable values entries as command
        self.command_menu.add_command(
            label="Save Field States to Command",
            command=commands.SaveCommandWindow,
        )

        # Load selected command
        self.command_menu.add_command(
            label="Load Field States from Command",
            command=commands.command_gui_load_command_call,
            accelerator="Ctrl+E",
        )

        # Apply selected command
        self.command_menu.add_command(
            label="Apply Selected Command",
            command=commands.command_gui_apply_action,
            accelerator="Ctrl+Y",
        )

        # Delete selected command
        self.command_menu.add_command(
            label="Delete Selected Command",
            command=commands.command_gui_delete_command,
        )

        self.command_select_menu = tk.Menu(
            self.command_menu, tearoff=0, bg="gray75", foreground="black"
        )

        # Only try to load the commands if there is a path to the
        # commands configuration file
        if bpn.CONFIG_FOLDER_PATH:
            self.update_command_list_menu()

        # Separator
        self.command_menu.add_separator()

        # Apply selected command
        self.command_menu.add_cascade(
            label="Select Command", menu=self.command_select_menu
        )

    def update_command_list_menu(self):
        """Deletes the already existing items and updates the view"""
        self.command_select_menu.delete(0, "end")
        # Read the commands config and create a radio button for each command
        for command_name in bpn.COMMAND_CONF.sections():
            self.command_select_menu.add_radiobutton(
                label=command_name,
                variable=self.selected_command,
                value=command_name,
            )

    def about_menu_init(self, *args, **kwargs):
        """About Menu Dropdown"""
        # Create the menu
        self.about_menu = tk.Menu(
            self, tearoff=0, bg="gray75", foreground="black"
        )

        # GitHub
        self.about_menu.add_command(
            label="Project", command=self.open_project_url
        )

        # Wiki
        self.about_menu.add_command(label="Help", command=self.open_wiki_url)

    def open_project_url(self):
        """Open the Project Url"""
        webbrowser.open(bpn.PROJECT_URL)

    def open_wiki_url(self):
        """Open the Wiki Url"""
        webbrowser.open(bpn.WIKI_URL)
