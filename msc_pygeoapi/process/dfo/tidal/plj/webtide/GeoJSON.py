#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidaprd/webtide/GeoJSON.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidaprd.webtide.GeoJSON implementation.
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
from dhp.sfmt.ISFMT import ISFMT
from dhp.sfmt.s102.IS102 import IS102
from dhp.sfmt.s104.IS104 import IS104
from dhp.util.JsonCfgIO import JsonCfgIO
from dhp.tidalprd.TidalPrd import TidalPrd
from dhp.tidalprd.ITidalPrd import ITidalPrd
from dhp.util.Trigonometry import Trigonometry
from dhp.util.IDataIndexing import IDataIndexing
from dhp.tidalprd.webtide.IGeoJSON import IGeoJSON
from dhp.tidalprd.webtide.IWebTide import IWebTide
from dhp.sfmt.s102.S102DataUtil import S102DataUtil
from dhp.tidalprd.webtide.WebTideTiles import WebTideTiles

#---
class GeoJSON(IGeoJSON) :

  """
  Read and store all the relevant GeoJSON formatted WebTide data
  input for one specific dataset(nwatl, arctic9c and so on).
  """

  #---
  def __init__(self, DataSetId, WebTideGeoJSONFile,
               FieldsIds, WebTideObj, WarningsLog= False) :

    """
    DataSetId : The string id. of a regional WebTide dataset which will be used
    as input data to produce predictions of tidal currents and or water levels
    for the S104 and-or S111 data files automated production.

    DataSetFile : The GeoJSON format dataset input data file.
    FieldsIds :  Field variable(s) string ids.
    WebTideObj : A WebTide class object instance.
    WarningsLog <OPTIONAL,default==False> : To put(or not to) log WARNING messages on the stdout file stream.

    TODO: Add types in the previous arguments nomenclature.
    """

    IGeoJSON.__init__(self)

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #--- The usual fool-proof checks:
    if WebTideGeoJSONFile is None :
      sys.exit("ERROR "+methID+" WebTideGeoJSONFile is None !\n")

    if FieldsIds is None :
      sys.exit("ERROR "+methID+" FieldsIds is None !\n")

    if WebTideObj is None :
      sys.exit("ERROR "+methID+" WebTideObj is None !\n")

    if WebTideObj._s102TilesObj is None :
      sys.exit("ERROR "+methID+" WebTideObj._s102TilesObj is None !\n")

    #--- Local shortcut to the S102Tiles object of WebTideObj:
    s102TilesObj= WebTideObj._s102TilesObj

    if s102TilesObj._baseLevelTiles is None :
      sys.exit("ERROR "+methID+" s102TilesObj._baseLevelTiles is None !\n")

    sys.stdout.write("INFO "+methID+" start: DataSetId -> "+DataSetId+
                     ", WebTideGeoJSONFile -> "+WebTideGeoJSONFile+", FieldsIds -> "+str(FieldsIds)+"\n")

    if not os.access(WebTideGeoJSONFile,os.F_OK) :
      sys.exit("ERROR "+methID+" input file -> "+WebTideGeoJSONFile+" not found !\n")

    #--- Get the GeoJSON formatted WebTide data:
    gjWebTideDataSet= JsonCfgIO.getIt(WebTideGeoJSONFile)

    if gjWebTideDataSet is None :
      sys.exit("ERROR "+methID+
                       " Unable to get GeoJSON data with JsonCfgIO.getIt from file -> "+WebTideGeoJSONFile+" !\n")
    #---

    #--- Validate the CRS of the GeoJSON formatted WebTide data:
    gjHorizDatumCode= gjWebTideDataSet[ self.CRS_ID[0] ][ self.PROPS_ID[0] ][ self.CRS_NAME_ID[0] ]

    #--- NOTE: self._horizDatumCode is an unary tuple.
    if gjHorizDatumCode != self.ALLOWED_CRS[ self._horizDatumCode[0] ][0] :

       sys.exit("ERROR "+methID+" Invalid CRS -> "+gjHorizDatumCode+" for data in file -> "+
                 WebTideGeoJSONFile+" Must be -> "+self.ALLOWED_CRS[ self._horizDatumCode ][0]+" !\n")
    #---

    #--- Extract dictionary of the 1st point data.
    #    NOTE: self.POINTS_ID is an unary tuple.
    pointData0= gjWebTideDataSet[ self.POINTS_ID[0] ][0]

    #--- Reset WebTideObj._fieldsVarsIds and WebTideObj._constsNames:
    WebTideObj._constsNames= None
    WebTideObj._fieldsVarsIds= None

    #--- _tilesWithData: Dictionary to store tiles that have data grid points enclosed in it.
    WebTideObj._tilesWithData= {}

    #--- Temp. local Lists:
    constsNamesList= []
    fieldsVarsIdsList= []

    #--- Iterate on the tidal constituents fields definitions of the first data point for now:
    #    (only fields names tidal constituents meta-data, no data values for now).
    #    TODO: Use tuple(pointData0[ self.PROPS_ID[0] ]) here ?.
    for dataIter in pointData0[ self.PROPS_ID[0] ] :

      #--- Split the field string id extracted(use of chained methods) with the IWebTide.OGR_FIELDS_IDS_SEP separator:
      splitFieldId= dataIter.split(self.FIELDS_IDS_SEP[0])

      #--- check if we have a valid field to use:
      if len(splitFieldId) == self.FIELDS_IDS_LLEN[0] and \
           splitFieldId[ self.FIELDS_IDS_IDX[0] ] in FieldsIds :

        #--- Add the fields variable id to the fieldsVarsIdsList if not already done:
        if splitFieldId[ self.FIELDS_IDS_IDX[0] ] not in fieldsVarsIdsList :

          fieldsVarsIdsList.append(splitFieldId[ self.FIELDS_IDS_IDX[0] ])
        #---

        #--- Extract constituent name from the split:
        constName= splitFieldId[ self.CONST_NAME_IDX[0] ]

        #--- Verify that the constituent name is not in constsNamesList already:
        if constName not in constsNamesList :
          constsNamesList.append(constName)
        #---

      #--- end outer if block,
    #--- end loop for dataIter in pointData0.

    #--- Check we have found something for the FieldsIds wanted.
    #    It is an error if constsNamesList is empty.
    if len(constsNamesList) == 0 :
      sys.exit("ERROR "+methID+
               " No constituents fields definitions found for field(s) -> "+
               str(FieldsIds) +" for the WebTide dataset -> "+WebTideGeoJSONFile+" !\n")
    #---

    WebTideObj._constsNames= tuple(constsNamesList)
    WebTideObj._fieldsVarsIds= tuple(fieldsVarsIdsList)

    #---
    sys.stdout.write("INFO "+methID+" Found constituents fields components -> "+
                      str(fieldsVarsIdsList)+" in the WebTide dataset -> "+DataSetId+"\n")

    sys.stdout.write("INFO "+methID+
                     " And the following constituents -> "+str(WebTideObj._constsNames) +" will be used. \n")

    #--- Pre-define fields data extraction strings ids to reduce loops operations:
    phaseValueStrId= self.TIDAL_COMP_IDS[ ITidalPrd.PHASE_ID[0] ]
    amplitudeValueStrId= self.TIDAL_COMP_IDS[ ITidalPrd.AMPLITUDE_ID[0] ]

    WebTideObj._fieldsVarsIdsDict= {}

    #--- Outer loop on the tidal constituents names:
    for constName in WebTideObj._constsNames :

      WebTideObj._fieldsVarsIdsDict[constName]= {}

      #--- Inner loop on the field variable(s) (Water levels(Z) and or currents
      #    cartesian components(U,v)) to consider
      for fieldsVarId in WebTideObj._fieldsVarsIds :

        #--- Build field variable(s) ids strings for GeoJSON data extraction:
        phaseFieldStr= constName + self.FIELDS_IDS_SEP[0] + \
                       fieldsVarId + self.FIELDS_IDS_SEP[0] + phaseValueStrId

        amplitudeFieldStr= constName + self.FIELDS_IDS_SEP[0] + \
                           fieldsVarId + self.FIELDS_IDS_SEP[0] + amplitudeValueStrId

        WebTideObj._fieldsVarsIdsDict[constName][fieldsVarId]= (phaseFieldStr,amplitudeFieldStr)

      #--- end inner block loop for fieldsVarId in WebTideObj._fieldsVarsIds :
    #--- end outer block loop for constName in WebTideObj._constsNames :

    sys.stdout.write("INFO "+methID+
                     " GeoJSON WebTide tidal constituents data extraction, could take 1.5 mins for the larger datasets...\n")

    dataSetNbValidPoints= 0

    #--- For the dataset points latitudes average.
    dataSetLatAvg= 0.0

    #--- Loop on all points data dictionaries to extract
    #    constituents data for this WebTide dataset.
    #    TODO: Use tuple( gjWebTideDataSet[ self.POINTS_ID[0] ] ) here ?.
    for pointDict in gjWebTideDataSet[ self.POINTS_ID[0] ] :

      pointDataDict= pointDict[ self.PROPS_ID[0] ]

      #--- Ensure that lon-lat data are ASCII strings for dictionary indexing:
      pointLatStr= str( pointDataDict[ self.GEOJSON_POINT_LAT_ID[0] ] )
      pointLonStr= str( pointDataDict[ self.GEOJSON_POINT_LON_ID[0] ] )

      ##--- Only use data grid points which have am average water column
      ##    value which is smaller than a given threshold:
      #if WebTideObj._fieldsVarsType == ISFMT.DATA_TYPES.WATERLEVELS.name :
      #  pointBathy= float(pointDataDict[ self.POINT_BATHY_FIELD_ID[0] ])
      #  #sys.stdout.write("INFO "+methID+" pointBathy="+str(pointBathy)+"\n")
      #  #--- Skip data grid point(or not)
      #  if pointBathy > IS104.WL_DEPTH_THRESHOLD[0] :
      #
      #    if WarningsLog :
      #      sys.stdout.write("WARNING "+methID+
      #                       " point data at lon, lat -> "+pointLonStr+", "+pointLatStr+" from dataset -> "+DataSetId+
      #                       " have an average water column value exceeding -> "+str(IS104.WL_DEPTH_THRESHOLD[0])+" threshold !\n")
      #    continue

        #--- end inner if.
        #sys.stdout.write("INFO "+methID+" pointBathy="+str(pointBathy)+" Ok !\n")
      #--- end outer if.

      #--- Now we need numeric values for lat-lon data.
      pointLatF= float(pointLatStr)
      pointLonF= float(pointLonStr)

      #--- Locate the grid point in the S102 tiles limits dicionaries structure
      #    at the desired tiles level(2,5 or 6):
      checkRet= S102DataUtil.setPointDataRefInTiles(DataSetId, pointLatF, pointLonF,
                                                    pointDataDict, WebTideObj, WarningsLog)

      #--- Check if the point have been succesfully located in the tiles structure:
      if checkRet is None :

        if WarningsLog :
          sys.stdout.write("WARNING "+methID+" Nothing to do with point data at lon, lat -> "+
                           pointLonStr+", "+pointLatStr+" from dataset -> "+DataSetId+" !\n")

        #--- Need to reject data grid point then go for the next data point to process.
        continue

      #--- Get the chart datum correction from the tidal constituents Z amplitudes
      #    BUT only if IS104.CHART_DATUM_CONV_ID[0] is not already defined in pointDataDict:
      #    (It could be eventally already defined in the json input data see TODO1 below)
      if IDataIndexing.UVZ_IDS.Z.name in WebTideObj._fieldsVarsIds \
           and IS104.CHART_DATUM_CONV_ID[0] not in pointDataDict.keys() :

        #sys.stdout.write("INFO "+methID+" Need to get chart datum correction for all data points\n")

        #--- TODO1: Implement the official chart datum conversion method(which still need
        #          to be determined as of 2018-12-05)
        #    TODO2: Implement a method reference select to quickly switch between
        #           ad-hoc and the eventual official chart datum conversion method.
        TidalPrd.getAdHocChartDatumCorrection(self.WLZ_AMP_STR_ID, pointDataDict)

      #--- end if block for chart datum conversion:

      #--- Update the latitudes average accumulator
      #    and the nb. points counter:
      dataSetLatAvg += pointLatF
      dataSetNbValidPoints += 1

      #sys.stdout.write("INFO "+methID+" after setPointDataRefInTiles \n")
      #sys.stdout.write("INFO "+methID+" exit 0 \n")

    #--- end loop for pointDict in gjWebTideDataSet[ self.POINTS_ID[0] ]

    #--- Could happen but very unlikely.
    if dataSetNbValidPoints == 0 :
      sys.exit("ERROR "+methID+ "dataSetNbValidPoints == 0 ! DataSetId -> "+DataSetId+"\n")
    #---

    #--- Convert the latitudes average to radians for tidal predictions needs:
    WebTideObj._dataSetLatRadAvg= ( self.DEGREES_2_RADIANS[0] * dataSetLatAvg/dataSetNbValidPoints ,)

    sys.stdout.write("INFO "+methID+
                     " WebTideObj._dataSetLatRadAvg[0]="+str(WebTideObj._dataSetLatRadAvg[0])+"\n")

    #print str(WebTideObj._tilesWithData.keys())

    #--- Fool-proof check on the number of valid(i.e. having the minimum nb.
    #    of grid points enclosed) tiles
    nbTilesWithData= len(WebTideObj._tilesWithData.keys())

    #--- Could happen but unlikely.
    if nbTilesWithData == 0 :
      sys.exit("ERROR "+methID+
                       " len(WebTideObj._tilesWithData.keys()) == 0 ! No S102 tiles found for WebTide dataset ->"+DataSetId+" !\n")
    #---

    sys.stdout.write("INFO "+methID+" Got -> "+
                      str(nbTilesWithData)+" valid tiles for dataset "+DataSetId+"\n")

    sys.stdout.write("INFO "+methID+" end\n")

  #--- end __init__ method block.
