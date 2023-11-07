import logging
import os
import re  # regular expressions
import string
import unicodedata

import batchpynamer as bpn
from batchpynamer.data.metadata_data_tools import meta_audio_get


def rename_apply_new_name_action(name, idx, path, fields_dict):
    rename_create_new_name_action(name, idx, path, **fields_dict)


def rename_system_rename(old_path, new_path):
    # Only rename if the old name is different from the new name
    if old_path == new_path:
        logging.info(f'"{old_path}" New name is the same as old name')
        return None

    if not os.path.exists(new_path):
        try:
            os.rename(old_path, new_path)
        # Catch exceptions for invalid filenames
        except OSError:
            error_msg = f"Couldn't rename file {old_path}.\nInvalid characters"

        except FileNotFoundError:
            error_msg = f"Couldn't rename file {old_path}.\nFile not found"
        else:
            logging.info(f"{old_path} -> {new_path}")
            return None

    # If path already exists don't write over it and skip it
    else:
        error_msg = (
            f'Couldn\'t rename file "{old_path}" to "{new_path}".\nPath already ex'
            "ists"
        )

    logging.error(error_msg)
    return error_msg


def rename_create_new_name_action(name, idx, path, **fields_dict):
    """
    Creates the new name going through all fields and making the changes
    to the old_name string
    """
    # Separate name and extension
    ext = ""
    if os.path.isfile(path):
        name, ext = rename_ext_split_action(name)

    name = rename_from_file_action(name, idx, fields_dict)
    name = rename_reg_exp_action(name, fields_dict)
    name = rename_name_basic_action(name, fields_dict)
    name = rename_replace_action(name, fields_dict)
    name = rename_case_change_action(name, fields_dict)
    name = rename_remove_action(name, fields_dict)
    name = rename_move_copy_text_action(name, fields_dict)
    name = rename_add_action(name, fields_dict)
    name = rename_add_folder_rename_action(name, path, fields_dict)
    name = rename_numbering_action(name, idx, fields_dict)

    ext = rename_ext_action(ext, fields_dict)
    # Re-add extension
    name = name + ext

    # Format any metadata fields that have been added to the name
    # (only if the metadata modules were imported)
    if bpn.METADATA_IMPORT:
        name = rename_metadata_format_action(name, path)

    # Remove leading and trailing whitespaces
    return name.strip()


def rename_ext_split_action(name):
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


def rename_from_file_action(name, idx, fields_dict):
    """
    Get the file to extract the names from, open it and match the names
    one to one per index base
    """
    rename_from_file_file = fields_dict.get("rename_from_file_file")
    rename_from_file_wrap = fields_dict.get("rename_from_file_wrap")

    if os.path.exists(rename_from_file_file):
        try:
            with open(rename_from_file_file, "r") as f:
                lines = f.readlines()
                lines_count = len(lines)
                try:
                    if rename_from_file_wrap:
                        name = lines[idx % lines_count]
                    else:
                        name = lines[idx]
                except IndexError:
                    pass
        except IsADirectoryError:
            pass

    return name


def rename_reg_exp_action(name, fields_dict):
    """
    Matches the regular expression specified in the match_reg entry
    and recreates the name with the words and number groups specified
    in replace_with entry
    e.g:
        name: Program Files
        match_reg: ^([A-Z][a-z]*) ([A-Z][a-z]*)     # separates 2 words
        replace_with: The /2 which are used to run the /1

        returns: The Files which are used to run the Program
    """
    reg_exp_match_reg = fields_dict.get("reg_exp_match_reg")
    reg_exp_replace_with = fields_dict.get("reg_exp_replace_with")

    reg_exp_match_reg = re.compile(reg_exp_match_reg)
    reg_grouping = reg_exp_match_reg.match(name)
    if reg_exp_match_reg != "" and reg_exp_replace_with != "":
        for i in range(0, len(reg_grouping.groups()) + 1):
            n = str(i)

            # Prevent IndexError blocking
            try:
                reg_exp_replace_with = reg_exp_replace_with.replace(
                    "/" + n, reg_grouping.group(i)
                )
            except IndexError:
                pass

        name = reg_exp_replace_with

    return name


def rename_name_basic_action(name, fields_dict):
    """Self explanatory"""
    name_basic_name_opt = fields_dict.get("name_basic_name_opt")

    if name_basic_name_opt == "Remove":
        name = ""
    elif name_basic_name_opt == "Reverse":
        name = name[::-1]
    elif name_basic_name_opt == "Fixed":
        name = fields_dict.get("name_basic_fixed_name")

    return name


