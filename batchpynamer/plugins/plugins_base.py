import ast
import imp
import logging

from scandirrecursive.scandirrecursive import scandir_recursive_sorted

import batchpynamer.gui as bpn_gui
from batchpynamer import plugins as bpn_plugins
from batchpynamer.gui import infobar
from batchpynamer.gui.trees import trees


class NoSelectionError(Exception):
    pass


class BasePlugin:
    finished_msg = None
    allow_no_selection = False

    def _run(self):
        pre_hook_return = self.pre_hook()

        self.selected_items = self.selection()

        if not self.allow_no_selection and not self.selected_items:
            raise NoSelectionError(
                "This plugin needs selected items to execute"
            )

        for item in self.selected_items:
            run_return = self.run(item, pre_hook_return=pre_hook_return)

        post_hook_return = self._post_hook(
            run_return=run_return, pre_hook_return=pre_hook_return
        )

    def selection(self):
        if bpn_gui.root:
            return bpn_gui.fn_treeview.selection_get()

    def pre_hook(self):
        if bpn_gui.root:
            infobar.show_working()

    def _post_hook(self, run_return=None, pre_hook_return=None):
        logging.debug(f'Applied "{type(self).__name__}" plugin')
        return post_hook(
            self, run_return=run_return, pre_hook_return=pre_hook_return
        )

    def post_hook(self, run_return=None, pre_hook_return=None):
        logging.info(self.finished_msg)
        if bpn_gui.root:
            trees.refresh_treeviews()

            infobar.finish_show_working(inf_msg=self.finished_msg)

    def run(self, item, pre_hook_return=None):
        raise NotImplementedError


class PluginsDictStruct:
    nested_dict = {}

    class PluginImport:
        def __init__(self, module_name, module_path, module_classes):
            self.module_classes = {}
            self.module_name = module_name
            self.module_path = module_path
            self.import_ = self.import_module()
            for class_ in module_classes:
                self.module_classes[class_] = self.run(class_)

        def import_module(self):
            return imp.load_source(self.module_name, self.module_path)

        def run(self, class_):
            return getattr(self.import_, class_)

        def __repr__(self):
            return str(self.module_classes)

    def __repr__(self):
        return str(self.nested_dict)

    def nested_set(dic, keys, value):
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})
        dic[keys[-1]] = value

    def set(self, key: str, values, full_path):
        nested_dict = self.nested_dict
        keys = key.split("/")
        for k in keys[:-1]:
            nested_dict = nested_dict.setdefault(k, {})
        nested_dict[keys[-1].replace(".py", "")] = self.PluginImport(
            keys[-1], full_path, values
        )


def _extract_plugins():
    """Recursively extract plugins from apporpiate dirs"""
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
                        if not n.name.startswith("_")
                    ],
                    entry.path,
                )

    logging.debug(f"Loaded plugin structure:\n{plugins_dict}")
    return plugins_dict
