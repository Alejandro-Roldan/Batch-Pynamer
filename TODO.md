* Rename field vars normalization names to be able to determine what reset it needs

* Move rename classes fields generation out of __init__ and move the globals out of the tk_init_hook to be easier accesible

* Change new_naming_x func name (trees:265)

* add error logging for rename from filename with files not existing and such a_from_file:100

* revise nfkd normalization and accent removal f_remove:482

* move sub remove rename funcs inside remove_rename func

* bug with crop before and selecting the last letter doesnt remove anything

* revise fromAddTo g_move:124 and f_remove:317 (possibly can be move into utils)

* revise tkInts vars set(0) when creating them for default value

* move numbering_create inside numbering_rename func
