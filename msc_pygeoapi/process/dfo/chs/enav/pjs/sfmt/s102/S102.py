#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/s102/S102.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s102.S102 implementation.
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

#--- Built-in modules:
import os
import sys
import inspect

#--- 3rd party ogr module from gdal osgeo package.
from osgeo import ogr

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.IS102 import IS102
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.S102Factory import S102Factory

#---
class S102(S102Factory):

  """
  class S102 is used to read and return(stored in a python dictionary) all
  the GDAL-OGR polygons which define the regular bounding-boxes of all the allowed
  ENAV DHP S102 tiles.
  """

  #---
  def __init__( self,
                BaseLevelId,
                BaseLevelS102PolygonsSHPFile,
                ExcludeTilesBBoxesTuple= None) :
    """
    Create a new Tiling object with a S-102 GDAL-OGR layer object
    read in a ESRI SHAPEFILE format file.

    BaseLevelId (type->string): The string id. of the s102 base level tiles dataset.

    BaseLevelS102PolygonsSHPFile (type->string) : Complete path to the ESRI Shapefile which holds
    the base level S-102 tiles GDAL-OGR layer object.

    ExcludeTilesBBoxesTuple (type->tuple) <OPTIONAL> Default->None : A tuple which holds one or more
    regular lat-lon bounding boxes used to exclude S102 L2 tiles that are considired useless (ex.
    outside the canadian coastal waters limits).

    Remark: Only ESRI SHAPEFILE format supported for now(Oct. 2018) but one can easily modify this 
    __init__ method to use other file formats if needed by implementing an if-else block dealing
    with an argument for the file format to use OR using OO paradigm by creating a super class for
    the new input type and make the S102 class inheriting from that super-class.
    """

    #; Doc Init S102Factory super class.
    S102Factory.__init__(self)

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methID+" Start\n")

    if BaseLevelId is None :
      sys.exit("ERROR "+methID+" BaseLevelId is None  !\n")

    if BaseLevelS102PolygonsSHPFile is None :
      sys.exit("ERROR "+methID+" BaseLevelS102PolygonsSHPFile is None  !\n")

    self._dataDict= {}

    #: Doc Set the base level(usually level 2) S102 tiles data dictionary
    self._baseLevelNameId= BaseLevelId

    self._dataDict[self._baseLevelNameId]= \
      self.getDataDictFromSHPFile(BaseLevelId, BaseLevelS102PolygonsSHPFile, ExcludeTilesBBoxesTuple, False)

    #--- Keep a shortcut reference to the base level tiles dictionary in self.
    self._baseLevelTiles= self._dataDict[self._baseLevelNameId]

    #--- Set the base level tiles regular cartesian indexing:
    self.setBaseLevelIndexing()

    sys.stdout.write("INFO "+methID+" End\n")

  #---
  def getLatitudesRangeTuple(self, Latitude) :

    """
    Return one of the latitudes range key tuple wich enclose a latitude argument.

    Latitude(type->float) : The latitude en decimal degrees which used to select the latitudes range.

    return(type->tuple)

    Remarks:

    1). Latitude argument assumed in decimal degrees.

    2). self._dataDict must already exists and must hold the latitudes list indexed by the 
    self._baseLevelTiles[self.LATITUDES_RANGE_ID[0]]
    """

    tupleRet= None

    #: Doc Extract the S102 latitudes ranges values defined as keys of
    #      self._baseLevelTiles[self.LATITUDES_RANGES_ID[0]] dictionary:
    baseLevelTilesLatRanges= tuple(self._baseLevelTiles[self.LATITUDES_RANGES_ID[0]].keys())

    #--- Loop on S102 tiles latitudes ranges.
    for latRangeTuple in baseLevelTilesLatRanges :

      if Latitude >= latRangeTuple[ self.LATITUDES_RANGE_SWC_IDX[0] ] \
        and Latitude <= latRangeTuple[ self.LATITUDES_RANGE_NWC_IDX[0] ] :

        #: Doc latitudes range found, set the return value with its tuple
        #      and stop searching.
        tupleRet= latRangeTuple
        break

    return tupleRet

  #---
  def getTileAtLevel(self, PointLatF, PointLonF,
                     S102Level2Use, LevelTilesDict, WarnLog= False) :
    """
    Find the tile enclosing a given coordinates lat,lon combo at a given S102 level.

    PointLatF (type->float) : A North hemisphere latitude(normally between 0.1 and 89.9) in decimal degrees.

    PointLonF (type->float) : A West hemisphere longitude(normally between -179.9 and -0.1) in decimal degrees.

    S102Level2Use (type->unary tuple): The string id. of the S102 level wanted for the tile.

    LevelTilesDict (type->dictionary): A dictionary of tiles available(possibly with finer resolution(s)
    tiles embedded in it)

    return (type->tuple) A tuple which contains the tile infos.

    Remark: Using self recursive call to explore embedded finer resolution(s) tiles (if any).
    """

    ##--- Uncomment for debugging
    #methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    ##--- Uncomment for debugging
    #if PointLatF is None :
    #  sys.exit("ERROR "+methID+" PointLatF is None !\n")

    ##--- Uncomment for debugging
    #if PointLonF is None :
    #  sys.exit("ERROR "+methID+" PointLonF is None !\n")

    ##--- Uncomment for debugging
    #if S102Level2Use is None :
    #  sys.exit("ERROR "+methID+" S102Level2Use is None  !\n")

    ##--- Uncomment for debugging
    #if LevelTilesDict is None :
    # sys.exit("ERROR "+methID+" LevelTilesDict is None  !\n")

    #--- Init. returned tuple at None
    tileDictTuple= None

    #: Doc NOTE: S102Level2Use should be an unary tuple holding a string id.
    if S102Level2Use[0] == LevelTilesDict[ IS102.LEVEL_ID[0] ] :

      #--- It is the right level, get the id. of the enclosing tile if any:
      tileId= self.getEnclosingTileId( LevelTilesDict[ self.THIS_LEVEL_TILES_ID[0] ], PointLatF, PointLonF)

      if tileId is not None :

        #: Doc Got a tile for the PointLatF,PointLonF combo,
        #      set return tuple with the tile id. and the tile dictionary:
        tileDictTuple= ( tileId, LevelTilesDict[ self.THIS_LEVEL_TILES_ID[0] ][tileId] )

    else :

      #: Doc Not the level to find, poke next level tiles (if any) now:
      thisLevelTilesDict= LevelTilesDict[ self.THIS_LEVEL_TILES_ID[0] ]

      #: Doc Loop on the next level tiles ids. (if any)
      for thisLevelTileId in thisLevelTilesDict.keys() :

        #: Doc Local shortcut to the next level tiles dictionary (could be None):
        nextLevelTilesDict= thisLevelTilesDict[thisLevelTileId][ self.TILES_NEXT_LEVEL_ID[0] ]

        if nextLevelTilesDict is not None :

          #: Doc Recursive call here to explore the next level tiles:
          tileDictTuple= self.getTileAtLevel(PointLatF, PointLonF, S102Level2Use, nextLevelTilesDict )

           #: Doc Break the loop if self.getTileAtLevel returns a non-None tuple:
          if tileDictTuple is not None : break

        #--- End block if nextLevelTilesDict is not None
      #--- End block loop for thisLevelTileId in thisLevelTilesDict.keys()
    #--- End block outer if-else S102Level2Use[0] == LevelTilesDict[ IS102.LEVEL_ID[0] ]

    #: Doc Return the tileDictTuple to the calling method:
    #     (which could be the same method but in the upper level recursive frame)
    return tileDictTuple

  #---
  def getNextLevelTiles(self, NextLevelId, S102NextLevelShapeFile,
                        PrevLevelTilesDataDict, ExcludeTilesBBoxesTuple= None, WarningsLog= False) :
    """
    Get the next S102 level tiles data dictionary.

    NextLevelId (type->string) : The next S102 level string id. of the tiles defined in S102NextLevelShapeFile.

    S102NextLevelShapeFile (type->string) : The path of the shapefile which contains the S102 tiles to get at
    the level wanted.

    PrevLevelTilesDataDict (type->dictionary) : The upper coarser resolution S102 level tiles data dictionary.

    ExcludeTilesBBoxesTuple (type->tuple) <OPTIONAL> Default->None : A tuple which holds one or more regular
    lat-lon bounding boxes used to exclude S102 L2 tiles that are considired useless(ex. outside the canadian
    coastal waters limits).

    WarningsLog (type->boolean) <OPTIONAL> Default->False : To log(or not) warnings messages on the stdout
    file stream.

    return (type->dictionary): The next S102 level tiles data dictionary extracted from S102NextLevelShapeFile.

    NOTE: The number of orphaned higher resolutions tiles that are not enclosed in a base
    level tile is computed and displayed to the stdout stream at the end of the method.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methID+" Start, S102NextLevelShapeFile="+S102NextLevelShapeFile+"\n")

    ##--- Uncomment for debugging
    #if NextLevelId is None :
    #  sys.exit("ERROR "+methID+" NextLevelId is None  !\n")

    ##--- Uncomment for debugging
    #if S102NextLevelShapeFile is None :
    #  sys.exit("ERROR "+methID+" S102NextLevelShapeFile is None  !\n")

    ##--- Uncomment for debugging
    #if PrevLevelTilesDataDict is None :
    #  sys.exit("ERROR "+methID+" PrevLevelTilesDataDict is None  !\n")

    if self.LATITUDES_RANGES_ID[0] not in PrevLevelTilesDataDict :
      sys.exit("ERROR "+methID+" self.LATITUDES_RANGES_ID[0] == "+
               self.LATITUDES_RANGES_ID[0]+" string id. key is not in PrevLevelTilesDataDict !\n")

    #: Doc Get the next S102 level tiles dictionary from S102NextLevelShapeFile.
    nextLevelTilesDataDict= \
      self.getDataDictFromSHPFile(NextLevelId, S102NextLevelShapeFile, ExcludeTilesBBoxesTuple , False)

    if self.LATITUDES_RANGES_ID[0] not in nextLevelTilesDataDict :
      sys.exit("ERROR "+methID+" self.LATITUDES_RANGES_ID[0] == "+
               self.LATITUDES_RANGES_ID[0]+" string id. key is not in nextLevelTilesDataDict !\n")
    #---

    #: Doc Count the number of orphaned higher resolutions tiles that
    #      are not enclosed in a base level tile.
    nbOrphanedTiles= 0

    #: Doc Local shortcut to the latitudes ranges sub-dictionary.
    tilesDataDictLatRanges= nextLevelTilesDataDict[ self.LATITUDES_RANGES_ID[0] ]

    #: Doc Nested loop on all next level tiles latitudes ranges.
    for nextLevelLatRange in tuple(tilesDataDictLatRanges.keys()) :
      for nextLevelTileId in tuple(tilesDataDictLatRanges[nextLevelLatRange]) :

        #: Doc Local shortcut to the next level tile dict.
        nextLevelTileDict= tilesDataDictLatRanges[nextLevelLatRange][nextLevelTileId]

        #: Doc Local shortcut to the next level point bounding box dictionary.
        nextLevelTileBBoxDict= nextLevelTileDict[ self.BOUNDING_BOX_ID[0] ]

        #: Doc North-East corner coordinates of the tile bounding box.
        nextBBoxNorthEastLLList= nextLevelTileBBoxDict[ self.BBOX_NORTH_EAST_CORNER[0] ]

        #: Doc South-West corner coordinates of the tile bounding box.
        nextBBoxSouthWestLLList= nextLevelTileBBoxDict[ self.BBOX_SOUTH_WEST_CORNER[0] ]

        #: Doc Get the lat,lon center of the tile bounding box.
        nextLevelTileCenterLat= (nextBBoxNorthEastLLList[ self.TILES_LAT_IDX[0] ] + nextBBoxSouthWestLLList[ self.TILES_LAT_IDX[0] ])/2.0
        nextLevelTileCenterLon= (nextBBoxNorthEastLLList[ self.TILES_LON_IDX[0] ] + nextBBoxSouthWestLLList[ self.TILES_LON_IDX[0] ])/2.0

        #: Doc Get the enclosing tile(if any) at the previous(coarser resolution) level.
        prevLevelTileTupleInfo= \
          self.getEnclosingTileInfo(PrevLevelTilesDataDict, nextLevelTileCenterLat, nextLevelTileCenterLon, True)

        #: Doc Found an orphaned higher resolution tile which is not enclosed by a coarser resolution tile.
        if prevLevelTileTupleInfo is None :

          nbOrphanedTiles += 1

          if WarningsLog :
            sys.stderr.write("WARNING "+methID+" No base level enclosing tile found for next level tile -> "
                                 + nextLevelTileId +" with bounding box -> "+ str(nextLevelTileBBoxDict) +"!\n")

          #: Doc We have an orphaned next level tile. Just keep going with the next next level tiles.
          continue

        #--- end if thisLevelTileTupleInfo is None

        #: Doc Local shortcut to the enclosing tile dict. at previous level.
        prevLevelTile= prevLevelTileTupleInfo[1]

        #: Doc prevLevelTile[self.TILES_NEXT_LEVEL_ID[0]] could be None at this point:
        if prevLevelTile[ self.TILES_NEXT_LEVEL_ID[0] ] is None :

          #: Doc Create the next level tiles dictionary in prevLevelTile.
          prevLevelTile[ self.TILES_NEXT_LEVEL_ID[0] ]= { IS102.LEVEL_ID[0] : NextLevelId,
                                                          self.THIS_LEVEL_TILES_ID[0] : { } }

        #--- end block if prevLevelTile[self.TILES_LEVELS.NEXT.name] is Non

        #: Doc Local shortcut to the next level tiles dict. in the enclosing
        #      tile dict. at the previous coarser resolution level.
        nextLevelTilesDictSc= prevLevelTile[ self.TILES_NEXT_LEVEL_ID[0] ]

        #: Doc Update the next level tiles dict. of the enclosing tile dict.
        #      at the previous level with the new enclosed tile infos.
        #      (i.e. embedding the next level tile dict. in its enclosing
        #      previous level tile dict.)
        nextLevelTilesDictSc[ self.THIS_LEVEL_TILES_ID[0] ].update( { nextLevelTileId : nextLevelTileDict } )

      #--- end loop for nextLevelTileId in nextLevelTilesDataDict.keys()
    #--- end loop for nextLevelTileId in nextLevelTilesDataDict[nextLevelLatRange]

    sys.stdout.write("INFO "+methID+" nb. of orphaned tiles= "+str(nbOrphanedTiles) +" for dataset -> "+S102NextLevelShapeFile+"\n")
    sys.stdout.write("INFO "+methID+" End\n")

    #: Doc Return the next level tiles dict. extracted from the SHP file to the calling method:
    return nextLevelTilesDataDict

  #--- end block method getNextLevelTiles.

  #---
  def getPointStrKeyId(self, Lon , Lat) :

    """
    Build a dictionary string id. key with a Lon, Lat coordinates combo. Will be used
    to index a model data grid point in a given S102 tile.

    Lon (type->float) : Longitude value.

    Lat (type->float) : Latitude value.

    return (type->string)
    """

    #--- NOTE: Using str() to be sure to get basic ASCII strings.
    return self.LON_ID[0] + "=" + str(Lon) + self.DICT_KEYS_SEP[0] + self.LAT_ID[0] + "=" + str(Lat)

  #--- end block method getPointStrKeyId

#  #--- Keep setLevelsInfo method for possible future usage:
#  def setLevelsInfo(self) :
#
#    methId= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
#
#    sys.stdout.write("INFO "+methId+" Start\n")
#
#    if self._dataDict is None :
#      sys.exit("ERROR "+methID+" self._dataDict is None !\n")
#
#    if IS102.TILES_LEVEL2_ID[0] not in self._dataDict :
#
#      sys.exit("ERROR "+methID+" IS102.TILES_LEVEL2_ID[0] key -> "+
#               IS102.TILES_LEVEL2_ID[0]+" not present in self._dataDict !\n")
#    #---
#
#    baseLevelTilesLatRangesDict= self._dataDict[ IS102.TILES_LEVEL2_ID[0] ]
#
#    for baseLevelTilesLatRange in baseLevelTilesLatRangesDict.keys() :
#
#      baseLevelTilesDict= baseLevelTilesLatRangesDict[baseLevelTilesLatRange]
#
#      for baseLevelTileId in baseLevelTilesDict.keys() :
#
#        #print baseLevelTileId
#        #rint str(baseLevelTilesDict[baseLevelTileId].keys())
#        #print str(baseLevelTilesDict[baseLevelTileId][self.TILES_NEXT_LEVEL[0] ])
#
#        baseLevelTileDict= baseLevelTilesDict[baseLevelTileId]
#
#        #--- Set baseLevelTileDict[ self.ENCLOSED_LEVELS_ID[0] ] at None before extracting
#        #    the enclosed tiles level(s) if any.
#        baseLevelTileDict[ self.ENCLOSED_LEVELS_ID[0] ]= None
#
#        tempLevelsIdsList= self.extractLevelsIds( baseLevelTileDict[ self.TILES_NEXT_LEVEL_ID[0] ] )
#
#        if tempLevelsIdsList is not None :
#
#          baseLevelTileDict[ self.ENCLOSED_LEVELS_ID[0] ]= tuple(tempLevelsIdsList)
#
#          #print baseLevelTileId
#          #print str(baseLevelTileDict[ self.ENCLOSED_LEVELS_ID[0] ])
#      #--- End block loop for baseLevelTileId in baseLevelTilesDict.keys()
#    #---  End block loop for baseLevelTilesLatRange in baseLevelTilesLatRangesDict.keys()
#
#    sys.stdout.write("INFO "+methId+" End\n")
#    #sys.stdout.write("INFO "+methId+" exit 0 \n")
