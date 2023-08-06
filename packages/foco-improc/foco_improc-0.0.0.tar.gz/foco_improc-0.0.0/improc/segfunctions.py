#!/usr/bin/env python3

import cv2
import json
import numpy as np
import sys
from scipy import ndimage, optimize, spatial
from skimage import feature, morphology
from skimage._shared.coord import ensure_spacing

from skimage.feature.peak import _get_excluded_border_width, _get_threshold, _get_peak_mask, _exclude_border
def _get_high_intensity_peaks(image, mask, num_peaks, min_distance, p_norm, anisotropy=None):
    """
    This is (unfortunately) a copy of https://github.com/scikit-image/scikit-image/blob/5e74a4a3a5149a8a14566b81a32bb15499aa3857/skimage/feature/peak.py#L10-L32
    It has been updated to take anisotropy into account
    """
    # get coordinates of peaks
    coord = np.nonzero(mask)
    intensities = image[coord]
    # Highest peak first
    idx_maxsort = np.argsort(-intensities)
    coord = np.transpose(coord)[idx_maxsort]
    if np.isfinite(num_peaks):
        max_out = int(num_peaks)
    else:
        max_out = None
    if anisotropy is not None:
        if not isinstance(anisotropy, np.ndarray):
            anisotropy = np.array(anisotropy)
        coord = coord.astype(anisotropy.dtype) * anisotropy[None,:]
    coord = ensure_spacing(coord, spacing=min_distance, p_norm=p_norm,
                           max_out=max_out)
    if anisotropy is not None:
        coord /= anisotropy[None,:]
        coord = coord.astype(int)
    if len(coord) > num_peaks:
        coord = coord[:num_peaks]
    return coord
def peak_local_max(image, min_distance=1, threshold_abs=None,
                   threshold_rel=None, exclude_border=True,
                   num_peaks=np.inf, footprint=None, labels=None,
                   num_peaks_per_label=np.inf, p_norm=np.inf, anisotropy=None):
    """
    This is (unfortunately) a copy of https://github.com/scikit-image/scikit-image/blob/v0.20.0/skimage/feature/peak.py#L120-L309
    It has been updated to take anisotropy into account
    """
    if (footprint is None or footprint.size == 1) and min_distance < 1:
        warn("When min_distance < 1, peak_local_max acts as finding "
             "image > max(threshold_abs, threshold_rel * max(image)).",
             RuntimeWarning, stacklevel=2)
    border_width = _get_excluded_border_width(image, min_distance,
                                              exclude_border)
    threshold = _get_threshold(image, threshold_abs, threshold_rel)
    if footprint is None:
        size = 2 * min_distance + 1
        footprint = np.ones((size, ) * image.ndim, dtype=bool)
    else:
        footprint = np.asarray(footprint)
    if labels is None:
        # Non maximum filter
        mask = _get_peak_mask(image, footprint, threshold)
        mask = _exclude_border(mask, border_width)
        # Select highest intensities (num_peaks)
        coordinates = _get_high_intensity_peaks(image, mask,
                                                num_peaks,
                                                min_distance, p_norm, anisotropy=anisotropy)
    else:
        _labels = _exclude_border(labels.astype(int, casting="safe"),
                                  border_width)
        if np.issubdtype(image.dtype, np.floating):
            bg_val = np.finfo(image.dtype).min
        else:
            bg_val = np.iinfo(image.dtype).min
        # For each label, extract a smaller image enclosing the object of
        # interest, identify num_peaks_per_label peaks
        labels_peak_coord = []
        for label_idx, roi in enumerate(ndiimage.find_objects(_labels)):
            if roi is None:
                continue
            # Get roi mask
            label_mask = labels[roi] == label_idx + 1
            # Extract image roi
            img_object = image[roi].copy()
            # Ensure masked values don't affect roi's local peaks
            img_object[np.logical_not(label_mask)] = bg_val
            mask = _get_peak_mask(img_object, footprint, threshold, label_mask)
            coordinates = _get_high_intensity_peaks(img_object, mask,
                                                    num_peaks_per_label,
                                                    min_distance,
                                                    p_norm, anisotropy=anisotropy)
            # transform coordinates in global image indices space
            for idx, s in enumerate(roi):
                coordinates[:, idx] += s.start
            labels_peak_coord.append(coordinates)
        if labels_peak_coord:
            coordinates = np.vstack(labels_peak_coord)
        else:
            coordinates = np.empty((0, 2), dtype=int)
        if len(coordinates) > num_peaks:
            out = np.zeros_like(image, dtype=bool)
            out[tuple(coordinates.T)] = True
            coordinates = _get_high_intensity_peaks(image, out,
                                                    num_peaks,
                                                    min_distance,
                                                    p_norm, anisotropy=anisotropy)
    return coordinates

