#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@file: pysto/pysto/imgproc.py
@package: pysto
@author: Ramón Casero <rcasero@gmail.com>
@copyright: © 2017  Ramón Casero <rcasero@gmail.com>
@license: GPL v3
@version: 1.3.0

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
##   block_split:
##      Split an nd-array into blocks with or without overlapping between the blocks.
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

def block_split(x, nblocks, by_reference=False, pad_width=0, mode='constant', **kwargs):
    """Split an nd-array into blocks.
    
    Split an N-dimensional array into blocks with or without overlapping 
    between the blocks.
    
    The overlap is set with parameter 'pad_width', in voxel units (default 0). 
    Overlap is useful in image processing to avoid "seams" or a "mosaic" effect
    when the blocks are put back together.
    
    The basic syntax (no overlap) is
    
        block_slices, blocks = block_split(x, nblocks, by_reference=False)
        
    Output 'block_slices' is a list of slice objects such that 
    
        blocks[i]=x[block_slices[i]]
    
    Note that if the array length is not a multiple of the block length, one 
    block will have a slightly different size as the others, as decided by 
    numpy.array_split().
    
    When pad_width>0, the array itself needs to be padded at the borders. This
    uses the same parameters as numpy.pad(). 
    
        block_slices, blocks, xout = block_split(x, nblocks, pad_width=0, mode='constant', **kwargs)
    
    Some examples:
    
        block_slices, blocks, xout = block_split(x, nblocks, pad_width=(2,3), mode='constant', constant_values=(4, 6))
        block_slices, blocks, xout = block_split(x, nblocks, pad_width=(2, 3), mode='edge')
        block_slices, blocks, xout = block_split(x, nblocks, pad_width=(2, 3), mode='linear_ramp', end_values=(5, -4))
        block_slices, blocks, xout = block_split(x, nblocks, pad_width=(2,), mode='maximum')
        block_slices, blocks, xout = block_split(x, nblocks, pad_width=(2, 3), mode='reflect', reflect_type='odd')
        ...
    
    See numpy.pad() documentation for all options: https://docs.scipy.org/doc/numpy/reference/generated/numpy.pad.html#numpy.pad.
    
    Output 'xout' returns the padded array. The blocks the correspond to
    
        blocks[i]=xout[block_slices[i]]
    
    Args:
        x: nd-array (numpy).
        
        nblocks: Scalar or list of the same length as x.shape, with the number 
        of blocks to create in each dimension. If nblocks is a scalar, then 
        that scalar applies to all dimensions. The number of blocks cannot be
        larger than the number of elements in the corresponding dimension.
        
        by_reference: (def False) Whether blocks are returns as sliced arrays 
        (by reference) or as copies of the slice array (by value). Changes to 
        blocks by reference apply to the original array. Changes to blocks by 
        value are only local.
        For blocks with padding, by_reference must be False, as otherwise 
        border blocks would point outside the memory region of the array.
        
        pad_width, mode, ...: Padding parameter. They are applied to each 
        block, adding elements around the border of x as required. These 
        parameters are the same used by function numpy.pad.
        
    Returns:
        block_slices: List of slice objects. Each slice applied to x produces 
        the corresponding block, blocks[i]=xout[block_slices[i]].
        
        blocks: List of blocks. Each block is a sliced array (a chunk of the 
        output array).
        
        xout: Array after padding. If pad_width=0, then xout=x.
    """
    
    # number of dimensions
    ndims = len(x.shape)

    # if nblocks given as a scalar, converto to tuple
    if (np.isscalar(nblocks)):
        nblocks = [nblocks]*ndims
    
    # if pad_width given as a scalar, convert to (pad_before,pad_after) tuple
    if (np.isscalar(pad_width)):
        pad_width = (pad_width, pad_width)
        
    # if pad_width given as a (pad_before,pad_after) tuple, convert to
    # ((pad_before,pad_after), (pad_before,pad_after),...) tuple
    if (isinstance(pad_width, tuple) and not(isinstance(pad_width[0], tuple))):
        pad_width = (pad_width,) * ndims
        
    # input arguments checks
    if (len(nblocks) != ndims):
        raise Exception('nblocks must have one element per dimension in x')

    if (len(pad_width) != ndims):
        raise Exception('pad_width must have one (p_before,p_after) tuple per dimension in x')

    if len([i for i, j in zip(nblocks, x.shape) if i > j]) > 0:
        raise Exception('There cannot be more blocks along a dimension than array elements')
        
    if (by_reference & np.min(pad_width)>0):
        raise Exception('Blocks with padding cannot be returned by reference, because some padding elements will be outside the array and others will overlap')

    # get two lists:
    # idx_start[d] = starting indices of each block along dimension d
    # idx_end[d] = ditto for end indices
    idx_start = []
    idx_end = []
    for d in range(ndims):
        idx = np.array_split(range(x.shape[d]), nblocks[d])
        idx_start += [[item[0] for item in idx]]
        idx_end += [[item[-1] for item in idx]]
    
    # total amount of padding (total=before+after) in each dimension
    pad_width_total = [np.sum(pad) for pad in pad_width]
    
    # recompute the end indices in the padded array (the start ones are already
    # valid, because the first block starts at the first padding element)
    # idx_end := idx_end + total padding
    idx_end = [i+w for i,w in zip(idx_end, pad_width_total)]
        
    # create indices for each block in the array (we use iterators, but you can
    # see the indices using e.g. list(idx_start))
    idx_start = itertools.product(*idx_start)
    idx_end = itertools.product(*idx_end)

    # add external margins to the array, if necessary (padding also removes the
    # reference to the input array, so if we want that the output blocks link 
    # by reference to the input array, we cannot pad)
    if (not(by_reference)):
        x = np.lib.pad(x, pad_width, mode, **kwargs)
    
    # iterate to extract all blocks from array
    blocks = []
    block_slices = []
    for (b_start, b_end) in zip(idx_start, idx_end):
        
        # create a slice object per dimension
        this_block_slice = []
        for d in range(ndims):
            this_block_slice += [slice(b_start[d],b_end[d]+1,1)]

        # keep copy of slice for output
        block_slices += [this_block_slice]
        
        # extract block from array
        if (by_reference):
            this_block = x[this_block_slice]
        else:
            this_block = np.copy(x[this_block_slice])
        
        # add margins to block
        
        # add block to output list
        blocks += [this_block]
        
    return block_slices, blocks, x

