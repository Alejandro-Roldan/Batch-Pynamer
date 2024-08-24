def no_duplicate_list(list_convert):
    """
    Return a list with no duplicated items
    Typical way to do it would be to convert to set, but sets are not
    ordered, meanwhile a dictionary can only have each key once and
    are ordered (since python 3)
    """
    return list(dict.fromkeys(list_convert))


def all_same_checker(list_, func_):
    """Checker function that extracted items (from list_ with func_) are all the same.

    Uses sets not being able to have repeated items. So if at some point the set has
    more than one iten they arent all the same.

    Raises IndexError if list_ is empty.
    And Value Error when multiple extracted items.

    Returns the extracted item after success.
    """

    # No items in list_
    if not list_:
        raise IndexError

    # Load items into set throug func_
    set_ = set()
    for item in list_:
        set_.add(func_(item))

        # Differnt extracted items
        if len(set_) > 1:
            raise ValueError

    # Return single extracted item
    return set_.pop()
