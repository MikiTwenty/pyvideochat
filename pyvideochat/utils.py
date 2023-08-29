# utils.py
# Copyright (C) 2023 Michele Ventimiglia (michele.ventimiglia01@gmail.com)
#
# This module is part of pyvideochat and is released under
# the MIT License: https://opensource.org/license/mit/

import os
from sys import platform

class _STDOFormat:
    TEXT = '\33[37m'
    SUCCESS = '\33[92m'
    WARNING = '\33[93m'
    LOADING = '\33[94m'
    INFO = '\33[0m'
    ERROR = '\33[91m'

class _Logger:
    def classic(message) -> None:
        print(f"{message}")

    def text(message) -> None:
        print(f"\n{_STDOFormat.TEXT}>> {message}{_STDOFormat.TEXT}")

    def input(message) -> str:
        return input(f"\n{_STDOFormat.TEXT}[INPUT] | {message} >> {_STDOFormat.TEXT}")

    def warning(message) -> None:
        print(f"\n{_STDOFormat.WARNING}[WARNING] | {message}{_STDOFormat.TEXT}")

    def success(message) -> None:
        print(f"{_STDOFormat.SUCCESS}[SUCCESS] | {message}{_STDOFormat.TEXT}")

    def error(message) -> None:
        print(f"{_STDOFormat.ERROR}[ERROR] | {message}{_STDOFormat.TEXT}")

    def loading(message) -> None:
        print(f"\n{_STDOFormat.LOADING}[LOADING] | {message}{_STDOFormat.TEXT}")

    def info(message) -> None:
        print(f"{_STDOFormat.INFO}[INFO] {message}{_STDOFormat.TEXT}")

def clear_output() -> None:
    """
    Clear terminal output
    """
    try:
        if platform == "linux" or platform == "linux2":
            os.system("clear")
        elif platform == "darwin" or platform == "win32":
            os.system("cls")
    except Exception as error:
        raise(error)