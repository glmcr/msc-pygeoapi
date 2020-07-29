#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/s102/IS102.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s102.IS102 implementation.
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

#--- Bulitin module(s).
import sys

#---
from msc_pygeoapi.process.dfo.pjs.geo.IGeo import IGeo
from msc_pygeoapi.process.dfo.pjs.util.IDataIndexing import IDataIndexing

#---
class IS102(IDataIndexing, IGeo) :

  """
  Class IS102 defines some constants parameters for its derived
  S102* classes. It's something comparable to the use of an interface
  in Java.
  """

  #--- Define the constants parameters that can be used outside
  #    IS102 derived classes instances.

  #: Doc Define a string id. for tiles dictionaries indexing.
  LEVEL_ID= ( str("ThisLevel") ,)

  #: Doc Define tiles allowed levels strings ids.
  TILES_LEVEL2_ID= ( str("L2") ,)
  TILES_LEVEL5_ID= ( str("L5") ,)
  TILES_LEVEL6_ID= ( str("L6") ,)

  PRODUCT_LEVEL_ID= ( str("S102LevelOut") ,)
  EXCLUDE_POINTS_ID= ( str("ExcludePointsIn") ,)

  #: Doc Define the default coarse resolution tile level for data other than S104 1D DH products at tide gages WL stations
  DEFAULT_TILES_BASE_LEVEL= ( TILES_LEVEL2_ID[0] ,)

  #: Doc Define the allowed levels in a tuple.
  TILES_ALLOWED_LEVELS= ( TILES_LEVEL2_ID[0], TILES_LEVEL5_ID[0], TILES_LEVEL6_ID[0] )

  #: Doc Only the ESRI_SHAPEFILE format allowed for now for tiles bounding boxes limits.
  TILES_BBOX_ALLOWED_FORMATS= ( str("ESRI_SHAPEFILE") ,)

  #: Doc Define the character which separates
  #      the S102 tiles names strings ids. prefixes
  #      (CA2, CA5, CA6) from the rest of the names.
  TILES_NAMES_SPLITSTR= ( str("_") ,)

  #--- Define the allowed file format for tiles bathymetry:
  #    No need to use bathymetry for now(2018-11-21)
  #TILES_BATHY_ALLOWED_FORMATS= ( "BAG" ,)

  #---
  def __init__(self) :

    IGeo.__init__(self)
    IDataIndexing.__init__(self)

    #: Doc Define some more S102 constant parameters but inside class this time.

    #--- Increments in degrees for a bathymetry cell for
    #    the 3 levels allowed(not used for now):
    #    NOTE: These parameters could be extracted directly
    #          from the BAG format files if we have to use
    #          them.
    #self.LEVEL2_LAT_DEGREES_INCR= ( 1.0 ,)
    #self.LEVEL5_LAT_DEGREES_INCR= ( 0.1 ,)
    #self.LEVEL6_LAT_DEGREES_INCR= ( 0.02 ,)

    #: Doc Define the normal lat,lon degrees extent for the base levet tiles.
    self._BASELEV_NORM_LLDEGREES_EXTENT= ( 1 ,)

    #: Doc Define integer indices for indexing the latitudes ranges corners data.
    self.LATITUDES_RANGE_SWC_IDX= ( 0 ,) #: Doc Latitudes ranges South-West corner for the range South limit.
    self.LATITUDES_RANGE_NWC_IDX= ( 1 ,) #: Doc Latitudes ranges North-west corner for the range North limit.

    #: Doc Define string id. for indexing latitudes ranges data.
    self.LATITUDES_RANGES_ID= ( str("LATS_RANGES") ,)

    #: Doc The feature string id. of the tile name id. in the ESRI_SHAPEFILE file. 
    self.TILE_NAME_FILE_ID= ( str("INFORM") ,)

    #: Doc The dictionary string id. key of the enclosed
    #      next level of tiles in a coarser level tile.
    #      (example: This NEXT id. key is indexing the
    #      sub-dictionary which contains the level 6
    #      tiles enclosed in a level 5 tile).
    self.TILES_NEXT_LEVEL_ID= ( str("NEXT") ,)
 
    #: Doc The dictionary string id. of the sub-dictionary 
    #      which contains the tiles of the level being processed.
    self.THIS_LEVEL_TILES_ID= ( str("THIS_LEVEL_TILES") ,)

    self.WEST_HEMI_SWCELL_LON= ( -180.0 ,)
    self.WEST_HEMI_NECELL_LON= (   -1.0 ,)

    self.WEST_HEMI_SWCELL_LAT= (  0.0 ,)
    self.WEST_HEMI_NECELL_LAT= ( 89.0 ,)

    self.BLTILE_LATAXIS_EXT_ID= ( str("LAT_DEGREES_EXTENT") ,)
    self.BLTILE_LONAXIS_EXT_ID= ( str("LON_DEGREES_EXTENT") ,)

    self.BLTILE_LATSIDX_RGE_ID= ( str("LATS_IDX_RGE") ,)
    self.BLTILE_LONSIDX_RGE_ID= ( str("LONS_IDX_RGE") ,)

    #: Doc Cannot have a base level tile with a longitude axis having more than 4 degrees 
    self.BLTILE_LONAXIS_MAXLEN= ( 4 ,)

    #: Doc Cannot have a base level tile with a latitude axis having more than 2 degrees.
    self.BLTILE_LATAXIS_MAXLEN= ( 2 ,)

    self.TILES_INDEXING= ( str("TILES_IDX") ,)

    #: Doc Define longitudes extremums for coordinates validations in the western hemisphere.
    self.WEST_HEMI_LON_MIN= ( -179.9 ,)
    self.WEST_HEMI_LON_MAX= ( -0.1 ,)

    #: Doc Define latitudes extremums for coordinates validations in the northern hemisphere.
    self.NORTH_HEMI_LAT_MIN= ( 0.1 ,)
    self.NORTH_HEMI_LAT_MAX= ( 89.9 ,)

    #: Doc Define tiles lon-lat min-max with opposite WEST_HEMI values
    #      They will be overriden by the S102Tiles object __init__ method
    #      then we cannot use unary tuples here:
    self.TILES_LON_MIN= self.WEST_HEMI_LON_MAX[0]
    self.TILES_LON_MAX= self.WEST_HEMI_LON_MIN[0]

    self.TILES_LAT_MIN= self.NORTH_HEMI_LAT_MAX[0]
    self.TILES_LAT_MAX= self.NORTH_HEMI_LAT_MIN[0]

    #: Doc Define integer indices for dictionary indexing.
    self.TILES_LAT_IDX= ( 1 ,)
    self.TILES_LON_IDX= ( 0 ,)

    #: Doc Define the already validated SHP files layers names for the allowed levels.
    self.LEVELS_LAYER_NAMES_ALLOWED= ( str("cell_niv_2_canada_05-06-2017_cvrage_Polygon") ,
                                       str("cell_niv_5_canada_29-06-2017_cvrage_Polygon") ,
                                       str("cell_niv_6_canada_05-07-2017_cvrage_Polygon") )
  #---
