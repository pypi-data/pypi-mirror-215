# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2023 Thomas Mahé <contact@tmahe.dev>

import argparse
import getpass
import inspect
import io
import sys
from enum import Enum
from typing import Callable, Optional


def get_callback_arguments(func: Callable, arguments: argparse.Namespace):
    return {p: getattr(arguments, p) for p in inspect.signature(func).parameters.keys()}


class Nargs(Enum):
    ONE_OR_DEFAULT = "?"
    ZERO_OR_MANY = "*"
    ONE_OR_MANY = "+"


class Secret:
    def __init__(self, value: str):
        self.value = value

    def get_secret(self):
        return self.value

    def __str__(self):
        return "****"


def ask(prompt: Optional[str] = None,
        confirmation=False,
        secret=False):
    if confirmation:
        if prompt is None:
            prompt = "Do you want to continue?"
        c = input(f'{prompt} [Y/n] ')
        if not "y" == c[0].lower():
            print("Abort.", file=sys.stderr)
            sys.exit(1)
    else:
        if prompt is None:
            prompt = ""

        if secret:
            print(f'{prompt}: ', end='', flush=True)
            p = Secret(getpass.getpass(stream=io.StringIO()))
            print('')
            return p

        else:
            return input(f'{prompt}: ')
