#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: pysto/tests/test_imfuse.py
@package: pysto
@author: Ramón Casero <rcasero@gmail.com>
@copyright: (C) 2017  Ramón Casero <rcasero@gmail.com>
@license: GPL v3
@version: 0.1.1

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

import os    
import matplotlib.pyplot as plt
import pysto.imgproc as pymg
import cv2

# root and test data directories for pysto
root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
data_path = os.path.join(root_path, 'tests', 'data')
    
def test_imfuse():
    """Test function for imfuse()
    """

    # path and name of test files
    im1_name = os.path.join(data_path, "left.png")
    im2_name = os.path.join(data_path, "right.png")
    
    # read test images and their masks
    im1 = cv2.imread(im1_name)
    im2 = cv2.imread(im2_name)
    
    # fuse images
    imf = pymg.imfuse(im1, im2)
    
    # plot images
    plt.close('all')
    plt.subplot(221)
    plt.imshow(im1)
    plt.title("Left image")
    plt.subplot(222)
    plt.imshow(im2)
    plt.title("Right image")
    plt.subplot(212)
    plt.imshow(imf)
    plt.title("imfuse")
    plt.show(block=False)
