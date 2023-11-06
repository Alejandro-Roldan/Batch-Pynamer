import batchpynamer.gui as bpn_gui
from batchpynamer.gui.notebook import notebook


class BasePlugin:
    short_description = None
    description = None
    finished_msg = None

    def __init__(self, allow_no_selection=False):
        self.allow_no_selection = allow_no_selection

    def _run(self):
        pre_hook_return = pre_hook()

        self.selected_items = selection()

        if not self.allow_no_selection and not self.selected_items:
            raise Exception()

        for item in selected_items:
            run_return = run(item, pre_hook_return=pre_hook_return)

        # refresh gui if bpn_gui.root
        # if notebook tab==
        # notebook.populate_fields()

        post_hook_return = post_hook(
            run_return=run_return, pre_hook_return=pre_hook_return
        )

    def selection(self):
        # if bpn_gui.root:
        pass

    def pre_hook(self):
        # info_bar.show_working()

        pass

    def post_hook(self, run_return=None, pre_hook_return=None):
        # info_bar.finish_show_working(inf_msg=self.finished_msg)
        pass

    def run(self, item, pre_hook_return=None):
        raise NotImplementedError


def extract_plugins():
    pass
