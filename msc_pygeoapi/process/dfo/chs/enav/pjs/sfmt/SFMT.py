#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMT.py
# Creation        : September/Septembre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMT implementation.
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
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.S102 import S102
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.IS102 import IS102
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTData import SFMTData
from msc_pygeoapi.process.dfo.chs.enav.pjs.util.JsonCfgIO import JsonCfgIO

#---
class SFMT(SFMTData) :

  """
  The SFMT class is the super class which is inherited by all S<NNN> sub-classes .
  """

  #---
  def __init__(self, S102Obj, JsonCommonMetaDataDict, JsonTemplatesDir,
               ProductStrNameId, TypeOfProductData, DataCodingFmt, OutputDir) :
    """
    S102Obj (type->S102): A S102 class instance object.

    JsonCommonMetaDataDict (type->dictionary) : A dictionary holding the common json
    formatted metadata to use for the S<NNN> DHP data.

    JsomTemplatesDir (type->string) : The complete directory path where the specific
    S<NNN> DHP data json formatted metadata file can be found.

    ProductStrNameId (type->string) : The string name id. for the product(i.e. S<NNN>).

    TypeOfProductData (type->int) : The integer code of the input data type (i.e. typeOfCurrentData
    or typeOfWaterLevelData metadata value (ex. forecasts), see the last version of the official 
    IHO S111 spec. PDF documentation file for more details).

    DataCodingFmt (type->enum.Enum) : The enum.Enum object that holds the integer code of the SFMT
    DHP gridded data type(i.e. dataCodingFormat metadata value, see the last version of the official
    IHO S111 spec. PDFdocumentation file for more details).

    OutputDir (type->string) : The output directory where to write the SFMT DHP data HDF5 files.
    """

    #---
    SFMTData.__init__(self, S102Obj, JsonCommonMetaDataDict)

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methId+" Start, TypeOfProductData="+str(TypeOfProductData)+
                     ", ProductStrNameId="+ProductStrNameId+", DataCodingFmt.name="+DataCodingFmt.name+", OutputDir="+OutputDir+"\n")

    #--- Some fool proof checks.
    if ProductStrNameId is None :
      sys.exit("ERROR "+methId+" ProductStrNameId is None !\n")

    if self._s102TilesObj is None :
      sys.exit("ERROR "+methId+" self._s102TilesObj is None !\n")

    if self._jsonCommonMetaDataDict is None :
      sys.exit("ERROR "+methId+" self._jsonCommonMetaDataDict is None !\n")

    #: Doc JsonTemplatesDir will be only used by the derived classes instances but
    #      anyways check if it's ok here before going further.
    if JsonTemplatesDir is None :
      sys.exit("ERROR "+methId+" argument JsonTemplatesDir is None ! \n")

    if not os.access(JsonTemplatesDir, os.F_OK) :
      sys.exit("ERROR "+methId+" JsonTemplatesDir -> "+JsonTemplatesDir+" not found ! \n")

    #: Doc Build the path to the SFMT DHP template json config file,
    jsonSpecProductConfigFile= JsonTemplatesDir + "/" + ProductStrNameId+self.NORMAL_JSON_FILE_EXT[0]

    sys.stdout.write("INFO "+methId+
                     " Getting specific product metadata config. from json formatted file -> "+jsonSpecProductConfigFile+"\n")

    #: Doc Retrieve the specific HDF5 root metadata dictionary from the json config. data file:
    self._jsonRootTypeMetaDataDict= JsonCfgIO.getIt(jsonSpecProductConfigFile)[ self.ROOT_GROUP_ID[0] ]

    #---
    if OutputDir is None :
      sys.exit("ERROR "+methId+" argument OutputDir is None ! \n")

    #---
    if not os.access(OutputDir, os.F_OK) :
      sys.exit("ERROR "+methId+" OutputDir -> "+OutputDir+" not found ! \n")

    #: Doc OutputDir Will be used later so keep a reference in self object:
    self._outputDir= OutputDir

    if TypeOfProductData is None :
      sys.exit("ERROR "+methId+" argument TypeOfProductData is None ! \n")

    if DataCodingFmt is None :
      sys.exit("ERROR "+methId+" argument DataCodingFmt is None ! \n")

    #--- Check if the DataCodingFmt Enum object is valid before going further.
    if DataCodingFmt.name not in tuple(ISFMT.ALLOWED_DATA_CODING_FMT.__members__.keys()) :
      sys.exit("ERROR "+methId+" Invalid SFMT DHP data coding format ->"+DataCodingFmt.name+" !\n")

    sys.stdout.write("INFO "+methId+" Using SFMT DHP data coding format -> "+DataCodingFmt.name+" !\n")

    #: Doc Set some specific HDF5 metadata for SFMT DHP data coding format 3.
    if DataCodingFmt.name == ISFMT.ALLOWED_DATA_CODING_FMT.three.name :

      #: Doc Set self._productGroupAttr2Set to the self.DC3_GROUP01_ATTRS_2SET
      #      dictionary for the setup of the HDF5 metadata for the specific SFMT
      #      DHP data coding format 3
      self._productGroupAttrDict2Set= self.DC3_GROUP01_ATTRS_2SET

      #: Doc Set the string suffix that has to be appended to the SFMT DHP
      #      HDF5 GROUP data structure string id for the specific data coding format 3
      self._productGroupDataStrSuffix= self.HDF5_DC3_GRP01_ID[0]

    #--- end if block.

    sys.stdout.write("INFO "+methId+" end\n")

  #--- Method to be overriden by the S<NNN> DHP derived classes
  def writeOneTile(self, TileId, TileDict, DateTimeStringsOutDict,
                   RegionalModelName, ConversionOperationFlag, OverWrite= True, InfoLog= False) :
    """
    Write a tiled SFMT DHP data HDF5 file.
    Method to be overriden by S104, S111 derived classes.

    TileId (type->string): A tile string id.

    TileDict (type->dictionary): The properly formatted dictionary containing the tile water levels data

    DateTimeStringsOutDict (type->dictionary): Already formatted SFMT DHP spec. date time stamps strings dictionary.

    RegionalModelName (type->string): A string id. name for the model from which the input data come from.

    ConversionOperationFlag (type->boolean): Data conversion flag to be handled by sub-classes.

    OverWrite (type->boolean) <OPTIONAL> Default->False: A flag to signal that the already existing data products
    files are to be overwritten with or without issuing a WARNING log message to the stdout stream.

    InfoLog (type->boolean) <OPTIONAL> Default->True: To put(or not) log INFO messages on the stdout stream.
    """

    #--- Shortcut to the S102Tiles object.
    s102TilesObj= self._s102TilesObj

    #: Doc Check for empty tiles(unlikely but we never know when an occurence of Murphy's law will eventually show up)
    if not s102TilesObj.POINTS_DATAOUT_ID[0] in TileDict :
      thisMethod= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
      sys.stdout.write("WARNING "+thisMethod+" No output currents data found in tile "+TileId+ " skip it !\n")
      return
    #--- end if block.

    #: Doc Shortcut to the tile points data dict:
    self._pointsDataOutDict= TileDict[ s102TilesObj.POINTS_DATAOUT_ID[0] ]

    #: Doc Get the sorted points data keys(strings). Those keys are the lon,lat pairs of each point.
    self._pointsDataOutKeysTuple= tuple( sorted( list(self._pointsDataOutDict.keys()) ) )

    #: Doc How many data points(metadata "numberOfNodes") contained in the DH product tile we have ?
    self._nbPoints= len(self._pointsDataOutKeysTuple)

    #--- Fool-proof check(un-comment it if needed) on the number of grid points:
    if self._nbPoints == 0 :
      sys.exit("ERROR "+str(__name__)+"."+str(inspect.stack(0)[0][3])+" method:"+" self._nbPoints == 0\n")

    if self._productGroupAttrDict2Set is None :
      sys.exit("ERROR "+str(__name__)+"."+str(inspect.stack(0)[0][3])+" method:"+" self._productGroupAttrDict2Set is None! \n")

    if InfoLog:
      thisMethod= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
      sys.stdout.write("INFO "+thisMethod+" Got "+str(self._nbPoints)+" data point(s) for tile -> "+TileId+"\n")
      sys.stdout.write("INFO "+thisMethod+" writing data for tile -> "+TileId+ "\n")

  #--- end writeOneTile method block
