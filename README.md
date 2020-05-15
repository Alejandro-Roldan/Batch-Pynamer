# Batch-Pynamer
A purely python batch file renamer specially made to work on linux.

It can also change audio files metadata for flac and mp3 files. If you don't have the metadata dependencies needed you can still use the rest of the program, which uses exclusively base python libraries.

Probably the only changes needed to make it run on windows is change the PATH constant to a windows like path.


Program Screenshots
-------------------
![screenshot](/doc/BatchPynamer-Rename_Screen.png?raw=true "Program Screenshot for the Rename Tab")
![screenshot](/doc/BatchPynamer-Metadata_Screen.png?raw=true "Program Screenshot for the Metadata Tab")


Dependencies
------------
* Python (`>=3.7`)

### Optional Dependencies

For the metadata:

* mutagen 
* Pillow

You can install them using pip
```
pip install *packagename*
```


Installing
----------

Download the BatchPynamer.py file and execute it.
As long as you have the dependencies it should work out of the box.

