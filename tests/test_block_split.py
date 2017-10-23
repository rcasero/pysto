#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: pysto/tests/test_block_split.py
@package: pysto
@author: Ramón Casero <rcasero@gmail.com>
@copyright: © 2017  Ramón Casero <rcasero@gmail.com>
@license: GPL v3
@version: 1.2.0

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

def example_2D_array_blocks():
    
    x = [
            np.array([[ 0,  1,  2,  3],
                      [10, 11, 12, 13],
                      [20, 21, 22, 23]]), 
    
            np.array([[ 4,  5,  6],
                      [14, 15, 16],
                      [24, 25, 26]]), 
    
            np.array([[ 7,  8,  9],
                      [17, 18, 19],
                      [27, 28, 29]]), 
    
            np.array([[30, 31, 32, 33],
                      [40, 41, 42, 43]]), 
    
            np.array([[34, 35, 36],
                      [44, 45, 46]]), 
    
            np.array([[37, 38, 39],
                      [47, 48, 49]])
    
    ]
            
    return x

def example_padded_2D_array_blocks():
    
    x = [np.array([[ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  1,  2,  3,  4,  5],
        [ 0,  0, 10, 11, 12, 13, 14, 15],
        [ 0,  0, 20, 21, 22, 23, 24, 25],
        [ 0,  0, 30, 31, 32, 33, 34, 35],
        [ 0,  0, 40, 41, 42, 43, 44, 45],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0]]),
        np.array([[ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 1,  2,  3,  4,  5,  6,  7,  8],
        [11, 12, 13, 14, 15, 16, 17, 18],
        [21, 22, 23, 24, 25, 26, 27, 28],
        [31, 32, 33, 34, 35, 36, 37, 38],
        [41, 42, 43, 44, 45, 46, 47, 48],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0]]),
        np.array([[ 0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0],
        [ 4,  5,  6,  7,  8,  9,  0],
        [14, 15, 16, 17, 18, 19,  0],
        [24, 25, 26, 27, 28, 29,  0],
        [34, 35, 36, 37, 38, 39,  0],
        [44, 45, 46, 47, 48, 49,  0],
        [ 0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0]]),
        np.array([[ 0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0],
        [ 6,  7,  8,  9,  0,  0,  0],
        [16, 17, 18, 19,  0,  0,  0],
        [26, 27, 28, 29,  0,  0,  0],
        [36, 37, 38, 39,  0,  0,  0],
        [46, 47, 48, 49,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0]])]
                
    return x

def example_3D_array_blocks():
    
    x = [np.array([[[ 0,  1,  2],
         [ 5,  6,  7],
         [10, 11, 12]]]), 
            np.array([[[ 3,  4],
         [ 8,  9],
         [13, 14]]]), 
            np.array([[[15, 16, 17],
         [20, 21, 22]]]), 
            np.array([[[18, 19],
         [23, 24]]]), 
            np.array([[[25, 26, 27],
         [30, 31, 32]]]), 
            np.array([[[28, 29],
         [33, 34]]]), 
            np.array([[[35, 36, 37],
         [40, 41, 42],
         [45, 46, 47]]]), 
            np.array([[[38, 39],
         [43, 44],
         [48, 49]]]), 
            np.array([[[50, 51, 52],
         [55, 56, 57]]]), 
            np.array([[[53, 54],
         [58, 59]]]), 
            np.array([[[60, 61, 62],
         [65, 66, 67]]]), 
            np.array([[[63, 64],
         [68, 69]]]), 
            np.array([[[70, 71, 72],
         [75, 76, 77],
         [80, 81, 82]]]), 
            np.array([[[73, 74],
         [78, 79],
         [83, 84]]]), 
            np.array([[[85, 86, 87],
         [90, 91, 92]]]), 
            np.array([[[88, 89],
         [93, 94]]]), 
            np.array([[[ 95,  96,  97],
         [100, 101, 102]]]), 
            np.array([[[ 98,  99],
         [103, 104]]])]
                
    return x



