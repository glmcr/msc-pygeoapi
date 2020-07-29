#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : DFO-CHS-ENAV-DHP
# File/Fichier    : dhp/sfmt/s104/IS104.py
# Creation        : Septembre/September 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s104.IS104 class implementation.
#
# Remarks :
#
# License      :
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation,
#    version 2.1 of the License.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the
#    Free Software Foundation, Inc., 59 Temple Place - Suite 330,
#    Boston, MA 02111-1307, USA.
#
#==============================================================================

#--- Do not allow relative imports.
from __future__ import absolute_import

#--- Built-in module(s).
import os
import sys
import time

#--- 3rd party h5py package.
import h5py

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.util.IDataIndexing import IDataIndexing

#---
class IS104(ISFMT) :

  """
  Class IS104 defines some constants parameters(using unary tuples)
  which are to be used by all S104 format flavors(Type3,Type2,...)
  It's something that is (loosely) comparable to an interface in Java.
  """

  OUT_FILES_PREFIX= ( str("104") ,)

  ELEV_METADATA_ID= ( str("waterLevelElevation"),)
  TREND_METADATA_ID= ( str("waterLevelTrend") ,)

  CHART_DATUM_CONV_ID= ( str("CHART_DATUM_CONV") ,)

  #--- STEADY trend if WL absolute value is les than WL_TREND_THRESHOLD
  WL_TREND_THRESHOLD= ( 0.2, )

  #--- Do not compute water levels trenda when we have data with
  #    time intervalls being >  900 seconds(15mins).
  WL_TREND_TIMEINCR_MAX= ( 900 ,)

  #--- Do not care about data grid point for which
  #    the depth(relative to its own MSL average value)
  #    is more than WL_DEPTH_THRESHOLD
  WL_DEPTH_THRESHOLD= ( 60.0 ,)

  #---
  def __init__(self) :

    ISFMT.__init__(self)

    #---
    self.GRIDDED_DATA_SUFFIX= ( str("-2D") ,)

    self.WL_TREND_STEADY=     ( 0 ,)
    self.WL_TREND_DECREASING= ( 1 ,)
    self.WL_TREND_INCREASING= ( 2 ,)
    self.WL_TREND_UNKNOWN=    ( 3 ,)

    #: Doc DHP official lowerLowWaterLargeTide (a.k.a. chart datum) integer code of the IHO S104 official spec.
    self.VERT_DATUM= ( self.LLWLT_VERT_DATUM[0], )

    #: Doc Shortcut to the Z water level elevation dictionary string id.
    self.WLZELEV_VALUEID= ( IDataIndexing.UVZ_IDS.Z.name ,)

    #--- Default value of the WL data arrays
    #    buffer at both ends for the WL trends
    #    computations.
    self.WLDATA_ARRAYS_BUFFER= ( 2 ,)

    #: Doc Get the h5py.special_dtype for the timestamp ATTRIBUTE.
    self.TMSTAMP_GRPSTR_DTYPE= ( h5py.special_dtype( vlen= self.H5PY_STRING_SPECIAL_DTYPE[0] ) ,)

    #: Doc Define self.METH_TYPE_PRODUCT_ID and self.TYPEOF_PRODUCT_DATA_ID
    #      metadata strings ids. according to the S104 spec(In fact it is
    #      the S111 spec. since the S104 spec is still lagging as of 20190926).
    self.TYPEOF_PRODUCT_DATA_ID= ( str("typeOfWaterLevelData") ,)
    self.METH_TYPE_PRODUCT_ID= ( str("methodWaterLevelsProduct") ,)

    #: Doc Static Water levels elevation and trend HDF5 compound type definition for
    #      data coding format 3. NOTE: Cannot use a tuple here, h5py really needs a list.
    self.ELEVTREND_TYPEDEF= [ ( str( IS104.ELEV_METADATA_ID[0] ), h5py.h5t.NATIVE_FLOAT),
                              ( str( IS104.TREND_METADATA_ID[0] ), h5py.h5t.NATIVE_INT32) ]

    #--- TODO: use a local shortcut tuple for
    #          self.PRODUCT_FEATURE_IDS[ISFMT.PRODUCTS_IDS.S104.name][0] ??

    #--- NOTE: self.PRODUCT_FEATURE_IDS[ISFMT.PRODUCTS_IDS.S104.name] is a reference to a tuple.
    self.HDF5_AUTO_METADATA_GROUP_F= [ self.PRODUCT_FEATURE_IDS[ISFMT.PRODUCTS_IDS.S104.name][0], str("featureName") ]

    #: Doc Set water levels specific keys to generic dictionary self.HDF5_SET_METADATA_PRODUCT to None for now.
    #      These will be dynamically set in the S104.__init_() method.
    self.HDF5_SET_METADATA_PRODUCT[ self.METH_TYPE_PRODUCT_ID[0] ]= None
    self.HDF5_SET_METADATA_PRODUCT[ self.TYPEOF_PRODUCT_DATA_ID[0] ]= None

    #: Doc Add currents specific fields in self.HDF5_AUTO_METADATA_PRODUCT generic metadata dictionary.
    #  NOTE: self.METH_TYPE_PRODUCT_ID[0] and self.TYPEOF_PRODUCT_DATA_ID[0] keys are also used in this dictionary
    #  even if it is also used in self.HDF5_SET_METADATA_PRODUCT. This redundancy is necessary because the SFMT
    #  DHP (in fact the S111 IHO spec. only as of 20190925) spec require using those parameter in two places(two
    #  different HDF5 GROUPs) in the product files metadata.
    self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ].append(self.METH_TYPE_PRODUCT_ID[0])
    self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ].append(self.TYPEOF_PRODUCT_DATA_ID[0])

    #--- NOTE: self.PRODUCT_FEATURE_IDS[ ISFMT.PRODUCTS_IDS.S104.name ] is an unary tuple.
    self.HDF5_AUTO_METADATA_PRODUCT[ self.NAME_ID[0] ]= self.PRODUCT_FEATURE_IDS[ ISFMT.PRODUCTS_IDS.S104.name ][0]
