#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/s102/S102Factory.py
# Creation        : Sept. 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s102.S102Factory implementation.
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
import math
import inspect

#--- 3rd party ogr module from gdal osgeo package:
from osgeo import ogr

#---
from dhp.sfmt.s102.IS102 import IS102
from dhp.geo.GeoFactory import GeoFactory
from dhp.sfmt.s102.S102TilesFactory import S102TilesFactory

#---
class S102Factory(GeoFactory, S102TilesFactory):

  """
  Class inherited by the S102 class mainly for modularization.
  (i.e. to avoid, as much as possible, having methods using methods
  from the same class or source file.)
  """

  #---
  def __init__(self) :

    #--- NOTE: GeoFactory super-class MUST be initialized before S102Tiles super-class.
    GeoFactory.__init__(self)
    S102TilesFactory.__init__(self)

  #---
  def getDataDictFromSHPFile(self, LevelId, S102PolygonsSHPFile,
                             ExcludeTilesBBoxesTuple= None, CheckForRegularBBox= False) :
    """
    Method that fill up a dictionary of S102 tiles bounding boxes from a SHP format file.

    LevelId (type->string): The S102 level of the tiles defined in S102PolygonsSHPFile.

    S102PolygonsSHPFile (type->string): The Shapefile which contains the S102 tiles to get.

    ExcludeTilesBBoxesTuple (type->tuple) <OPTIONAL> Default->None : A tuple holding one or 
    more regular lat-lon bounding boxes used to exclude S102 L2 tiles that are considired
    useless (ex. outside the canadian coastal waters limits).

    CheckForRegularBBox (type->boolean) <OPTIONAL> Default->False: Boolean flag to (or not to)
    do the check if tiles bounding boxes are regular. (Should obviously be at True for debugging)
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #--- Two fool-proof checks:
    if LevelId is None :
      sys.exit("ERROR "+methId+" LevelId is None ! \n")

    if S102PolygonsSHPFile is None :
      sys.exit("ERROR "+methId+" S102PolygonsSHPFile is None ! \n")

    sys.stdout.write("INFO "+methId+" Start, LevelId="+LevelId+
                     ", S102PolygonsSHPFile="+S102PolygonsSHPFile+"\n")

    #: Doc Assuming first that we do not have to exclude some tiles.
    excludeTilesBBoxes= None

    #: Doc Check if we have to exclude some tiles.
    if ExcludeTilesBBoxesTuple is not None :

      #; Doc Use a temp. list to fill up with the excluding b. boxes lat,lon data.
      excludeTilesBBoxes= []

      #: Doc Need to format lat,lon combos of the exclude b. boxes as lon,lat
      #      tuples combos to get the same convention as the S102 tiles bounding boxes.
      for bboxIter in ExcludeTilesBBoxesTuple :

        #--- Note the clockwise ordering and the omission of the repetition
        #    of the regular SW b. box corner as the normal vector closed polygon
        #    convention wants. Need also to convert the bboxIter lat,lon data to
        #    floats as the lat,lon values could be strings at this point.
        bboxTuple= ( ( float(bboxIter[1]), float(bboxIter[0]) ), #--- SW b. box corner.
                     ( float(bboxIter[1]), float(bboxIter[2]) ), #--- NW b. box corner.
                     ( float(bboxIter[3]), float(bboxIter[2]) ), #--- NE b. box corner.
                     ( float(bboxIter[3]), float(bboxIter[0]) )  #--- SE b. box corner.
                   )

        excludeTilesBBoxes.append( bboxTuple )

      #--- End inner for loop block.

      #; Doc Get a tuple with the filled list.
      excludeTilesBBoxes= tuple(excludeTilesBBoxes)

      sys.stdout.write("INFO "+methId+" Will use regular bounding boxes -> "+
                       str(excludeTilesBBoxes)+" to exclude tiles that are considered useless.\n")
    #--- End if block.

    #: Doc The OGR layer to get from the shapefile should have its name defined as the file name(without the extension):
    levelLayerName= os.path.basename(S102PolygonsSHPFile).split(".")[0]

    #: Doc Check that the levelLayerName is allowed.
    if levelLayerName not in self.LEVELS_LAYER_NAMES_ALLOWED :
      sys.exit("ERROR "+methId+
               " Invalid SHP layer name -> "+levelLayerName+ " !\n")
    #--- End if block.

    #: Doc Check for the shapefile existence.
    if not os.access(S102PolygonsSHPFile, os.F_OK) :
      sys.exit("ERROR "+methId+" input file -> "+S102PolygonsSHPFile+" not found ! \n")
    #--- End if block.

    sys.stdout.write("INFO "+methId+" Trying to get OGR layer: "+
                      levelLayerName+" in S102PolygonsSHPFile: "+S102PolygonsSHPFile+"\n")

    #--- NOTE 1: osgeo.ogr object does not have a Close() method(which is a bit strange IMHO).
    #    NOTE 2: The 0 at 2nd arg. signal that the file is opened in read mode only.
    s102IndexData= ogr.Open(S102PolygonsSHPFile, 0)

    if s102IndexData is None :
      sys.exit("ERROR "+methId+" Unable to open file: "+S102PolygonsSHPFile + " with ogr.Open !\n")

    #: Doc Be sure to pass a good'ol plain ASCII string to GetLayerByName
    #      OGR method otherwise it could crash.
    s102Layer= s102IndexData.GetLayerByName( str(levelLayerName) )

    if s102Layer is None :
      sys.exit("ERROR "+methId+" Unable to get s102Layer ->"+
                       levelLayerName+" from -> "+S102PolygonsSHPFile+" with s102IndexData.GetLayerByName !\n")
    #--- End if block.

    #: Doc Validate the OGR layer SRS:
    self.validateOGRLayerSRS(s102Layer)

    #: Doc Create an empty dictionary which we will fill up with some shapefile data.
    dataDictRet= {}

    #: Doc Add the sub-dict for the level latitudes ranges list.
    dataDictRet[ self.LATITUDES_RANGES_ID[0] ]= {}

    #--- local shorcut to this level latitudes ranges dict.
    dataDictRetLatRanges= dataDictRet[ self.LATITUDES_RANGES_ID[0] ]

    #: Doc To count the number of valid tiles.
    validTiles= 0

    #: Local boolean used to control it we have to reject(or not) a tile candidate.
    rejectTile= False

    #: Doc Loop on all OGR SHP features.
    for tileFeatureId in tuple(range(s102Layer.GetFeatureCount())) :

      #: Doc Tile OGR polygon feature object.
      tilePolygon= s102Layer.GetFeature(tileFeatureId)

      if tilePolygon is None :
        sys.exit("ERROR "+methId+
                 " Unable to get tile polygon at feature index: " + str(tileFeatureId) + " !\n")
      #--- End if block.

      #--- No method chaining allowed here (unfortunately). Really need to separate
      #    OGR objects retreivals to avoid dereferencing None objects.
      tileGref= tilePolygon.GetGeometryRef()

      if tileGref is None :
        sys.exit("ERROR "+methId+
                 " Unable to get tile polygon geometry ref at feature index: "+str(tileFeatureId)+"!\n")
      #--- End if block.

      tileGref0= tileGref.GetGeometryRef(0)

      if tileGref0 is None :
        sys.exit("ERROR "+methId+
                 " Unable to get tile polygon geometry ref0 at feature index: "+str(tileFeatureId)+"!\n")
      #--- End if block.

      #: Doc Extract tile bounding box limits data.
      tileBoundingBox= tuple( tileGref0.GetPoints() )

      if tileBoundingBox is None :
        sys.exit("ERROR "+methId+
                 " Unable to get tile polygon bounding box points at feature index: "+str(tileFeatureId)+" !\n")
      #--- End if block.

      #: Doc Extract tile string id.
      tileId= tilePolygon.GetField(self.TILE_NAME_FILE_ID[0])

      if tileId is None :
        sys.exit("ERROR "+methId+
                 " Unable to get tile polygon bounding box string id at feature index: "+str(tileFeatureId)+"!\n")
      #--- End if block.

      #: Doc South-West corner latitude coord. of the tile bounding box.
      swcLat= tileBoundingBox[ self.BBOX_SOUTH_WEST_CORNER[0] ][ self.TILES_LAT_IDX[0] ]

      #: Doc North-West corner latitude coord. of the tile bounding box.
      nwcLat= tileBoundingBox[ self.BBOX_NORTH_WEST_CORNER[0] ][ self.TILES_LAT_IDX[0] ]

      #: Doc Exclude tile if one of swcLat OR nwcLat is inside one of the
      #     excludeTilesBBoxes.
      if excludeTilesBBoxes is not None :

        #: Doc South-West corner longitude coord. of the tile bounding box.
        swcLon= tileBoundingBox[ self.BBOX_SOUTH_WEST_CORNER[0] ][ self.TILES_LON_IDX[0] ]

        #: Doc South-West corner longitude coord. of the tile bounding box.
        necLat= tileBoundingBox[ self.BBOX_NORTH_EAST_CORNER[0] ][ self.TILES_LON_IDX[0] ]

        #: Doc North-West corner longitude coord. of the tile bounding box.
        necLon= tileBoundingBox[ self.BBOX_NORTH_EAST_CORNER[0] ][ self.TILES_LON_IDX[0] ]

        rejectTile= False

        #: Doc Loop on the excluding b. boxes.
        for bbox in excludeTilesBBoxes :

          #: Doc Reject the tile if inside one of the forbidden b. box.
          if self.insideBoundingBox(swcLat, swcLon, bbox) \
            or self.insideBoundingBox(necLat, necLon, bbox) :

            rejectTile= True
            break

          #--- end inner if
        #--- end for loop block
      #--- end outer if

      #: Doc Skip the rejected tile if we have to and continue with the next tile.
      if rejectTile : continue

      #: Doc Define the latitudes range tuple of the tile
      #      (float conversion just to be sure).
      latRange= (float(swcLat), float(nwcLat))

      #: Doc Add this latitudes range tuple as a sub-dict to the
      #      dataDictRetLatRanges dict. if not already present in it.
      if latRange not in tuple( dataDictRetLatRanges.keys() ) :
        dataDictRetLatRanges[latRange]= {}
      #--- End if block.

      #: Doc Get rid of the South-West corner polygon closing point
      #      duplication at tileBoundingBox[5] for the tile dict in
      #      dataDictRetLatRanges (NOTE: The OGR polygon object
      #      reference is also stored in the tile dict for possible
      #      subsequent usage with OGR land-water masks).
      dataDictRetLatRanges[latRange][tileId]= { self.TILES_NEXT_LEVEL_ID[0] : None,
                                                IS102.LEVEL_ID[0]           : LevelId,
                                                self.OGR_TILE_POLYGON_ID[0] : tilePolygon,
                                                self.BOUNDING_BOX_ID[0]     : tileBoundingBox[0:4] }

      #: Doc Verify that the bounding box of the tile is indeed regular.
      if CheckForRegularBBox :

        bboxPolygon= tuple( dataDictRetLatRanges[latRange][tileId][ self.BOUNDING_BOX_ID[0] ] )

        bBoxNorthEastLLList= tuple( bboxPolygon[ self.BBOX_NORTH_EAST_CORNER[0] ] )
        bBoxSouthWestLLList= tuple( bboxPolygon[ self.BBOX_SOUTH_WEST_CORNER[0] ] )

        bBoxNorthWestLLList= tuple( bboxPolygon[ self.BBOX_NORTH_WEST_CORNER[0] ] )
        bBoxSouthEastLLList= tuple( bboxPolygon[ self.BBOX_SOUTH_EAST_CORNER[0] ] )

        if bBoxNorthWestLLList[ self.TILES_LAT_IDX[0] ] != bBoxNorthEastLLList[ self.TILES_LAT_IDX[0] ] :

          sys.exit("ERROR "+methId+
                   " Tile bounding box North-West point latitude != tile bounding box North-East point latitude !\n")

        #--- end if inner block

        if bBoxSouthEastLLList[ self.TILES_LAT_IDX[0] ] != bBoxSouthWestLLList[ self.TILES_LAT_IDX[0] ] :
          sys.exit("ERROR "+methId+
                   " Tile bounding box South-East point latitude != tile bounding box South-West point latitude !\n")
        #--- end if inner block.

        if bBoxNorthWestLLList[ self.TILES_LON_IDX[0] ] != bBoxSouthWestLLList[ self.TILES_LON_IDX[0] ] :
          sys.exit("ERROR "+methId+
                   " Tile bounding box North-West point longitude != tile bounding box SouthWest point longitude !\n")
        #--- end if inner block.

        if bBoxSouthEastLLList[self.TILES_LON_IDX[0]] != bBoxNorthEastLLList[self.TILES_LON_IDX[0]] :
          sys.exit("ERROR "+methId+
                   " Tile bounding box South-East point longitude != tile bounding box North-East point longitude !\n")
        #--- end inner if block.

      #--- end outer if block.

      #: Doc Update tiles bounding boxes regular limits in the dict to be returned.

      #---  NOTE: dataDictRetLatRanges[latRange][tileId][ self.BOUNDING_BOX_ID[0] ] is a tuple.
      for lon,lat in dataDictRetLatRanges[latRange][tileId][ self.BOUNDING_BOX_ID[0] ] :

        #: Doc Verify that S102 tiles limits are indeed located in the NW hemisphere.

        #    NOTE: This is normally not needed but it could detect problems if the
        #          S-102 dataset has changed and have not been thoroughly verified
        #          (Errare Humanum Est -> the EHE principle) before being used.
        #          The performance is not affected at all even on a rather old
        #          slow machine.

        if not self.checkForNorthWestHemi(lat,lon) :
          sys.exit("ERROR "+methId+" Invalid North-West hemisphere lat-lon point: "+str(lat)+", "+str(lon)+"\n")

        #: Doc Update the global tiles ensemble limits:
        if lon > self.TILES_LON_MAX : self.TILES_LON_MAX= lon

        if lon < self.TILES_LON_MIN : self.TILES_LON_MIN= lon

        if lat > self.TILES_LAT_MAX : self.TILES_LAT_MAX= lat

        if lat < self.TILES_LAT_MIN : self.TILES_LAT_MIN= lat

      #--- end for loop block.

      validTiles += 1

    #--- End loop: for tileFeatureId in range(s102Layer.GetFeatureCount())

    sys.stdout.write("INFO "+methId+" Got -> "+str(validTiles) +" S102 tiles for "+LevelId+" level.\n")
    sys.stdout.write("INFO "+methId+" And -> "+str(len(dataDictRetLatRanges))+" latitudes ranges indices for "+LevelId+" level.\n")

    sys.stdout.write("INFO "+methId+" self.TILES_LON_MAX= "+ str( self.TILES_LON_MAX) + " \n")
    sys.stdout.write("INFO "+methId+" self.TILES_LON_MIN= "+ str( self.TILES_LON_MIN) + " \n")
    sys.stdout.write("INFO "+methId+" self.TILES_LAT_MAX= "+ str( self.TILES_LAT_MAX) + " \n")
    sys.stdout.write("INFO "+methId+" self.TILES_LAT_MIN= "+ str( self.TILES_LAT_MIN) + " \n")

    sys.stdout.write("INFO "+methId+" End\n")

    return dataDictRet

  #--- end block method getDataDict

  #---
  def getEnclosingTileId(self, TilesDataDict, ALatInDecimalDegrees, ALonInDecimalDegrees) :

    """
    Find and return the tile id. which encloses 2D lat,lon coordinates.

    TilesDataDict (type->dictionary): A dictionary of S102 tiles bounding boxes.

    ALatInDecimalDegrees (type->float): A North hemisphere latitude(normally between 0.1 and 89.9) in decimal degrees.

    ALonInDecimalDegrees (type->float): A West hemisphere longitude(normally between -179.9 and -0.1) in decimal degrees.
    """

    #--- NOTE: No fool-proof checks for performance reasons.

    #methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    #sys.stdout.write(methId + "Start \n")

    ret= None

    #---
    for tileId in tuple(TilesDataDict.keys()) :

      tileDataDict= TilesDataDict[tileId]

      if self.insideBoundingBox(ALatInDecimalDegrees,
                                ALonInDecimalDegrees, tileDataDict[ self.BOUNDING_BOX_ID[0] ]) :

        #--- Ok the lat-lon combo is inside tile bounding box:
        ret= tileId
        break

    #sys.stdout.write(methId + "ret="+ ret +"\n")

    return ret

  #---
  def getEnclosingTileInfo(self, TilesDataDict,
                           ALatInDecimalDegrees, ALonInDecimalDegrees, WarningsLog= False) :
    """
    Method which tries to find the S-102 tile which encloses a given
    lat-lon coordinates(in decimal degrees only) location.

    ALatInDecimalDegrees (type->float): A North hemisphere latitude(normally between 0.1 and 89.9) in decimal degrees.

    ALonInDecimalDegrees (type->float): A North hemisphere longitude(normally between -179.9 and -0.1) in decimal degrees.

    WarningsLog (type->boolean) <OPTIONAL> Default->False: To put(or not) log WARNING messages on the stderr file stream.

    return (type->tuple) : A tuple with the tile string id. and a sublist containing the 4 lon-lat
    combos(points) which define the tile limits if we found one OR the Python object
    None if no enclosing tile is found.

    Remark: The method checks for lat-lon locations that are outside the tiles ensemble global limits.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #--- Init. return value to None
    ret= None

    #: Doc Check if ALatInDecimalDegrees,ALonInDecimalDegrees are inside tiles global limits first:
    if self.outsideGlobalLimits(ALatInDecimalDegrees, ALonInDecimalDegrees) :

      if WarningsLog :
        sys.stderr.write("WARNING "+methId+" ALat="+str(ALatInDecimalDegrees)+
                         " and-or ALon="+str(ALonInDecimalDegrees)+" outside of tiles global limits !\n")
      #--- end inner if block.

    else :

      if self.LATITUDES_RANGES_ID[0] not in tuple(TilesDataDict.keys()) :
        sys.exit("ERROR "+methId+" self.LATITUDES_RANGES_ID[0] == "+
                  self.LATITUDES_RANGE_ID[0]+" string id. key is not in TilesDataDict !\n")
      #--- end inner if block.

      tilesDataDictLatRanges= TilesDataDict[ self.LATITUDES_RANGES_ID[0] ]

      #: Doc Iterate on the tiles latitudes indexing ranges items.
      for latitudesRange in tuple(tilesDataDictLatRanges.keys()) :

        #: Doc No need to search in the polygons of the latitudesRange if the latitude
        #    argument ALatInDecimalDegrees is outside this latitudesRange.

        if ALatInDecimalDegrees < latitudesRange[ self.LATITUDES_RANGE_SWC_IDX[0] ] or \
               ALatInDecimalDegrees > latitudesRange[ self.LATITUDES_RANGE_NWC_IDX[0] ] :

          #--- Continue with the next latitudesRange in TilesDataDict.keys():
          continue

        #--- end inner if block.

        #--- TODO: Check if we can squeeze more performance by using unary tuples
        #          for variables that do not change in this loop:
        for tilePolygonId in tuple(tilesDataDictLatRanges[latitudesRange]) :

          #print("str(tilePolygonId)="+str(tilePolygonId))
          #print("tilePolygonId keys:"+str(TilesDataDict[latitudesRange].keys())+"\n")

          #--- Loop shorcut to the tile dictionary:
          tileDataDict= tilesDataDictLatRanges[latitudesRange][tilePolygonId]

          if self.insideBoundingBox(ALatInDecimalDegrees,
                                    ALonInDecimalDegrees, tileDataDict[ self.BOUNDING_BOX_ID[0] ]) :

            #--- Ok coordinates are inside BBox
            ret= ( tilePolygonId, tileDataDict )
            break

          #--- end inner if block.

          #--- End inner if block.
        #--- End inner for loop block.
      #--- End outer for loop block.
    #--- End outer if-else block.

    return ret

  #--- end block method getEnclosingTileInfoList

  #---
  def setBaseLevelIndexing(self) :

    """
    Define the base level tiles 2D grid indexing using the tiles South-West corners as integer indices.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methId+" start\n")

    if self._baseLevelNameId != IS102.DEFAULT_TILES_BASE_LEVEL[0] :
      sys.exit("ERROR "+methId+" self._baseLevelNameId != IS102.DEFAULT_TILES_BASE_LEVEL[0]\n")

    if self._baseLevelTiles is None :
      sys.exit("ERROR "+methId+" self._baseLevelTiles is None !\n")

    #: Doc Create the sub-dictionary that will hold the tiles referenced by cartesian i,j indices.

    #      NOTE: We do not have tiles for all cartesian i(lon),j(lat) indices of the Western
    #            hemisphere then there will be some missing indices in this dictionary.
    self._baseLevelTiles[ self.TILES_INDEXING[0] ]= {}

    #: Doc Get the dictionary(indexed with latitudes ranges tuples) holding all tiles infos. dictionaries.
    baseLeveltilesLatRangesDict= self._baseLevelTiles[ self.LATITUDES_RANGES_ID[0] ]

    #: Doc Loop on all latitudes ranges holding the tiles infos. dictionaries.
    for latRange in tuple(sorted(baseLeveltilesLatRangesDict.keys())) :

      #: Doc Get this latitude range dictionary.
      baseLevelTilesDict= baseLeveltilesLatRangesDict[latRange]

      #:Doc Loop on tiles dictionaries contained by this latitudes range:
      for tileKey in tuple( baseLevelTilesDict.keys() ) :

        #:Doc Get the tile dictionary:
        baseLeveltileDict= baseLevelTilesDict[tileKey]

        #print(str(baseLeveltileDict))

        #: Doc Get the tile lon,lat bounding box object:
        tileBBoxPolygon= baseLeveltileDict[ self.BOUNDING_BOX_ID[0] ]

        #: Doc South-West corner decimal degrees lon,lat tuple of the tile bounding box:
        swcCorner= tileBBoxPolygon[ self.BBOX_SOUTH_WEST_CORNER[0] ]

        #: Doc North-East corner decimal degrees lon,lat tuple of the tile bounding box:
        necCorner= tileBBoxPolygon[ self.BBOX_NORTH_EAST_CORNER[0] ]

        #print("swcCorner="+str(swcCorner))
        #print("necCorner="+str(necCorner))

        #: Doc Tile South-West corner lat,lon
        swcLat= swcCorner[ self.TILES_LAT_IDX[0] ]
        swcLon= swcCorner[ self.TILES_LON_IDX[0] ]

        #: Doc Tile North-East corner lat,lon
        necLat= necCorner[ self.TILES_LAT_IDX[0] ]
        necLon= necCorner[ self.TILES_LON_IDX[0] ]

        #: Doc Get the tile longitude extent:
        tileLonDegreesExtent= ( int(necLon - swcLon) ,)

        #--- Another fool-proof check: Cannot have a base level tile
        #    having more than than four degrees extent for its longitude axis
        if tileLonDegreesExtent[0] > self.BLTILE_LONAXIS_MAXLEN[0] :

          sys.exit("ERROR "+methId+" Found an invalid base level tile -> "+
                   tileBBoxPolygon[ self.TILE_NAME_FILE_ID[0] ]+tileBBoxPolygon[ self.TILE_NAME_FILE_ID[0] ]+
                   " which have more than -> "+str(self.BLTILE_LONAXIS_MAXLEN[0])+" degree extent for its longitude axis !\n")
        #--- end if block.

        #: Doc Store the tileLonDegreesExtent in the tile dict:
        baseLeveltileDict[ self.BLTILE_LONAXIS_EXT_ID[0] ]= tileLonDegreesExtent

        #: Doc Get the tile latitude extent:
        baseLeveltileDict[ self.BLTILE_LATAXIS_EXT_ID[0] ]= tileLatDegreesExtent= ( int(necLat - swcLat) ,)

        #--- Another fool-proof check: Cannot have a base level tile
        #    having more than than two degrees extent for its latitude axis
        if tileLatDegreesExtent[0] > self.BLTILE_LATAXIS_MAXLEN[0] :

          sys.exit("ERROR "+methId+" Found an invalid base level tile -> "+
                   tileBBoxPolygon[ self.TILE_NAME_FILE_ID[0] ]+tileBBoxPolygon[ self.TILE_NAME_FILE_ID[0] ]+
                   " which have more than -> "+str(self.BLTILE_LATAXIS_MAXLEN[0])+" degree extent for its latitude axis !\n")
         #--- end if block.

        #: Doc Store the tileLatDegreesExtent in the tile dict:
        baseLeveltileDict[ self.BLTILE_LATAXIS_EXT_ID[0] ]= tileLatDegreesExtent

        #: Doc Get the cartesian integer i,j indices for the tile
        latIdx= int(math.floor(swcLat - self.WEST_HEMI_SWCELL_LAT[0]))
        lonIdx= int(math.floor(swcLon - self.WEST_HEMI_SWCELL_LON[0]))

        ijIdx= (lonIdx, latIdx)

        #--- Maybe not necessary to do that fool-proof check but we never really know
        #    when and where the good'ol Murphy's law will evetually show up.
        if ijIdx in tuple(self._baseLevelTiles[ self.TILES_INDEXING[0] ].keys()) :

          sys.exit("ERROR "+methId+" ijIdx="+str(ijIdx)+
                   " already defined in self._baseLevelTiles[ self.TILES_INDEXING[0] ] !\n")
        #--- end if block.

        #: Do Use the tuple of cartesian i,j indices combo to index a reference to the tile in a cartesian frame:
        self._baseLevelTiles[ self.TILES_INDEXING[0] ][ ijIdx ]= baseLeveltileDict

      #--- end inner for tileKey in tuple( baseLevelTilesDict.keys() ) loop block
    #---  end outer for latRange in tuple(baseLeveltilesLatRangesDict.keys()) loop block

    sys.stdout.write("INFO "+methId+" end\n")

  ###--- Keep for possible future usage:
  ##def extractLevelsIds(self, TileDict) :
  ##  """
  #  Method extracting the levels ids. of all the finer resolutions
  #  tiles levels that are enclosed(kind of russian dolls principle)
  #  in a given S102 tile dictionary.
  #  TileDict: A S102 tile dictionary.
  #  Note: Using tail recursive call.
  #  """
  #  methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
  #  #--- Init. the list to be returned to None:
  #  levelsIdsList= None
  #  #--- TileDict being None is unlikely to happen but taking no chances.
  #  if TileDict is not None :
  #    #print("TileDict[ IS102.LEVEL_ID[0]="+str(TileDict[ IS102.LEVEL_ID[0]]))
  #    #--- Set the list to be returned with this TileDict level id.
  #    levelsIdsList= [ TileDict[ IS102.LEVEL_ID[0] ] ]
  #    #print str(TileDict.keys())
  #    #print str(TileDict[ self.THIS_LEVEL_TILES_ID[0] ].keys())
  #    #print str(TileDict[ self.THIS_LEVEL_TILES_ID[0] ][self.TILES_NEXT_LEVEL_ID[0]].keys())
  #    thisLevelTilesDict= TileDict[ self.THIS_LEVEL_TILES_ID[0] ]
  #    for thisLevelTileId in thisLevelTilesDict.keys() :
  #      #print str(TileDict[ self.THIS_LEVEL_TILES_ID[0] ][tileId].keys())
  #      thisLevelTileDict= thisLevelTilesDict[thisLevelTileId]
  #      if thisLevelTileDict[ self.TILES_NEXT_LEVEL_ID[0] ] is not None :
  #        #--- NOTE: Recursive call:
  #        levelsIdsList += self.extractLevelsIds( thisLevelTileDict[ self.TILES_NEXT_LEVEL_ID[0] ] )
  #        #--- No need to check the other tiles if at
  #        #    least one have been found then exit the loop:
  #        break
  #      #--- End block if thisLevelTileDict[ self.TILES_NEXT_LEVEL_ID[0] ]
  #    #--- End block loop for thisLevelTileId in thisLevelTilesDict.keys()
  #  #--- End block if TileDict is not None
  #  return levelsIdsList
