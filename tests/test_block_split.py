#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: pysto/tests/test_block_split.py
@package: pysto
@author: Ramón Casero <rcasero@gmail.com>
@copyright: (C) 2017  Ramón Casero <rcasero@gmail.com>
@license: GPL v3
@version: 1.1.0

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
    
            np.array([[ 4,  5,  6,  7],
                      [14, 15, 16, 17],
                      [24, 25, 26, 27]]), 
    
            np.array([[ 8,  9],
                      [18, 19],
                      [28, 29]]), 
    
            np.array([[30, 31, 32, 33],
                      [40, 41, 42, 43]]), 
    
            np.array([[34, 35, 36, 37],
                      [44, 45, 46, 47]]), 
    
            np.array([[38, 39],
                      [48, 49]])
            ]
            
    return x


def example_3D_array_blocks():
    
    x = [
            np.array([[[ 0,  1],
                       [ 3,  4]],
 
                      [[15, 16],
                       [18, 19]],
 
                      [[30, 31],
                       [33, 34]],
 
                      [[45, 46],
                       [48, 49]],
 
                      [[60, 61],
                       [63, 64]]]), 

            np.array([[[ 2],
                       [ 5]],
 
                      [[17],
                       [20]],
 
                      [[32],
                       [35]],
 
                      [[47],
                       [50]],
 
                      [[62],
                       [65]]]), 

            np.array([[[ 6,  7],
                       [ 9, 10]],
 
                      [[21, 22],
                       [24, 25]],
 
                      [[36, 37],
                       [39, 40]],
 
                      [[51, 52],
                       [54, 55]],
 
                      [[66, 67],
                       [69, 70]]]), 

            np.array([[[ 8],
                       [11]],
 
                      [[23],
                       [26]],
 
                      [[38],
                       [41]],
 
                      [[53],
                       [56]],
 
                      [[68],
                       [71]]]), 

            np.array([[[12, 13]],
 
                      [[27, 28]],
 
                      [[42, 43]],
 
                      [[57, 58]],
 
                      [[72, 73]]]), 

            np.array([[[14]],
 
                      [[29]],
 
                      [[44]],
 
                      [[59]],
 
                      [[74]]]), 

            np.array([[[ 75,  76],
                       [ 78,  79]],
 
                      [[ 90,  91],
                       [ 93,  94]],
 
                      [[105, 106],
                       [108, 109]],
 
                      [[120, 121],
                       [123, 124]],
 
                      [[135, 136],
                       [138, 139]]]), 

            np.array([[[ 77],
                       [ 80]],
 
                      [[ 92],
                       [ 95]],
 
                      [[107],
                       [110]],
 
                      [[122],
                       [125]],
 
                      [[137],
                       [140]]]), 

            np.array([[[ 81,  82],
                       [ 84,  85]],
 
                      [[ 96,  97],
                       [ 99, 100]],
 
                      [[111, 112],
                       [114, 115]],
 
                      [[126, 127],
                       [129, 130]],
 
                      [[141, 142],
                       [144, 145]]]), 

            np.array([[[ 83],
                       [ 86]],
 
                      [[ 98],
                       [101]],
 
                      [[113],
                       [116]],
 
                      [[128],
                       [131]],
 
                      [[143],
                       [146]]]), 

            np.array([[[ 87,  88]],
 
                      [[102, 103]],
 
                      [[117, 118]],
 
                      [[132, 133]],
 
                      [[147, 148]]]), 

            np.array([[[ 89]],
 
                      [[104]],
 
                      [[119]],
 
                      [[134]],
 
                      [[149]]]), 

            np.array([[[150, 151],
                       [153, 154]],
 
                      [[165, 166],
                       [168, 169]],
 
                      [[180, 181],
                       [183, 184]]]), 

            np.array([[[152],
                       [155]],
 
                      [[167],
                       [170]],
 
                      [[182],
                       [185]]]), 

            np.array([[[156, 157],
                       [159, 160]],
 
                      [[171, 172],
                       [174, 175]],
 
                      [[186, 187],
                       [189, 190]]]), 

            np.array([[[158],
                       [161]],
 
                      [[173],
                       [176]],
 
                      [[188],
                       [191]]]), 

            np.array([[[162, 163]],
 
                      [[177, 178]],
 
                      [[192, 193]]]), 

            np.array([[[164]],
 
                      [[179]],
 
                      [[194]]])]
                
    return x



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
    block_slices, blocks = pymg.block_split(x, (2,3))
    
    expected_blocks = example_2D_array_blocks()
    
    # check that all blocks were computed as expected    
    for eb, b in zip(expected_blocks, blocks):
        assert((eb == b).all())
        
    # set one block to zeros, and check whether the original array changes too
    blocks[3][...] = 0
    assert((x[3:5, 0:4] == blocks[3]).all())
    

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
    
    # split into 2,3 blocks
    block_slices, blocks = pymg.block_split(x, (2,3), by_reference=False)
    
    expected_blocks = example_2D_array_blocks()
    
    # check that all blocks were computed as expected    
    for eb, b in zip(expected_blocks, blocks):
        assert((eb == b).all())
        
    # set one block to zeros, and check that the original array has not changed
    blocks[3][...] = 0
    assert((x[3:5, 0:4] == expected_blocks[3]).all())

# slice a 3D array into blocks
def test_3d_array():
    
    R = 13
    C = 5
    S = 3
    
    # create 3D array
    x = np.array(range(R*C*S)).reshape(R,C,S)
    
    # array([[[  0,   1,   2],
    #     [  3,   4,   5],
    #     [  6,   7,   8],
    #     [  9,  10,  11],
    #     [ 12,  13,  14]],
    # 
    #    [[ 15,  16,  17],
    #     [ 18,  19,  20],
    #     [ 21,  22,  23],
    #     [ 24,  25,  26],
    #     [ 27,  28,  29]],
    # 
    # ...
    # 
    #    [[180, 181, 182],
    #     [183, 184, 185],
    #     [186, 187, 188],
    #     [189, 190, 191],
    #     [192, 193, 194]]])
    
    # split into blocks
    block_slices, blocks = pymg.block_split(x, (3,3,2))

    # load ground truth
    expected_blocks = example_3D_array_blocks()

    # check that all blocks were computed as expected    
    for eb, b in zip(expected_blocks, blocks):
        assert((eb == b).all())

def test_slicing():
    
    R = 11
    C = 6
    S = 3
    T = 4
    
    # create 3D array
    x = np.array(range(R*C*S*T)).reshape(R,C,S,T)
    
    # split into blocks
    block_slices, blocks = pymg.block_split(x, (3,3,2,3))
    
    # check that the blocks are the same as the slices of the array
    for i in range(len(blocks)):
        assert((blocks[i] == x[block_slices[i]]).all())