def reg_peaks(im, peaks, thresh = 36, anisotropy = (6,1,1)):
    """
    function that drops peaks that are found too close to each other (Not used by Spool or Thread)
    """
    peaks = np.array(peaks)
    anisotropy = np.array(anisotropy,dtype=int)
    for i in range(len(anisotropy)):
        peaks[:,i]*=anisotropy[i]

    diff = spatial.distance.cdist(peaks,peaks,metric='euclidean')
    complete = False
    while not complete:
        try:
            x,y = np.where(diff == np.min(diff[diff!=0]))
            x,y = x[0],y[0]
            if diff[x,y] >= thresh:
                complete = True
            else:
                peak1 = peaks[x] // anisotropy
                peak2 = peaks[y] // anisotropy

                if im[tuple(peak1)] > im[tuple(peak2)]:
                    diff = np.delete(diff, y, axis = 0)
                    diff = np.delete(diff, y, axis = 1)
                    peaks = np.delete(peaks, y, axis = 0)
                else:
                    diff = np.delete(diff, x, axis = 0)
                    diff = np.delete(diff, x, axis = 1)
                    peaks = np.delete(peaks, x, axis = 0)
        except:
            print("\nUnexpected error: ", sys.exc_info())
            complete = True

    for i in range(len(anisotropy)):
        peaks[:,i]= peaks[:,i]/anisotropy[i]
    return np.rint(peaks).astype(int)


def convAxis(im, axis, kernel):
    '''
    1d convolution along arbitrary axis of an image. 


    Method is to reshape numpy array into a 2d image, then apply cv2.filter2D to perform a 2d filtering operation utilizing your 1d kernel, and then reshaping the entire array back 

    Parameters
    ----------
    im : np.array
        numpy array for image data. can be an arbitrary number of dimensions
    axis : int
        integer axis designating along which axis to do the convolution
    kernel : np.array
        1d numpy array designating the kernel. 

    Outputs
    -------
    im : np.array
        numpy array for filtered image data

    '''
    if len(kernel.shape) == 1:
        kernel.reshape((len(kernel),1))
    axis = int(axis)
    shape = np.array(im.shape)
    shape[0],shape[axis] = shape[axis],shape[0]
    return np.swapaxes(cv2.filter2D(
        np.swapaxes(im,axis,0).reshape((im.shape[axis], int(im.size/im.shape[axis]))), 
        -1, 
        kernel).reshape((shape)),0,axis)

def gaussian2d(im, *args):
    """
    performs 2d convolution along last 2 dimensions of image data. currently, only handles 3d numpy arrays

    Parameters
    ----------
    im : np.array
        3d numpy array. the last 2 axes will be filtered through a 2d gaussian convolution
    gaussian : tuple (no keyword)
        tuple containing the size of the gaussian to use. can be passed anywhere from 2 to 4 arguments. if 2 arguments, the interpretation will be (width, sigma) with the window-width and sigma applied to both the x and y axes. if 3 arguments, the first two will be the width in x and y respectively, with the last being the sigma. if 4 arguments, it will be interpreted as (widthx, widthy, sigmax, sigmay)

    
    """
    width_x = width_y = 19
    sigma_x = sigma_y = 6        
    if args:
        #case: tuples
        if isinstance(args[0],tuple):
            if len(args[0]) == 2:
                width_x = args[0][0]
                width_y = args[0][0]
                sigma_x = args[0][1]
                sigma_y = args[0][1]
            if len(args[0]) == 3:
                width_x = args[0][0]
                width_y = args[0][1]
                sigma_x = args[0][2]
                sigma_y = args[0][2]    
            if len(args[0]) == 4:
                width_x = args[0][0]
                width_y = args[0][1]
                sigma_x = args[0][2]
                sigma_y = args[0][3]
        for i in range(im.shape[0]):
            im[i] = cv2.GaussianBlur(im[i], (width_x,width_y), sigma_x, sigmaY=sigma_y)
    else:
        for i in range(im.shape[0]):
            im[i] = cv2.GaussianBlur(im[i], (19,19), 6)

    return im