def rename_replace_action(name, fields_dict):
    """Does the replace action for the new name"""
    replace_replace_this = fields_dict.get("replace_replace_this")
    replace_replace_with = fields_dict.get("replace_replace_with")
    replace_match_case = fields_dict.get("replace_match_case")

    # When replacing with match case it's a simple matter
    if replace_match_case:
        name = name.replace(replace_replace_this, replace_replace_with)
    # But when replacing without minding the case...
    # (If replace_replace_this is empty it breaks)
    elif replace_replace_this != "":
        # Start searching from the start of the string
        idx = 0
        # Find at what position what we want to replace is (all lowercase)
        # If find returns a -1 it means it didn't find it and we can break
        while (
            idx := name.lower().find(replace_replace_this.lower(), idx) != -1
        ):
            # Create the new name
            name = (
                name[:idx]
                + replace_replace_with
                + name[idx + len(replace_replace_this) :]
            )

            # New index from where to search
            idx = idx + len(replace_replace_with)

    return name


def rename_case_change_action(name, fields_dict):
    """Does the case change for the new name"""
    case_case_want = fields_dict.get("case_case_want")

    if case_case_want == "Upper Case":
        name = name.upper()

    elif case_case_want == "Lower Case":
        name = name.lower()

    elif case_case_want == "Title":
        name = name.title()

    elif case_case_want == "Sentence":
        name = name.capitalize()

    return name


def rename_remove_action(name, fields_dict):
    """Main remove function. It's been broken down into simpler parts"""

    def _remove_n_chars(name):
        """Removes chars depending on their index"""
        remove_first_n = fields_dict.get("remove_first_n")
        # Need this to be a negative number
        remove_last_n = -fields_dict.get("remove_last_n")
        # Need this to be one less of the displayed number
        remove_from_n = fields_dict.get("remove_from_n") - 1
        remove_to_n = fields_dict.get("remove_to_n")

        name = name[remove_first_n:]
        # Only act when the index is not 0
        if remove_last_n != 0:
            name = name[:remove_last_n]
        # Only act when the index is not -1
        if remove_from_n != -1:
            # Doing it with str slices is faster than transforming it to a list
            name = name[:remove_from_n] + name[remove_to_n:]

        return name

    def _remove_words_chars(name):
        """
        Firstly removes the apparition of a word (must be between spaces).
        Secondly removes every apparition of any of the chars that were
        input in the entry.
        """
        remove_rm_words = fields_dict.get("remove_rm_words")
        remove_rm_chars = fields_dict.get("remove_rm_chars")

        # Only try this if theres somethin in remove_rm_words, otherwise it would
        # have to transform the string into lists and loop through the whole
        # name of each selected item everytime
        if remove_rm_words:
            # Create list of words to remove, splitted spaces
            remove_rm_words = remove_rm_words.split()
            # Create a list out of the name string, splitted spaces
            name_list = name.split()

            # Use list comprehension to loop trough the name (as a list) and
            # create an output list with the words that are Not inside the
            # remove_rm_words list, then join the list into a str with
            # spaces inbetween
            name = " ".join(
                [word for word in name_list if word not in remove_rm_words]
            )

        # Removes every apparition of all chars in the str by themselves
        for chara in remove_rm_chars:
            name = name.replace(chara, "")

        return name

    def _crop_remove(name):
        """
        Crops before or after the specified char(s).
        It can also crop inbetween 2 char(s), ex:
        a*b (for cropping between the first ocurrence of a and b)
        \[*\] (for cropping between [ and ])
        """
        remove_crop_pos = fields_dict.get("remove_crop_pos")
        remove_crop_this = fields_dict.get("remove_crop_this")

        # If this field is empty do nothing
        if remove_crop_this:
            # If the combobox is not in 'Special' do the regular crops
            if remove_crop_pos != "Special":
                name_tuple = name.partition(remove_crop_this)
                if remove_crop_pos == "Before" and name_tuple[2]:
                    name = name_tuple[2]
                elif remove_crop_pos == "After" and name_tuple[0]:
                    name = name_tuple[0]
            else:
                # Create a regular expresion from the given string
                reg_exp = remove_crop_this.replace("*", ".+?", 1)
                reg_exp = re.compile(reg_exp)
                name = re.sub(reg_exp, "", name)

        return name

    def _remove_checkbuttons(name):
        """Checks what checkbuttons are active and removes accordingly"""
        remove_digits = fields_dict.get("remove_digits")
        remove_d_s = fields_dict.get("remove_d_s")
        remove_accents = fields_dict.get("remove_accents")
        remove_chars = fields_dict.get("remove_chars")
        remove_sym = fields_dict.get("remove_sym")

        if remove_digits:
            for char in string.digits:
                name = name.replace(char, "")
        # Remove double spaces for single space
        if remove_d_s:
            name = name.replace("  ", " ")
        # Replace accents for their no accented counterpart
        if remove_accents:
            # Not sure how this thing works (from stackoverflow)
            nfkd_form = unicodedata.normalize("NFKD", name)
            name = "".join(
                [c for c in nfkd_form if not unicodedata.combining(c)]
            )
        if remove_chars:
            for char in string.ascii_letters:
                name = name.replace(char, "")
        if remove_sym:
            for char in string.punctuation:
                name = name.replace(char, "")

        return name

    def _lead_dots(name):
        """Removes either '.' or '..' right at the begining"""
        remove_lead_dots = fields_dict.get("remove_lead_dots")
        if remove_lead_dots != "None":
            name = name.replace(remove_lead_dots, "", 1)

        return name

    name = _remove_n_chars(name)
    name = _remove_words_chars(name)
    name = _crop_remove(name)
    name = _remove_checkbuttons(name)
    name = _lead_dots(name)

    return name


