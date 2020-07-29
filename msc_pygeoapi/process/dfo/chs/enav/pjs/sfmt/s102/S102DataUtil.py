#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/s102/S102DataUtil.py
# Creation        : July/Juillet 2020 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s102.S102DataUtil implementation.
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
import inspect

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.IS102 import IS102
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTModelFactory import SFMTModelFactory

#---
class S102DataUtil(IS102) :

  """
  Provide utility @staticmethods
  """

  #---
  def __init__( self ) :

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    sys.stdout.write("INFO "+methId+" start\n")

    IS102.__init__(self)

    sys.stdout.write("INFO "+methId+" end\n")

  #---
  @staticmethod
  def setPointDataRefInTiles( ModelDataId: str,
                              PointLatF: float,
                              PointLonF: float,
                              TilePointDataDict: dict,
                              ModelDataObj: SFMTModelFactory,
                              WarningsLog: bool = False) -> tuple :
    """
    Generic @staticmethod used to set a reference to a
    model data point dictionary in the S102 tiles bounding
    boxes bundle at the desired level.

    ModelDataId (type->string): The string id. of the
    model(WebTide, NEMO, H2D2) from which the ModelDataObj
    was created.

    PointLatF (type->float): The latitude of the model
    data point in floating point format.

    PointLonF (type->float): The longitude of the model
    data point in floating point format.

    TilePointDataDict (type->dict): The model data grid
    point dictionary that we want to set the reference
    to in the tiles bundle at the target S102 level.

    ModelDataObj (type->SFMTModelFactory): The regional
    input model data object from which the PointDataDict
    have been taken.

    return (type->tuple): tuple holding the updated tile dictionary

    REMARK: This method is not used by classes of
    models.eccc package.
    """

    #--- TODO: Replace ModelDataObj argument by a S102TilesObj class instance object.

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #-- NOTE: Fool-proof checks are commented for performance reasons. You can uncomment
    #      them to get (a lot) more details for debugging purposes.

    #if TilePointDataDict  is None :
    #  sys.exit("ERROR "+methID+" TilePointDataDict is None !\n")

    #if ModelDataObj is None :
    #  sys.exit("ERROR "+methID+" WebTideObj is None !\n")

    #if ModelDataObj._s102TilesObj is None :
    #  sys.exit("ERROR "+methID+" ModelDataObj._s102TilesObj is None !\n")

    #if s102TilesObj._baseLevelTiles is None :
    #  sys.exit("ERROR "+methID+" s102TilesObj._baseLevelTiles is None !\n")

    #if s102TilesObj.LATITUDES_RANGE_ID[0] not in s102TilesObj._baseLevelTiles.keys() :
    #  sys.exit("ERROR "+methID+
    #           " s102TilesObj.LATITUDES_RANGE_ID[0] == "+
    #           s102TilesObj.LATITUDES_RANGE_ID[0]+
    #           " string id. key is not in s102TilesObj._baseLevelTiles keys !\n")

    #if ModelDataObj._s102Level2Use is None :
    #  sys.exit("ERROR "+methID+" ModelDataObj._s102Level2Use is None !\n")

    #: Doc Local shortcut to the S102Tiles object of WebTideObj:
    s102TilesObj= ModelDataObj._s102TilesObj

    #: Doc Local shortcut to the WebTideObj._s102Level2Use
    tilesLevel2Use= ModelDataObj._s102Level2Use

    #: Doc Set the tile dict. tuple to be returned to None
    #    to signal that the WebTide data point is not valid by default
    tileDictTuple= None

    #: Doc Shortcut to the base level S102 tiles dictionary:
    baseLevelTiles= s102TilesObj._baseLevelTiles

    #: Doc Get the S-102 base level tile which encloses the LLU data point if any:
    enclosingTileInfoList= \
      s102TilesObj.getEnclosingTileInfo(baseLevelTiles, PointLatF, PointLonF, False)

    #: Doc Reject the data grid point if not enclosed by any S102 tile.
    if enclosingTileInfoList is None :

      if WarningsLog :
        sys.stdout.write("WARNING "+methID+
                         ": point at latitude="+str(PointLatF)+
                         " and longitude="+str(PointLonF)+
                         " is not enclosed by any S102 base level tile ! data point rejected !\n")
      #--- end inner if block

      #--- Nothing more to do so get outta'here
      return tileDictTuple

    #--- End outer if block

    #: Doc I we get here then we have a model data grid point which is enclosed in a S102 tile limits
    #    extract the base level tile string id.:
    baseLevelTileId= enclosingTileInfoList[0]

    #: Doc Put the point data in the tile dictionary at the right
    #      S102 level for the ouput files:
    baseLevelTileDict= enclosingTileInfoList[1]

    #: Doc First check if the target level is the (coarser) base one.
    #
    #  TODO: Should find a cleaner way to handle this if-elif-else block
    #        which have an inner if-else block.
    if tilesLevel2Use[0] == IS102.DEFAULT_TILES_BASE_LEVEL[0] :

      #: Doc Will return the baseLevelTileDict reference having the data point dictionary in it
      tileDictTuple= s102TilesObj.addPointDataInTileDict( TilePointDataDict, ModelDataId,
                                                          baseLevelTileDict, baseLevelTileId)

      #: Doc Store the tile reference in WebTideObj._tilesWithData dictionary
      #      for later direct usage:
      if baseLevelTileId not in ModelDataObj._tilesWithData.keys() :
        ModelDataObj._tilesWithData[baseLevelTileId]= baseLevelTileDict

    #: Doc Need to check for the higher resolution tiles.
    elif baseLevelTileDict[ s102TilesObj.TILES_NEXT_LEVEL_ID[0] ] is not None :

      #: Doc Get the next level tiles head dictionary:
      nextLevelTilesDict= baseLevelTileDict[ s102TilesObj.TILES_NEXT_LEVEL_ID[0] ]

      #: Doc Get the tile string id. and its dictionary from the nextLevelTilesDict:
      tileDictTuple= s102TilesObj.getTileAtLevel( PointLatF,
                                                  PointLonF,
                                                  tilesLevel2Use,
                                                  nextLevelTilesDict )

      #: Doc We've got a tile if tileDictTuple is not None:
      if tileDictTuple is not None :

        #: Doc Set the data point dictionary reference in the right tile(refered by tileDictTuple[1])
        #    at this targeted level:
        s102TilesObj.addPointDataInTileDict( TilePointDataDict,
                                             ModelDataId,
                                             tileDictTuple[1],
                                             baseLevelTileId)

        #: Doc Get the updated tile string id.:
        tileId= tileDictTuple[0]

        #: Doc Store the updated tile reference in WebTideObj._tilesWithData dictionary
        #     for later direct usage(if not already stored in it):
        if tileId not in ModelDataObj._tilesWithData.keys() :
          ModelDataObj._tilesWithData[tileId]= tileDictTuple[1]

        #sys.stdout.write("INFO "+methID+" tilesLevel2Use[0]="+
        #                 str(tilesLevel2Use[0])+" tileDictTuple="+
        #                 str(tileDictTuple)+"\n")

      else :

        #--- Quite Unlikely to happen except if new tiles and or new data points have been added:
        if WarningsLog :
          sys.stdout.write("WARNING "+methID+
                           ": No tiles at level -> "+
                           str(tilesLevel2Use[0])+
                           " for point at latitude="+str(PointLatF)+
                           " and longitude="+str(PointLonF)+
                           " for model data -> "+ModelDataId+"\n")

        #--- end inner if block: Nothing more to do so get outta'here.
        return tileDictTuple

      #--- End inner if-else block.

    else :

      #--- Unlikely to happen except if new tiles and or new data points have been added:
      if WarningsLog :
        sys.stdout.write("WARNING "+methID+
                         " No tiles at level -> "+
                         str(tilesLevel2Use[0])+
                         " for point at latitude="+str(PointLatF)+
                         " and longitude="+str(PointLonF)+
                         " for model data  ->"++ModelDataId++"\n")

      #--- end inner if block: Nothing more to do so get outta'here
      return tileDictTuple

    #--- end outer if-elif-else block.

    #sys.stdout.write("INFO "+methID+" End  \n")

    #--- Return the tuple holding the updated tile dictionary to the calling method:
    return tileDictTuple
