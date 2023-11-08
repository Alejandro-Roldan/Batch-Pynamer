"""Batch-Pynamer"""


__license__ = "GPL3"
__version__ = "8.0.3"
__release__ = True
__author__ = __maintainer__ = "Alejandro Roldán"
__email__ = "alej.roldan.trabajos@gmail.com"
__url__ = "https://github.com/Alejandro-Roldan/Batch-Pynamer"

import logging

TITLE = f"{__name__}-V{__version__}"

# URLS
PROJECT_URL = __url__
WIKI_URL = "https://github.com/Alejandro-Roldan/Batch-Pynamer/wiki"


# Metadata availabe flag
try:
    import mutagen
    import PIL

    # If succesful set flag
    METADATA_IMPORT = True
except ImportError:
    metadata_import_error_msg = (
        "No metadata modules available. This "
        "program is able to edit metadata tags if you install the mutagen "
        "and Pillow libraries"
    )
    logging.warning(metadata_import_error_msg)
    METADATA_IMPORT = False


def __init__():
    pass
