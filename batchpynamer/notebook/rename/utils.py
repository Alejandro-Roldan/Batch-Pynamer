import batchpynamer as bpn
from batchpynamer.notebook.metadata.utils import meta_audio_get
from batchpynamer.notebook.rename import (
    a_from_file,
    b_reg_exp,
    c_name_basic,
    d_replace,
    e_case,
    f_remove,
    g_move,
    h_add_to_str,
    i_add_folder_name,
    j_numbering,
    k_ext_replace,
)
from batchpynamer.notebook.utils import de_ext


def new_naming(name, idx, path, **fields_dict):
    """
    Creates the new name going through all fields and making the changes
    to the old_name string
    """
    # Separate name and extension
    name, ext = de_ext(name)

    name = a_from_file.rename_from_file_rename(name, idx, fields_dict)  # (0)
    name = b_reg_exp.reg_exp_rename(name, fields_dict)  # (1)
    name = c_name_basic.name_basic_rename(name, fields_dict)  # (2)
    name = d_replace.replace_action(name, fields_dict)  # (3)
    name = e_case.case_change(name, fields_dict)  # (4)
    name = f_remove.remove_rename(name, fields_dict)  # (5)
    name = g_move.move_copy_action(name, fields_dict)  # (6)
    name = h_add_to_str.add_rename(name, fields_dict)  # (7)
    name = i_add_folder_name.add_folder_rename(name, path, fields_dict)  # (8)
    name = j_numbering.numbering_rename(name, idx, fields_dict)  # (9)

    ext = k_ext_replace.ext_rename(ext, fields_dict)  # (10)

    # Remove leading and trailing whitespaces and re-add the extension
    name = name.strip() + ext

    # Format any metadata fields that have been added to the name
    # (only if the metadata modules were imported)
    if bpn.METADATA_IMPORT:
        name = metadata_rename_format(name, path)

    return name


def metadata_rename_format(str_, path):
    """Format the string with the values from the metadata dictionary"""
    # Only load the metadata if the string contains '{' and '}'
    if ("{" and "}") in str_:
        meta_audio = meta_audio_get(path)

        # If the past function returned something (it was a valid file)
        if meta_audio:
            # Get a dict that's the same as meta_audio but only the first
            # item of each key (because the metadata is a dict of lists)
            metadata = {item: meta_audio[item][0] for item in meta_audio}
            # Get a list of the keys in the dict adding the string between
            # curly braces
            field_list = ["{" + key + "}" for key in metadata.keys()]

            # Individually check and replace for each possible key in the dict
            # (need to do this because if you want to use curly braces in the
            # string it would raise an error and would skip any actual editing)
            for field in field_list:
                # **variable unpacks a dictionary into keyword arguments
                # eg: ['a':1, 'b':2] unpacks into function(a=1, b=2)
                # (also *variable unpack a list/tuple into position arguments)
                str_ = str_.replace(field, field.format(**metadata))

    return str_
