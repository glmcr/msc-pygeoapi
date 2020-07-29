#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTFactory.py
# Creation        : September/Septembre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTFactory implementation.
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
import time
import inspect

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMT import SFMT
from msc_pygeoapi.process.dfo.pjs.util.JsonCfgIO import JsonCfgIO
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.S102 import S102
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.S104 import S104
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s111.S111 import S111
from msc_pygeoapi.process.dfo.pjs.util.TimeMachine import TimeMachine
from msc_pygeoapi.process.dfo.pjs.tidal.webtide.WebTideFactory import WebTideFactory
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTFactoryAttr import SFMTFactoryAttr
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTDataFactory import SFMTDataFactory
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTModelFactory import SFMTModelFactory
#from msc_pygeoapi.process.dfo.chs.enav.pjs..models.eccc.NEMOFactory import NEMOFactory

#---
class SFMTFactory(SFMTFactoryAttr, TimeMachine) :

  """
  Class used mainly for SFMT DHP code modularization. It is not used
  like a real Java "factory" class mechanism despite its name.
  """

  #---
  def __init__( self,
                MainJsonConfigFile: str,
                MainCfgDir: str= None ) :
    """
    Constructor for class SFMTFactory.

    MainJsonConfigFile (type->str) : A json format file
    which contains the common config. parameters.

    MainCfgDir (type->str) <OPTIONAL> Default->None :
    DHP package config. directory path.
    """

    #---
    TimeMachine.__init__(self)

    #: Doc Need to use None for now for the
    #  S102Obj arg. to SFMTFactoryAttr.__init__ here.
    SFMTFactoryAttr.__init__(self, None)

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methId+
                     " start: MainJsonConfigFile="+
                     MainJsonConfigFile+", MainCfgDir="+str(MainCfgDir)+"\n")

    if MainJsonConfigFile is None :
      sys.exit("ERROR "+methId+" MainJsonConfigFile is None ! \n")

    #--- Check if the json config. file exists:
    if not os.access(MainJsonConfigFile, os.F_OK) :
      sys.exit("ERROR: Main json main config. file -> "+
               MainJsonConfigFile+" not found !\n")
    #---

    #--- TODO : Use unary tuples for all self._<something> stuff ??
    self._mainCfgDir= MainCfgDir

    sys.stdout.write("INFO "+methId+
                     " self._mainCfgDir="+str(self._mainCfgDir)+" \n")

    #--- Get the main Json config. dictionary.
    mainJSONCfgFileDict= JsonCfgIO.getIt(MainJsonConfigFile)

    if mainJSONCfgFileDict is None :
      sys.exit("ERROR "+methId+
               " mainJSONCfgFileDict returned by JsonCfgIO.getIt(MainJsonConfigFile) is None ! \n")
    #---

    #: Doc Get the items string ids. keys of the mainJSONCfgFileDict dict.
    mainJSONCfgDictKeys= tuple(mainJSONCfgFileDict.keys())

    #: Doc Check if we have all mandatory config.
    #  parameters in the JSONConfigFileDict.
    #  (NOTE: self.JSON_MAINPARAMS_IDS is a tuple)
    for mandatoryCfgParam in self.JSON_MAINPARAMS_IDS :

      if mandatoryCfgParam not in mainJSONCfgDictKeys :
        sys.exit("ERROR "+methId+" Mandatory cfg param id. -> "+
                 mandatoryCfgParam+" not present in mainJSONCfgFileDict ! \n")

      #--- end inner if block.
    #--- end for loop block

    #: Do Extract the main storage directory path from the mainJSONCfgFileDict.
    self._mainStorageDir= mainJSONCfgFileDict[ ISFMT.JSON_MAIN_STORAGEDIR_ID[0] ]

    #--- checking for self._mainStorageDir existence:
    if not os.access(self._mainStorageDir, os.F_OK) :
      sys.exit("ERROR "+methId+
               " main storage directory -> "+
               self._mainStorageDir+" not found ! \n")
    #---

    sys.stdout.write("INFO "+methId+
                     " main storage directory used -> "+
                     self._mainStorageDir+" \n")

    #: Doc Extract the model data input directory if defined in the mainJSONCfgFileDict.
    if self.JSON_MODELDATA_INPUT_DIR[0] in mainJSONCfgDictKeys :

      self._inputDataDir= \
        mainJSONCfgFileDict[ self.JSON_MODELDATA_INPUT_DIR[0] ]

      sys.stdout.write("INFO "+methId+
                       " Will use model data input directory -> "+
                       self._inputDataDir+"\n")

      #: Doc Control if self._inputDataDir exists before going further.
      if not os.access(self._inputDataDir, os.F_OK) :

        sys.exit("ERROR "+methId+
                 " self._inputDataDir -> "+self._inputDataDir+" not found !!\n")
      #--- end inner if block.
    #--- end outer if block.

    #: Doc Extract main output directory where to
    #  put the new SFMT DHP data files.
    self._mainOutputDir= \
      mainJSONCfgFileDict[ self.JSON_PRODUCTS_OUTDIR_ID[0] ]

    #: Doc self._mainOutputDir could be absent at this point.
    if not os.access(self._mainOutputDir, os.F_OK) :

      sys.stdout.write("WARNING "+methId+
                       " main output directory -> "+self._mainOutputDir+
                       " not found, check it is inside self._mainStorageDir\n")

      #: Doc Extract main output directory where to put the SFMT DHP data files.
      self._mainOutputDir= self._mainStorageDir + \
                           "/" + mainJSONCfgFileDict[ self.JSON_PRODUCTS_OUTDIR_ID[0] ]

    #: Doc Checking for mandatrory mainOutputDir existence at this point :
    if not os.access(self._mainOutputDir, os.F_OK):

      sys.exit("ERROR "+methId+
               " main output directory -> "+
               self._mainOutputDir+" not found ! \n")
    #---

    sys.stdout.write("INFO "+methId+
                     " main output directory used -> "+self._mainOutputDir+"\n")

    #: Doc Get the output file format if it is defined in the json main config. dict.
    if self.JSON_CFG_OUTPUT_FMT_ID[0] in mainJSONCfgDictKeys :

      #: Doc Keep the alternative output format value as an attribute in self for subsequent usage:
      self._altOutputFormat= \
        mainJSONCfgFileDict[ self.JSON_CFG_OUTPUT_FMT_ID[0] ]
    #--- end if block.

    #: Doc The SFMT DHP HDF5 json formatted metadata templates
    #  definitions directory path is normally already defined
    #  and is not relative(i.e. it's a complete path) if we
    #  are running inside the ECCC Maestro oper. env.
    jsonMetaDataTemplatesDir= \
      mainJSONCfgFileDict[ self.JSON_META_DATA_DIR_ID[0] ]

    sys.stdout.write("INFO "+methId+
                     " Checking for jsonMetaDataTemplatesDir="+
                     jsonMetaDataTemplatesDir+"\n")

    #: Doc self._ecccMaestroInstance= False by default.
    self._ecccMaestroInstance= False

    #--- Check if it is a valid directory
    if not os.access(jsonMetaDataTemplatesDir, os.F_OK) :

      #; Doc It is an error here if self._mainCfgDir is at None.
      if not os.access(self._mainCfgDir, os.F_OK) :
        sys.exit("ERROR "+methId+
                 " self._mainCfgDir -> "+self._mainCfgDir+" not found ! \n")
      #---

      #: Doc Get the SFMT DHP HDF5 metadata json formatted
      #  templates definitions directory path from the json
      #  main config. dictionary(NOTE: os.sep is the directory
      #  arborescence separator) :
      jsonMetaDataTemplatesDir= self._mainCfgDir + os.sep + \
                                mainJSONCfgFileDict[ self.JSON_META_DATA_DIR_ID[0] ]

      if not os.access(jsonMetaDataTemplatesDir,os.F_OK) :
        sys.exit("ERROR "+methId+
                 " jsonMetaDataTemplatesDir -> "+
                 jsonMetaDataTemplatesDir+" not found ! \n")
      #---

      sys.stdout.write("INFO "+methId+" Running outside ECCC Maestro oper. env.\n")

    else : #--- We're inside the ECCC Maestro oper. env.

      self._ecccMaestroInstance= True

      #: Doc Define the path of the specific ECCC Maestro config. directory.
      self._maestroCfgDir= os.path.dirname(MainJsonConfigFile)

      sys.stdout.write("INFO "+methId+
                       " jsonMetaDataTemplatesDir is valid, self._maestroCfgDir="+
                       self._maestroCfgDir+"\n")

      sys.stdout.write("INFO "+methId+
                       " Running inside ECCC Maestro oper. env., self._ecccMaestroInstance set at True\n")

    #--- outer if-else block

    sys.stdout.write("INFO "+methId+
                    " self._ecccMaestroInstance="+str(self._ecccMaestroInstance)+"\n")

    sys.stdout.write("INFO "+methId+
                     " Will use jsonMetaDataTemplatesDir="+jsonMetaDataTemplatesDir+"\n")

    #: Doc Extract(if any) the minimum nb. of model data points
    #  that are allowed per tile.
    if self.JSON_MIN_NB_POINTS_ID[0] in mainJSONCfgDictKeys :

      #: Doc Replace the default min. nb. of model data points per
      #  tile tuple by a new tuple containing the new value:
      self._minNbPointsPerTile= \
        ( int(mainJSONCfgFileDict[ self.JSON_MIN_NB_POINTS_ID[0] ]) ,)

      sys.stdout.write("INFO "+methId+
                       " Default min. nb points per tile is changed for -> "+
                       str(self._minNbPointsPerTile[0])+"\n")
    #--- end if block.

    #: Doc Put JSONTemplatesDir in the object for subsequent usage:
    self._jsonTemplatesDir= jsonMetaDataTemplatesDir

    #: Doc Get the mandatory input data config. dictionary which must be
    #: defined in mainJSONCfgFileDict
    self._inputDataCfgDict= mainJSONCfgFileDict[ self.JSON_INPUT_DATA_ID[0] ]

    #: Doc Check if the string id. for the type of input is in the keys of
    #: mandatory input data config. dictionary:
    inputDataCfgDictKeys= tuple(self._inputDataCfgDict.keys())

    if self.JSON_INPUT_DATATYPE_ID[0] not in inputDataCfgDictKeys :
      sys.exit("ERROR "+methId+" Mandatory string id. -> "+
                      self.JSON_INPUT_DATATYPE_ID[0]+
                      " not present in self._inputDataCfgDict ! \n")
    #--- end if block.

    #: Doc Get the name of the input data type.
    inputDataType= self._inputDataCfgDict[ self.JSON_INPUT_DATATYPE_ID[0] ]

    inputDataTypeOk= False

    #: Doc Checking if input data type is valid:
    #: (NOTE: ISFMT.ALLOWED_INPUT_DATA_TYPES is an enum.Enum object)
    for allowedInputType in ISFMT.ALLOWED_INPUT_DATA_TYPES :

      if inputDataType == allowedInputType.name :

        inputDataTypeOk= True
        break
      #--- end if block.

    #--- end for loop block.

    #: Doc Not a valid input data type if
    #  inputDataTypeOk == False at this point:
    if not inputDataTypeOk :
      sys.exit("ERROR "+methId+
               " Invalid input type -> "+inputDataType+" !\n")
    #---

    #: Doc Check if the string id. of the mandatory input parameters
    #: is defined in self._inputDataCfgDict.
    if self.JSON_INPUT_DATAPARAMS_ID[0] not in inputDataCfgDictKeys :
      sys.exit("ERROR "+methId+" Mandatory string id. -> "+
                      self.JSON_INPUT_DATAPARAMS_ID[0]+
                      " not present in self._inputDataCfgDict ! \n")
    #--- end if block.

    #: Doc Keep the inputDataType object reference in self object for subsequent usage.
    self._inputDataType= inputDataType

    sys.stdout.write("INFO "+methId+" Using input type -> "+inputDataType+"\n")

    #: Doc Get the common SFMT DHP HDF5 json
    #  formatted metadata complete file path.
    jsonCommonMetaDataFile= \
      self._jsonTemplatesDir + "/" + self.COMMON_METADATA_FILENAME[0]

    #---
    if not os.access(jsonCommonMetaDataFile, os.F_OK) :
      sys.exit("ERROR "+methId+" jsonCommonMetaDataFile -> "+
                      jsonCommonMetaDataFile+" not found ! \n")
    #---

    sys.stdout.write("INFO "+methId+
                     " Getting common SFMT DHP HDF5 metadata from file -> "+
                     jsonCommonMetaDataFile+"\n")

    #: Doc Get the dict. from the common SFMT DHP HDF5 json formatted
    #: metadata file just to check if some mandatory static strings
    #: ids. keys are defined in it before going further in the exec.
    self._jsonCommonMetaData= JsonCfgIO.getIt(jsonCommonMetaDataFile)

    #: Doc Some preliminary checks done before starting the intensive data inputs processing.
    for checkIt in self.JSON_STRIDS_CHECKS :

      if checkIt not in tuple( self._jsonCommonMetaData.keys() ) :
        sys.exit("ERROR "+methId+" \""+checkIt+
                 "\" string id. MUST be defined in self._jsonCommonMetaData dictionary at this point\n")
      #--- end  if block
    #--- end for loop block.

    sys.stdout.write("INFO "+methId+" Common JSON metadata seems ok ! \n")

    #--- 20200723: The check for the self.JSON_INPUT_CFGFILE_ID[0]
    #              seems to be useless now.
    #    TODO: Remove the following if-else block when it is sure that
    #          it is indeed useless.
    ##: Doc The SFMT DHP HDF5 json formatted metadata file
    ##  path is normally not defined in the inputDataCfgDict
    ##  dictionary if running inside ECCC Maestro oper. env.
    #if self.JSON_INPUT_CFGFILE_ID[0] in inputDataCfgDictKeys :
    #  self._prodJsonCfgFile= self._mainCfgDir + \
    #    mainJSONCfgFileDict[ self.JSON_INPUT_DATA_ID[0] ][ self.JSON_INPUT_CFGFILE_ID[0] ]
    #  if not os.access(self._prodJsonCfgFile, os.F_OK) :
    #    sys.exit("ERROR "+methId+" self._prodJsonCfgFile -> "+
    #                    self._prodJsonCfgFile+" not found ! \n")
    #  #--- end inner if block
    #  sys.stdout.write("INFO "+methId+
    #                   " Will use specific products Json configuration file -> "+
    #                   self._prodJsonCfgFile+"\n")
    #else :
    #  sys.stdout.write("INFO "+methId+
    #                   " No specific Json configuration products file to load,"+
    #                   " assuming we are inside ECCC HPC operations world\n")
    #--- end outer if-else block

    #: Doc Check if we have a request for an output format other than SFMT DHP data:
    #:
    #: TODO : Could we get rid of the possibility of having results in another
    #  formats than the official IHO S102 tiled DHP format ??
    if self._altOutputFormat is None :

      #: Doc Need to load all S102 tiles bounding boxes SHP data:
      sys.stdout.write("INFO "+methId+
                       " Need to load tiles bounding boxes data for input data type -> "+
                       self._inputDataType+"\n")

      #: Doc Need to have the string id. of the S102 tiles bounding boxes SHP files
      #      defined in mainJSONCfgDictKeys:
      if self.JSON_TILES_SHP_FILES_ID[0] not in mainJSONCfgDictKeys :

        sys.exit("ERROR "+methId+" String id. key -> "+
                         self.JSON_TILES_SHP_FILES_ID[0]+
                         " not present in mainJSONCfgFileDict !\n")
      #--- end inner if block.

      #; Doc We could have to exclude some S102 L2 tiles.
      excludeTilesBBoxesTuple= None

      if self.JSON_EXCLUDE_TILES_ID[0] in mainJSONCfgDictKeys :

        excludeTilesBBoxesTuple= \
          tuple( mainJSONCfgFileDict[ self.JSON_EXCLUDE_TILES_ID[0] ] )

        sys.stdout.write("INFO "+methId+ " Will use regular bounding boxes -> "+
                         str(excludeTilesBBoxesTuple)+" to exclude some tiles.\n")
      #-- end if block.

      #--- TODO: Add control on the tiles bounding boxes files format used to
      #          avoid awkward SNAFUs related to input file formats not supported:
      s102Obj= SFMTDataFactory.getS102TilesBBoxes( self._mainCfgDir,
                                                   mainJSONCfgFileDict[ self.JSON_TILES_SHP_FILES_ID[0] ],
                                                   excludeTilesBBoxesTuple )

      #: Doc Use S102TilesObj.setS102TilesRef method to set its inner S102 class instance object reference.
      self.setS102TilesRef(s102Obj)

    else :

      sys.stdout.write("INFO "+methId+
                       " self._altOutputFormat is not None then "+
                       "no Need to load tiles bounding boxes data for input data type -> "+
                       self._inputDataType+"\n")

      sys.exit("ERROR "+methId+
               " Implementation of alternative format outputs not ready yet !\n")

      self.setS102TilesRef(None)

    #--- end outer if-else block.

    sys.stdout.write("INFO "+methId+" end \n")

  #--- Note the -> SFMTModelFactory: It means
  #    that getProducts return an object instance
  #    of the class SFMTModelFactory.
  def getProducts( self,
                   SFMTObjInst,
                   NbMultiProcesses: int = 1,
                   OptionalArgs: tuple = None ) -> SFMTModelFactory:
    """
    Write the SFMT DHP data files according to the json formatted config.
    parameters loaded when the SFMTFactory class object was instantiated
    and sets the date-time limits to use for the products.

    SFMTObjInst (type->SFMTObj) : A SFMTObj class object instance.

    NbMultiProcesses (type->int) Default==1 : The number of multiprocessing
    objects to use for the possibly parallelized SFMT DHP outputs.

    OptionalArgs (type->tuple) Default->None : Could have optional args. to
    deal with (ex. coming from ECCC Maestro oper. env.).
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #: Doc SFMTObjInst must not be None here.
    if SFMTObjInst is None :
      sys.exit("ERROR "+methId+" SFMTObjInst is None !\n")
    #---

    #: Doc And we must have SFMTObjInst._sFMTFactoryObj is
    #      self (i.e. it must be the same object, himself
    #      if we want to go into punology) at this point.
    if SFMTObjInst._sFMTFactoryObj is not self :
      sys.exit("ERROR "+methId+" SFMTObjInst._sFMTFactoryObj is not self !\n")
    #---

    sys.stdout.write("INFO "+methId+
                     " start: NbMultiProcesses="+
                     str(NbMultiProcesses)+", OptionalArgs="+str(OptionalArgs)+"\n")

    #: Doc Dynamically determined lastHourSeconds for normal operations:
    lastHourSeconds= \
      self.roundPastToTimeIncrSeconds(self.SECONDS_PER_HOUR[0], int(time.time()))

    ##--- hard-coded static lastHourSeconds for WebTide stuff validation only:
    ##    To be commented for normal operations.
    #lastHourSeconds= self.getSeconds("20180720.120000Z", self.DEFAULT_GET_SECONDS_FMT[0])

    #: Doc Go back ISFMT.HOURS_IN_PAST_START[0] hours
    #  from lastHourSeconds to get some data in the near past:
    startHourSseUTC= lastHourSeconds - \
      self.SECONDS_PER_HOUR[0] * ISFMT.HOURS_IN_PAST_START[0]

    #: Doc The ending timestamp for the SFMT DHP data files outputs.
    endHourSseUTC= lastHourSeconds + \
      ISFMT.DEFAULT_FUTURE_HOURS[0] * self.SECONDS_PER_HOUR[0]

    sys.stdout.write("INFO "+methId+" Will use -> "+
                      self.getDateTimeStringZ(startHourSseUTC)+
                      " as starting time for the SFMT DHP data\n")

    sys.stdout.write("INFO "+methId+" Will use -> "+
                     self.getDateTimeStringZ(endHourSseUTC)+
                     " as ending time for the SFMT DHP data\n")

    #--- Fool-proof checks again:
    if self._inputDataType is None :
      sys.exit("ERROR "+methId+" self._inputDataType is None !\n")

    if self._inputDataCfgDict is None :
      sys.exit("ERROR "+methId+" self._inputDataCfgDict is None !\n")

    if self.JSON_INPUT_DATAPARAMS_ID[0] not in tuple(self._inputDataCfgDict.keys()) :
      sys.exit("ERROR "+methId+" string id. -> "+
               self.JSON_INPUT_DATAPARAMS_ID[0]+
               " key not present in self._inputDataCfgDict !\n")
    #--- end if.

    #: Doc Shortcut to the main parameters config. dictionary:q
    inputParamsDict= self._inputDataCfgDict[ self.JSON_INPUT_DATAPARAMS_ID[0] ]

    inputParamsDictKeys= tuple(inputParamsDict.keys())

    #: Doc Set self._applyConversion to True as the default.
    #:
    #: NOTE: Currents should almost always be converted from m/s to knots
    #: and all 2D models water levels should be converted to chart datums
    #: BUT IWLS tide gages data(wlo,wlp,wlf) are already always defined to
    #: the chart datums so the the IWLS S104 data processing class must not
    #: consider the value of self._applyConversion.

    self._applyConversion= True

    #: Doc Override self._applyConversion if
    #  self.JSON_APPLY_CONV_ID[0] is defined in paramsDict.
    if self.JSON_APPLY_CONV_ID[0] in inputParamsDictKeys :
      self._applyConversion= \
        bool( int( inputParamsDict[self.JSON_APPLY_CONV_ID[0]] ) )
    #---

    sys.stdout.write("INFO "+methId+
                     " self._applyConversion="+str(self._applyConversion)+"\n")

    #: Doc Init the modelDataFactoryObj to None for subsequent error control:
    modelDataFactoryObj= None

    #: Doc Checking if the model input data is from one
    #      of the ECCC-NEMO (rather large)family of models.
    if self._inputDataType == ISFMT.ECCCNEMO_STR_ID[0] :

      #--- NOTE: The SFMTObjInst as the 1st arg. to NEMOFactory
      #          class instance object constructor.
      modelDataFactoryObj= NEMOFactory( SFMTObjInst,
                                        inputParamsDict,
                                        OptionalArgs,
                                        self._altOutputFormat )
    #---

    #--- Specific DFO NEMO input data ??? The DFO NEMO input data
    #    should have the same format as ECCC NEMO.
    #elif self._inputDataType == ISFMT.DFO_NEMO_ID[0] :
    #  modelDataFactoryObj= DFONemoFactory(self, self._mainCfgDir, inputParamsDict, self._altOutputFormat )
    #

    #--- Uncomment for to be able to use WebTideFactory stuff:
    #    NOTE: WebTide src code as not been run since June 2019 so
    #          it will surely not work on the 1st try.
    elif self._inputDataType == ISFMT.WEBTIDE_STR_ID[0] :
      #modelDataFactoryObj= WebTideFactory(self, inputParamsDict, self._altOutputFormat )

      modelDataFactoryObj= WebTideFactory( SFMTObjInst,
                                           inputParamsDict,
                                           self._altOutputFormat )
    #---

    #: Doc Need a valid None modelDataFactoryObj at this point:
    if modelDataFactoryObj is None :
      sys.exit("ERROR "+methId+
               " modelDataFactoryObj cannot be None at this point !\n")
    #---

    #: Doc Use the processFactoryInputInfo method(OOP polymorphic call) of the modelDataFactoryObj.
    modelDataFactoryObj.processFactoryInputInfo(startHourSseUTC, endHourSseUTC, NbMultiProcesses)

    sys.stdout.write("INFO "+methId+" end\n")

    return modelDataFactoryObj

  #---
  def writeTileDHProduct( self,
                          TileId: str,
                          TileDict: dict,
                          DateTimeStringsOutDict: dict,
                          RegionalModelName: str= None,
                          OverWriteWarn: bool= False,
                          INFOLog: bool= False) :
    """
    Generic method to be used by the specific input data
    objects(WebTide, ECCC and so on)to write the SFMT DHP
    data files (ex. see the use of this method in the
    ECCCModelTiles sub-class)

    TileId (type->str): The original string id. of the S102
    data tile(Ex. "CA5_4150N07060W") coming from the indexed
    shapefile DB.

    TileDict (type->dict): The tile dictionary holding
    the model input data (currents, water levels) to write.

    DateTimeStringsOutDict (type->dict): The dictionary
    holding all the already formatted timestamps of the model
    input data.

    RegionalModelName (type->str) <OPTIONAL> Default->None:
    A regional model name ("NEMO:RIOPS","WebTide:arctic9") to
    use for identification in the SFMT DHP HDF5 metadata.

    OverWriteWarn (type->bool) <OPTIONAL> Default->False:
    A flag to signal that the already existing data products
    files are to be overwritten with or without issuing a
    WARNING log message to the stdout stream.

    INFOLog (type->bool) <OPTIONAL> Default->False:
    To log or not to log INFO messages to the stdout stream.

    REMARK: This method seems unnecessary in the context of
    ECCC Maestro operational env. but in the future it could
    become possible that we will have to produce more than
    one SFMT DHP data type files in just one instance of the
    main Python script.
    """

    #--- NOTE: No fool-proof checks here for performance reasons.

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    if INFOLog :
      sys.stdout.write("INFO "+methId+" Start: TileId -> "+TileId+
                       ", RegionalModelName="+RegionalModelName+
                       ", self._applyConversion="+str(self._applyConversion)+"\n")
    #---

    gotASNAFU= False

    #: Doc Check if we have some S104 DHP data to write:
    if self._s104Obj :

      self._s104Obj.writeOneTile( TileId,
                                  TileDict,
                                  DateTimeStringsOutDict,
                                  RegionalModelName,
                                  self._applyConversion,
                                  OverWriteWarn,
                                  INFOLog )
    else :

      gotASNAFU= True

      if INFOLog :
        sys.stdout.write("WARNING "+methId+" No S104 data to write ! \n")

    #: Doc Check if we have some S111 DHP data to write:
    if self._s111Obj :

      self._s111Obj.writeOneTile( TileId,
                                  TileDict,
                                  DateTimeStringsOutDict,
                                  RegionalModelName,
                                  self._applyConversion,
                                  OverWriteWarn,
                                  INFOLog )
    else :

      #--- If we end up here and gotASNAFU == True then it is an error.
      if gotASNAFU :
        sys.exit("ERROR "+methId+
                 " Both self._s104Obj and self._s111Obj are None !\n")
      #---

      if INFOLog :
        sys.stdout.write("WARNING "+methId+" No S111 data to write ! \n")

    if INFOLog :
      sys.stdout.write("INFO "+methId+" End \n")
