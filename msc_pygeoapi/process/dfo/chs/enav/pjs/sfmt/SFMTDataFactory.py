#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTDataFactory
# Creation        : October/Octobre 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTDataFactory implementation.
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

#--- Built-in modules.
import os
import sys
import inspect

#--- 3rd party h5py package:
import h5py

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.S102 import S102
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.IS102 import IS102
from msc_pygeoapi.process.dfo.chs.enav.pjs.util.TimeMachine import TimeMachine
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTOutFileAttr import SFMTOutFileAttr

#---
class SFMTDataFactory(TimeMachine, SFMTOutFileAttr) :

  """
  Provide some utility instance methods to S<NNN> sub-classes(except S102).
  """

  #---
  def __init__(self, S102Obj) :

    """
    S102Obj (type->S102): A S102 class instance object.
    """

    TimeMachine.__init__(self)
    SFMTOutFileAttr.__init__(self, S102Obj)

  #---
  def setCoordinatesHDF5MetaData(self, NbPoints, AxisNameDSetDict,
                                 PointsDataKeysTuple, HDF5CoordinatesGroup) :
    """
    Set the coordinates positioning Group in the HDF5 file data structure.

    NbPoints (type->int): Number of grid points(at least one obviously) in the coordinates
    positioning HDF5 GROUP data structure.

    AxisNameDSetDict (type->dictionary): A dictionary holding the lon-lat strings ids. to
    use for the H5T_COMPOUND type definition.

    PointsDataKeysTuple (type->tuple): A tuple holding all the point(s) lon-lat coordinates combo.

    HDF5CoordinatesGroup (type->h5py file GROUP data object): The HDF5 GROUP data structure object
    where to set the coordinates.

    return (type->h5py file HDF5 GROUP data structure object)
    """

    #--- Uncomment for degugging:
    #methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #: Doc AxisNames lon-lat strings ids should be in the AxisNameDSetDict[ self.DSET_ID[0] ][ self.DATAVALUE_ID[0] ]
    #      sub-dictionary and indexed with [ self.LONPOS_IDX_ID[0] ] and [ self.LATPOS_IDX_ID[0] ] respectively:

    #    NOTE: Need to use the str() function here to be sure that numpy do not crash.
    lonStrId= str(AxisNameDSetDict[ self.DSET_ID[0] ][ self.DATAVALUE_ID[0] ][ self.LONPOS_IDX_ID[0] ])
    latStrId= str(AxisNameDSetDict[ self.DSET_ID[0] ][ self.DATAVALUE_ID[0] ][ self.LATPOS_IDX_ID[0] ])

    #: Doc Define the H5T_COMPOUND type having lon,lat as type members.
    geometryValuesTypeDef= [ (lonStrId, h5py.h5t.NATIVE_FLOAT), (latStrId, h5py.h5t.NATIVE_FLOAT) ]

    #: Doc Create the dataset containing an array(dimensions (nbPoints,1) of geometryValuesTypeDef
    #      H5T_COMPOUND type objects.

    #      NOTE: Using (numCOL=nbPoints,numROW=1) array mapping which is the usual array mapping(x,y)
    #      used in numerical modelling(so we got a row vector here).
    geometryValuesData= HDF5CoordinatesGroup.create_dataset( self.GEOMVALUES_ID[0],
                                                             (NbPoints,1), dtype= geometryValuesTypeDef)
    #: Doc Data points ieration counter.
    midx= 0

    #: Doc Loop names shorcuts to the self._s102TilesObj LAT LON indexing values (which are unary tuples BTW):
    TILES_LAT_IDX= self._s102TilesObj.TILES_LAT_IDX
    TILES_LON_IDX= self._s102TilesObj.TILES_LON_IDX

    #: Doc Define the constant string split character just once as an unary tuple.
    splitChar= ( str("=") ,)

    #: Doc Loop on data points lons-lats pairs to extract the float values.
    for lonLatPair in PointsDataKeysTuple :

      #: Doc Extract lon-lat values from lonLatPair string key.
      tmpSplit= lonLatPair.split(self.DICT_KEYS_SEP[0])

      #: Doc Set the geometryValuesData H5T_COMPOUND type members values
      #      (Note the indexing. It is somewhat like a member assignation done on an array of structs objects in C language:
      #      arrayOfStructs[index].member= value
      geometryValuesData[midx,lonStrId]= float(tmpSplit[ TILES_LON_IDX[0] ].split( splitChar[0] )[1])
      geometryValuesData[midx,latStrId]= float(tmpSplit[ TILES_LAT_IDX[0] ].split( splitChar[0] )[1])

      midx += 1

    #--- end loop on pointsDataKeysList

    #: Doc return the HDF5CoordinatesGroup object for subsequent usage by the calling method.
    return HDF5CoordinatesGroup

  #---
  def getDTStringsSecondsDiff(self, ADateTimeString, AnotherDateTimeString, DateTimeStringFmt) :

    """
    Return the difference in seconds between two time stamps regardless
    of their respective values(the returned value could be > 0, 0 or < 0 ).

    ADateTimeString (type->string): A timestamp string with the DateTimeStringFmt format.

    AnotherDateTimeString (type->string): Another timestamp string with the DateTimeStringFmt format.

    DateTimeStringFmt (type->string): The string format to use to convert the timestamps strings to seconds.

    NOTE: No fool-proof checks here for performance reasons.

    return (type->string)
    """

    #--- NOTE: No fool-proof checks here for performance reasons:

    return self.getSeconds(ADateTimeString, DateTimeStringFmt) - \
             self.getSeconds(AnotherDateTimeString, DateTimeStringFmt)

  #---
  @staticmethod
  def getS102TilesBBoxes(CfgDir, S102TilesBBoxesFilesDict, ExcludeTilesBBoxesTuple= None) :

    """
    Static class method(not bounded to a SFMTDataFactory class instance object) that
    retreives the S102 tiles bounding boxes data from ESRI shapefile(s).

    CfgDir (type->string): The config. dir where to find the shapefile(s).

    S102TilesBBoxesFilesDict (type->dictionary): A dictionary holding the name(s) of the S102 tiles
    bounding boxes of the shapefile(s).

    ExcludeTilesBBoxesTuple (type->tuple) <OPTIONAL> Default->None : A tuple holding one or more
    regular lat-lon bounding boxes used to exclude S102 L2 tiles that are considired useless(ex.
    outside the canadian coastal waters limits).
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    if S102TilesBBoxesFilesDict is None :
      sys.exit("ERROR "+methId+" S102TilesBBoxesFilesDict is None ! \n")

    #: Doc Check if we have to exclude some tiles.
    if ExcludeTilesBBoxesTuple is not None :

      sys.stdout.write("INFO "+methId+ " Will use regular bounding boxes -> "+
                       str(ExcludeTilesBBoxesTuple)+" to exclude some tiles.\n")
    #--- end if block.

    #: Doc Sort the string ids. keys in increasing order.
    s102TilesBBoxesFilesDictKeys= tuple( sorted( S102TilesBBoxesFilesDict.keys() ) )

    if len(s102TilesBBoxesFilesDictKeys) == 0 :
      sys.exit("ERROR "+methId+" S102TilesBBoxesFilesDict must contain at least one level file ! \n")

    #: Doc Loop on the S102 levels ids. keys to validate the ids.:
    for tilesLevelId in s102TilesBBoxesFilesDictKeys :

      #--- Validate the id.
      if tilesLevelId not in IS102.TILES_ALLOWED_LEVELS :
        sys.exit("ERROR "+methId+" Invalid S102 level -> "+tilesLevelId+" !\n")

    #: Doc Need at least the default S102 base level(which is 2 normallY) in the input data:
    if IS102.DEFAULT_TILES_BASE_LEVEL[0] not in s102TilesBBoxesFilesDictKeys :
      sys.exit("ERROR "+methId+" S103 base level -> "+
               IS102.DEFAULT_TILES_BASE_LEVEL[0]+" not present in S102TilesBBoxesFilesDict !\n")

    baseLevelSHPFile= S102TilesBBoxesFilesDict[ IS102.DEFAULT_TILES_BASE_LEVEL[0] ]

    #: Doc baseLevelSHPFile could already be a complete path if we are running inside ECCC HPC operations maestro world
    if not os.access(baseLevelSHPFile, os.F_OK) :

      if CfgDir is None :
        sys.exit("ERROR "+methId+" CfgDir is None ! \n")

      #--- End inner if.

      #: Doc Need to build complete path for the base level SHP file.
      #  (NOTE os.sep is the directory arborescence separator)
      baseLevelSHPFile= CfgDir + os.sep + baseLevelSHPFile

      #: Doc Need to re-verify if baseLevelSHPFile exists and it is now an ERROR if not found at this point:
      if not os.access(baseLevelSHPFile, os.F_OK) :
        sys.exit("ERROR "+methId+" baseLevelSHPFile -> " + baseLevelSHPFile + " not found ! \n")

      #--- End inner if.

    else :
      sys.stdout.write("INFO "+methId+" Running inside ECCC Maestro operations world\n")

    #--- End if-else block

    sys.stdout.write("INFO "+methId+" Reading S102 base level -> "+
                     IS102.TILES_LEVEL2_ID[0]+" tiles in -> "+ baseLevelSHPFile+"\n")

    #: Doc Create the base level S102 object:
    s102Tiles= S102( IS102.DEFAULT_TILES_BASE_LEVEL[0], baseLevelSHPFile, ExcludeTilesBBoxesTuple)

    #: Doc Add next level(s) tiles data(if any):
    if len(s102TilesBBoxesFilesDictKeys) > 1 :

      #: Doc Get the dictionary holding the base level tiles bounding boxes definitions:
      thisLevelTilesDict= s102Tiles._dataDict[ IS102.DEFAULT_TILES_BASE_LEVEL[0] ]

      #print ("thisLevelTilesDict 1"+str(thisLevelTilesDict.keys()))

      #: Doc Loop on the next S102 levels(at least one here) to process:
      for nextLevelId in s102TilesBBoxesFilesDictKeys[1:] :

        if not os.access(S102TilesBBoxesFilesDict[ nextLevelId ], os.F_OK) :

          #: Doc Need to build complete path for the next S102 level SHP file:
          nextLevelSHPfile= CfgDir + S102TilesBBoxesFilesDict[ nextLevelId ]

        else :

          #: Doc S102TilesBBoxesFilesDict[ nextLevelId ] is a complete S102 file path
          nextLevelSHPfile= S102TilesBBoxesFilesDict[ nextLevelId ]

        #--- End if-else block

        sys.stdout.write("INFO "+methId+" adding tiles at level -> "+
                         nextLevelId+" from file -> "+nextLevelSHPfile+"\n")

        #print("thisLevelTilesDict 2"+str(thisLevelTilesDict.keys()))

        #: Doc Set the s102Tiles._dataDict sub-dictionary of the next level tiles bounding boxes data:
        s102Tiles._dataDict[nextLevelId]= \
          s102Tiles.getNextLevelTiles(nextLevelId, nextLevelSHPfile, thisLevelTilesDict, ExcludeTilesBBoxesTuple)

        #: Doc Set the next level dictionary shortcut for the next loop iteration(if any):
        thisLevelTilesDict= s102Tiles._dataDict[nextLevelId]

      #--- end block loop for nextLevelId in s102TilesShapefilesDict.keys()[1:]
    #--- end block if len(S102TilesShapefilesTuple) > 1

    sys.stdout.write("INFO "+methId+" end \n")

    #--- Return the created and filled S102 object to the calling method.
    return s102Tiles

  #---
  def setDateTimeHDF5MetaData(self, TimeIncrInterval, DateTimeKeys, HDF5MetaDataDict) :

    """
    Build the starting and ending timestamps strings (i.e. the values of the
    "dateTimeOfFirstRecord" and the "dateTimeOfLastRecord" ATTRIBUTEs of the HDF5
    "<product>" GROUP) in the S<NNN> DHP format used (Ex. "20180722T120000Z")
    and put the values in the HDF5MetaDataDict dictionary. Also set the time interval
    value in the HDF5MetaDataDict dictionary(i.e. the "timeRecordInterval" ATTRIBUTE
    of the same HDF5 "<product>" GROUP) and also set the "numGRP" and "numberOfTimes"
    ATTRIBUTEs of the of the same HDF5 "<product>.01" GROUP in the HDF5MetaDataDict dictionary.

    TimeIncrInterval (type->int): the interval of time(in seconds) between two successive(in time) data values.

    DateTimeKeys (type->tuple): Tuple holding all the date timestamps strings for the products.

    HDF5MetaDataDict (type->dictionary): The dictionary to set with the extracted time parameters.

    return (type->dictionary)

    NOTE: Fool-proof checks are commented for performance reasons.
    """

    #--- Uncomment for degugging:
    #methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #--- Get first and last date-times as splitted strings from DateTimeKeys:
    #    MOTE: Its obvious here that the DateTimeKeys must be in increasing order.
    #          and that we must have at least two items in DateTimeKeys tuple.

    #: Doc First date-timestamp:
    frstDateTimeSplit= DateTimeKeys[0].split(self.DATE_TIME_SPLIT_STR[0])

    #: Doc Last date-timestamp:
    lastDateTimeSplit= DateTimeKeys[ len(DateTimeKeys)-1 ].split(self.DATE_TIME_SPLIT_STR[0])

    #### COMMENTED FOR PERFORMANCE REASONS:
    ##--- Check if the timeRecordInterval is the same for the rest of the date time stamps:
    ##    (unlikely to happen, this check could be removed for performance reasons)
    #prevDt= 1
    #for nextDt in DateTimeKeys[2:] :
    #  secondsDiff= self.getSeconds(nextDt, self.DEFAULT_GET_SECONDS_FMT[0]) - \
    #                 self.getSeconds(dateTimesKeys[prevDt], self.DEFAULT_GET_SECONDS_FMT[0])
    #  if secondsDiff != timeRecordInterval :
    #    sys.exit("ERROR " +thisMethod+
    #              " Found an invalid timeRecordInterval -> "+str(secondsDiff)+" between "+nextDt+" and "+prevDt + " \n")
    #  else:
    #    prevDt += 1
    ##--- end loop on DateTimesKeys[2:]
    #  sys.stdout.write("INFO "+thisMethod+" Time intervals between successive time stamps are all the same with value -> "
    #                    +str(timeRecordInterval)+ " seconds \n")

    #: Doc Set the timeRecordInterval attribute in HDF5MetaDataDict:
    HDF5MetaDataDict[ self.TIME_REC_INTRV_ID[0] ][ self.DATAVALUE_ID[0] ]= TimeIncrInterval

    #: Doc Format first and last date-times strings as wanted by the S111&S104 data spec.:
    frstYYYYMMDDhhmmss= ( frstDateTimeSplit[0] + self._jsonCommonMetaDataDict[ self.DATETIME_SEP_ID[0] ] + frstDateTimeSplit[1] ,)
    lastYYYYMMDDhhmmss= ( lastDateTimeSplit[0] + self._jsonCommonMetaDataDict[ self.DATETIME_SEP_ID[0] ] + lastDateTimeSplit[1] ,)

    #: Doc Set the string values of dateTimeOfFirstRecord and dateTimeOfLastRecord ATTRIBUTEs
    HDF5MetaDataDict[ self.DATETIME_FRST_REC_ID[0] ][ self.DATAVALUE_ID[0] ]= frstYYYYMMDDhhmmss[0]
    HDF5MetaDataDict[ self.DATETIME_LAST_REC_ID[0] ][ self.DATAVALUE_ID[0] ]= lastYYYYMMDDhhmmss[0]

    #: Doc How many timestamps do we have ??:
    nbTimeIncrements= ( len(DateTimeKeys) ,)

    #: Doc Here numGRP and numberOfTimes HDF5 metadata values are both the value of nbTimeIncrements
    HDF5MetaDataDict[ self.NUM_GRP_ID[0] ][ self.DATAVALUE_ID[0] ]= nbTimeIncrements[0]
    HDF5MetaDataDict[ self.NUM_TIMES_ID[0] ][ self.DATAVALUE_ID[0] ]= nbTimeIncrements[0]

    return HDF5MetaDataDict
