#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : DFO-CHS-ENAV-DHP
# File/Fichier    : dhp/sfmt/s102/S102TilesFactory.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - class dhp.sfmt.s102.S102TilesFactory implementation.
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
import inspect

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.IS102 import IS102
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.S102DataAttr import S102DataAttr

#---
class S102TilesFactory(S102DataAttr) :

  """
  Utility class inherited by S102Factory for modularization.
  (i.e. to avoid, as much as possible, having methods using methods
  from the same class or source file.)
  """

  #---
  def __init__(self) :

    S102DataAttr.__init__(self)

  #---
  def addPointDataInTileDict(self, PointDataDict, DataSetId, TileDict, BaseLevelTileId) :

    """
    Store a model grid point data dictionary in a tile dicionary.

    PointDataDict (type->dictionary) : A model grid point data dictionary.

    DataSetId (type->string): The model dataset id. from which the PointDataDict comes from.

    TileDict (type->dictionary): The tile dictionary where to store the grid point data dictionary.

    BaseLevelTileId (type->string): The id. of the base level tile which encloses the tile
    or the id of the tile itself (used for ERROR message(s) only).

    return (type->dictionary): TileDict with the PointDataDict added as a new item.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    ##--- Uncomment for debugging
    #if TileDict is None :
    #  sys.exit("INFO "+methID+" TileDict is None !\n")

    ##--- Uncomment for debugging
    #if PointDataDict is None :
    #  sys.exit("INFO "+methID+" PointDataDict is None !\n")

    #: Doc First, check if the dataset Id. is already defined in TileDict:
    if self.MODEL_NAME_ID[0] not in TileDict.keys() :

      #: Doc Add the  dataset Id. in the tile dictionary
      TileDict[ self.MODEL_NAME_ID[0] ]= DataSetId

    #: Doc if the already defined dataset id. in the dictionary is
    #      the same as DataSetId argument, if not then it is an ERROR:
    #      NOTE: A tile cannot have data coming from different datasets.
    elif TileDict[ self.MODEL_NAME_ID[0] ] != DataSetId :

      sys.exit("ERROR "+methID+" Attempt to use another dataset -> "+
                DataSetId+" for base level tile -> "+BaseLevelTileId+
                " is already using dataset -> "+ TileDict[ self.MODEL_NAME_ID[0] ]+" !\n")

    #--- End if-elif block

    #: Doc Create the data points in TileDict if not already created:
    if self.POINTS_DATAIN_ID[0] not in TileDict.keys() :

      TileDict[ self.POINTS_DATAIN_ID[0] ]= {}
    #--- End if block.

    #: Doc Add the PointDataDict in the base level tile sub-dictionary
    #      indexed by self.POINTS_DATAIN_ID[0] string:
    TileDict[ self.POINTS_DATAIN_ID[0] ].update( PointDataDict )

    #: Doc Return the tile dictionary to the calling method.
    return TileDict

  #---
  def checkForNorthWestHemi(self, ALatInDecimalDegrees, ALonInDecimalDegrees, WarningsLog= False) :

    """
    Check if a longitude, latitude(in decimal degrees only) combo is indeed located in the North-West hemisphere.

    ALatInDecimalDegrees (type->float): A North hemisphere latitude(normally between 0.1 and 89.9) in decimal degrees.

    ALonInDecimalDegrees (type->float): A West hemisphere longitude(normally between -179.9 and -0.1) in decimal degrees.

    WarningsLog (type->boolean) <OPTIONAL> Default->False: To put(or not) log WARNING messages on the stderr stream.

    return (type->boolean)
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    ret= True

    if ALonInDecimalDegrees < self.WEST_HEMI_LON_MIN[0] or ALonInDecimalDegrees > self.WEST_HEMI_LON_MAX[0] :

      if WarningsLog :
        sys.stderr.write("WARNING "+methId+
                         " Invalid Western hemisphere longitude: " + str(ALonInDecimalDegrees) + " !\n")
      #--- end inner if block.

      ret= False
    #--- end outer if block

    if ALatInDecimalDegrees < self.NORTH_HEMI_LAT_MIN[0] or ALatInDecimalDegrees > self.NORTH_HEMI_LAT_MAX[0] :

      if WarningsLog :
        sys.stderr.write("WARNING "+methId+
                         " Invalid Northern hemisphere latitude: " + str(ALatInDecimalDegrees) + " !\n")
      #--- end inner if block

      ret= False
    #--- end outer if block

    return ret

  #---
  @staticmethod
  def getTileOutFileName(OutFilePrefix, TileId, OutFileExt) :

    """
    Static utility method to build the name of a tiled SFMT DHP data file name according to the official CHS-SHC spec.

    OutFilePrefix (type->string): The prefix(string) of the official tiled SFMT DHP data file name.

    TileId (type->string): The string id. of the tile holding the data to write.

    OutFileExt (type->string): The file extension(string) of the official tiled SFMT DHP data file name.

    return (type->string) : The SFMT DHP data file name with the right format according
    to the official spec. of the IHO.
    """

    #--- Note: No args. validation here for performance reasons:

    #: Doc Get rid of the underscores(if any) in the tiles ids.
    tileIdSplit= TileId.split( IS102.TILES_NAMES_SPLITSTR[0] )

    if len(tileIdSplit) > 1 :

      #: Doc Assuming that the split produced only two items here:
      oFileNameTileId= tileIdSplit[0] + tileIdSplit[1]

    else :
      oFileNameTileId= TileId

    #--- end if-else block.

    #: Doc Need to check if the S102 tile string name id. respects the SFMT DHP naming convention.
    lenCheck= len(ISFMT.PRODUCTS_CHS_TAG[0])

    if oFileNameTileId[0:lenCheck] != ISFMT.PRODUCTS_CHS_TAG[0] :

      #: Doc SFMT DHP naming convention not respected, modify tileId string with the right format:
      oFileNameTileId= ISFMT.PRODUCTS_CHS_TAG[0] + oFileNameTileId[lenCheck-2:]

    #: Doc Append the file extension to the returned string:
    #      NOTE: Use of str() to be sure to return a basic ASCII string
    #           just in case we have some UNICODE strings as arguments.
    return str(OutFilePrefix + oFileNameTileId  + OutFileExt)

  #---
  def insideBoundingBox(self, ALatInDecimalDegrees, ALonInDecimalDegrees, TileBBoxDict) :

    """
    Check if a georeferenced lat-lon point is inside a S102 tile bounding box.

    ALatInDecimalDegrees (type->float): A North hemisphere latitude(normally between 0.1 and 89.9) in decimal degrees.

    ALonInDecimalDegrees (type->float): A West hemisphere longitude(normally between -179.9 and -0.1) in decimal degrees.

    TileBBoxDict (type->dictionary): S102 tile bounding box dictionary.

    return (type->boolean) inside->True, outside->False.
    """

    #--- NOTE: No fool-proof checks for performance reasons.

    #: Doc South-West corner of the the tile Bounding box:
    swcPoint= TileBBoxDict[ self.BBOX_SOUTH_WEST_CORNER[0] ]

    tileLatMin= swcPoint[ self.TILES_LAT_IDX[0] ]
    tileLonMin= swcPoint[ self.TILES_LON_IDX[0] ]

    #: Doc North-East corner of the the tile Bounding box:
    necPoint= TileBBoxDict[ self.BBOX_NORTH_EAST_CORNER[0] ]

    tileLatMax= necPoint[ self.TILES_LAT_IDX[0] ]
    tileLonMax= necPoint[ self.TILES_LON_IDX[0] ]

    #: Doc Note the >= operator
    return ALatInDecimalDegrees >= tileLatMin and ALatInDecimalDegrees <= tileLatMax \
             and ALonInDecimalDegrees >= tileLonMin and ALonInDecimalDegrees <= tileLonMax
  #--- 
  def outsideGlobalLimits(self, ALatInDecimalDegrees, ALonInDecimalDegrees) :

    """
    Check(and return the result as a boolean) if data point lat-lon
    coordinates (in decimal degrees only) combo is inside the S102 (all) tiles ensemble global limits.

    ALatInDecimalDegrees (type->float): A North hemisphere latitude(normally between 0.1 and 89.9) in decimal degrees.
    
    ALonInDecimalDegrees (type->float): A West hemisphere longitude(normally between -179.9 and -0.1) in decimal degrees.
    
    return (type->boolean): inside->True, outside->False.
    """

    return ALatInDecimalDegrees < self.TILES_LAT_MIN or ALatInDecimalDegrees > self.TILES_LAT_MAX \
             or ALonInDecimalDegrees < self.TILES_LON_MIN or ALonInDecimalDegrees > self.TILES_LON_MAX

#  #--- Keep for possible future usage
#  @staticmethod
#  def getValid1DLLIndices(LLDataLen, LLData, LowerLLLimit, UpperLLLimit) :
#
#    valid1DIndices= []
#    
#    #---
#    for llIter in tuple( range(0, LLDataLen) ):
#
#      if LLData[llIter] >= LowerLLLimit and LLData[llIter] <= UpperLLLimit :
#
#        valid1DIndices.append(llIter)
#
#    return tuple(valid1DIndices)  
