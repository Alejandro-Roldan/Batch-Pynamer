class BasePlugin:
    def __init__(self, allow_no_selection=False):
        self.allow_no_selection = allow_no_selection

    def _run(self):
        self.selected_items = selection()

        pre_hook_return = pre_hook()

        if not self.allow_no_selection and not self.selected_items:
            raise Exception()

        run_return = run(self.selected_items, pre_hook_return=pre_hook_return)

        post_hook_return = post_hook(
            run_return=run_return, pre_hook_return=pre_hook_return
        )

    def selection(self):
        pass

    def pre_hook(self):
        pass

    def post_hook(self, run_return=None, pre_hook_return=None):
        pass

    def run(self, selected_items, pre_hook_return=None):
        raise NotImplementedError


class PluginVisual(BasePlugin):
    def selection(self):
        """Extracts selection from GUI"""
        # TODO


def extract_plugins():
    pass
