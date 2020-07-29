#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTModelFactory.py
# Creation        : September/Septembre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTModelFactory implementation.
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

#--- 3rd party h5py package:
import h5py

#---
from msc_pygeoapi.process.dfo.pjs.util.JsonCfgIO import JsonCfgIO
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.S102 import S102
from msc_pygeoapi.process.dfo.pjs.util.TimeMachine import TimeMachine
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.IS102 import IS102
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTMetaData import SFMTMetaData
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTModelAttr import SFMTModelAttr
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.S104DataCodingFmt3 import S104DataCodingFmt3
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s111.S111DataCodingFmt3 import S111DataCodingFmt3

#--- Uncomment the following import if we have to produce WebTide DHP
#from dhp.tidalprd.ITidalPrd import ITidalPrd

#---
class SFMTModelFactory(TimeMachine, SFMTModelAttr) :

  """
  Another SFMT class used for the modularization of the code. It
  is not used like a real Java "factory" class mechanism despite
  its name.
  """

  #---
  def __init__( self,
                SFMTObjInst ) :

    """
    SFMTObjInst (type->SFMTObj) : A SFMTObj class instance object.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    sys.stdout.write("INFO "+methId+" start\n")

    TimeMachine.__init__(self)

    #--- Usual fool-proof checks.
    if SFMTObjInst is None :
      sys.exit("ERROR "+methId+" SFMTObjInst is None !\n")

    if SFMTObjInst._sFMTFactoryObj is None :
      sys.exit("ERROR "+methId+" SFMTObjInst._sFMTFactoryObj is None !\n")

    SFMTModelAttr.__init__( self,
                            SFMTObjInst._s102TilesObj,
                            SFMTObjInst._sFMTFactoryObj )

    #--- 20200723: self._sFMTFactoryObj._prodJsonCfgFile
    #              seems to be useless now.
    #    TODO: Remove the following nested if block when it is sure that
    #          it is indeed useless.
    #
    #if self._sFMTFactoryObj._prodJsonCfgFile is not None :
    #  sys.stdout.write("INFO "+methId+
    #                   " Running outside ECCC Maestro oper. env.\n")
    #  if not os.access(self._sFMTFactoryObj._prodJsonCfgFile, os.F_OK) :
    #    sys.exit("ERROR "+methId+
    #             "self._sFMTFactoryObj._prodJsonCfgFile -> "+
    #             self._sFMTFactoryObj._prodJsonCfgFile+" not found !\n")
    #  #--- end inner if block
    ##--- end outer if block

    sys.stdout.write("INFO "+methId+" end\n")

  #--- processFactoryInputInfo method is normally
  #    inherited(a.k.a @override in Java) by sub-classes:
  def processFactoryInputInfo( self,
                               StartHourSseUTC: int,
                               EndHourSseUTC: int,
                               TimeIncrInterval: int,
                               NbMultiProcesses: int = 1,
                               SetTimeStamps: bool = False) :
    """
    Generic method that starts the process to get the data that will be used for the
    SFMT DHP data files. This method is inherited by the specific sub classes for
    each input data type allowed(Ex. class WebTideFactory via class WebTideOutput)

    StartHourSseUTC (type->int): The 1st timestamp in seconds since the
    epoch in UTC(a.k.a ZULU) of the data.

    EndHourSseUTC (type->int): The last timestamp in seconds since the
    epoch in UTC of the data.

    TimeIncrInterval (type->int): The interval of time(in seconds)
    between two successive(in time) data values.

    NbMultiProcesses (type->int) <OPTIONAL> Default->1 :
    The number of multiprocessing objects(a.k.a. "threads").
    NOTE: Used only by sub classes.

    SetTimeStamps (type->boolean) <OPTIONAL> Default->False :
    To compute(or not to) the successive timestamps infos.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methId+" start\n")

    #--- Usual fool-proof checks:
    if StartHourSseUTC is None :
      sys.exit("ERROR "+methId+" StartHourSseUTC is None !\n")

    if EndHourSseUTC is None :
      sys.exit("ERROR "+methId+" EndHourSseUTC is None !\n")

    if TimeIncrInterval is None :
      sys.exit("ERROR "+methId+" TimeIncrSeconds is None !\n")

    if StartHourSseUTC <= 0 :
      sys.exit("ERROR "+methId+" StartHourSseUTC <= 0 !\n")

    if EndHourSseUTC <= 0 :
      sys.exit("ERROR "+methId+" End HourSseUTC <= 0 !\n")

    if TimeIncrInterval <= 0 :
      sys.exit("ERROR "+methId+" TimeIncrInterval <= 0 !\n")

    if TimeIncrInterval > self.MAXTIME_INTERVALL_SEC[0]  :
      sys.exit("ERROR "+methId+
               " TimeIncrInterval > "+
               str(self.MAXTIME_INTERVALL_SEC[0])+" seconds  !\n")
    #---

    if EndHourSseUTC <= StartHourSseUTC :
      sys.exit("ERROR "+methId+
               " EndHourSseUTC <= StartHourSseUTC !"+
               " Sorry, backward time usage not allowed ! \n")
    #---

    #: Doc Local shortcut to the self._sFMTFactory.
    #      NOTE: self._sFMTFactoryObj should have been already
    #      checked by sub-classes instances for being not None.
    sFMTFactoryObj= self._sFMTFactoryObj

    #--- 20200723: sFMTFactoryObj._prodJsonCfgFile
    #              seems to be useless now.
    #    TODO: Remove the following nested if block when it is sure that
    #          it is indeed useless.
    #
    #: Doc sFMTFactoryObj._prodJsonCfgFile could be None if we are running
    #      inside ECCC operations frontend machines.
    #if sFMTFactoryObj._prodJsonCfgFile is not None :
    #
    #  if not os.access(sFMTFactoryObj._prodJsonCfgFile, os.F_OK) :
    #    sys.exit("ERROR "+methId+
    #             " sFMTFactoryObj._prodJsonCfgFile -> "
    #             +sFMTFactoryObj._prodJsonCfgFile+" not found !\n")
    #
    #  #--- end inner if block
    ##--- end outer if block

    if sFMTFactoryObj._mainStorageDir is None :
      sys.exit("ERROR "+methId+": sFMTFactoryObj._mainStorageDir is None ! !\n")
    #---

    if not os.access(sFMTFactoryObj._mainStorageDir, os.F_OK) :
      sys.exit("ERROR "+methId+
               " sFMTFactoryObj._mainStorageDir -> "
               +sFMTFactoryObj._mainStorageDir+" not found !\n")
    #---

    #: Doc Need to add one more time increment for the next loop in order to get
    #      all the timestamps strings wanted in the self._dateTimeStringsIdxDict dictionary.
    loopUpperBnd= EndHourSseUTC + TimeIncrInterval

    #: Doc Check if we have to set the timestamps at this stage.
    if SetTimeStamps :

      sys.stdout.write("INFO "+methId+
                       " SetTimeStamps==True, setting timestamps here with TimeIncrInterval="+
                       str(TimeIncrInterval)+"\n")

      #: Doc Reset self._dateTimeStringsIdxDict to an empty dictionary before filling it.
      self._dateTimeStringsIdxDict= { }

      #: Doc Populate the self._dateTimeStringsIdxDict:
      for timeIncr in range(StartHourSseUTC, loopUpperBnd, TimeIncrInterval) :
        self._dateTimeStringsIdxDict[timeIncr]= self.getDateTimeStringZ(timeIncr)
      #--- end for loop block.

    #--- end if block.

    sys.stdout.write("INFO "+methId+" end\n")

  #--- setupOutputObjects: method that has to be overriden
  #    by derived classes:
  def setupOutputObjects(self, ProductType) :

    """
    Do the setup of output objects. This method
    should be overriden by sub classes(Ex. WebTideOutput).
    Only some fool-proof checks are done here for now.

    ProductType (type->str): Ex. CURRENTS, WATERLEVELS, and more others.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methId+" start\n")

    if ProductType is None :
      sys.exit("ERROR "+methId+" ProductType is None !\n")

    if self._sFMTFactoryObj is None :
      sys.exit("ERROR "+methId+" self._sFMTFactoryObj is None !\n")

    if self._sFMTFactoryObj._mainOutputDir is None :
      sys.exit("ERROR "+methId+
               " self._sFMTFactoryObj._mainOutputDir is None !\n")
    #---
    if self._sFMTFactoryObj._s102TilesObj is None :
      sys.exit("ERROR "+methId+
               " self._sFMTFactoryObj._s102Tiles is None !\n")
    #---
    if self._sFMTFactoryObj._jsonCommonMetaData is None :
      sys.exit("ERROR "+methId+
               " self._sFMTFactoryObj._jsonCommonMetaData is None !\n")
    #---
    if self._sFMTFactoryObj._jsonTemplatesDir is None :
      sys.exit("ERROR "+methId+
               " self._sFMTFactoryObj._jsonTemplatesDir is None !\n")
    #---

    sys.stdout.write("INFO "+methId+" end\n")

  #---
  def setupDCFmt3OutputObjects( self,
                                ProductType: str,
                                TypeOfData: str,
                                DataSourceId: str,
                                DoTimeStampsSetup: bool = True) :
    """
    Do the generic data coding format 3 setup of the output
    for S<NNN> DHP data.

    ProductType (type->string): S<NNN> DHP type id.

    TypeOfData (type->string): The type of data as defined in the IHO spec.
    (i.e. MODEL_FORECAST, ASTRO_PREDICTION, ...)

    DataSourceId (type->string): The model id. from which the input data
    comes from(i.e. WebTide, ECCC-NEMO, ...).

    DoTimeStampsSetup (type->boolean) <OPTIONAL> Default->True: Boolean
    flag to(or not to) signal that the timestamps setup has to be done.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #--- ProductType argument is supposed to be ok(i.e. not None) at this point.

    if TypeOfData is None :
      sys.exit("ERROR "+methID+" TypeOfData is None !\n")

    if DataSourceId is None :
      sys.exit("ERROR "+methID+" DataSourceId is None !\n")

    if self._sFMTFactoryObj is None :
      sys.exit("ERROR "+methID+" self._sFMTFactoryObj is None !\n")

    #: Doc Shortcut to the SFMTFactory object -> self._sFMTFactoryObj :
    sFMTFactoryObj= self._sFMTFactoryObj

    if sFMTFactoryObj._ecccMaestroInstance is None :
      sys.exit("ERROR "+methID+" sFMTFactoryObj._ecccMaestroInstance is None !\n")

    sys.stdout.write("INFO "+methId+
                     " start: DataSourceId="+DataSourceId+
                     ", sFMTFactoryObj._ecccMaestroInstance="+
                     str(sFMTFactoryObj._ecccMaestroInstance)+"\n")

    #: Doc Shortcut to the main parent directory where to write products:
    mainOutputDir= sFMTFactoryObj._mainOutputDir

    #: Doc Shortcut to some of the objects references
    #      that are contained by the self._sFMTFactory object
    #      and used as (shortcuts) arguments to the S<NNN>
    #      DHP data output objects creation methods:
    s102TilesObj      = sFMTFactoryObj._s102TilesObj
    jsonTemplatesDir  = sFMTFactoryObj._jsonTemplatesDir
    jsonCommonMetaData= sFMTFactoryObj._jsonCommonMetaData

    #: Doc Default output directories defined to the same directory.
    #      (i.e. All tiled output files will be written in the same
    #      directory regardless of the product types)
    s104OutputDir= s111OutputDir= mainOutputDir

    #: Doc Define specific output directories for each available SFMT DHP types
    #      but only when running outside ECCC Maestro oper. env.
    if not sFMTFactoryObj._ecccMaestroInstance :

      s111OutputDir= mainOutputDir + "/" + \
                     ISFMT.PRODUCTS_IDS.S111.name + "/" + DataSourceId

      s104OutputDir= mainOutputDir + "/" + \
                     ISFMT.PRODUCTS_IDS.S104.name + "/" + DataSourceId

      #s412OutputDir= mainOutputDir + "/" + ISFMT.PRODUCTS_IDS.S412.name + "/" + DataSourceId

    #--- End if block.

    #: Doc Create S111 currents SFMT DHP data output object
    if ProductType == ISFMT.DATA_TYPES.CURRENTS.name :

      sys.stdout.write("INFO "+methId+" Creating a S111 DHP data output object\n")

      sFMTFactoryObj._s111Obj= S111DataCodingFmt3( s102TilesObj,
                                                   jsonCommonMetaData,
                                                   jsonTemplatesDir,
                                                   TypeOfData,
                                                   DataSourceId,
                                                   s111OutputDir )

    #: Doc Create S104 2D water levels DHP data output object
    elif ProductType == ISFMT.DATA_TYPES.WATERLEVELS.name:

      sys.stdout.write("INFO "+methId+
                       " Creating a S104 2D DHP data output object.\n")

      sFMTFactoryObj._s104Obj= S104DataCodingFmt3( s102TilesObj,
                                                   jsonCommonMetaData,
                                                   jsonTemplatesDir,
                                                   TypeOfData,
                                                   DataSourceId,
                                                   s104OutputDir )
    if DoTimeStampsSetup :

      #: Doc Need to finish with the setup of the output time stamps once instead of doing it for each output file:
      self.setupOutputTimeStampsStrings( self.TIMESTAMP_GROUP_PREFIX_ID,
                                         ( jsonCommonMetaData[ self.DATETIME_SEP_ID[0] ] ,))

    sys.stdout.write("INFO "+methId+" end\n")

  #---
  def setupOutputTimeStampsStrings( self,
                                    DateTimeStringsIdxDict: dict,
                                    TimeStampHDF5GroupPrefix: tuple,
                                    HDF5DateTimeSep: tuple) -> dict :
    """
    Build all the rightly formatted output timestamps
    once-and-for-all(the OAFA principle) instead of doing
    it repeatedly(and costly in terms of performance)
    for each output file.

    DateTimeStringsIdxDict (type->dict) : A dictionary
    holding date timestamps strings in the YYYYMMDD.hhmmssZ format.
    (Ex. 20190511.180000Z). The indexings keys of this dictionary
    are the seconds since the epoch that corresponds to their indexed
    date timestamps strings.

    TimeStampHDF5GroupPrefix (type->tuple): An unary tuple holding
    the string prefix to use for the GROUPs names.

    HDF5DateTimeSep (type->tuple): An unary tuple holding the SFMT
    DHP metadata for the YYYYMMDD hhmmss character string separator.

    return (type->dictionary) : All the rightly formatted output
    timestamps built are stored(indexed) as unary tuples in the
    returned dictionary.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    ##--- Usual fool-proof checks. Uncomment for debugging.
    #if DateTimeStringsIdxDict is None :
    #  sys.exit("ERROR "+methId+" DateTimeStringsIdxDict is None !\n")

    #if HDF5DateTimeSep is None :
    #  sys.exit("ERROR "+methId+" HDF5DateTimeSep is None !\n")

    #: Doc timestamps counter needed for the SFMT DHP data timestamp string format.
    timeStampOutIdx= 0

    ##: Doc Create the empty dateTimeStringsOutDict dictionary to fill up and return:
    dateTimeStringsOutDict= { }

    #:Doc Loop on all timestamps and fill up dateTimeStringsOutDict with
    #     the rightly formatted output timestamps.
    for timeIncrKey in tuple(sorted(DateTimeStringsIdxDict.keys())) :

      #: Doc The default formatted timestamp string:
      dateTimeStampStrZ= DateTimeStringsIdxDict[timeIncrKey]

      #: Doc Get the date-time string rightly formatted
      #  (using the default formatted seconds since
      #  the epoch timestamp string as key id. in DateTimeStringsIdxDict)
      dateTimeStampValueStr= SFMTMetaData.getDateTimeStampStrTuple( TimeStampHDF5GroupPrefix,
                                                                    timeStampOutIdx+1,
                                                                    dateTimeStampStrZ,
                                                                    self.DATE_TIME_SPLIT_STR[0],
                                                                    HDF5DateTimeSep )

      #: Doc NOTE : Using a unary tuple for the date-time string
      #             returned by SFMTMetaData.setDateTimeStampStrings.
      dateTimeStringsOutDict[dateTimeStampStrZ]= ( dateTimeStampValueStr ,)

      #: Doc Increment timeStampOutIdx for the next iteration.
      timeStampOutIdx += 1

    #--- End for loop block for timeIncrKey.

    return dateTimeStringsOutDict

  #--- End method setupOutputTimeStampsStrings.
