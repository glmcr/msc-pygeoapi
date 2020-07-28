#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidaprd/webtide/IWebTide.py
# Creation        : August/Aout 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidaprd.webtide.IWebTide implementation.
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
import enum
import inspect

#---
#from dhp.sfmt.s102.IS102 import IS102
#from msc_pygeoapi.process.dfo.util.ITimeMachine import ITimeMachine
from msc_pygeoapi.process.dfo.tidal.astro.foreman.IForeman import IForeman

#---
class IWebTide(IForeman, ITimeMachine) :

  """
  Defines some constants parameters for all WebTide* sub-classes bundle.
  """

  #--- Enum for Allowed WebTide input formats(only GEOJSON for now):
  __ALLOWED_DATASETS_FORMATS= enum.Enum( str("ALLOWED_DATASETS_FORMATS"), [ str("GEOJSON") ])

  #---
  def __init__(self) :

    ITimeMachine.__init__(self)
    IForeman.__init__(self)

    #--- Defines some parameters related
    #    to the JSON formatted WebTide
    #    input data files. These are the strings
    #    keys ids. that serve to index parameters
    #    in the JSON formatted input data dictionaries.
    #    (See file DataSetsForS111.json located in
    #     <main directory>cfg/WebTide/JSON directory
    #    for example)

    self.JSON_DATASETS_ID= ( str("DataSets") ,)
    self.JSON_DATASETS_DIR_ID= ( str("DataSetsDir") ,)

    self.JSON_DATASET_FORMAT_ID= ( str("Format") ,)
    self.JSON_DATASET_FILE_ID= ( str("File") ,)
    self.JSON_DATASET_ROTATION_ID= ( str("Rotation") ,)

    self.JSON_DATASET_LANDWATER_DIR_ID= ( str("CanCoastalLandDataDir") ,)
    self.JSON_DATASET_LANDWATER_FILE_ID= ( str("CanCoastLinesLandShpFiles") ,)

    #--- Some dicionaries keys used for both JSON formatted
    #    data indexing and S102 tiles dictionaries indexing.
    self.JSON_ROT_COSSIN_ID= ( str("CosSin") ,)
    self.JSON_ROT_DIRECTION_ID= ( str("Direction") ,)

    #self.ROT_DIRECTIONS_ALLOWED= ( str("CounterClockwise") ,)

    #--- keys ids. for tidal constituents amplitudes and phases:
    self.TIDAL_COMP_IDS= { self.AMPLITUDE_ID[0] : str("Am"), self.PHASE_ID[0] : str("Ph") }

    #--- Latitudes and longitudes string ids. used in Webtide GeoJson format input files.
    self.GEOJSON_POINT_LAT_ID= ( str("lat") ,)
    self.GEOJSON_POINT_LON_ID= ( str("lon") ,)

    #--- Not used for now
    #self.BASE_LEVEL_TILES_TIME_INTERVALL= ( self.SECONDS_PER_HOUR[0] ,)
    #self.NEXT_LEVEL_TILES_TIME_INTERVALL= ( self.SECONDS_PER_15_MINS[0] ,)

    #--- self.MAX_NB_DATASETS_PER_TILE Not used for now:
    #self.MAX_NB_DATASETS_PER_TILE= ( len(IS102.TILES_ALLOWED_LEVELS) ,)
    #self.ROT_DIRECTIONS_ALLOWED= ( str("CounterClockwise") ,)
