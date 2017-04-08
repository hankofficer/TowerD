"""
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from enum import IntEnum


class rc(IntEnum):
    Success = 0
    Failed = -1
    Error = -2
    NotImplementedYet = -3


class mouse(IntEnum):
    Left = 1
    Middle = 2
    Right = 3
