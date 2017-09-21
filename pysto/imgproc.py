#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@file: pysto/pysto/imgproc.py
@package: pysto
@author: Ramón Casero <rcasero@gmail.com>
@copyright: (C) 2017  Ramón Casero <rcasero@gmail.com>
@license: GPL v3
@version: 1.1.1

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
##   block_split(x, nblocks):
##      Split an nd-array into blocks.
##
##   imfuse: 
##      Composite of two images.
##
##   matchHist: 
##      Modify image intensities to match the histogram of a reference image.
##
###############################################################################

import numpy as np
import cv2
import itertools

###############################################################################
## block_split
###############################################################################

def block_split(x, nblocks):
    """Split an nd-array into blocks.
    
    Split an N-dimensional array into blocks. This syntax returns one slice 
    object per block
    
        block_slices, _ = block_split(x, nblocks)
    
    so that the i-th block is x[block_slices[i]]. Because slicing works by 
    reference, you can operate on the block, and the operations are applied to
    the original array x.
    
    For convenience, the function can also output references to the blocks.
    
        block_slices, blocks = block_split(x, nblocks)
    
    Args:
        x: nd-array (numpy).
        
        nblocks: list of the same length as x.shape, with the number of blocks 
        to create in each dimension.
        
    Returns:
        block_slices: list of slice object. Each slice applied to x produces 
        the corresponding block.
        
        blocks: list of blocks. Each block is a sliced array (a chunk of the 
        original array).
    """
    
    if (len(nblocks) != len(x.shape)):
        raise Exception('nblocks must have one element per dimension in x')

    if len([i for i, j in zip(nblocks, x.shape) if i > j]) > 0:
        raise Exception('There cannot be more blocks along a dimension than elements')

    # number of dimensions
    ndims = len(x.shape)

    # block size in each dimension to produce the required number of blocks
    block_shape = np.ceil(np.true_divide(x.shape, nblocks))
    block_shape = list(block_shape.astype(int))
    
    # list of lists. idx_start = [[0, 5, 10], [0, 2, 4], [0, 2]]
    # means that dimension=0 blocks start at indices [0,5,10]
    #            dimension=1 blocks start at indices [0,2,4]
    #            dimension=2 blocks start at indices [0,2]
    idx_start = []
    idx_end = []
    for d in range(ndims):
        # first index of each block
        idx_start += [list(range(0,x.shape[d],block_shape[d]))]
        # last index of each block if the array were big enough
        idx_end += [list(np.array(idx_start[d]) + block_shape[d] - 1)]
        # match the size of the last block to the size of the array
        idx_end[d][-1] = x.shape[d]-1
    
    # create indices for each block in the array (we use iterators, but you can
    # see the indices using e.g. list(idx_start))
    idx_start = itertools.product(*idx_start)
    idx_end = itertools.product(*idx_end)
    
    # convert to list so that we can provide the block indices at the output 
    # (otherwise, the iterators get exhausted, and return [])
    #idx_start = list(idx_start)
    #idx_end = list(idx_end)
    
    # iterate to extract all blocks from array
    blocks = []
    block_slices = []
    for (b_start, b_end) in zip(idx_start, idx_end):
        
        # create a slice object per dimension
        this_block_slice = []
        for d in range(ndims):
            this_block_slice += [slice(b_start[d],b_end[d]+1,1)]

        # extract block from array
        block_slices += [this_block_slice]
        blocks += [x[this_block_slice]]
        
    return block_slices, blocks


###############################################################################
## imfuse
###############################################################################

def imfuse(a, b):
    """Composite of two images.
    
    Create a false-colour RGB image that combines two input images. This is
    useful to visually assess the overlapping of two images.
    
    C = imfuse(A, B)
    
    Args:
        A, B: Two input images, of any size, grayscale or RGB.
        
    Returns:
        C: Output image. It is built by converting A,B to grayscale, if 
        necessary. Then, the RGB channels of C are set as C=(B,A,B)
    """
    
    # convert to grayscale if colour images
    if (len(a.shape)>2):
        a = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    if (len(b.shape)>2):
        b = cv2.cvtColor(b, cv2.COLOR_RGB2GRAY)
    
    # get size of image that contains both images
    sz = np.maximum(a.shape, b.shape)
    
    # zero-padding of images, if necessary, so that they match the output
    a = np.lib.pad(a, ((0, sz[0]-a.shape[0]), (0, sz[1]-a.shape[1])), 'constant')
    b = np.lib.pad(b, ((0, sz[0]-b.shape[0]), (0, sz[1]-b.shape[1])), 'constant')

    # the output fused image 
    return np.dstack((b, a, b))

