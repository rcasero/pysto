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
@version: 1.0.1

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
##   TypicalBorderIntensity:
##      typical intensity value of the voxels on the perimeter of the image.
##
###############################################################################

import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

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

    origin = im.GetOrigin()
    spacing = im.GetSpacing()
    size = im.GetSize()

    # when origin='lower', the image will be upside down, so we need to take
    # that into account for the vertical axis
    if ('origin' in kwargs) and (kwargs['origin'] == 'lower'):
        extent = (
                origin[0], origin[0] + (size[0]-1) * spacing[0],
                origin[1] + (size[1]-1) * spacing[1], origin[1]
                )
    else:
        extent = (
                origin[0], origin[0] + (size[0]-1) * spacing[0],
                origin[1], origin[1] + (size[1]-1) * spacing[1]
                )

    
    # pass the call to matplotlib.imshow
    return plt.imshow(sitk.GetArrayFromImage(im), extent=extent, **kwargs)

###############################################################################
## TypicalBorderIntensity
###############################################################################

def TypicalBorderIntensity(im, mode='median'):
    """Compute the typical values at the boundaries of SimpleITK Images or np.arrays
    
    For each channel of an n-dimensional SimpleITK image, it extracts all the 
    voxels in its perimeter, and computes the typical value (median or mean). 
    If the input is an np.array, it's treated as a 1-channel image (greyscale).
    
    Args:
        im: SimpleITK n-dimensional image, colour or greyscale, or a numpy 
        array.
        
        mode: Method to compute the typical value. Options are 'median' 
        (default) and 'mean'.
    """
    
    # convert input image to np.array type, if necessary, keeping a note of 
    # whether it has more than one component (colour)
    if type(im) == np.ndarray:
        numberOfComponentsPerPixel = 1
        dimension = im.ndim
    elif type(im) == sitk.SimpleITK.Image:
        numberOfComponentsPerPixel = im.GetNumberOfComponentsPerPixel()
        dimension = im.GetDimension()
        im = sitk.GetArrayFromImage(im)
        # Note: ITK Size=(50,100) image becomes np.array im.shape=(100,50)
    else:
        raise Exception('Function not implemented for type(im) = ' + str(type(im)))
    if numberOfComponentsPerPixel == 1:
        size = im.shape
    else:
        size = im.shape[0:-1]
        
    # check that for colour images, the colour channel is the last index
    if numberOfComponentsPerPixel > 1:
        assert(im.shape[-1] == numberOfComponentsPerPixel)
        
    # initialise output
    typicalBorderIntensity = [None,] * numberOfComponentsPerPixel
    
    # loop colour channels
    for component in range(numberOfComponentsPerPixel):

        # init variable to keep copy of all pixels on the edge
        border_values = []

        #print('*')
        
        for d in range(dimension):
            
            # to avoid repeating pixels, we avoid the first and last elements 
            # of already sampled dimensions
            slice_left_edge = [slice(1,size[d_prev]-1,1) for d_prev in range(d)]
            slice_right_edge = [slice(1,size[d_prev]-1,1) for d_prev in range(d)]
            
            # to sample the current dimension, we only take the first or last 
            # elements, respectively for the left and right edges
            slice_left_edge += [slice(0,1,1)]
            slice_right_edge += [slice(size[d]-1,size[d],1)]
            
            # from posterior dimensions, we take all elements
            slice_left_edge += [slice(0,size[d_post],1) for d_post in range(d+1,dimension)]
            slice_right_edge += [slice(0,size[d_post],1) for d_post in range(d+1,dimension)]

            # colour channel index, if necessary            
            if numberOfComponentsPerPixel>1:
                slice_left_edge += [slice(component,component+1,1)]
                slice_right_edge += [slice(component,component+1,1)]
            
            #print(slice_left_edge)
            #print(slice_right_edge)
            
            # get border values in this slice and component
            border_values = np.concatenate([border_values, im[slice_left_edge].flatten()])
            border_values = np.concatenate([border_values, im[slice_right_edge].flatten()])
            
            # compute typical value
            if (mode == 'median'):
                 typicalBorderIntensity[component] = np.median(border_values)
            elif (mode == 'mean'):
                 typicalBorderIntensity[component] = np.mean(border_values)
            else:
                raise Exception('Mode not implemented')

    if numberOfComponentsPerPixel == 1:
        return typicalBorderIntensity[0]
    else:
        return typicalBorderIntensity
