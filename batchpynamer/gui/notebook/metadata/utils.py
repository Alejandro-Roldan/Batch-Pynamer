def no_duplicate_list(list_convert):
    """
    Return a list with no duplicated items
    Typical way to do it would be to convert to set, but sets are not
    ordered, meanwhile a dictionary can only have each key once and
    are ordered (since python 3)
    """
    return list(dict.fromkeys(list_convert))
