#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/webtide/IGeoJSON.py
# Creation        : September/Septembre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.webtide.IGeoJSON implementation. It is
#                used like a Java interface.
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

#---
import os
import sys

#---
from msc_pygeoapi.process.dfo.pjs.geo.IGeo import IGeo
from msc_pygeoapi.process.dfo.pjs.tidal.ITidalPrd import ITidalPrd
from msc_pygeoapi.process.dfo.pjs.util.Trigonometry import Trigonometry
from msc_pygeoapi.process.dfo.pjs.tidal.webtide.IWebTide import IWebTide
from msc_pygeoapi.process.dfo.pjs.util.IDataIndexing import IDataIndexing

#---
class IGeoJSON(IGeo, IWebTide, Trigonometry) :

  """
  Defines some specific GeoJSON constant parameters (using
  unary tuples) related to the WebTide input data of that format.
  """

  POINT_ID= ( str("ID") ,)

  def __init__(self) :

    IGeo.__init__(self)
    IWebTide.__init__(self)
    Trigonometry.__init__(self)

    #---
    self.POINTS_ID= ( str("features"), )

    self.POINT_COORDS_ID= ( str("coordinates") ,)

    self.PROPS_ID= ( str("properties") ,)

    self.CRS_ID= ( str("crs") ,)
    self.CRS_NAME_ID= ( str("name") ,)

    """
    For CRS compatibilty validation between WebTide data and S102 tiles bounding boxes.
    NOTE: self.DEFAULT_HORIZ_DATUM_CODE is an unary tuple.
    """
    self.ALLOWED_CRS= { self.DEFAULT_HORIZ_DATUM_CODE[0] : ( str("urn:ogc:def:crs:OGC:1.3:CRS84") ,) }

    """
    self.BATHYMETRY_FIELD_ID: string key id. of WebTide bathymetry data in GeoJSON format.
    """
    self.POINT_BATHY_FIELD_ID= ( str("Bathy") ,)

    self.FIELDS_IDS_SEP= ( str(".") ,)
    self.FIELDS_IDS_LLEN= ( 3 ,)

    self.CONST_NAME_IDX= ( 0 ,)
    self.FIELDS_IDS_IDX=  ( 1 ,)
    self.TIDAL_COMP_IDX= ( 2 ,)

    """
    self.WLZ_AMP_STRID: Used by getAdHocChartDatumCorrection method.
    """
    self.WLZ_AMP_STR_ID= ( IDataIndexing.UVZ_IDS.Z.name +
                           self.FIELDS_IDS_SEP[0] + self.TIDAL_COMP_IDS[ ITidalPrd.AMPLITUDE_ID[0] ] ,)

