#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/geo/IGeoLandWaterMasks.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.geo.IGeoLandWaterMasks implementation.
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
from enum import Enum #--- enum not available for python versions <= 2.7.6

#---
from msc_pygeoapi.process.dfo.pjs.geo.IGeo import IGeo

#---
class IGeoLandWaterMasks(IGeo) :

  """
  Defines some constant parameters related to the usage of
  geo-referenced land-water masks for the CHS-ENAV SFMT DHP data.
  """

  #---
  def __init__(self):

    IGeo.__init__(self)

    self.OGR_ALLOWED_GEOMETRIES_NAMES= ( str("POLYGON") ,)
    self.ALLOWED_FORMATS= Enum( str("ALLOWED_FORMATS"), [ str("ESRI_SHAPEFILE") ])
