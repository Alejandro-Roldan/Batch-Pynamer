"""Code related to data management"""

RENAME_ORDER = [
    "from_file",
    "reg_exp",
    "name_basic",
    "replace",
    "case",
    "remove",
    "move",
    "add_to_str",
    "add_folder_name",
    "numbering",
    "ext_replace",
]

ALL_RENAME_FIELDS = {
    "rename_from_file_file": "",
    "rename_from_file_wrap": False,
    "reg_exp_match_reg": "",
    "reg_exp_replace_with": "",
    "name_basic_name_opt": "Keep",
    "name_basic_fixed_name": "",
    "replace_replace_this": "",
    "replace_replace_with": "",
    "replace_match_case": False,
    "case_case_want": "Same",
    "remove_first_n": 0,
    "remove_last_n": 0,
    "remove_from_n": 0,
    "remove_to_n": 0,
    "remove_rm_words": "",
    "remove_rm_chars": "",
    "remove_crop_pos": "Before",
    "remove_crop_this": "",
    "remove_digits": False,
    "remove_d_s": True,
    "remove_accents": False,
    "remove_chars": False,
    "remove_sym": False,
    "remove_lead_dots": "None",
    "move_parts_ori_pos": "None",
    "move_parts_ori_n": 0,
    "move_parts_end_pos": "Start",
    "move_parts_end_n": 0,
    "move_parts_sep": "",
    "add_to_str_prefix": "",
    "add_to_str_insert_this": "",
    "add_to_str_at_pos": 0,
    "add_to_str_suffix": "",
    "add_to_str_word_space": False,
    "add_folder_name_name_pos": "Prefix",
    "add_folder_name_pos": 0,
    "add_folder_name_sep": "",
    "add_folder_name_levels": 0,
    "numbering_mode": "None",
    "numbering_at_n": 0,
    "numbering_start_num": 0,
    "numbering_incr_num": 1,
    "numbering_pad": 1,
    "numbering_sep": "",
    "numbering_type_base": "Base 10",
    "ext_replace_change_ext": "Same",
    "ext_replace_fixed_ext": "",
}

IMG_EXTS = (".jpg", ".jpeg", ".png")
AUDIO_EXTS = (".mp3", ".flac", ".ape")
