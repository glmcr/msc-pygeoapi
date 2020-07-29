#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/geo/IGeo.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.geo.IGeo implementation
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

#---
class IGeo(object) :

  """
  Define constant parameters related to GIS processing for CHS-ENAV SFMT DHP data.
  """

  #---
  def __init__(self):

    self.WEST_HEMI_ID= ( str("W") ,)
    self.EAST_HEMI_ID= ( str("E") ,)
    self.SOUTH_HEMI_ID= ( str("S") ,)
    self.NORTH_HEMI_ID= ( str("N") ,)

    self.ALLOWED_HEMI_IDS= ( self.WEST_HEMI_ID[0],
                             self.EAST_HEMI_ID[0],
                             self.SOUTH_HEMI_ID[0],
                             self.NORTH_HEMI_ID[0] )

    self.ALLOWED_HORIZ_DATUMS= { str("EPSG") : [ str("4326") ] }

    self.DEFAULT_HORIZ_DATUM_REF= ( str("EPSG") ,)
    self.DEFAULT_HORIZ_DATUM_CODE= ( 4326 ,)

    self._horizDatumRef= ( self.DEFAULT_HORIZ_DATUM_REF[0] ,)
    self._horizDatumCode= ( self.DEFAULT_HORIZ_DATUM_CODE[0] ,)

    self.BOUNDING_BOX_ID= ( str("BOUNDING_BOX") ,)

    self.BBOX_SOUTH_WEST_CORNER= ( 0 ,)
    self.BBOX_NORTH_EAST_CORNER= ( 2 ,)

    self.BBOX_SOUTH_EAST_CORNER= ( 3 ,)
    self.BBOX_NORTH_WEST_CORNER= ( 1 ,)

    self.TWO_POINTS_BBOX_LAT_MIN= ( 0 ,)
    self.TWO_POINTS_BBOX_LON_MIN= ( 1 ,)
    self.TWO_POINTS_BBOX_LAT_MAX= ( 2 ,)
    self.TWO_POINTS_BBOX_LON_MAX= ( 3 ,)

    self.OGR_LAYERS_ID= ( str("LAYERS") ,)
    self.OGR_POLYGONS_ID= ( str("POLYGONS"),)

    self.OGR_TILE_POLYGON_ID= ( str("TILE_POLYGON"),)
