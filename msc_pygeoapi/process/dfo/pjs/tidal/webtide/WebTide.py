#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidaprd/webtide/WebTide.py
# Creation        : August/Aout 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidaprd.webtide.WebTide implementation.
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

#---
import os
import sys
import math
import inspect

#---
from dhp.geo.Geo import Geo
from dhp.sfmt.ISFMT import ISFMT
from dhp.sfmt.s102.IS102 import IS102
from dhp.sfmt.s104.IS104 import IS104
from dhp.util.Vector2D import Vector2D
from dhp.tidalprd.TidalPrd import TidalPrd
from dhp.tidalprd.ITidalPrd import ITidalPrd
from dhp.util.Trigonometry import Trigonometry
from dhp.tidalprd.webtide.GeoJSON import GeoJSON
from dhp.tidalprd.webtide.IWebTide import IWebTide

#--- WebTide tidal predictions calculations are normally
#    (as of 20191031) done using M. Foreman's method
from dhp.tidalprd.astro.foreman.IForeman import IForeman

#---
class WebTide(IWebTide, TidalPrd, Geo) :

  """
  Instance objects of class WebTide are used to hold a specific WebTide
  dataset(Ex. ne_pac4) input data and to provide some data processing methods
  (Ex. getTilePredictions) to help produce the SFMT DHP made with WebTide
  input data. The S111,S104 data files produced with WebTide input data is intended
  to be used as backups in the eventuality that we do not have any access to ECCC
  and DFO NEMO family models results.
  """

  #---
  def __init__(self, DataSetId, DataSetFile, Format,
               S102TilesObj, DataSetDict, TidalFieldsType) :
    """
    DataSetId: The string id. of a regional WebTide dataset which will be used
    as input data to produce predictions of tidal currents and or water levels
    for the S104 and-or S111 data files automated production.

    DataSetFile : The dataset input data file.

    Format : The file format of the input data file.

    S102TilesObj : A S102 class object instance. It is not a S102Tiles class object
    despite its name.

    DataSetDict : A JSON formatted dictionary holding the WebTide dataset input data.

    TidalFieldsType : The tidal predictions fields wanted(i.e. CURRENTS, WATERLEVELS, ...)
    """

    #---
    Geo.__init__(self)
    IWebTide.__init__(self)
    TidalPrd.__init__(self)

    methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + str(" method:")

    #--- Store the dataset id. in self._meeMySelfAndI
    self._meeMySelfAndI= None

    #--- Declare some important parameters to keep as attributes
    #    inside self object instances.
    self._constsNames= None
    self._s102Level2Use= None
    self._tilesWithData= None
    self._fieldsVarsIds= None
    self._fieldsVarsType= None
    self._fieldsVarsIdsDict= None
    self._dataSetLatRadAvg= None

    #--- Some other parameters to keep as attributes
    #    inside self object instances.
    self._landWaterMasksObj= None
    self._uvRotationParamsDict= None
    self._twoPointsExcludeBBoxTuple= None

    #--- method reference(a.k.a. function-method pointer in C,C++ jargon)
    #    to the DFO classic de-facto legacy Foreman procedure which is the default.
    #    TODO: Implement the possibility to specify other tidal predictions
    #    than the default one:
    self.getTilePredictions= self.getForemanTilePredictions

    #--- Some fool-proof checks:
    if DataSetId is None :
      sys.exit("ERROR "+methID+" DataSetId is None !\n")

    #---
    self._meeMySelfAndI= ( DataSetId ,)

    if DataSetFile is None :
      sys.exit("ERROR "+methID+" DataSetFile is None !\n")

    if Format is None :
      sys.exit("ERROR "+methID+" Format is None !\n")

    if Format not in IWebTide._IWebTide__ALLOWED_DATASETS_FORMATS :
      sys.exit("ERROR "+methID+" Invalid Format -> "+ Format.name +" !\n")

    #--- Only geojson input format allowed for now for WebTide datasets:
    if Format != IWebTide._IWebTide__ALLOWED_DATASETS_FORMATS.GEOJSON :
      sys.exit("ERROR "+methID+" Only GEOJSON dataset format allowed !\n")

    if S102TilesObj is None :
      sys.exit("ERROR "+methID+": S102TilesObj is None ! !\n")

    #--- Keep a reference to the S111Obj.S102Tile in self for later usage:
    self._s102TilesObj= S102TilesObj

    if DataSetDict is None :
      sys.exit("ERROR "+methID+": DataSetDict is None ! !\n")

    if TidalFieldsType is None :
      sys.exit("ERROR "+methID+" TidalFieldsType is None !\n")

    #--- Keep a ref. to the TidalFieldsType in self object:
    self._fieldsVarsType= TidalFieldsType

    #--- Get the field variable(s) ids. from the static ITidalPrd.FIELDS_IDS dictionary:
    tidalVarsIds= ITidalPrd.FIELDS_IDS[ self._fieldsVarsType ]

    #--- Check if the field variable(s) ids. defined in the dataset dict. are(is) valid.
    if IS102.PRODUCT_LEVEL_ID[0] not in DataSetDict.keys() :
      sys.exit("ERROR "+methID+" IS102.PRODUCT_LEVEL_ID[0] key -> "+
                IS102.PRODUCT_LEVEL_ID[0] +" not present in DataSetDict kyes !\n")
    #---

    #--- Extract the S102 level wanted for this dataset and store it
    #    in self for subsequent usage by other methods:
    self._s102Level2Use= tuple( DataSetDict[ IS102.PRODUCT_LEVEL_ID[0] ] )

    #--- Check if the requested S102 level is a valid one:
    if self._s102Level2Use[0] not in IS102.TILES_ALLOWED_LEVELS :
      sys.exit("ERROR "+methID+
               " Invalid S102 tiles level ->"+self._s102Level2Use[0]+" !\n")
    #---

    sys.stdout.write("INFO "+methID+" start\n")

    sys.stdout.write("INFO "+methID+" DataSetId -> "+self._meeMySelfAndI[0]+"\n")
    sys.stdout.write("INFO "+methID+" DataSetFile -> "+DataSetFile+"\n")
    sys.stdout.write("INFO "+methID+" Format -> "+Format.name+"\n")
    sys.stdout.write("INFO "+methID+" self._s102Level2Use[0]="+str(self._s102Level2Use[0])+"\n")

    #sys.stdout.write("INFO "+methID+" TidalFieldsIds -> "+str(TidalFieldsIds)+"\n")

    #--- Check if we have some zones(lat-lon regular bounding boxes) from which
    #    we have to exclude input data grid points:
    if IS102.EXCLUDE_POINTS_ID[0] in DataSetDict.keys() :

      #--- Keep a reference to the TwoPointsExcludeBBoxTuple in self for later usage:
      #    (NOTE: Could be None)
      self._twoPointsExcludeBBoxTuple= tuple( DataSetDict[ IS102.EXCLUDE_POINTS_ID[0] ] )
    #---

    #--- Uncomment for using land-water masks.
    #    NOTE : Still need more testing and validation.
    #    TODO : Implement usage of CHS ENC charts(converted to SHP format)
    #           for land-water masks:
    #
    #if self.DATASETS_JSON_IDS.CanCoastLinesLandShpFiles.name in DataSetDict.keys() :
    #  landWaterMaskFilesList= dataSetDict[self.DATASETS_JSON_IDS.CanCoastLinesLandShpFiles.name]
    #  sys.stdout.write("INFO "+methID+" Using land-water polygons mask file(s) ->"+str(landWaterMaskFilesList)+"\n")
    #  self._landWaterMasksObj= GeoLandWaterMasks(landWaterMasksDir, tuple(landWaterMaskFilesList))

    #--- check for possible U,V currents components rotation for a dataset:
    if self.JSON_DATASET_ROTATION_ID[0] in DataSetDict.keys() :

      #--- Keep the U,V currents components rotation parameters in self object:
      self._uvRotationParamsDict= DataSetDict[ self.JSON_DATASET_ROTATION_ID[0] ]

      ##--- Check if we got something to rotate :
      #if self.UUC_ID[0] not in tidalVarsIds :
      #  sys.exit("ERROR "+methID+
      #                   " Currents components rotation: No U currents component variables defined in tidalVarsIds !\n")
      ##---
      #if self.VVC_ID[0] not in tidalVarsIds :
      #  sys.exit("ERROR "+methID+
      #                   " Currents components rotation: No V currents component variables defined in tidalVarsIds !\n")
      ##---

      #---
      sys.stdout.write("INFO "+methID+" Got UV components rotations -> "+
                        str(self._uvRotationParamsDict)+" to do for dataset -> "+DataSetId+"\n")
    #--- end if block.

    sys.stdout.write("INFO "+methID+" Using tidalVarsIds -> "+
                     str(tidalVarsIds)+" as fields id(s) to search in the WebTide dataset\n")

    #--- Check if we really got the two currents components:
    if self.UUC_ID[0] in tidalVarsIds and self.VVC_ID[0] not in tidalVarsIds :
      sys.exit("ERROR "+methID+" Only tidal current component ->"+self.UUC_ID[0]+
               " defined in tidalVarsIds ! ! Need ->"+self.UUC_ID[0]+" component also !\n")
    #---

    if self.VVC_ID[0] in tidalVarsIds and self.UUC_ID[0] not in tidalVarsIds:
      sys.exit("ERROR "+methID+" Only tidal current ->"+self.VVC_ID[0]+
               " defined in tidalVarsIds ! Need ->"+self.UUC_ID[0]+" component also !\n")
    #---

    #--- Get and put the WebTide data in the relevant S102 tiles:
    #    TODO: add code to deal with other datasets formats than GeoJSON:
    GeoJSON(self._meeMySelfAndI[0], DataSetFile, tidalVarsIds, self, False)

    sys.stdout.write("INFO "+methID+" end\n")

  #---
  def getForemanTilePredictions(self, ForemanFactoryObj, TileDict, DateTimeStampsDict,
                                Deg2RadConversion= True, UseDataSetLatavg= False, InfosLog= False) :
    """
    Compute all the tidal predictions for all timestamps needed for all WebTide
    data grid points enclosed in a S102 bounding box tile. The predictions are computed
    for water levels(if the WebTide dataset from which the data points comes from have
    the WL constituents, STLE400 dataset does not have those) or currents or both depending
    on the self._fieldsVarsIds tuple contents.

    ForemanFactoryObj : The ForemanFactory object going with the dataset from which
    the data points comes from.

    TileDict: A tile data dictionary.

    DateTimeStampsDict : A dictionary holding all the timestamps(as seconds since the epoch)
    as the keys) needed for the predictions. The contents of the dictionary
    are the corresponding timestamps as strings.

    Deg2RadConversion<OPTIONAL,default==True> : A flag to indicate that the degrees to radians
    conversion need(or does not need) to be applied to the Greenwich phase lags data.

    UseDataSetLatavg<OPTIONAL,default==False> : A flag to indicate that the latitudes averages
    of the grid points of a dataset need(or does not need) to be used for the tidal predictions
    instead of using each data points unique latitude(which is the default). The latitudes
    averages was mainly used for validation but can be activated if it is necessary.+

    InfoLog<OPTIONAL,default==True> : To put(or not to) log INFO messages on the stdout file stream.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + str(" method:")

    ##--- Commented fool-proof checks, Uncomment for debugging
    #if ForemanFactoryObj is None :
    #  sys.exit("ERROR "+methID+" ForemanFactoryObj is None !\n")

    ##--- Uncomment for debugging
    #if TileDict is None :
    #  sys.exit("ERROR "+methID+" TileDict is None !\n")


    #print str(TileDict.keys())
    #print TileDict["S102LevelOut"]

    ##--- Uncomment for debugging
    #if self._constsNames is None :
    #  sys.exit("ERROR "+methID+" self._constsNames is None !\n")

    ##--- Uncomment for debugging
    #if self._fieldsVarsIds is None :
    #  sys.exit("ERROR "+methID+" self._fieldsVarsIds is None !\n")

    ##--- Uncomment for debugging
    #if self._fieldsVarsIdsDict is None :
    #  sys.exit("ERROR "+methID+" self._fieldsVarsIdsDict is None !\n")

    ##--- Uncomment for debugging
    #if self._s102TilesObj is None :
    #  sys.exit("ERROR "+methID+" self._s102TilesObj is None !\n")

    #--- Local shorcut to self._s102TilesObj:
    s102TilesObj= self._s102TilesObj

    #--- Shortcut to the WebTide points input data dictionary in the S102 tile:
    tilePointsDataInDict= TileDict[ self.POINTS_DATAIN_ID[0] ]

    #--- Create the POINTS_DATAOUT dictionary in tilePointsDataDict if not already created:
    if self.POINTS_DATAOUT_ID[0] not in TileDict.keys() :
      TileDict[ self.POINTS_DATAOUT_ID[0] ]= {}

    #--- Shortcut to the WebTide points output data dictionary in the S102 tile:
    tilePointsDataOutDict= TileDict[ self.POINTS_DATAOUT_ID[0] ]

    #--- Extract the F_NODAl_MOD_ADJ_INIT value from the static data:
    fNodalModAdjInit= \
      ForemanFactoryObj.staticData[ self.ASTRO_PARAMS_ID[0] ][ self.F_NODAL_MOD_ADJ_INIT_ID[0] ]

    #--- Check if we have to rotate currents U,V components
    #    after their computation:
    if self._uvRotationParamsDict is not None :

      #--- Extract rotation direction from self._uvRotationParamsDict:
      jsonParamsDirection= self._uvRotationParamsDict[ self.JSON_ROT_DIRECTION_ID[0] ]

      rotation2DMethodsAllowed= tuple(self._2DRotationMethods.keys())

      #--- Check if the jsonParamsDirection is a valid one:
      if jsonParamsDirection != rotation2DMethodsAllowed :
        sys.exit("ERROR "+methID+" Invalid rotation direction -> "+jsonParamsDirection+" !\n")
      #---

      #--- Set the reference to the appropriate 2D rotation method:
      rotation2DMethodRef= self._2DRotationMethods[jsonParamsDirection]

      #--- Use a local Vector2D object to do the UV components rotations:
      v2d= Vector2D()

      jsonParamsCosSinAngles= tuple(self._uvRotationParamsDict[ self.JSON_ROT_COSSIN_ID[0] ])

      #astroStaticParamsId= self.ASTRO_PARAMS_ID[0]

      #--- Shortcut to the astro static parameters data:
      astroStaticParamsData= ForemanFactoryObj.staticData[ self.ASTRO_PARAMS_ID[0] ]

      rotationAngleCos= jsonParamsCosSinAngles[ astroStaticParamsData[ self.COS_IDX_ID[0] ] ]
      rotationAngleSin= jsonParamsCosSinAngles[ astroStaticParamsData[ self.SIN_IDX_ID[0] ] ]

    #--- end if block.

    #--- Define the strings ids. shorcuts for the amplitude and phase fields used in loops:
    phaseValueStrId= self.TIDAL_COMP_IDS[ ITidalPrd.PHASE_ID[0] ]
    amplitudeValueStrId= self.TIDAL_COMP_IDS[ ITidalPrd.AMPLITUDE_ID[0] ]

    sortedTilePointsDataInDict= tuple( sorted( tuple(tilePointsDataInDict.keys()) ), key=int)

    #dataSetLatAvgRad= self.DEGREES_2_RADIANS[0] * WebTideObj._dataSetLatAvg

    if InfosLog :
      sys.stdout.write("INFO "+methID+" Got -> "+str(len(sortedTilePointsDataInDict))+" points to process \n")

    #--- Loop on all input WebTide points in the tile dictionary and set them for the predictions:
    for pointDataDictId in sortedTilePointsDataInDict :

      #--- Shortcut to the point input data in tilePointsDataDict
      pointDataInDict= tilePointsDataInDict[pointDataDictId]

      #print("pointDataDictId="+pointDataDictId +", data="+ str(pointDataInDict))

      #--- Build the point(as an unary tuple) string key for the point output predictions:
      pointStrKey= ( s102TilesObj.getPointStrKeyId( pointDataInDict[ self.POINT_LON_ID[0] ],
                                                    pointDataInDict[ self.POINT_LAT_ID[0] ] ) ,)

      #--- Create the point data dictionary for output in tilePointsDataDict
      tilePointsDataOutDict[ pointStrKey[0] ]= { }

      #--- Shortcut to the point data dictionary for output:
      pointDataOutDict= tilePointsDataOutDict[ pointStrKey[0] ]

      #--- Possible presence of a specific chart datum conversion value for the point:
      #    Transfer the chart datum conversion value in pointDataOutDict for the outputs.
      if IS104.CHART_DATUM_CONV_ID[0] in pointDataInDict :
        pointDataOutDict[IS104.CHART_DATUM_CONV_ID[0]]= pointDataInDict[IS104.CHART_DATUM_CONV_ID[0]]

      #--- Accumulate all ForemanConstituentAstro objects created for this WebTide point in local fcaObjects(temp. list for now)
      fcaObjects= []

      for constName in self._constsNames :

        #--- Populate the fcaObjects list in the outer loop on constituents:
        if constName not in tuple( pointDataInDict.keys() ):

          #--- Need to create the sub dictionary for the constituent in pointDataDict:
          pointDataInDict[constName]= {}

          #--- Each tidal constituent have its own ForemanConstituentAstro object to use:
          pointDataInDict[constName][ IForeman.CONST_ASTRO_ID[0] ]= \
            ForemanFactoryObj.getNewConstituentObj(constName, fNodalModAdjInit, fcaObjects)
        #--- end if constName not in pointDataDict :

        for fieldsVarId in self._fieldsVarsIds :

          #print str(self._fieldsVarsIdsDict[constName][fieldsVarId])
          phaseFieldStr= self._fieldsVarsIdsDict[constName][fieldsVarId][0]
          amplitudeFieldStr= self._fieldsVarsIdsDict[constName][fieldsVarId][1]

          #--- Ensure that the amplitudes and phases values extracted from the dataset are floats:
          phaseValue= float( pointDataInDict[phaseFieldStr] )
          amplitudeValue= float( pointDataInDict[amplitudeFieldStr])

          #--- Conversion of the phase from decimal degrees to radians by default unless Deg2RadConversion==False
          if Deg2RadConversion : phaseValue *= self.DEGREES_2_RADIANS[0]

          #--- Add the constituent data to the grid point dictionary with the relevant string indices for subsequent retreivals.
          pointDataInDict[constName][fieldsVarId]= {}

          #--- Set the tidal constituent phase in pointDataDict for the variable fieldsVarId:
          pointDataInDict[constName][fieldsVarId][phaseValueStrId]= phaseValue

          #--- Set the tidal constituent amplitude in pointDataDict for the variable fieldsVarId:
          pointDataInDict[constName][fieldsVarId][amplitudeValueStrId]= amplitudeValue

          #print "constName: "+constName+", data="+str(pointDataInDict[constName])

        #-- end for fieldsVarId in self._fieldsVarsIds :
      #--- end for constName in self._constsNames :

      #print str(self._constsNames)
      #print str(pointDataInDict)

      #--- fcaObjects is constant(in this method only) at this point so convert it to a tuple.
      fcaObjects= tuple(fcaObjects)

      timeIncrSeconds= ForemanFactoryObj._timeIncrSeconds

      timeStartSeconds= ForemanFactoryObj._secondsSinceEpochStart
      timeEndSeconds= ForemanFactoryObj._secondsSinceEpochEnd

      if UseDataSetLatavg :
        #--- Using dataset points latitudes radians average:
        latRad= ( self._dataSetLatRadAvg[0] ,)

      else :
        #--- Using each point latitude in radians for astronomic infos.
        latRad= ( self.DEGREES_2_RADIANS[0] * float( pointDataInDict[ self.POINT_LAT_ID[0] ] ) ,)

      #print "latRad="+str(latRad)

      #--- Set the shallow water constituents references to the relevant main constituents astronomic infos.
      ForemanFactoryObj.setShWtDerivationObjectsRfs(fcaObjects)

      #--- Loop on all timestamps needed:
      for timeIncr in tuple(sorted( tuple(DateTimeStampsDict.keys()) )) :

        dateTimeStringZ= DateTimeStampsDict[timeIncr]
        #dateTimeStringZ= self.getDateTimeStringZ(timeIncr)

        #print("timeIncr="+str(timeIncr))
        #print("dateTimeStringZ="+dateTimeStringZ)

        #--- Create the point time-stamped output dictionary in pointDataOutDict
        pointDataOutDict[dateTimeStringZ]= {}

        #--- Get the evolving time reference from the ForemanFactory object:
        timeRefDiff= ForemanFactoryObj.updateTimeRef( timeIncr, latRad[0], fcaObjects)

        #sys.stdout.write("INFO "+methID+" computing prediction at time incr.-> "+ dateTimeStringZ +"\n")

        #--- Init point currents and water level(if any) accumulators for this time stamp
        for varId in self._fieldsVarsIds :
          pointDataOutDict[dateTimeStringZ][varId]= 0.0

        #--- end loop for varId in fieldsVarsIdsTuple :

        #--- Compute the new tidal predictions at time-stamp dateTimeStringZ for the tidal variables in fieldsVarsIdsTuple :
        for varId in self._fieldsVarsIds :
          for fcaObj in fcaObjects :

            #--- Local shortcut to the WebTide point data dict for the constituent and variable combo:
            fcaVarPointInDict= pointDataInDict[fcaObj.getName()][varId]

            #--- The current value is accumulated in pointDataOutDict[dateTimeStringZ][varId]
            #    (Dictionay indexing with the dateTimeStringZ)
            pointDataOutDict[dateTimeStringZ][varId] += \
              fcaObj.computeTidalAmplitudeAt(fcaVarPointInDict[amplitudeValueStrId], fcaVarPointInDict[phaseValueStrId], timeRefDiff)

          #--- end for fcaObj in fcaObjects.
        #--- end for varId in fieldsVarsIdsTuple.

        #--- Rotate the u,v components ??
        if self._uvRotationParamsDict is not None :

          #--- Need to rotate UV components:
          #print "bef rotation:"+str(pointDataOutDict[dateTimeStringZ])

          v2d._iComp= pointDataOutDict[dateTimeStringZ][ self.UUC_ID[0] ]
          v2d._jComp= pointDataOutDict[dateTimeStringZ][ self.VVC_ID[0] ]

          #--- Rotate UV components of v2d according to rotationAngleCos and
          #    rotationAngleSin parameters: NOTE: rotation2DMethodRef is a
          #    reference(like a function pointer in C) to a specific 2D
          #    rotation method. NOTE: use a two items returned tuple here ??
          #    performance impact ??
          rotation2DMethodRef(rotationAngleCos, rotationAngleSin, v2d)

          #--- Update the uv data in pointDataOutDict with the rotated components:
          pointDataOutDict[dateTimeStringZ][ self.UUC_ID[0] ]= v2d._iComp
          pointDataOutDict[dateTimeStringZ][ self.VVC_ID[0] ]= v2d._jComp

          #print "aft. rotation:"+str(pointDataOutDict[dateTimeStringZ])
        #--- end block if self._uvRotationParamsDict is not None :
        #sys.stdout.write("INFO "+methID+" Done with time-stamp -> "+dateTimeStringZ+"\n")
      #--- end for timeIncr in range(timeStartSeconds, timeEndSeconds, timeIncrSeconds) :

      #print str(pointDataOutDict.keys())
      #sys.stdout.write("INFO "+methID+" exit 0 \n")

      #--- Set the pointDataInDict object to None to allow the
      #    garbage collector to sweep the now useless input data memory.
      pointDataInDict= None

      #sys.stdout.write("INFO "+methID+" Done for all time-stamps for pointDataDictId -> "+pointDataDictId +"\n")

    #--- end loop for pointDataDictId in sortedTilePointsDataInDict

    #--- Set the tilePointsDataInDict object to None to allow the
    #    garbage collector to sweep the now useless input data memory.
    tilePointsDataInDict= None

    #print str(TileDict["POINTS_DATAOUT"].keys())
    #sys.stdout.write("INFO "+methID+" exit 0\n")
    #sys.exit(0)

    if InfosLog:
      sys.stdout.write("INFO "+methID+" End \n")

    return TileDict

  #--- end method getTilePredictions
 
  #---
  @staticmethod
  def getFormatId(RequestedId) :

    """
    Get the WebTide allowed dataset format enum.Enum object type
    from the IWebTide._IWebTide__ALLOWED_DATASETS_FORMATS.

    RequestedId (type->string): A string normally extracted from 
    a JSON config. dictionary which represents the input format 
    to be used for WebTide input data.

    return (type->enum.Enum) : The enum.Enum object type for the
    input format wanted if the RequestedId represents an allowed
    input format, otherwise we have an ERROR and the exec. flow 
    is stopped.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    ##--- Uncomment for debugging
    #if RequestedId is None:
    #  sys.stderr.write("ERROR "+methID+" RequestedId is None !\n")  
    #  sys.exit(1)

    found= False
    
    #--- Loop on all allowed dataset formats enum.Enum objects:
    for enumId in IWebTide._IWebTide__ALLOWED_DATASETS_FORMATS :

      #--- We have a match with the strings RequestedId argument
      #    and an allowed dataset formats enum.Enum object: 
      if RequestedId == enumId.name :

        found= True
        break

      #--- end if block.
    #--- End block loop for enumId.

    #--- RequestedId not valid, abandon ship !
    if not found :
      
      sys.stderr.write("ERROR "+methID+" Invalid WebTide format Id request -> "+CheckId +
                       " ! Must be one of -> "+IWebTide._IWebTide__ALLOWED_DATASETS_FORMATS.__members__.keys()+"\n")  
      sys.exit(1)

    #--- Return the 
    return IWebTide._IWebTide__ALLOWED_DATASETS_FORMATS[RequestedId]  
