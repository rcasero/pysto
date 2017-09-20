#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@file: pysto/tests/test_matchHist.py
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

import pysto.imgproc as pymg
import os 
import cv2
import matplotlib.pyplot as plt

# root and test data directories for pysto
root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
data_path = os.path.join(root_path, 'test', 'data')
    
def test_matchHist():
    """Test function for matchHist()
    """

    # path and name of test files
    imref_name = os.path.join(data_path, "right.png")
    im_name = os.path.join(data_path, "left.png")
    maskref_name = os.path.join(data_path, "right_mask.png")
    mask_name = os.path.join(data_path, "left_mask.png")

    # read test images and their masks
    imref = cv2.imread(imref_name)
    im = cv2.imread(im_name)
    maskref = cv2.imread(maskref_name)
    mask = cv2.imread(mask_name)
    maskref = maskref[:, :, 1]==255
    mask = mask[:, :, 1]==255

    # plot images
    plt.close('all')
    fig, ax = plt.subplots(2, 2)
    ax[0, 0].imshow(imref)
    ax[0, 0].set_title("Ref image")
    ax[1, 0].imshow(im)
    ax[1, 0].set_title("Image to be corrected")
    ax[0, 1].imshow(maskref)
    ax[0, 1].set_title("Ref mask")
    ax[1, 1].imshow(mask)
    ax[1, 1].set_title("Mask of image to be corrected")
 
    # match histogram of im to imref, only taking into account the pixels==1 in
    # the masks
    im_matched = pymg.matchHist(imref, im, maskref=maskref, mask=mask)
    
    # plot images
    fig, ax = plt.subplots(2, 2)
    ax[0, 0].imshow(imref)
    ax[0, 0].set_title("Ref image")
    ax[1, 0].imshow(im_matched)
    ax[1, 0].set_title("Corrected image")
    ax[0, 1].imshow(maskref)
    ax[0, 1].set_title("Ref mask")
    ax[1, 1].imshow(mask)
    ax[1, 1].set_title("Mask of corrected image")

    plt.show(block=False)
    plt.close()
    