###############################################################################
## block_stack
###############################################################################

def block_stack(blocks, block_slices, pad_width=0):
    """Reassemble blocks into an nd-array.
    
    Stack a list of blocks to reassemble the original array. This function 
    is the opposite of block_split().
    
        x, block_slices_no_padding = block_stack(blocks, block_slices, pad_width=0)
        
    If the blocks were created with overlap (padding), the padding is removed
    before the blocks are stacked.
    
    Args:
        blocks: List of blocks (output of block_split). Each block is a sliced 
        array (a chunk of the array we want to recover). The blocks may be 
        overlapping if padding was chosen in block_split().
        
        block_slices: List of slice objects with padding. Each slice applied to 
        the original padded x produces the corresponding padded block, 
        blocks[i]=x_padded[block_slices[i]].
        
        pad_width: (def 0) Scalar or tuple describing the amount of padding 
        that was used in block_split().
        
    Returns:
        x: nd-array (numpy).
        
        block_slices_no_padding: List of slice objects without padding. Each 
        slice applied to x produces one non-overlapping block, 
        block_no_padding=x[block_slices_no_padding].
    """

    # number of blocks (length of the list of blocks, whereas in block_split(),
    # nblocks is a tuple with the number of blocks in each axis)
    nblocks = len(blocks)
    
    # number of dimensions
    ndims = len(block_slices[0])
    
    # if pad_width given as a scalar, convert to (pad_before,pad_after) tuple
    if (np.isscalar(pad_width)):
        pad_width = (pad_width, pad_width)
        
    # if pad_width given as a (pad_before,pad_after) tuple, convert to
    # ((pad_before,pad_after), (pad_before,pad_after),...) tuple
    if (isinstance(pad_width, tuple) and not(isinstance(pad_width[0], tuple))):
        pad_width = (pad_width,) * ndims

    # input arguments checks
    if (nblocks != len(block_slices)):
        raise Exception('Not the same number of blocks as slices')
        
    if (len(pad_width) != ndims):
        raise Exception('pad_width must have one (p_before,p_after) tuple per dimension in x')

    # size of whole output array. We get the start and stop value of every 
    # slice. If start=X, it means the array has at least size X+1. If stop=X, 
    # the array has at least X elements
    x_shape = [0] * ndims
    for d in range(ndims):
        x_shape[d] = np.max([[sl[d].start + 1]+[sl[d].stop] for sl in block_slices]) - pad_width[d][0]
        x_shape[d] -= pad_width[d][1]
    
    # init output array
    x = np.empty(tuple(x_shape), dtype=blocks[0].dtype)
    x[:] = np.NAN

    # remove padding from block_slices
    block_slices_no_padding = []
    for sl, b in zip(block_slices, blocks):
        
        # reindex slice so that it points to the block without padding
        this_block_slice = [] # referred to full output array
        slice_to_remove_padding = [] # referred to current block, only to remove padding
        for d in range(ndims):
            # slice referred to the full output array
            this_block_slice += [slice(sl[d].start,
                                       sl[d].stop  - pad_width[d][0] - pad_width[d][1],
                                       sl[d].step)]
    
            # local slice only to remove the padding in current block
            slice_to_remove_padding += [slice(pad_width[d][0],
                                              b.shape[d] - pad_width[d][1],1)]
        
        block_slices_no_padding += [this_block_slice]
        
        # assign current block (without padding) to output array
        x[this_block_slice] = b[slice_to_remove_padding]
    

    return x, block_slices_no_padding
    
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
    