# test no padding, blocks by reference (changes in blocks affect the original 
# array)
def test_blocks_by_reference():
    
    # create test 2D array
    R = 5
    C = 10
    
    x = np.array(range(R*C)).reshape(R,C)
    
    # array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
    #        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    #        [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    #        [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    #        [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]])
    
    # split into 2,3 blocks
    block_slices, blocks, xout = pymg.block_split(x, nblocks=(2,3), by_reference=True)

    # check number of blocks
    assert(2*3 == len(blocks))

    # check that array hasn't changed
    assert((x == xout).all())
    
    # load ground truth    
    expected_blocks = example_2D_array_blocks()
    
    # check that all blocks were computed as expected    
    for eb, b in zip(expected_blocks, blocks):
        assert((eb == b).all())
        
    # set one block to zeros, and check that the original array changes too
    blocks[3][...] = 0
    assert((x[3:5, 0:4] == blocks[3]).all())
    
# test no padding, blocks by value (changes in blocks don't affect the original 
# array)
def test_blocks_by_value():
    
    # create test 2D array
    R = 5
    C = 10
    
    x = np.array(range(R*C)).reshape(R,C)
    
    # array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
    #        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    #        [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    #        [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    #        [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]])
    
    # split into blocks
    block_slices, blocks, xout = pymg.block_split(x, nblocks=(2,3), by_reference=False)

    # check number of blocks
    assert(2*3 == len(blocks))

    # check that array hasn't changed
    assert((x == xout).all())
    
    # load ground truth    
    expected_blocks = example_2D_array_blocks()
    
    # check that all blocks were computed as expected    
    for eb, b in zip(expected_blocks, blocks):
        assert((eb == b).all())
        
    # set one block to zeros, and check that the original array does not change
    blocks[3][...] = 0
    assert((x[block_slices[3]] == expected_blocks[3]).all())
    

# slice a 3D array into blocks
def test_3d_array():
    
    S = 3
    R = 7
    C = 5
    
    # create 3D array
    x = np.array(range(R*C*S)).reshape(S,R,C)
    
    # array([[[  0,   1,   2],
    #     [  3,   4,   5],
    #     [  6,   7,   8],
    #     [  9,  10,  11],
    #     [ 12,  13,  14]],
    # 
    # ...
    # 
    #   [[ 90,  91,  92],
    #    [ 93,  94,  95],
    #    [ 96,  97,  98],
    #    [ 99, 100, 101],
    #    [102, 103, 104]]])
    
    # split into blocks
    block_slices, blocks, _ = pymg.block_split(x, nblocks=(3,3,2), by_reference=True)

    # load ground truth
    expected_blocks = example_3D_array_blocks()

    # check that all blocks were computed as expected    
    for eb, b in zip(expected_blocks, blocks):
        assert((eb == b).all())

# check that trying to use blocks by reference with padding will throw an exception
def test_no_reference_with_padding():
    
    # create test 2D array
    R = 5
    C = 10
    
    x = np.array(range(R*C)).reshape(R,C)
    
    # array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
    #        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    #        [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    #        [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    #        [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]])
    
    # split into blocks
    try:
        block_slices, blocks, xout = pymg.block_split(x, nblocks=(2,3), pad_width=3, by_reference=True)
    except Exception:
        pass
    else:
        raise Exception('Exception not raised')
    
# check that padding works
def test_padding():
    
    # create test 2D array
    R = 5
    C = 10
    
    x = np.array(range(R*C)).reshape(R,C)
    
    # array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
    #        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    #        [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    #        [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    #        [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]])
    
    # split into blocks
    block_slices, blocks, xout = pymg.block_split(x, nblocks=(1,4), 
                                                  pad_width=(2,3), mode='constant', constant_values=0)

    # check number of blocks
    assert(1*4 == len(blocks))

    # check that array has been padded
    assert((np.pad(x, pad_width=(2,3), mode='constant') == xout).all())
    
    # load ground truth    
    expected_blocks = example_padded_2D_array_blocks()
    
    # check that all blocks were computed as expected    
    for eb, b in zip(expected_blocks, blocks):
        assert((eb == b).all())