def gaussian3d(im, *args):
    """
    applies 3d gaussian convolution over the image as a separable 2d-1d convolution. should be able to handle 3d and 4d images, if the 4d image is indexed (z,c,x,y). 

    Parameters
    ----------
    im : np.array
        3d or 4d numpy array with indexing (z,x,y) or (z,c,x,y)
    gaussian : tuple (no keyword)
        specifies aspects of gaussian kernel. can handle 4 or 6 arguments. if 4 arguments, will be read as 
            first arg: width x and width y
            second arg : width z
            third : sigma x and y
            fourth : sigma z
        if 6 arguments, will be read as (widthx,y,z, sigma x,y,z)



    """
    #print("Applying 3D Gaussian filter...")
    width_x = width_y = 19
    width_z = 5
    sigma_x = sigma_y = 6
    sigma_z = 1
    if args:
        if len(args[0]) == 4:
            width_x = width_y = args[0][0]
            width_z = args[0][2]
            sigma_x = sigma_y = args[0][1]
            sigma_z = args[0][3]
        elif len(args[0]) == 6: 
            width_x = args[0][0]
            width_y = args[0][1]
            width_z = args[0][4]
            sigma_x = args[0][2]
            sigma_y = args[0][3]
            sigma_z = args[0][5]
    s = im.shape


    im = im.reshape(-1, im.shape[-2], im.shape[-1])
    im = gaussian2d(im, (width_x,width_y, sigma_x,sigma_y))
    im = im.reshape(s)
    #print('Starting 3D convolution')
    
    if len(s) == 3:
        im = convAxis(im, 0, cv2.getGaussianKernel(width_z,sigma_z))
    
    return im 


def medFilter2d(im,*size):
    """
    Median filter image, applied to all z's and channels

    Parameters
    ----------
    im : np.array
        3 or 4d numpy array for your image data
    size : int (optional)
        width of median filter window. default is 3
    """
    if size:
        size = size[0]
    else:
        size = 3
    if len(im.shape) == 3:
        for i in range(im.shape[0]):
            im[i] = cv2.medianBlur(im[i],size)
    elif len(im) == 4:
        for i in range(im.shape[0]):
            for j in range(im.shape[1]):
                im[i,j] = cv2.medianBlur(im[i,j],size)

    return im

def medFilter3d(im,*size):
    """
    Median filter image in 3d, applied to all z's. only handles 3d images at the moment, and runs pretty damn slow. 

    Parameters
    ----------
    im : np.array
        3 or 4d numpy array for your image data
    size : int (optional)
        width of median filter window. default is 3
    """
    if size:
        size = size[0]
    else:
        size = 3
    return ndimage.filters.median_filter(im, size = size)



def findpeaks2d(im):
    """
    finds peaks in 2d on each z step using np.roll and comparisons. currently only handles 3d implementations

    Parameters
    ----------
    im : np.array
        3d numpy array within which peaks will be found. 

    Outputs:
    --------
    peaks : np.array
        np.array containing the indices for where peaks were found
    """
    #print('Finding peaks...')
    centers_newway = np.array(np.where(\
              (np.roll(im,1, axis = 1) < im) \
            * (np.roll(im,-1, axis = 1) < im) \
            * (np.roll(im,1, axis = 2) < im) \
            * (np.roll(im,-1, axis = 2) < im) \
            * (im!=0))).T

    return centers_newway

