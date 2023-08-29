# setup.py
# Copyright (C) 2023 Michele Ventimiglia (michele.ventimiglia01@gmail.com)
#
# This module is part of videochat and is released under
# the MIT License: https://opensource.org/license/mit/

import os
import fnmatch
from typing import Sequence
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), "VERSION")) as version:
    VERSION = version.readline().strip()

with open("requirements.txt") as requirements:
    requirements = requirements.read().splitlines()

with open("README.md") as readme:
    long_description = readme.read()


def build_py_modules(basedir: str, excludes: Sequence = ()) -> Sequence:
    # create list of py_modules from tree
    res = set()
    _prefix = os.path.basename(basedir)
    for root, _, files in os.walk(basedir):
        for f in files:
            _f, _ext = os.path.splitext(f)
            if _ext not in [".py"]:
                continue
            _f = os.path.join(root, _f)
            _f = os.path.relpath(_f, basedir)
            _f = "{}.{}".format(_prefix, _f.replace(os.sep, "."))
            if any(fnmatch.fnmatch(_f, x) for x in excludes):
                continue
            res.add(_f)
    return list(res)


setup(
    name = "pyvideochat",
    version = VERSION,
    description = "pyvideochat is a Python package to do videochat using Python",
    author = "Michele Ventimiglia",
    author_email = "michele.ventimiglia01@gmail.com",
    license = "MIT",
    url="https://github.com/MikiTwenty/pyvideochat",
    packages = find_packages(exclude=["test", "test.*"]),
    include_package_data = True,
    py_modules = build_py_modules("./pyvideochat"),
    package_dir = {"pyvideochat": "pyvideochat"},
    python_requires=">=3.7",
    install_requires = requirements,
    tests_require = requirements,
    zip_safe = False,
    long_description = long_description,
    long_description_content_type = "text/markdown",
    classifiers = [
        # Picked from
        #   http://pypi.python.org/pypi?:action=list_classifiers
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)