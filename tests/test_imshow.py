#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file: pysto/tests/test_imfuse.py
@package: pysto
@author: Ramón Casero <rcasero@gmail.com>
@copyright: © 2017  Ramón Casero <rcasero@gmail.com>
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
import SimpleITK as sitk
import pysto.imgprocITK as pitk

# root and test data directories for pysto
root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
data_path = os.path.join(root_path, 'tests', 'data')

def test_imshow():
    
    # image file
    im_file = os.path.join(data_path, 'euxassay_003820_14.jpg')
    
    # read image
    im = sitk.ReadImage(im_file)
    
    # give image spacing and offset values
    im.SetSpacing((14.0e-6, 14.0e-6))
    im.SetOrigin((10.0, 5.0))
    
    # plot image
    pitk.imshow(im, origin='lower')
    pitk.imshow(im)
