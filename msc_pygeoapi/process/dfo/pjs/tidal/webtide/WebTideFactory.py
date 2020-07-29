#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidaprd/webtide/WebTideFactory.py
# Creation        : August/Aout 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidaprd.webtide.WebTideFactory implementation.
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
import multiprocessing

#---
from msc_pygeoapi.process.dfo.pjs.util.JsonCfgIO import JsonCfgIO
from msc_pygeoapi.process.dfo.pjs.tidal.ITidalPrd import ITidalPrd
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.pjs.tidal.webtide.WebTide import WebTide
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.IS102 import IS102
from msc_pygeoapi.process.dfo.pjs.tidal.webtide.IWebTide import IWebTide
from msc_pygeoapi.process.dfo.chs.enav.pjs.util.FilesDirs import FilesDirs
from msc_pygeoapi.process.dfo.pjs.tidal.astro.foreman.IForeman import IForeman
from msc_pygeoapi.process.dfo.pjs.tidal.webtide.WebTideOutput import WebTideOutput
from msc_pygeoapi.process.dfo.chs.enav.pjs.models.ModelDataAttr import ModelDataAttr
from msc_pygeoapi.process.dfo.pjs.tidal.astro.foreman.ForemanFactory import ForemanFactory

#--- No land-waters masks used for now but we plan
#    to possibly use some(espacially near the ports) in the future.
#from dhp.geo.GeoLandWaterMasks import GeoLandWaterMasks

