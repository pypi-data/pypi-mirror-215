# SPDX-FileCopyrightText: 2023-present woidzero <woidzeroo@gmail.com>
#
# SPDX-License-Identifier: MIT

import sys


def main():
    from .cli import cdnjs

    sys.exit(cdnjs())
