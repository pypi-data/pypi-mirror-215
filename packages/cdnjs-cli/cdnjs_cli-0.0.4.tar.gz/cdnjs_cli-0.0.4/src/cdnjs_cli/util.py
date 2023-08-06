# SPDX-FileCopyrightText: 2023-present woidzero <woidzeroo@gmail.com>
#
# SPDX-License-Identifier: MIT

import requests

from cachecontrol import CacheControl
from cachecontrol.caches import FileCache


def getLib(lib):
    try:
        se = CacheControl(requests.Session(), cache=FileCache(".cache"))
        res = se.get(f"https://api.cdnjs.com/libraries/{lib}?fields=latest")
        return res.json()["latest"]
    except KeyError or lib is None:
        return -1