def rename_move_copy_text_action(name, fields_dict):
    """
    Copies and pastes the selected characters to the selected
    position.
    """
    move_parts_ori_pos = fields_dict.get("move_parts_ori_pos")
    move_parts_ori_n = fields_dict.get("move_parts_ori_n")
    move_parts_end_pos = fields_dict.get("move_parts_end_pos")
    move_parts_end_n = fields_dict.get("move_parts_end_n")
    move_parts_sep = fields_dict.get("move_parts_sep")

    if move_parts_ori_pos == "Start":
        if move_parts_end_pos == "End":
            name = (
                name[move_parts_ori_n:]
                + move_parts_sep
                + name[:move_parts_ori_n]
            )

        elif move_parts_end_pos == "Position":
            name = (
                name[move_parts_ori_n:move_parts_end_n]
                + move_parts_sep
                + name[:move_parts_ori_n]
                + move_parts_sep
                + name[move_parts_end_n:]
            )

    elif move_parts_ori_pos == "End":
        if move_parts_end_pos == "Start":
            name = (
                name[-move_parts_ori_n:]
                + move_parts_sep
                + name[:-move_parts_ori_n]
            )

        elif move_parts_end_pos == "Position":
            name = (
                name[:move_parts_end_n]
                + move_parts_sep
                + name[-move_parts_ori_n:]
                + move_parts_sep
                + name[move_parts_end_n:-move_parts_ori_n]
            )

    return name


def rename_add_action(name, fields_dict):
    """
    Adds the char(s) to the specified position.
    Also can add spaces before capital letters.
    """
    add_to_str_prefix = fields_dict.get("add_to_str_prefix")
    add_to_str_insert_this = fields_dict.get("add_to_str_insert_this")
    add_to_str_at_pos = fields_dict.get("add_to_str_at_pos")
    add_to_str_suffix = fields_dict.get("add_to_str_suffix")
    add_to_str_word_space = fields_dict.get("add_to_str_word_space")

    # Add prefix
    name = add_to_str_prefix + name

    # If blocks to determine where to write the sub str
    # To be able to do it seamlessly it needs different ways to act
    # depending on the position
    if add_to_str_at_pos == 0:
        name = add_to_str_insert_this + name
    elif add_to_str_at_pos == -1 or add_to_str_at_pos >= len(name):
        name = name + add_to_str_insert_this
    elif add_to_str_at_pos > 0:
        name = (
            name[:add_to_str_at_pos]
            + add_to_str_insert_this
            + name[add_to_str_at_pos:]
        )
    elif add_to_str_at_pos < -1:
        add_to_str_at_pos += 1
        name = (
            name[:add_to_str_at_pos]
            + add_to_str_insert_this
            + name[add_to_str_at_pos:]
        )

    # Add suffix
    name = name + add_to_str_suffix

    if add_to_str_word_space:  # add a space before each capital letter
        name = "".join([" " + ch if ch.isupper() else ch for ch in name])

    return name


def rename_add_folder_rename_action(name, path, fields_dict):
    add_folder_name_name_pos = fields_dict.get("add_folder_name_name_pos")
    add_folder_name_sep = fields_dict.get("add_folder_name_sep")
    add_folder_name_levels = fields_dict.get("add_folder_name_levels")

    # Active when the level is at least 1
    if add_folder_name_levels > 0:
        # Split the directory into a list with each folder
        folders = path.split("/")
        # Initilize the full folder name
        folder_full = ""
        # Loop for each directory level, start at 2 to skip an empty level
        # and the active level (the item itself)
        for i in range(2, add_folder_name_levels + 2):
            # Error handling for setting a level higher than folders are
            try:
                folder_full = folders[-i] + add_folder_name_sep + folder_full
            except IndexError:
                pass

        if add_folder_name_name_pos == "Prefix":
            name = folder_full + name
        elif add_folder_name_name_pos == "Suffix":
            name = name + add_folder_name_sep + folder_full
            # Remove the extra trailing separator
            if add_folder_name_sep:
                name = name[: -len(add_folder_name_sep)]
        elif add_folder_name_name_pos == "Position":
            add_folder_name_pos = fields_dict.get("add_folder_name_pos")
            # If blocks to determine where to write the sub str
            # To be able to do it seamlessly it needs different ways to act
            # depending on the position
            if add_folder_name_pos == 0:
                name = folder_full + name
            elif add_folder_name_pos == -1 or add_folder_name_pos >= len(name):
                name = name + add_folder_name_sep + folder_full
                # Remove the extra trailing separator
                if add_folder_name_sep:
                    name = name[: -len(add_folder_name_sep)]
            elif add_folder_name_pos > 0:
                name = (
                    name[:add_folder_name_pos]
                    + add_folder_name_sep
                    + folder_full
                    + name[add_folder_name_pos:]
                )
            elif add_folder_name_pos < -1:
                add_folder_name_pos += 1
                name = (
                    name[:add_folder_name_pos]
                    + add_folder_name_sep
                    + folder_full
                    + name[add_folder_name_pos:]
                )

    return name


