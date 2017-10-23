#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 13:35:45 2017

@author: rcasero
"""

"""
@file: pysto/tests/test_block_split.py
@package: pysto
@author: Ramón Casero <rcasero@gmail.com>
@copyright: © 2017  Ramón Casero <rcasero@gmail.com>
@license: GPL v3
@version: 1.0.0

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

# auxiliary function to check that split+stack recovers the original array
def aux_split_stack(R, C, nblocks, S=1, pad_width=0, mode='constant', constant_values=0):
    
    if (S==1):
        x = np.array(range(R*C)).reshape(R,C)
    else:
        x = np.array(range(S*R*C)).reshape(S,R,C)
    
    # array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
    #        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    #        [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    #        [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    #        [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]])
    
    # split into blocks
    block_slices, blocks, xout = pymg.block_split(x, nblocks=nblocks, 
                                                  pad_width=pad_width, mode=mode, constant_values=constant_values)

    # check number of blocks
    assert(np.prod(nblocks) == len(blocks))

    # check that array has been padded
    assert((np.pad(x, pad_width=pad_width, mode='constant') == xout).all())

    # stack blocks
    x2, block_slices2 = pymg.block_stack(blocks, block_slices, pad_width=pad_width)
    
    # check that the array is correctly recovered
    assert((x == x2).all())

# check that splitting and stacking with padding works
def test_split_stack():
    
    # 2D, no padding
    aux_split_stack(R=5, C=10, nblocks=(3,4), S=1, 
                    pad_width=0, mode='constant', constant_values=0)
    aux_split_stack(R=5, C=10, nblocks=(2,2), S=1, 
                    pad_width=0, mode='constant', constant_values=0)
    
    # 2D, padding
    aux_split_stack(R=5, C=10, nblocks=(3,4), S=1, 
                    pad_width=(2, 3), mode='constant', constant_values=0)
    aux_split_stack(R=5, C=10, nblocks=(2,2), S=1, 
                    pad_width=(2, 3), mode='constant', constant_values=0)
    
     # 3D, no padding
    aux_split_stack(R=5, C=10, nblocks=(3,4,2), S=5, 
                    pad_width=0, mode='constant', constant_values=0)
    aux_split_stack(R=5, C=10, nblocks=(2,2,3), S=5, 
                    pad_width=0, mode='constant', constant_values=0)
    
    # 3D, padding
    aux_split_stack(R=5, C=10, nblocks=(3,4,2), S=5, 
                    pad_width=(2, 3), mode='constant', constant_values=0)
    aux_split_stack(R=5, C=10, nblocks=(2,2,3), S=5, 
                    pad_width=(2, 3), mode='constant', constant_values=0)
    
 