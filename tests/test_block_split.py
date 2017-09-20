#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: pysto/tests/test_block_split.py
@package: pysto
@author: Ramón Casero <rcasero@gmail.com>
@copyright: (C) 2017  Ramón Casero <rcasero@gmail.com>
@license: GPL v3
@version: 0.1.0

This file is part of pysto.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details. The offer of this
program under the terms of the License is subject to the License
being interpreted in accordance with English Law and subject to any
action against the University of Oxford being under the jurisdiction
of the English Courts.

You should have received a copy of the GNU General Public License
along with this program.  If not, see
<http://www.gnu.org/licenses/>.
"""

import numpy as np
import pysto.imgproc as pymg

def test_block_split():
    
    R = 13
    C = 5
    S = 3
    
    # create 3D array
    x = np.array(range(R*C*S)).reshape(R,C,S)
    
    # split into blocks
    b = pymg.block_split(x, (4,2,2))

