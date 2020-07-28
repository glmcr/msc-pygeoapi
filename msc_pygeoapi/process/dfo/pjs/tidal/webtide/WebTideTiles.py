#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidaprd/webtide/WebTideTIles.py
# Creation        : October/Octobre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidaprd.webtide.WebTideTiles implementation.
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
import math
import inspect

#---
from dhp.sfmt.s102.IS102 import IS102
from dhp.sfmt.s104.IS104 import IS104
from dhp.tidalprd.ITidalPrd import ITidalPrd
from dhp.tidalprd.webtide.IWebTide import IWebTide
from dhp.tidalprd.webtide.IGeoJSON import IGeoJSON
from dhp.sfmt.s102.S102DataUtil import S102DataUtil
from dhp.sfmt.SFMTModelFactory import SFMTModelFactory

#---
class WebTideTiles(IWebTide) :

  """
  Class used mainly for WebTide source code modularization.
  Defines some methods for the WebTide tiles input data processing.
  This class is sub-classed by classes WebTideOutput.py and GeoJSON.py.
  (i.e. otherwise said, it is a super class of classes WebTideOutput.py and GeoJSON.py).
  """

  def __init__(self) :

    #---
    IWebTide.__init__(self)

  #---
  @staticmethod
  def setPointDataRefInTiles(DataSetId, PointLatF, PointLonF,
                             PointDataDict, WebTideObj, WarningsLog= False) :
    """
    Method used to set a reference to a WebTide data point dictionary
    in the S102 tiles bounding boxes bundle at the desired level.

    DataSetId : The string id. of the regional dataset from which the
    WebTideObj was created.

    PointLatF : The latitude of the WebTide data point in floating point format.

    PointLonF : The longitude of the WebTide data point in floating point format.

    PointDataDict : The dictionary that we want to set the reference in the tiles
    bundle at the target S102 level.

    WebTideObj : The regional input data WebTide object from which the PointDataDict have been taken.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #-- NOTE: Fool-proof checks are commented for performance reasons. You can uncomment
    #      them to get (a lot) more details for debugging purposes.

    ##--- Uncomment for debugging:
    #if WebTideObj is None :
    #  sys.exit("ERROR "+methID+" WebTideObj is None !\n")

    ##--- Uncomment for debugging:
    #if WebTideObj._s102TilesObj is None :
    #  sys.exit("ERROR "+methID+" WebTideObj._s102TilesObj is None !\n")

    ##--- Uncomment for debugging:
    #if s102TilesObj._baseLevelTiles is None :
    #  sys.exit("ERROR "+methID+" s102TilesObj._baseLevelTiles is None !\n")

    ##--- Uncomment for debugging:
    #if s102TilesObj.LATITUDES_RANGE_ID[0] not in s102TilesObj._baseLevelTiles.keys() :
    #  sys.exit("ERROR "+methID+" s102TilesObj.LATITUDES_RANGE_ID[0] == "+
    #           s102TilesObj.LATITUDES_RANGE_ID[0]+" string id. key is not in s102TilesObj._baseLevelTiles keys !\n")

    ##--- Uncomment for debugging:
    #if WebTideObj._s102Level2Use is None :
    #  sys.exit("ERROR "+methID+" WebTideObj._s102Level2Use is None !\n")

    #--- We can have WebTide data points outside the West
    #    hemisphere in the Pacific(ne_pac4 dataset):
    if not WebTideObj._s102TilesObj.checkForNorthWestHemi(PointLatF, PointLonF, False) :

      if WarningsLog :
        sys.stdout.write("WARNING "+methID+": point latitude="+str(PointLatF)+" and-or point longitude="+
                         str(PointLonF)+" outside the North-West Hemisphere ! "+DataSetId+" data point rejected !\n")
      #---

      #--- Nothing more to do so get outta'here.
      return None

    #--- end outer if block.

    #--- We could have to deal with some area(s) where we have to exclude grid points:
    if WebTideObj._twoPointsExcludeBBoxTuple is not None :

      #sys.stdout.write("WARNING "+methID+" Checking to exclude point at for dataset -> "+DataSetId+" !\n")

      if WebTideObj.needToExcludePoint(PointLatF, PointLonF, WebTideObj._twoPointsExcludeBBoxTuple) :

        if WarningsLog :
          sys.stdout.write("WARNING "+methID+" Need to exclude point at lat,lon-> "+
                            str(PointLatF)+", "+str(PointLonF)+" for dataset -> "+DataSetId+" !\n")
        #---

        #--- Nothing more to do so get outta'here
        return None

      #--- end inner if block WebTideObj.needToExcludePoint(pointLatF, pointLonF, WebTideObj._twoPointsExcludeBBoxTuple )
    #--- end outer block WebTideObj._twoPointsExcludeBBoxTuple is not None

    #--- Local shortcut to the GeoLandWaterMasks object in WebTideObj
    #    (NOTE: Could be None)
    landWaterMasksObj= WebTideObj._landWaterMasksObj

    #--- Check for dry grid point only if landWaterMasksObj is not None:
    if landWaterMasksObj is not None and \
      not landWaterMasksObj.isPoint2DWet(PointLonF, PointLatF) :

      if WarningsLog :
        sys.stdout.write("WARNING "+methID+" The dataset "+DataSetId +" point at latitude="+
                         str(PointLatF)+" and longitude="+str(PointLonF)+" is on land ! Point rejected !\n")
      #---

      #--- Nothing more to do so get outta'here
      return None
    #--- end if block.

    #--- Build the dictionary to be referenced from the data point
    #    numeric id. and a reference to the PointDataDict:
    tilePointDataDict= { str(PointDataDict[ IGeoJSON.POINT_ID[0] ]) : PointDataDict }

    #print("tilePointDataDict="+str(tilePointDataDict))

    #--- Use the @staticmethod setPointDataRefInTiles of
    #    S102DataUtil class to locate the data point inside
    #    a valid tile.
    return S102DataUtil.setPointDataRefInTiles( DataSetId,
                                                PointLatF,
                                                PointLonF,
                                                tilePointDataDict,
                                                WebTideObj )
  #---
  def getPredictionsForTile( self, TidalPrdFactoryObj, WebTideObj,
                             TileId, TileDict, DateTimeStampsDict, InfoLog= False ) :
    """
    Method used to "encapsulate" the tidal prediction method used.

    TidalPrdFactoryObj : The TidalPrd object going with the WebTide dataset object WebTideObj
    from which the tile data dictionary was extracted.

    WebTideObj : The regional input data WebTide object from which the tile data dictionary
    was extracted.

    TileId : The id. of the tile going with the TileDict.

    TileDict : The WebTide tile dictionary holding the tidal constituents data
    used to compute tidal predictions.

    DateTimeStampsDict : A dictionary holding all the timestamps(as seconds since the epoch)
    as the keys) needed for the predictions. The contents of the dictionary
    are the corresponding timestamps as strings.

    InfoLog<OPTIONAL,default==False> : To put(or not to) log INFO messages on the stdout file stream.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #-- NOTE: Fool-proof checks are commented for performance reasons. You can uncomment
    #      them to get (a lot) more details for debugging purposes.

    ##--- Uncomment for debugging.
    #if TidalPrdFactoryObj is None :
    #  sys.exit("ERROR "+methId+" TidalPrdFactoryObj is None !\n")

    ##--- Uncomment for debugging:
    #if WebTideObj is None :
    #  sys.exit("ERROR "+methId+" WebTideObj is None !\n")

    ##--- Uncomment for debugging:
    #if WebTideObj._s102Level2Use is None :
    #  sys.exit("ERROR "+methId+" WebTideObj._s102Level2Use is None !\n")

    ##--- Uncomment for debugging:
    #if WebTideObj._s102Level2Use is None :
    #  sys.exit("ERROR "+methId+" WebTideObj._s102Level2Use is None !\n")

    #--- Shortcut to the WebTideObj._s102TilesObj
    #s102TilesObj= WebTideObj._s102TilesObj

    ##--- Uncomment for debugging:
    #if TileId is None :
    #  sys.exit("ERROR "+methId+" TileId is None !\n")

    ##--- Uncomment for debugging:
    #if TileDict is None :
    #  sys.exit("ERROR "+methId+" TileDict is None !\n")

    ##--- Uncomment for debugging:
    #if WebTideObj._meeMySelfAndI is None:
    #  sys.exit("ERROR "+methId+" WebTideObj._meeMySelfAndI is None !\n")

    ##--- Uncomment for debugging:
    #if TileDict[ IS102.LEVEL_ID[0] ] != WebTideObj._s102Level2Use[0] :
    #  sys.exit("ERROR "+methId+" TileDict[ IS102.LEVEL_ID[0] ] -> "+str(TileDict[ IS102.LEVEL_ID[0] ])+
    #                   " != WebTideObj._s102Level2Use[0] -> "+str(WebTideObj._s102Level2Use[0])+" !\n")

    ##--- Uncomment for debugging:
    #if TileDict[ self.MODEL_NAME_ID[0] ] != WebTideObj._meeMySelfAndI[0] :
    #  sys.exit("ERROR "+methId+" Dataset mismatch between TileDict[ self.MODEL_NAME_ID[0] ] ->"+
    #                    TileDict[ self.MODEL_NAME_ID[0] ]+" and dataSetId -> "+WebTideObj._meeMySelfAndI[0]+" !\n")

    if InfoLog :
      sys.stdout.write("INFO "+methId+" Computing tidal predictions for tile -> "+
                        TileId+" with dataset -> "+WebTideObj._meeMySelfAndI[0]+"\n")
    #---

    #--- Compute the predictions for the data points of the tile.
    WebTideObj.getTilePredictions( TidalPrdFactoryObj, TileDict, DateTimeStampsDict)

    #--- Really slower with assignation for TileDict ???
    #TileDict= WebTideObj.getTilePredictions( TidalPrdFactoryObj, TileDict, DateTimeStampsDict )

    if InfoLog :
      sys.stdout.write("INFO "+methId+" end \n")
    #---

    #--- Return the TileDict to signal that the tile have predictions for the output.
    return TileDict

  #--- End method getPredictionsForTile
