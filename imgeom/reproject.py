# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import (absolute_import, unicode_literals, division,
                        print_function)

from astropy import wcs as fitswcs
from gwcs import wcs
import numpy as np

def reproject(wcs1, wcs2):
    """
    Given two WCSs return a function which takes
    coordinates in the first WCS and computes them in the second one.

    It performs the forward transformation of wcs1 followed by the
    inverse of wcs2.

    Parameters
    ----------
    wcs1, wcs2 : astropy.wcs.WCS or gwcs.wcs.WCS
        WCS objects

    Returns
    -------
    _reproject : func
        Function to compute the transformations.
        It takes x, y positions in wcs1 and returns x,y positions in wcs2.

    """
    args = []
    if isinstance(wcs1, fitswcs.WCS):
        forward = wcs1.all_pix2world
        args = [1]
    elif isinstance(wcs2, wcs.WCS):
        forward = wcs1.forward_transform
    else:
        raise ValueError("Expected astropy.wcs.WCS or gwcs.WCS object.")

    if isinstance(wcs2, fitswcs.WCS):
        args = [1]
        inverse = wcs2.wcs_world2pix
    elif isinstance(wcs2, wcs.WCS):
        inverse = wcs2.forward_transform.inverse
    else:
        raise ValueError("Expected astropy.wcs.WCS or gwcs.WCS object.")

    def _reproject(x, y):
        forward_args = [x, y] + args
        sky = forward(*forward_args)
        inverse_args = sky + args
        return inverse(*inverse_args)
    return _reproject