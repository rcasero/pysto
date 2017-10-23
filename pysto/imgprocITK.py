#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:50:02 2017

@author: rcasero
"""

"""
@file: pysto/pysto/imgprocITK.py
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

###############################################################################
## Summary of functions in this module:
##
##   imshow:
##      matplotlib.imshow extended for the ITK Image class.
##
###############################################################################

import SimpleITK as sitk
import matplotlib.pyplot as plt

###############################################################################
## block_split
###############################################################################

def imshow(im, **kwargs):
    """matplotlib.imshow extended for the ITK Image class.
    
    Light wrapper around matplotlib.imshow so that ITK images are plotted with
    real world coordinates.
    
        ... = imshow(im, ...)
    
    Args:
        im: 2D ITK Image class.
        
        ...: Optional arguments, the same that can be passed to matplotlib.imshow.
        
    Returns:
        Same as matplotlib.imshow.
    """

    # compute extent of the image
    origin = im.GetOrigin()
    spacing = im.GetSpacing()
    size = im.GetSize()
    extent = (
            origin[0], origin[0] + (size[0]-1) * spacing[0],
            origin[1], origin[1] + (size[1]-1) * spacing[1]
            )
    
    # pass the call to matplotlib.imshow
    return plt.imshow(sitk.GetArrayFromImage(im), extent=extent, **kwargs)
