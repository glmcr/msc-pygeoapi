#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : DFO-CHS-ENAV-DHP
# File/Fichier    : dhp/sfmt/s111/S111DataCodingFmt3.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s111.S111DataCodingFmt3 implementation.
#
# Remarks :
#
# License :
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
import time
import inspect
import multiprocessing

#--- 3rd party h5py package
import h5py

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s111.S111 import S111
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.IS104 import IS104
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s111.IS111 import IS111

#---
class S111DataCodingFmt3(S111) :

  """
  Class S111DataCodingFmt3 is used to produce S111 data tiled files in the
  DataCodingFormat nb.3 (i.e. currents data coming from unstructured grids models
  like FVCOM or WebTide). Please consult the official IHO S111 document spec.
  for more details.

  NOTE: We could also use data from models results mapped on polar-stereographic or regular
  lon-lat grids as if they were coming from unstructured grids provided that it is
  compatible with the de-facto default GIS EPSG:4326 reference system spec.
  """

  #---
  def __init__(self, S102TilesObj, JsonCommonMetaDataDict,
               JsonTemplatesDir, TypeOfCurrentData, GenericModelName, OutputDir) :
    """
    Constructor for class S111DataCodingFmt3.

    S102TilesObj (type->S102Tiles): A S102Tiles object.

    JsonCommonMetaDataDict (type->dictionary): A dictionary holding the json formatted common meta data to use for the SFMT
    DHP data

    JSONTemplatesDir (type->string): The complete path of the directory where to find the S111 DHP data json formatted 
    metadata definitions used.

    TypeOfCurrentData (type->int): The type of the currents data(See TYPES_OF_DATA dictionary defined in ISFMTMetaDataAttr
    super-class src file for details).

    DataCodingFmt (type->Enum.enum): The Enum.enum object instance that holds the integer code of the SFMT DHP
    gridded data type(i.e. dataCodingFormat metadata value see last version of the official IHO S111 spec. PDF doc. file).

    GenericModelName (type->string): A string which is representative of model from which the currents input data used for
    the S111 DHP data comes from (ex. "NEMO", "H2D2" "WebTide"). No mention of a regional entity of the model at this point.
    """

    thisMethod= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+thisMethod+" Start: JsonTemplatesDir="+JsonTemplatesDir+
                     ", OutputDir="+OutputDir+", GenericModelName="+GenericModelName+"\n")

    #: Doc super class __init__ method. Note the ISFMT.ALLOWED_DATA_CODING_FMT.three argument.
    S111.__init__(self, S102TilesObj, JsonCommonMetaDataDict, JsonTemplatesDir,
                  TypeOfCurrentData, ISFMT.ALLOWED_DATA_CODING_FMT.three, GenericModelName, OutputDir)

    sys.stdout.write("INFO "+thisMethod+" End\n")

  #---
  def writeOneTile(self, TileId, TileDict, DateTimeStringsOutDict,
                   RegionalModelName= None, ConvertMs2Knots= True, OverWrite= True, InfoLog= False) :
    """
    Write a tiled S111 DHP data HDF5 file using the IHO spec. data coding format nb.3.

    TileId (type->dictionary): A dictionary holding model currents data points for a tile.

    TileDict (type->dictionary): A dictionary holding model currents data points for a tile.

    DateTimeStringsOutDict (type->dictionary): Already formatted SFMT DHP spec. date-timestamps strings dictionary.

    RegionalModelName (type->string) <OPTIONAL> Default->None: The name of the regional(ex. CIOPS-E) model from which the water levels data come from.

    ConvertMs2Knots (type->boolean) <OPTIONAL> Default->True: To convert(or not) meters/seconds to knots if needed(and it normally always the case).

    OverWrite (type->boolean) <OPTIONAL> Default->True: A flag to signal(or not) that the already existing data products files are to be overwritten
    with or without issuing a WARNING log message to the stdout stream.

    INFOLog (type->boolean) <OPTIONAL> Default ->False : To put(or not) log INFO messages on the stdout stream.

    NOTE: Just one fool-proof check for performance reasons.

    TODO: There is still some slight redundancy between this method and the equivalent S104DataCoding3.writeOneTile
    method so it would be more optimal(in terms of OOP paradigm) to implement the common processing in a
    SFMTDataCodingFmt3 super-class writeOneTile method to get rid of this redundancy.
    """

    if InfoLog :
      thisMethod= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
      sys.stdout.write("INFO "+thisMethod+" Start : TileId="+TileId+
                       ", self._outputDir="+self._outputDir+", ConvertMs2Knots="+str(ConvertMs2Knots)+"\n")
    #--- end if block.

    #: Doc Using S111 super class writeOneTile for generic processing.
    super(S111DataCodingFmt3,self).writeOneTile(TileId, TileDict, DateTimeStringsOutDict,
                                                RegionalModelName, ConvertMs2Knots, OverWrite, InfoLog)

    #--- NOTE: No check for the validity of the three items returned by
    #          super(S111DataCodingFmt3,self)writeOneTile here for performance reasons.

    #: Doc Currents speed and direction compound type definition
    speedDirectionTypeDef= [ (str(IS111.DIR_METADATA_ID[0] ), h5py.h5t.NATIVE_FLOAT),
                             (str(IS111.SPEED_METADATA_ID[0] ), h5py.h5t.NATIVE_FLOAT) ]

    #: Doc Get the h5py.special_dtype for the timestamp ATTRIBUTE.
    timeStampGroupStrDtype= ( h5py.special_dtype( vlen= self.H5PY_STRING_SPECIAL_DTYPE[0] ) ,)

    #: Doc Loop on all time-stamps available for the tile
    for dateTimeKey in self._dateTimeKeys :

      if InfoLog:
        sys.stdout.write("INFO "+thisMethod+" writing tile "+TileId +" data at dateTime -> "+ dateTimeKey +"\n")

      #: Doc Get the already and rightly DHP formatted date time stamp string from DateTimeStringsOutDict.

      #--- NOTE1: Each DateTimeStringsOutDict[dateTimeKey] is an unary tuple.
      #    NOTE2: We get a quite spectacular(about 2.5 times faster) performance gain with that trick
      #           instead of re-doing the string formatting operation for each time stamp of
      #           each output file
      dateTimeStampStrings= DateTimeStringsOutDict[dateTimeKey][0]

      #: Doc NOTE: dateTimeStampStrings is a two item tuple:
      timeStampGroup= self._hdf5ProductGroupData.create_group(dateTimeStampStrings[0][0])

      #: Doc Create time stamp attribute in timeStampGroup.
      timeStampGroup.attrs.create(self.TIMESTAMP_METADATA_ID[0], dateTimeStampStrings[1][0], dtype= timeStampGroupStrDtype[0] )

      #: Doc Create speed,direction values dataset compound type in timeStampGroup.

      #--- NOTE: Keep the same (numCOL=self._nbPoints,numROW=1) array mapping as the geometry compound type.
      valuesData= timeStampGroup.create_dataset(self.VALUES_METADATA_ID[0],
                                                (self._nbPoints,1), dtype= speedDirectionTypeDef)

      #: Doc Counter for valuesData compound type object loop indexing:
      valueIdx= 0

      #: Doc Loop on tile points:
      for lonLatPairKey in self._pointsDataOutKeysTuple :

        #: Doc Get the UU,VV pair for the model data point at the time-stamp being processed from
        #      the self._pointsDataOutDict (tile dictionary)
        uuvvPair= self._pointsDataOutDict[lonLatPairKey][dateTimeKey]

        #: Doc Set the proper velocity(converted to knots) and navigation angle in the valuesData output:
        self.setCurrSpeedAndDirection(uuvvPair, valueIdx, valuesData, ConvertMs2Knots)

        #: Doc Increment compound type array index:
        valueIdx += 1

      #--- end loop on tile points:
    #--- end loop on time-stamps

    #--- Close the HDF5 python stuff and get outta'here
    self._hdf5FileRootObj.close()

    if InfoLog :
      sys.stdout.write("INFO " +thisMethod+" Done with writing tile "+TileId+
                       ", process id="+str(multiprocessing.current_process())+"\n") # HDF5 data in file "+ oFilePath +"\n")

  #--- end method writeOneTile
