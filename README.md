# Batch-Pynamer
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A purely python batch file renamer specially made to work on linux.

It can also change and use metadata for flac, mp3 and mp4 files. If you don't have the metadata dependencies needed you can still use the rest of the program, which uses exclusively base python libraries.

It can probably run on Windows and Mac mostly without issue, but it hasn't been tested.


### The Wiki has how every option, menu and key works!
Check the wiki

Program Screenshots
-------------------
![screenshot](/doc/BatchPynamer-Rename_Screen.png?raw=true "Program Screenshot for the Rename Tab")
![screenshot](/doc/BatchPynamer-Metadata_Screen.png?raw=true "Program Screenshot for the Metadata Tab")


Dependencies
------------
* Python (`>=3.8`)

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

clone the repository
cd into it and run
```
pip install . --break-system-packages
```


Batch-Pynamer-Plugins
---------------------
Check this project sibling project with for some plugins [Batch-Pynamer-Plugins](https://github.com/Alejandro-Roldan/Batch-Pynamer-Plugins.git)
