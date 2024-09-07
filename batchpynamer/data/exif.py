#!/usr/bin/env python3

from exif import Image as ExifImage
from mutagen import MutagenError
from mutagen._file import FileType
from mutagen._util import convert_error, loadfile


class EXIF(FileType):
    _mimes = ["image/jpeg"]

    tags = None

    @convert_error(IOError, MutagenError)
    @loadfile(writable=True)
    def delete(self, filething=None):
        raise NotImplementedError

    @convert_error(IOError, MutagenError)
    @loadfile()
    def load(self, filething):
        fileobj = filething.fileobj

        self.image = ExifImage(fileobj)

        # Extract metadata tags skiping a few specific private tags
        self.tags = {
            exif_name: [str(self.image.get(exif_name))]
            for exif_name in self.image.list_all()
            if exif_name
            not in (
                "jpeg_interchange_format",
                "jpeg_interchange_format_length",
                "exif_version",
            )
            and not exif_name.startswith("_")
        }

    @convert_error(IOError, MutagenError)
    @loadfile(writable=True)
    def save(self, filething=None):
        for exif_name in self.tags:
            value = self.tags[exif_name]
            self.image.set(exif_name, value)

        filething.fileobj.write(self.image.get_file())
