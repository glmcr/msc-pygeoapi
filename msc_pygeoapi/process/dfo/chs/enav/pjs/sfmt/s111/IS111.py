#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : DFO-CHS-ENAV-DHP
# File/Fichier    : dhp/sfmt/s111/IS111.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s111.IS111 implementation.
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
import sys
import math
import time

#---
from collections import namedtuple

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT

#---
class IS111(ISFMT) :

  """
  Class IS111 defines some constants(with unary tuples) which
  are to be used by all S-111 format flavors(Type3,Type2,...)
  It's something that is (loosely) comparable to an interface in Java.
  """

  OUT_FILES_PREFIX= ( str("111") ,)

  SPEED_METADATA_ID= ( str("surfaceCurrentSpeed") ,)
  DIR_METADATA_ID= ( str("surfaceCurrentDirection") ,)

  #---
  def __init__(self) :

    ISFMT.__init__(self)

    #---
    self.KNOTS_2_METERS_SECONDS= ( 1852.0/3600.0 ,)
    self.METERS_SECONDS_2_KNOTS= ( 1.0/self.KNOTS_2_METERS_SECONDS[0] ,)

    #: Doc Define the IHO S-111 spec. depthTypeIndex metadata values (see table 12.1 of the IHO S-111 spec. pdf doc version 1.0.1 2019)
    self.DEPTH_TYPE_INDEX= namedtuple( str("depthTypeIndex"), str("layerAverage seaSurface verticalDatum seaBottom")) ( 1, 2, 3, 4)

    #: Doc Using 2(Sea surface) as default for depthTypeIndex metadata.
    #      See official IHO document spec. "Surface Current Product Specification" version 1.0.0 May 2018 p.56
    #      https://www.iho.int/mtg_docs/com_wg/IHOTC/S-100_PS/S-111_Surface_Currents_Product_Specification_Documents
    self.DEFAULT_DEPTH_TYPE_INDEX= ( self.DEPTH_TYPE_INDEX.seaSurface ,)

    #: Doc Update the self.ROOT_GROUP_ATTRS_2SET dictionary already created in ISFMTMetaDataAttr and SFMTData super classes:
    self.ROOT_GROUP_ATTRS_2SET[ self.DEPTH_TYPE_INDX_ID[0] ]= { self.DTYP_ID[0] : self.HDF5_INT_TYPE_ID[0] }

    #: Doc Add surfaceCurrentDepth to already defined(in super class ISFMTMetaDataAttr) self.HDF5_AUTO_METADATA_ROOT list.
    self.AUTO_METADATA_ROOT.append( str("surfaceCurrentDepth") )

    #: Doc Define self.METH_TYPE_PRODUCT_ID and self.TYPEOF_PRODUCT_DATA_ID
    #      metadata strings ids. according to the official IHO S111 spec.
    self.METH_TYPE_PRODUCT_ID= ( str("methodCurrentsProduct") ,)
    self.TYPEOF_PRODUCT_DATA_ID= ( str("typeOfCurrentData") ,)

    #--- NOTE: self.PRODUCT_FEATURE_IDS[ISFMT.PRODUCTS_IDS.S111.name] is a reference to a tuple
    self.HDF5_AUTO_METADATA_GROUP_F= [ self.PRODUCT_FEATURE_IDS[ISFMT.PRODUCTS_IDS.S111.name][0], str("featureName") ]

    #: Doc set currents specific keys to generic dictionary self.HDF5_SET_METADATA_PRODUCT to None for now.
    #      These will be dynamically set in the S111.__init_() method.
    self.HDF5_SET_METADATA_PRODUCT[ self.METH_TYPE_PRODUCT_ID[0] ]= None
    self.HDF5_SET_METADATA_PRODUCT[ self.TYPEOF_PRODUCT_DATA_ID[0] ]= None

    #: Doc Add currents specific fields in self.HDF5_AUTO_METADATA_PRODUCT generic metadata dictionary.
    #  NOTE: self.TYPEOF_PRODUCT_DATA_ID[0] and self.METH_TYPE_PRODUCT_ID[0] keys are also used in this dictionary
    #  even if it is also used in self.HDF5_SET_METADATA_PRODUCT. This redundancy is necessary because the IHO
    #  SFMT (in fact the S111 spec. only as of 20190925) official specs. require using those parameter in two places(two
    #  different HDF5 GROUPs) in the product files metadata.
    self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ].append(str("speedUncertainty"))
    self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ].append(str("directionUncertainty"))
    self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ].append(self.METH_TYPE_PRODUCT_ID[0])
    self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ].append(self.TYPEOF_PRODUCT_DATA_ID[0])

    #: Doc Set the metadata name(i.e. SurfaceCurrent here) of the product in the generic self.HDF5_AUTO_METADATA_PRODUCT dictionary.
    self.HDF5_AUTO_METADATA_PRODUCT[ self.NAME_ID[0] ]= self.PRODUCT_FEATURE_IDS[ ISFMT.PRODUCTS_IDS.S111.name ][0]
