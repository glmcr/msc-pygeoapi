# =================================================================
#
# Author: Gilles Mercier
#         <gilles.mercier@dfo-mpo.gc.ca> <gilles.mercier2@canada.ca>
#
# Copyright (c) 2020 Gilles Mercier
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

# import os
import logging
from collections import namedtuple

LOGGER = logging.getLogger(__name__)

def bbox_check(llbbox: namedtuple):

    """
    Validate a regular EPSG:4236 lat-lon bounding box.
    SW corner latitude MUST be smaller than NE corner latitude.
    SW corner longitude MUST be smaller than NE corner longitude.

    :param namedtuple: Contains the regular EPSG:4236 lat-lon
                       bounding box attributes.
    """


    if llbbox.swc_lat < 0:
       msg = 'llbbox.swc_lat={}'.format(llbbox.swc_lat)+' < 0'
       LOGGER.error(msg)
       raise ValueError(msg)


    if llbbox.nec_lat < 0:
        msg = 'llbbox.nec_lat={}'.format(llbbox.nec_lat)+' < 0'
        LOGGER.error(msg)
        raise ValueError(msg)


    if llbbox.swc_lon > 0:
        msg = 'llbbox.swc_lon={}'.format(llbbox.swc_lon)+' > 0'
        LOGGER.error(msg)
        raise ValueError(msg)


    if llbbox.nec_lon > 0:
        msg = 'llbbox.nec_lon={}'.format(llbbox.nec_lon)+' > 0'
        LOGGER.error(msg)
        raise ValueError(msg)


    if llbbox.swc_lat > llbbox.nec_lat:
        msg = 'llbbox.swc_lat={}'.format(llbbox.swc_lat)+\
              ' > llbbox.nec_lat={}'.format(llbbox.nec_lat)
        LOGGER.error(msg)
        raise ValueError(msg)


    if llbbox.swc_lon > llbbox.nec_lon:
        msg = 'llbbox.swc_lon={}'.format(llbbox.swc_lon)+\
              ' > llbbox.nec_lon={}'.format(llbbox.nec_lon)
        LOGGER.error(msg)
        raise ValueError(msg)