def rename_numbering_action(name, idx, fields_dict):
    """Calls to create the numbering and then sets it up inplace"""

    def _numbering_create(n, base, padding):
        """
        Creates the final numbering to add as a str

        Changes the number to the the chosen base, removes the part of the
        string that specifies that its a number in such a base and then
        adds the padding 0s.
        For the letter cases transforms the number to what letter it would
        correspond and adds the padding As
        """
        padding_char = "0"
        # Number cases
        if base == "Base 10":
            n = str(n)
        elif base == "Base 2":
            n = bin(n)
            n = n[2:]
        elif base == "Base 8":
            n = oct(n)
            n = n[2:]
        elif base == "Base 16":
            n = hex(n)
            n = n[2:]

        # Letter cases
        else:
            # Uses a cycle variable to know how many times it has to loop
            # ex: 1 -> A, 27 -> AA, 53 -> BA
            cycle = n // 26
            letter_n = ""
            for a in range(0, cycle + 1):
                letter_n = letter_n + string.ascii_lowercase[n - 26 * cycle]

            padding_char = "a"
            n = letter_n

            if base == "Upper Case Letters":
                padding_char = "A"
                n = n.upper()

        # Add right padding
        n = n.rjust(padding, padding_char)

        return n

    numbering_mode = fields_dict.get("numbering_mode")
    numbering_at_n = fields_dict.get("numbering_at_n")
    numbering_start_num = fields_dict.get("numbering_start_num")
    numbering_incr_num = fields_dict.get("numbering_incr_num")
    numbering_sep = fields_dict.get("numbering_sep")
    numbering_type_base = fields_dict.get("numbering_type_base")
    numbering_pad = fields_dict.get("numbering_pad")

    # Calculate what number we are in taking into account the step and
    # the starting number
    n = idx + numbering_start_num + (numbering_incr_num - 1) * idx
    # Change the number to string in whatever base
    n = _numbering_create(n, numbering_type_base, numbering_pad)

    if numbering_mode == "Prefix":
        name = n + numbering_sep + name
    elif numbering_mode == "Suffix":
        name = name + numbering_sep + n
    elif numbering_mode == "Both":
        name = n + numbering_sep + name + numbering_sep + n
    elif numbering_mode == "Position":
        # If blocks to determine where to write the separators and how to
        # act depending on where we have to write it to make it seem
        # seamless
        if numbering_at_n == 0:
            name = n + numbering_sep + name
        elif numbering_at_n == -1 or numbering_at_n >= len(name):
            name = name + numbering_sep + n
        elif numbering_at_n > 0:
            name = (
                name[:numbering_at_n]
                + numbering_sep
                + n
                + numbering_sep
                + name[numbering_at_n:]
            )
        elif numbering_at_n < -1:
            numbering_at_n += 1
            name = (
                name[:numbering_at_n]
                + numbering_sep
                + n
                + numbering_sep
                + name[numbering_at_n:]
            )

    return name


def rename_ext_action(ext, fields_dict):
    ext_replace_change_ext = fields_dict.get("ext_replace_change_ext")
    ext_replace_fixed_ext = fields_dict.get("ext_replace_fixed_ext")

    if ext_replace_change_ext == "Lower":
        ext = ext.lower()
    elif ext_replace_change_ext == "Upper":
        ext = ext.upper()
    elif ext_replace_change_ext == "Title":
        ext = ext.title()
    elif ext_replace_change_ext == "Extra":
        ext = ext + "." + ext_replace_fixed_ext
    elif ext_replace_change_ext == "Fixed":
        ext = "." + ext_replace_fixed_ext
    elif ext_replace_change_ext == "Remove":
        ext = ""

    return ext


def rename_metadata_format_action(name, path):
    """Format the string with the values from the metadata dictionary"""
    # Only load the metadata if the string contains '{' and '}'
    if ("{" and "}") in name:
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
                name = name.replace(field, field.format(**metadata))

    return name
