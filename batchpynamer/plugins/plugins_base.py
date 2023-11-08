import ast
import imp
import logging

from scandirrecursive.scandirrecursive import scandir_recursive_sorted

import batchpynamer.gui as bpn_gui
from batchpynamer import plugins as bpn_plugins
from batchpynamer.gui import infobar
from batchpynamer.gui.trees import trees

GUI_PLUGIN_DESC_LIMIT = 50


class NoSelectionError(Exception):
    pass


class BasePlugin:
    """To develop plugins

    Plugins Must heredate from "BasePlugin" class (even if not directly).
    They Must define the "run" method. If not: a "NotImplementedError" will be
    raised.

    They can also define the "selection", "pre_hook" and "post_hook" methods.

    It also has a "short_desc", "finished_msg" and "allow_no_selection"
    attributes.
    "short_desc" will be used for displaying in GUI if available (with limited
    chars)

    A "NoSelectionError" will be raised if no selection unless
    "allow_no_selection=True"
    """

    # Optional attributes
    # When used for GUI display it will be limited to GUI_PLUGIN_DESC_LIMIT
    # number of chars
    short_desc = None
    finished_msg = "Finished plugin execution"
    allow_no_selection = False

    def __init__(self):
        """Init short_desc"""
        if self.short_desc is not None:
            # Convert to str the short desc just in case
            self.short_desc = str(self.short_desc)

    def _run(self):
        """Private method with the full execution logic"""
        self.pre_hook_return = self.pre_hook()

        # Get selection
        self.selection_return = self.selection()
        if not self.allow_no_selection and not self.selection_return:
            # And handle empty selection
            raise NoSelectionError(
                "This plugin needs selected items to execute"
            )
        elif self.allow_no_selection and not self.selection_return:
            # Run just once without item
            self.run_return = self.run()
        else:
            self.run_return = []
            # Or execute the plugin to each item when selection
            for item in self.selection_return:
                if item_return := self.run(item=item):
                    self.run_return.append(item_return)

        self.post_hook_return = self._post_hook()

    def pre_hook(self):
        """What to do before starting"""
        if bpn_gui.root:
            infobar.show_working()

    def selection(self):
        """Gets selection"""
        if bpn_gui.root:
            return bpn_gui.fn_treeview.selection_get()

    def run(self, item=None):
        """The core of the plugin

        Needs to be defined
        """
        raise NotImplementedError

    def _post_hook(self):
        """Private post hook to add debug info"""
        logging.debug(f'Applied "{type(self).__name__}" plugin')
        return self.post_hook()

    def post_hook(self):
        """What to do after finishing"""
        logging.info(self.finished_msg)
        if bpn_gui.root:
            trees.refresh_treeviews()

            infobar.finish_show_working(inf_msg=self.finished_msg)


class PluginsDictStruct:
    """Structure that holds the nested plugins"""

    nested_dict = {}

    class PluginImport:
        """Plugin import class

        For each plugin file: holds its import, the classes in it, the module
        name and the module path
        """

        def __init__(self, module_name, module_path, module_classes):
            self.module_name = module_name
            self.module_path = module_path
            self.import_ = self.import_module()

            # Load each class
            self.module_classes = {}
            for class_ in module_classes:
                instance_ = self.imported_class(class_)()
                # Only add the plugins that heredate from BasePlugin
                if isinstance(instance_, BasePlugin):
                    # GUI display name use short_desc if available (limited
                    # chars and remove trailing and leading spaces) else: use
                    # the class name
                    name = (
                        instance_.short_desc[:GUI_PLUGIN_DESC_LIMIT].strip()
                        if instance_.short_desc
                        else class_
                    )
                    self.module_classes[name] = instance_

        def import_module(self):
            """Import the module"""
            return imp.load_source(self.module_name, self.module_path)

        def imported_class(self, class_):
            """Get the imported class"""
            return getattr(self.import_, class_)

        def __repr__(self):
            """Display for debugging"""
            return str(self.module_classes)

    def set(self, key: str, values, full_path):
        """Sets the nested dicts dinamically"""

        nested_dict = self.nested_dict
        # Split path into directory names
        keys = key.split("/")
        # Loop through the directories (no file)
        for k in keys[:-1]:
            nested_dict = nested_dict.setdefault(k, {})
        # Set the file key (last key) to the corresponding PluginImport
        # instance
        nested_dict[keys[-1].replace(".py", "")] = self.PluginImport(
            keys[-1], full_path, values
        )

    def __repr__(self):
        """Display for debugging"""
        return str(self.nested_dict)


def _extract_plugins():
    """Recursively extract plugins from appropiate dirs"""

    plugins_dict = PluginsDictStruct()
    for path in bpn_plugins.plugin_dirs:
        try:
            scanned = scandir_recursive_sorted(
                path=path,
                # Only Files
                folders=False,
                # Prevent files that start with "_..."
                mask="[^_].+",
                # Only ".py"
                ext_tuple=("py",),
                hidden=False,
                depth=-1,
                files_before_dirs=True,
            )
        except FileNotFoundError:
            pass
        else:
            for entry in scanned:
                entry_replaced = entry.path.replace(path, "")

                with open(entry, "r") as f:
                    node = ast.parse(f.read())

                plugins_dict.set(
                    entry_replaced,
                    [
                        n.name
                        for n in node.body
                        if isinstance(n, ast.ClassDef)
                        # Prevent classes that start with "_..."
                        if not n.name.startswith("_")
                    ],
                    entry.path,
                )

    logging.debug(f"Loaded plugin structure:\n{plugins_dict}")
    return plugins_dict
