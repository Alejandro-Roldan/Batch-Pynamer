from setuptools import setup

import batchpynamer


def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name=batchpynamer.__name__,
    version=batchpynamer.__version__,
    description=(
        "A purely python batch file renamer (and metadata editor) specially ma"
        "de to work on linux"
    ),
    long_description=readme(),
    long_description_content_type="text/markdown",
    url=__url__,
    author=batchpynamer.__author__,
    author_email=batchpynamer.__email__,
    license=batchpynamer.__license__,
    packages=["batchpynamer"],
    entry_points={
        "console_scripts": [
            "batchpynamer = batchpynamer.batchpynamer:_gui_run"
        ]
    },
    package_data={},
    zip_safe=False,
    python_requires=">=3.8",
)
