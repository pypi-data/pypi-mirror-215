# SPDX-FileCopyrightText: 2023-present woidzero <woidzeroo@gmail.com>
#
# SPDX-License-Identifier: MIT

import click

from .__about__ import __prog_name__, __version__

from .injector import addTag
from .logger import Logger
from .util import getLib


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("file")
@click.argument("lib")
@click.version_option(version=__version__, prog_name=__prog_name__)
def cdnjs(file, lib):
    src = getLib(lib)

    if src == -1:
        return Logger.error(f"No library named `{lib}` found.")

    addTag(src, file)
    Logger.success(f"Added `{lib}` to a `{file}`.")
