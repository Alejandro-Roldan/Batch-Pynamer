def de_ext(name):
    """
    Removes the extension from the selected path.
    Returns the name of the field and the extension separate.
    If theres no extension returns an empty extension.
    """
    file_name, dot, ext = name.rpartition(".")
    if file_name != "":
        ext = dot + ext
        name = file_name
    else:
        ext = ""

    return name, ext
