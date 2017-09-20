#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:09:02 2017

@author: rcasero
"""

import os    
import matplotlib.pyplot as plt
import pysto.imgproc as pymg
import cv2

# root and test data directories for pysto
root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
data_path = os.path.join(root_path, 'test', 'data')
    
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