#---
class WebTideFactory(WebTideOutput, IS102, ModelDataAttr) :

  """
  Class used mainly for WebTide code modularization. It is not used
  like a real Java "factory" class mechanism despite its name. It is used
  to hold the WebTide datasets objects needed for production of the S104,
  S111 data files used as backups for the canadian coastal waters in the
  eventuality that we do not have access to DFO-ECCC joint venture NEMO
  models results.
  """

  #---
  #def __init__(self, SFMTFactoryObj, ParamsDict, AltOutputFormat= None) :
  def __init__( self,
                SFMTObjInst,
                ParamsDict: dict,
                AltOutputFormat: str = None) :
    """
    SFMTObjInst (type->SFMTObj) : A SFMTObj class instance object.

    ParamsDict : (type->dict) The dictionary holding the main parameters config.

    AltOutputFormat (type->str) <OPTIONAL, default==None> : An alternative output
    format(not a S1** one) to use.
    """

    #---
    IS102.__init__(self)
    ModelDataAttr.__init__(self)

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + str(" method:")

    #--- Usual fool-proof checks:
    if SFMTObjInst is None :
      sys.exit("ERROR "+methId+" SFMTObjInst is None !")

    if SFMTObjInst._sFMTFactoryObj is None :
      sys.exit("ERROR "+methId+" SFMTObjInst._sFMTFactoryObj is None !")

    #--- Local shortcut ref. to SFMTObjInst._sFMTFactoryObj
    sFMTFactoryObj= SFMTObjInst._sFMTFactoryObj

    #--- Need to __init__ WebTideOutput after the
    #    1st fool proof checks have been done.
    WebTideOutput.__init__(self, SFMTObjInst, sFMTFactoryObj)

    #--- Some more fool-proof checks:
    if ParamsDict is None :
      sys.exit("ERROR "+methId+" ParamsDict is None !")

    #print("ParamsDict="+str(ParamsDict))
    #print("sFMTFactoryObj._inputDataCfgDict="+str(sFMTFactoryObj._inputDataCfgDict))
    #print(methId+"exit 0")
    #sys.exit(0)

    #--- sFMTFactoryObj._mainCfgDir : The path of the parent directory
    #    where to find WebTides datasets config. file(s).
    if sFMTFactoryObj._mainCfgDir is None :
      sys.exit("ERROR "+methId+" sFMTFactoryObj._mainCfgDir is None !\n")

    if sFMTFactoryObj._s102TilesObj is None :
      sys.exit("ERROR "+methId+" sFMTProductsObj._s102TilesObj is None ! !\n")

    #--- 20200723: sFMTFactoryObj._prodJsonCfgFile probably useless now
    #if sFMTFactoryObj._prodJsonCfgFile is None :
    #  sys.exit("ERROR "+methId+" sFMTFactoryObj._prodJsonCfgFile is None !\n")

    #--- 20200723: sFMTFactoryObj._prodJsonCfgFile probably useless now
    #if not os.access(sFMTFactoryObj._prodJsonCfgFile, os.F_OK) :
    #  sys.exit("ERROR "+methId+
    #           " sFMTFactoryObj._prodJsonCfgFile -> "+
    #           sFMTFactoryObj._prodJsonCfgFile+" not found !\n")
    #---

    sys.stdout.write("INFO "+methId+" ParamsDict="+str(ParamsDict))

    if IForeman.JSON_LEGACY_FILE_ID[0] not in tuple(ParamsDict.keys()) :
      sys.exit("ERROR "+methId+" string id. -> "+
               IForeman.JSON_LEGACY_FILE_ID[0]+" not present in ParamsDict !\n")
    #---

    self._foremanLegacyFile= None

    #--- self._fieldsVarsType to be defined by the corresponding
    #    parameter read from the Json config. file.
    #    20200720: Now inherited from ModelDataAttr class
    #self._fieldsVarsType= None

    #--- TODO: Use an unary tuple for self._fieldsVarType ?
    self._fieldsVarType= ParamsDict[ self.JSON_FIELDSVARS_ID[0] ]

    sys.stdout.write("INFO "+methId+
                     " self._fieldsVarType="+self._fieldsVarType+"\n")

    #--- Keep the JSON formatted Foreman legacy static parameters file in
    #    self object for subsequent usage:
    self._foremanLegacyFile= SFMTFactoryObj._mainCfgDir + \
                               ParamsDict[ IForeman.JSON_LEGACY_FILE_ID[0] ]

    if not os.access(self._foremanLegacyFile, os.F_OK) :
      sys.exit("ERROR "+methId+
               " self._foremanLegacyFile -> "+self._foremanLegacyFile+" not found !\n")
    #---
    print(methId+"end, exit 0")
    sys.exit(0)

  #---
  def processFactoryInputInfo( self,
                               StartHourSseUTC: int,
                               EndHourSseUTC: int,
                               NbMultiProcesses: int = 1 ) :
    """
    Method which overrides the processFactoryInputInfo method
    of the SFMTModelFactory super class and starts the S111,
    S104 DHP data files production.

    StartHourSseUTC: The 1st timestamp in seconds since the
    epoch in UTC(a.k.a ZULU) of the data.

    EndHourSseUTC: The last timestamp in seconds since the
    epoch in UTC of the data.

    NbMultiProcesses <DEFAULT==1> : The number of multiprocessing
    objects(a.k.a. "threads") to use to speed up exec.
    """

    methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + str(" method:")

    #--- Use super class getFactoryProducts for generic processing first.
    super(WebTideFactory, self).getFactoryProducts( StartHourSseUTC,
                                                    EndHourSseUTC,
                                                    ITidalPrd.DEFAULT_TIMEINCR_SECONDS[0],
                                                    NbMultiProcesses )
    sys.stdout.write("INFO "+methID+
                     " start, NbMultiProcesses="+str(NbMultiProcesses)+"\n")

    #--- Usual fool proof checks:
    if self._sFMTFactoryObj is None :
      sys.exit("ERROR "+methID+" self._sFMTFactoryObj is None !\n")

    if self._sFMTFactoryObj._s102TilesObj is None :
      sys.exit("ERROR "+methID+" self._sFMTFactoryObj._s102TilesObj is None ! !\n")

    if self._foremanLegacyFile is None :
      sys.exit("ERROR "+methID+" self._foremanLegacyFile is None ! !\n")

    if not os.access(self._foremanLegacyFile, os.F_OK) :
      sys.exit("ERROR "+methID+
               " self._foremanLegacyFile -> "+self._foremanLegacyFile +" not found !\n")
    #---

    #--- Create ForemanFactory object here with the starting and ending timestamps
    #    for subsequent usage:
    foremanFactoryObj= ForemanFactory( self._foremanLegacyFile,
                                       StartHourSseUTC,
                                       EndHourSseUTC )

    if self._sFMTFactoryObj._prodJsonCfgFile is None :
      sys.exit("ERROR "+methID+
               " self._sFMTFactoryObj._prodJsonCfgFile is None ! !\n")
    #---

    sys.stdout.write("INFO "+methID+
                     " self._sFMTFactoryObj._prodJsonCfgFile -> "+
                     self._sFMTFactoryObj._prodJsonCfgFile+"\n")

    if not os.access(self._sFMTFactoryObj._prodJsonCfgFile, os.F_OK) :
      sys.stderr.write("ERROR "+methID+
                       " self._sFMTFactoryObj._prodJsonCfgFile -> "+
                       self._sFMTFactoryObj._prodJsonCfgFile +" not found !\n")
    #---

    if NbMultiProcesses is None :
      sys.stdout.write("WARNING "+methID+
                       " NbMultiProcesses is None ! Setting it to one ! \n")
      NbMultiProcesses= 1
    #---

    #--- Get the datasets definition(Names, directory,..) from the
    #    specific WebTide JSON config file in local dicionary dataSetsJSONDict:
    dataSetsJSONDict= JsonCfgIO.getIt(self._sFMTFactoryObj._prodJsonCfgFile)

    if self.JSON_DATASETS_DIR_ID[0] not in dataSetsJSONDict.keys() :
      sys.exit("ERROR "+methID+" self.JSON_DATASETS_DIR_ID[0] key -> "+
               self.JSON_DATASET_DIR_ID[0]+" not present in dataSetsJSONDict !\n")
    #---

    #--- Directory where to find the WebTide datasets files :
    dataSetsDir= dataSetsJSONDict[ self.JSON_DATASETS_DIR_ID[0] ]

    if self.JSON_DATASETS_ID[0] not in dataSetsJSONDict :
      sys.stderr.write("ERROR "+methID+" self.JSON_DATASETS_ID[0] key -> "+
                       self.JSON_DATASETS_ID[0]+" not present in dataSetsJSONDict !\n")
      sys.exit(1)
    #---

    if self.JSON_FIELDSVARS_ID[0] in dataSetsJSONDict.keys() :

      #--- Setting the fields variables( U,V for CURRENTS OR Z for WATERLEVELS ) wanted:
      fieldsTypeId= dataSetsJSONDict[ self.JSON_FIELDSVARS_ID[0] ]

      if fieldsTypeId not in tuple(ITidalPrd.FIELDS_IDS.keys()) :
        sys.exit("ERROR "+methID+
                 " Invalid fields variables id. -> "+fieldsTypeId+" !\n")
      #--- End inner if block:

      self._fieldsVarType= fieldsTypeId
    #--- End outer if block:

    #--- Do the setup for the output object(s):
    self.setupOutputObjects(self._fieldsVarType)

    sys.stdout.write("INFO "+methID+" Will produce fields variable(s) -> "+
                      str(ITidalPrd.FIELDS_IDS[self._fieldsVarType])+"\n")

    #--- Get the datasets JSON dictionaries in a tuple:
    dataSetsJSONDictsTuple= tuple( dataSetsJSONDict[ self.JSON_DATASETS_ID[0] ] )

    #--- Dictionary to store each dataset retreived from files.
    dataSetsObjs= {}

    #--- Shortcut to self._sFMTFactoryObj:
    sFMTFactoryObj= self._sFMTFactoryObj

    #--- Shortcut to self._sFMTFactoryObj._s102Tiles
    s102Tiles= sFMTFactoryObj._s102Tiles

    #--- base level tiles dictionary should be there:
    if IS102.TILES_LEVEL2_ID[0] not in tuple(s102Tiles._dataDict.keys() ) :
      sys.exit("ERROR "+methID+" Mandatory key -> "+
               IS102.TILES_LEVEL2_ID[0]+" is not present in s102Tiles._dataDict !\n")
    #---

    #--- Get rid of L2 tiles which do not have enclosed L5 tiles
    #    inside them but just for water levels (It means that there is no
    #    shallow soundings in it to justify the need of higher resolution
    #    levels L5,L6).
    if self._fieldsVarType == ISFMT.DATA_TYPES.WATERLEVELS.name :

      #--- Shorcut to the base level tiles dictionary:
      blTilesDict= s102Tiles._dataDict[ IS102.TILES_LEVEL2_ID[0] ]

      #--- Latitudes ranges dict, should be there:
      if self.LATITUDES_RANGES_ID[0] not in tuple(blTilesDict.keys() ) :
        sys.exit("ERROR "+methID+" Mandatory key -> "+
                 self.LATITUDES_RANGES_ID[0]+" is not present in blTilesDict !\n")
      #---

      #--- Shortcut to the latitudes ranges dictionary of the level 2 tiles dict.:
      blTilesLatRangesDict= blTilesDict[ self.LATITUDES_RANGES_ID[0] ]

      #--- Loop on the latitudes ranges base level tiles dictionaries:
      for blTilesDictKey in tuple(blTilesLatRangesDict.keys()) :

        #--- Shortcut to the base level tiles dictionaries for this latitudes range:
        tilesDict= blTilesLatRangesDict[blTilesDictKey]

        #--- Loop on the base level tiles ids. for each latitudes range:
        for tileId in tuple(tilesDict.keys()) :

          tileDict= tilesDict[tileId]

          if tileDict[ self.TILES_NEXT_LEVEL_ID[0] ] == None :

            #--- Zap the tile from its parent dictionary.
            #    since there is no L5 level tiles inside this tile.
            del tilesDict[tileId]

          #--- end  block if tileDict[ self.TILES_NEXT_LEVEL_ID[0] ] == None
        #--- end block for tileId in tilesDict.keys()
      #--- end block for blTilesDictKey in tuple(blTilesLatRangesDict.keys())
    #--- end if self._fieldsVarType == ISFMT.DATA_TYPES.WATERLEVELS.name

    #--- Loop on all WebTide datasets to gather tidal constituents from each Webtide dataset:
    for dataSetJSONDict in dataSetsJSONDictsTuple :

      dataSetJSONDictKeys= tuple(dataSetJSONDict.keys())

      if self.MODEL_NAME_ID[0] not in dataSetJSONDictKeys :
        sys.exit("ERROR "+methID+" self.MODEL_NAME_ID[0] key -> "+
                 self.MODEL_NAME_ID[0]+" not present in dataSetJSONDict !\n")
      #--- End block if self.MODEL_NAME_ID[0] not in dataSetJSONDict

      dataSetId= dataSetJSONDict[self.MODEL_NAME_ID[0]]

      sys.stdout.write("INFO "+methID+" Processing dataset -> "+dataSetId+"\n")

      if self.JSON_DATASET_FORMAT_ID[0] not in dataSetJSONDictKeys :
        sys.exit("ERROR "+methID+" self.JSON_DATASET_FORMAT_ID[0] key -> "+
                 self.JSON_DATASET_FORMAT_ID[0]+" not present in dataSetJSONDict !\n")
      #---

      #--- NOTE: dataSetFormat is an Enum attribute returned by WebTide.getFormatId
      dataSetFormat= WebTide.getFormatId( dataSetJSONDict[self.JSON_DATASET_FORMAT_ID[0]] )

      if self.JSON_DATASET_FILE_ID[0] not in dataSetJSONDictKeys :
        sys.exit("ERROR "+methID+" self.JSON_DATASET_FILE_ID[0] key -> "+
                 self.JSON_DATASET_FILE_ID[0]+" not present in dataSetJSONDict !\n")
      #---

      #--- The file containing the dataset tidal constituents data:
      dataSetFile= dataSetsDir+ "/" + dataSetJSONDict[ self.JSON_DATASET_FILE_ID[0] ]

      #--- Get the tidal constituents data from the dataSetFile:
      dataSetsObjs[dataSetId]= WebTide( dataSetId,
                                        dataSetFile,
                                        dataSetFormat,
                                        s102Tiles,
                                        dataSetJSONDict,
                                        self._fieldsVarType )
      #---
      sys.stdout.write("INFO "+methID+
                       " Done with getting tidal constituents for dataset -> "+dataSetId+"\n")

      #--- Create regional models sub-directories for S111 products(if any):
      if sFMTFactoryObj._s111Obj is not None :
        FilesDirs.createNewSubDir(sFMTFactoryObj._s111Obj._outputDir, dataSetId)
      #---

      #--- Create regional models sub-directories for S104 products(if any):
      if sFMTFactoryObj._s104Obj is not None :
        FilesDirs.createNewSubDir(sFMTFactoryObj._s104Obj._outputDir, dataSetId)
      #---

    #--- end loop for dataSetJSONDict in dataSetsJSONDictsTuple :

    #--- Now compute all(currents and-or water levels) tidal predictions with
    #    all the valid WebTide data gathered:
    for dataSetJSONDict in dataSetsJSONDictsTuple :

      dataSetId= dataSetJSONDict[ self.MODEL_NAME_ID[0] ]

      #--- Start the possibly parallelized(NbMultiProcesses>1) data production for a given WebTide dataset.
      self.produceDataSetOutputs( foremanFactoryObj,
                                  dataSetId,
                                  dataSetsObjs[dataSetId],
                                  NbMultiProcesses )

    #--- End block loop for dataSetJSONDict in dataSetsJSONDictsTuple

    ##--- Need to instruct the main exec. entity to wait(join) for all threads
    ##    to finish execution if we want to do something else(like a remote xfer)
    ##    which needs all the new products being available before going further.
    #if NbMultiProcesses > 1 :

      ##--- loop on all threadHandle objects in dataSetsThreadsHandles tuple
      #for threadHandle in dataSetsThreadsHandles:

        ##--- The threadHandle.join() tells the main exec. entity
        ##    to wait for the thread to finish its exec.
        #threadHandle.join()

      #--- end block loop for threadHandle
    #--- end block if NbMultiProcesses > 1

    sys.stdout.write("INFO "+methID+" end\n")

  #---