###############################################################################
## matchHist
###############################################################################

def matchHist(imref, im, maskref=np.ones(0, dtype=bool), mask=np.ones(0, dtype=bool), nbr_bins=256):
    """Modify image intensities to match the histogram of a reference image.
    
    imout = matchHist(imref, im)
    
    Args:
        imref, im: Grayscale or colour 2D images [row, col, channel]. im is the
                   image we want to modify so that it matches the histogram 
                   (channel by channel) of imref.

    Returns:                   
        imout: The modified version of im.
                   
    imout = matchHist(imref, im, maskref=[], mask=[], nbr_bins=256)
    
    Optional:
        maskref, mask: Bool masks for imref, im, respectively. The masks must 
                       have the same number of [rows,cols] as their respective
                       images, but only 1 channel. Pixels set to False in the
                       mask are completely ignored (default: no mask)
                       
        nbr_bins: Number of bins used to compute histograms (default: 256)
    """
    
    # duplicate inputs, to avoid modifying the objects they point to outside
    # this function
    imout = im.copy()
    imrefaux = imref.copy()
    
    # mask must be boolean
    if maskref.dtype != "bool":
        raise TypeError("maskref must be of type bool")
    if mask.dtype != "bool":
        raise TypeError("mask must be of type bool")
        
    # mask must have only one channel. The same is applied to each image 
    # channel
    if maskref.ndim > 2:
        raise ValueError("maskref can have at most one channel")
    if mask.ndim > 2:
        raise ValueError("mask can have at most one channel")
        
    # grayscale images will be treated as multi-channel images with 1 channel
    if len(imrefaux.shape) < 3:
        imrefaux = imrefaux[:,:,np.newaxis]
    if len(imout.shape) < 3:
        imout = imout[:,:,np.newaxis]
    
    # masks must have the same [rows,cols] as the corresponding image
    if (len(maskref) > 0) & (maskref.shape != imref.shape[0:2]):
        raise ValueError('maskref must have the same [rows,col] as imref')
    if (len(mask) > 0) & (mask.shape != im.shape[0:2]):
        raise ValueError('mask must have the same [rows,col] as im')
    
    # compute histogram of each channel of the reference and converted images
    for i in range(0, imrefaux.shape[2]):
        
        # extract channel from the image
        chanref = imrefaux[:, :, i]
        chan = imout[:, :, i]
        
        # extract masked pixels, if masks are provided. Otherwise, use all 
        # pixels flattening the channel
        if len(maskref) > 0:
            chanref_flat = chanref[maskref]
        else:
            chanref_flat = chanref.flatten()
            
        if len(mask) > 0:
            chan_flat = chan[mask]
        else:
            chan_flat = chan.flatten()

        # compute histograms
        imhistref, binsref = np.histogram(chanref_flat, nbr_bins, normed=True)
        imhist, bins = np.histogram(chan_flat, nbr_bins, normed=True)
            
        # cumulative distribution function
        cdfhistref = imhistref.cumsum()
        cdfhist = imhist.cumsum()
        
        # bin centers
        cbinsref = (binsref[:-1] + binsref[1:]) / 2.0
        cbins = (bins[:-1] + bins[1:]) / 2.0
        
        # map intensity values in current channel so that they match the 
        # reference histogram
        chan_flat_to_cdf = np.interp(chan_flat, cbins, cdfhist)
        chan_flat_mapped = np.interp(chan_flat_to_cdf, cdfhistref, cbinsref)
        
        # tranfer corrected pixels to image
        if len(mask) > 0:
            chan[mask] = chan_flat_mapped
        else:
            chan = np.reshape(chan_flat_mapped, chan.shape)
            
        imout[:, :, i] = chan
        
    # return corrected image
    return imout
    