def findpeaks3d(im):
    """ 
    find peaks in the 3d image and return as a list of tuples. handles 3d and 4d images. with 4d images, images need to be indexed (z,c,x,y)

    Parameters
    ----------
    im : np.array
        3d or 4d numpy array within which peaks will be found. 

    Outputs:
    --------
    peaks : np.array
        np.array containing the indices for where peaks were found
    """

    if len(im.shape) == 3:
        centers_newway = np.array(np.where(
              (np.roll(im,1, axis = 0) < im) \
            * (np.roll(im,-1, axis = 0) < im) \
            * (np.roll(im,1, axis = 1) < im) \
            * (np.roll(im,-1, axis = 1) < im) \
            * (np.roll(im,1, axis = 2) < im) \
            * (np.roll(im,-1, axis = 2) < im) \
            * (im!=0))).T

    elif len(im.shape)==4:
        for i in range(im.shape[1]):
            if i == 0:
                centers_newway = np.array(np.where(np.roll(np.roll(im[:,i],1, axis = 0) >im[:,i], -1, axis = 0) * np.roll(np.roll(im[:,i],-1, axis = 0) > im[:,i], 1, axis = 0) * np.roll(np.roll(im[:,i],1, axis = 1) > im[:,i], -1, axis = 1) * np.roll(np.roll(im[:,i],-1, axis = 1) > im[:,i], 1, axis = 1) * (im[:,i]!=0))).T
            else:
                #print(centers_newway.shape)
                #print(np.array(np.where(np.roll(np.roll(im[:,i],1, axis = 0) >im[:,i], -1, axis = 0) * np.roll(np.roll(im[:,i],-1, axis = 0) > im[:,i], 1, axis = 0) * np.roll(np.roll(im[:,i],1, axis = 1) > im[:,i], -1, axis = 1) * np.roll(np.roll(im[:,i],-1, axis = 1) > im[:,i], 1, axis = 1) * (im[:,i]!=0))).T.shape)
                centers_newway = np.concatenate((centers_newway, np.array(np.where(np.roll(np.roll(im[:,i],1, axis = 0) >im[:,i], -1, axis = 0) * np.roll(np.roll(im[:,i],-1, axis = 0) > im[:,i], 1, axis = 0) * np.roll(np.roll(im[:,i],1, axis = 1) > im[:,i], -1, axis = 1) * np.roll(np.roll(im[:,i],-1, axis = 1) > im[:,i], 1, axis = 1) * (im[:,i]!=0))).T ), axis = 0)

    return centers_newway

def findpeaks3d_26nn(data=None, verbose=False):
    """Improved local maximum detection for a 3D array

    Parameters
    ---------
    data : 3d ndarray
    verbose : bool
        Spam output that might help debugging

    Returns
    -------
    peaks : ndarray
        coordinates of the local maxima


    Find local maxima by comparison to the 26NN voxels (1-padded bounding cube)

    Using a maximum filter on a huge 3D chunk (say with 
    scipy.ndimage.maximum_filter()) is prohibitively slow. Therefore, this
    function uses a two step search. The legacy peakfinding function
    (findpeaks3d, which considers only 6NN) is used first for speed. Then,
    detected peaks are compared to all 26NN to find the proper local maxima.
    The speedup of this two-step approach relies on there being very few actual
    peaks in the 3D chunk (a safe assumption for C. elegans neurons).
    """
    peaks1 = findpeaks3d(data)

    def keep(ix, shape):
        """only keep peaks that are not on the box edge"""
        for lim, size in zip(ix, shape):
            if lim[0] < 0:
                return False
            if lim[2] > size-1:
                return False
        return True

    peaks2 = []
    for p in peaks1:
        req_ix = [[i-1, i, i+1] for i in p]
        if keep(req_ix, data.shape):
            ix = np.ix_(*req_ix)
            bbox = data[ix]*1
            pk_val = bbox[1,1,1]*1
            bbox[1,1,1]-=1
            if all(pk_val > bbox.ravel()):
                peaks2.append(p)
            else:
                if verbose:
                    print('-- false peak --')
                    print(bbox)
    if verbose:
        print('----------------')
        print('num real:', len(peaks2))
        print('num totl:', len(peaks1))
        print('----------------')
    return np.asarray(peaks2)

