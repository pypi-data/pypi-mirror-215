# SPDX-FileCopyrightText: 2023-present woidzero <woidzeroo@gmail.com>
#
# SPDX-License-Identifier: MIT

import mcfc

class Logger:
    def success(*objects):
        mcfc.echo("&a✔&r", *objects)

    def info(*objects):
        mcfc.echo("&bℹ&r", *objects)

    def error(*objects):
        mcfc.echo("&c✖&r", *objects)

    def warn(*objects):
        mcfc.echo("&e⚠&r", *objects)
