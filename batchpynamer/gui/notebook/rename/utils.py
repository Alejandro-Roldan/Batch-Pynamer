import logging

from batchpynamer.gui.basewidgets import BpnIntVar


def spin_box_lower_limit_update(a: BpnIntVar, b: BpnIntVar):
    """Checks if the a value is bigger than b value

    If so raises b value accordingly.
    """
    a_val = a.get()
    b_val = b.get()

    if a_val > b_val:
        b.set(a_val)
