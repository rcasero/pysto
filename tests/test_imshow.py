#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:31:17 2017

@author: rcasero
"""

import os
import SimpleITK as sitk
import pysto.imgprocITK as pitk

# root and test data directories for pysto
root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
data_path = os.path.join(root_path, 'tests', 'data')

# image file
im_file = os.path.join(data_path, 'euxassay_003820_14.jpg')

# read image
im = sitk.ReadImage(im_file)

# give image spacing and offset values
im.SetSpacing((14.0e-6, 14.0e-6))
im.SetOrigin((10.0, 5.0))

# plot image
pitk.imshow(im)