def template_filter(data, template, threshold=0.5):
    """template filter and threshold 

    parameters
    ----------
    data : (ndarray)
    template : (ndarray) same number of dimensions as data (i.e. 3D if data is 3D)
    threshold : (float) float in [-1, 1] 

    returns
    -------
    filtered: (ndarray) same shape as input data
    """
    # pad the template match result to match the original data shape
    res = feature.match_template(data, template)
    pad = [int((x-1)/2) for x in template.shape]
    res = np.pad(res, tuple(zip(pad, pad)))
    filtered = res*np.array(res>threshold)
    return filtered

def peak_filter_2(data=None, params=None):
    """peakfilter 2: template matching filter scheme"""
    # handle params
    if params is None:
        params = {}
    p = {'threshold':0.5, 'template':None}
    p.update(params)

    template = p.get('template', None)
    if template is None:
        raise Exception('template required')

    filtered = template_filter(data, template, p['threshold'])
    footprint = np.zeros((3,3,3))
    footprint[1,:,1] = 1
    footprint[1,1,:] = 1
    for i in range(3):
        filtered = morphology.erosion(filtered, selem=footprint)
    labeled_features, num_features = ndimage.label(filtered)
    centers = []
    for feature_index in range(num_features):
        center = ndimage.center_of_mass(filtered, labels=labeled_features, index=feature_index)
        centers.append(list(center))

    centers = np.array(centers)
    centers = np.rint(centers[~np.isnan(centers).any(axis=1)]).astype(int)
    intensities = filtered[tuple(centers.T)]
    # Highest peak first
    idx_maxsort = np.argsort(-intensities)
    centers = centers[idx_maxsort]

    centers = ensure_spacing(centers, spacing=9)
    return np.rint(centers).astype(int)

def get_bounded_chunks(data=None, peaks=None, pad=None):
    """Get bounding chunks around peaks

    Parameters
    ----------
    data : ndarray
        array to chunk
    peaks : ndarray
        peak coordinates for data
    pad : list/array
        defines bounding box around a peak by padding voxels to both sides

    Returns
    -------
    out : ndarray
        array of bounded chunks of data around peaks

    """
    # cull out peaks for which the bounding box goes beyond data bounds
    chunks = []
    for position in peaks:
        try:
            chunk = data[position[0] - pad[0]:position[0] + pad[0] + 1, position[1] - pad[1]:position[1] + pad[1] + 1, position[2] - pad[2]:position[2] + pad[2] + 1]
            # this is failing to fail for out-of-bounds chunks, assert is a quick fix
            assert chunk.shape == (pad[0]*2+1, pad[1]*2+1, pad[2]*2+1)
            chunks.append(chunk)
        except:
            pass
    return np.array(chunks)

def peak_local_max_anisotropic(image, anisotropy, min_distance, num_peaks, mask=None):
    """
    A gross hack to make skimage's peak_local_max work on anisotropic data

    Parameters
    ----------
    image : ndarray
    anisotropy : list or tuple of ints
    min_distance : int (minimium isotropic voxel distance for peak_local_max)
    num_peaks: int (num_peaks for peak_local_max)

    Returns
    -------
    peaks : ndarray
    mask: ndarray (returned so that it can be passed back for repeat calls to avoid recalculation)
    """
    if mask is None:
        expanded_shape = tuple([dim_len * ani for dim_len, ani in zip(image.shape, anisotropy)])
        mask = np.zeros(expanded_shape, dtype=np.uint16)
        mask[tuple([np.s_[::ani] for ani in anisotropy])] = 1
        expanded_image = np.copy(image)
        for dim in range(len(anisotropy)):
            expanded_image = np.repeat(expanded_image, anisotropy[dim], axis=dim)
        expanded_image*= mask
        peaks = feature.peak_local_max(expanded_image, min_distance=min_distance, num_peaks=num_peaks)
        peaks //= anisotropy
        return peaks, mask