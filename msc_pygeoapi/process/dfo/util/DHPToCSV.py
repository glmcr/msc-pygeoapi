#-*-Python-*-
# -*- coding: ascii -*-
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/util/DHPToCSV.py
# Creation        : January/Janvier 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Module dhp.util.DHPToCSV implementation
#                for ENAV-DHP products to csv format conversion
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
import glob
import inspect

#---
import h5py
#---
from dhp.sfmt.ISFMT import ISFMT
from dhp.sfmt.s104.IS104 import IS104
from dhp.sfmt.s111.IS111 import IS111
from dhp.util.Py2And3 import Py2And3
from dhp.util.JsonCfgIO import JsonCfgIO

#--- TODO: Add the possibility(option) of using this class in the DHPMain script ??

#---
class DHPToCSV(ISFMT) :

  #---
  def __init__(self) :

    ISFMT.__init__(self)

    #: Doc Only data coding format 3 allowed for now:
    self.__csvConvMethodsDict= { ISFMT.ALLOWED_DATA_CODING_FMT.three.name :
                                 self.DataCodingFmt3ToCSV }

  #---
  def convert( self,
               DHPInputDirectory,
               CSVOutputDirectory,
               DataCodingFmt) :
    """
    Conversion of SFMT DHP data files to CSV ASCII format.

    DHPInputDirectory (type->string): Directory where to
    found the SFMT DHP data file(s).

    CSVOutputDirectory (type->string): Directory where to
    write the CSV files outputs.

    DataCodingFmt (type->enum.Enum) : The enum.Enum object
    that contains the integer code of the SFMT DHP gridded
    or time series data type(i.e. dataCodingFormat metadata
    value, see the last version of the official IHO S111
    spec. PDF documentation file for more details).

    Remark: CSVOutputDirectory cannot be the same as
    DHPInputDirectory.
    """

    methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

    #--- Usual fool-proof checks:
    if DHPInputDirectory is None :
      sys.exit("ERROR "+methID+" DHPInputDirectory is None !\n")

    if CSVOutputDirectory is None :
      sys.exit("ERROR "+methID+" CSVOutputDirectory is None !\n")

    if DataCodingFmt is None :
      sys.exit("ERROR "+methID+" DataCodingFmt is None !\n")

    if not os.access(DHPInputDirectory, os.F_OK) :
      sys.exit("ERROR "+methID+
               " DHPInputDirectory -> "+DHPInputDirectory+" not found !\n")

    if not os.access(CSVOutputDirectory, os.F_OK) :
      sys.exit("ERROR "+methID+
               " CSVOutputDirectory -> "+CSVOutputDirectory+" not found !\n")
    #---

    if DataCodingFmt.name not in \
      tuple(ISFMT.ALLOWED_DATA_CODING_FMT.__members__.keys())  :

      sys.exit("ERROR "+methId+
               " Invalid SFMT DHP data coding format ->"+
               DataCodingFmt.name+" !\n")
    #--- end if block.

    #: Doc Get all DHP files(just the names without the input directory path) in a tuple.
    inputFiles= \
      tuple( sorted( glob.glob(DHPInputDirectory + "/*" + ISFMT.OUT_FILES_EXTENSION[0] ) ) )

    if len(inputFiles) == 0 :
      sys.exit("ERROR "+methID+
               " No file found in "+DHPInputDirectory+" !\n")
    #---

    s104MetaDataTuple= ( ISFMT.PRODUCTS_IDS.S104.name,
                         IS104.ELEV_METADATA_ID[0]   ,
                         IS104.TREND_METADATA_ID[0]   )

    s111MetaDataTuple= ( ISFMT.PRODUCTS_IDS.S111.name,
                         IS111.DIR_METADATA_ID[0]    ,
                         IS111.SPEED_METADATA_ID[0] )

    #: Doc Loop on input files to deal with both S111 and S104 DHP formats.
    for iFilePath in inputFiles :

      #: Doc Extract the DHP data file name first
      #  three characters which should be a <NNN>(like 111)  prefix:
      fileType= os.path.basename(iFilePath)[0:3]

      #: Doc Build the path of the input file.
      #iFilePath= DHPInputDirectory + "/" + iFile

      if fileType == IS111.OUT_FILES_PREFIX[0] :

        sys.stdout.write("INFO "+methID+
                         " Processing S111 product input file -> "+
                         iFilePath+"\n")

        #: Doc Apply the specific SFMT data coding conversion to CSV method.
        self.__csvConvMethodsDict[DataCodingFmt.name] ( iFilePath,
                                                        s111MetaDataTuple,
                                                        CSVOutputDirectory )

        #self.DataCodingFmt3ToCSV(iFilePath, s111MetaDataTuple, CSVOutputDirectory)

      #--- end inner if block.

      elif fileType == IS104.OUT_FILES_PREFIX[0] :

        sys.stdout.write("INFO "+methID+
                         " Processing S104 product input file -> "+
                         iFilePath+"\n")

        #: Doc Only data coding format 3 allowed for now:
        self.__csvConvMethodsDict[DataCodingFmt.name] ( iFilePath,
                                                        s104MetaDataTuple,
                                                        CSVOutputDirectory )

      else :

        #: Doc Skip other files which does not have the official file prefix string
        continue

      #--- end if-elif-else block.
    #--- end loop on SFMT DHP data files.

  #-- end method.

  def DataCodingFmt3ToCSV(self, DHPFile, DHPMetaDataTuple, CSVOutputDirectory) :

    """
    Convert SFMT DHP data coding format nb.3 HDF5 file(s)
    to a bunch of CSV files. We have to create one CSV
    file for each timestamp entry found in one DHP data
    HDF5 file.

    DHPFile (type->string): Complete file path to one
    DHP data coding format nb.3 HDF5 file.

    DHPMetaDataTuple (type->tuple): The specific(S111,
    S104, S412, ...) DHP metadata config. tuple.

    CSVOutputDirectory  (type->string): The main
    directory where to write the CSV outputs.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methID+
                           " start, DHPFile="+DHPFile+
                           ", CSVOutputDirectory="+CSVOutputDirectory+"\n")

    #--- Usual fool-proof checks:
    if DHPFile is None :
      sys.exit("ERROR "+methID+" DHPFile is None !\n")

    if not os.access(DHPFile, os.F_OK) :
      sys.exit("ERROR "+methID+" DHPFile -> "+DHPFile+" not found !!\n")

    if DHPMetaDataTuple is None :
      sys.exit("ERROR "+methID+" DHPMetaDataTuple is None !\n")

    if len(DHPMetaDataTuple) != 3 :
      sys.exit("ERROR "+methID+" DHPMetaDataTuple must hold three items !\n")

    if CSVOutputDirectory is None :
      sys.exit("ERROR "+methID+" CSVOutputDirectory is None !\n")

    if not os.access(CSVOutputDirectory, os.F_OK) :
      sys.exit("ERROR "+methID+" CSVOutputDirectory -> "+CSVOutputDirectory+" not found !\n")

    #: Doc Open HDF5 DH product input file in read mode.
    hdf5FileRootObj= h5py.File(DHPFile, "r")

    if hdf5FileRootObj is None :
      sys.exit("ERROR "+methID+" Cannot open DHPFile -> "+DHPFile+" !\n")

    #: Doc Extract the product feature id. in ProductMetaDataTuple.
    ProductHDF5FeatureId= DHPMetaDataTuple[0]

    #: Doc Get the corresponding product group feature id. from self.PRODUCT_FEATURE_IDS dictionary.
    prodHDF5FeatureGroupId= self.PRODUCT_FEATURE_IDS[ ProductHDF5FeatureId ][0]

    #: Doc Shortcut to the product feature group:
    prodHDF5FeatureGroup= hdf5FileRootObj[ prodHDF5FeatureGroupId ]

    if prodHDF5FeatureGroup is None :
      sys.exit("ERROR "+methID+
               " Cannot get the product HDF5 feature group -> "+
               prodHDF5FeatureGroupName+" from file -> "+DHPFile+" !\n")
    #--- end if block.

       #: Doc Check if the data coding format is indeed type 3.
    checkDataCodingFmt= prodHDF5FeatureGroup.attrs.get(self.DATA_CODING_FMT_ID[0])

    if checkDataCodingFmt is None :
      sys.exit("ERROR "+methID+ " Cannot get the HDF5 attribute -> "+
               self.DATA_CODING_FMT_ID[0]+" from the product HDF5 feature group -> "+prodHDF5FeatureGroupName+" !\n")
    #--- end if block.

    if checkDataCodingFmt != ISFMT.ALLOWED_DATA_CODING_FMT.three.value :
      sys.exit("ERROR "+methID+ " Invalid data coding format -> "+str(checkDataCodingFmt)+
               " Need data coding format -> "+str(ISFMT.ALLOWED_DATA_CODING_FMT.three.value)+" !\n")

    #--- end if block.

    #: Doc Build the string id. of the HDF5 GROUP 01.
    group01StrId= self.PRODUCT_FEATURE_IDS[ ProductHDF5FeatureId ][0] + self.HDF5_DC3_GRP01_ID[0]

    #: Doc Get the product HDF5 GROUP 01 data structure from the hdf5FileRootObj.
    group01Obj= hdf5FileRootObj[ prodHDF5FeatureGroupId + "/" + group01StrId ]

    #: Doc Get the product positioning(i.e. lon-lat coordinates) HDF5 GROUP.
    lonLatPosCompoundObj= group01Obj[ self.LLPOS_ID[0] ]

    #: Doc Extract the lon-lat Positioning sub-GROUP infos. from its HDF5 compound type object:
    #      (Note the [0] indexing at the end of the command)
    lonLatPosCompoundData= tuple(lonLatPosCompoundObj.values())[0]

    if lonLatPosCompoundData is None :
      sys.exit("ERROR "+methID+ " Cannot get the HDF5 compound type -> "+
               self.LLPOS_ID[0]+" from the product HDF5 group -> "+group01StrIndex+" !\n")

    nbTimeStamps= group01Obj.attrs.get(self.NUM_GRP_ID[0])

    if nbTimeStamps is None :
      sys.exit("ERROR "+methID+ " Cannot get the HDF5 attribute -> "+
               self.NUM_GRP_ID[0]+" from the product HDF5 GROUP -> "+group01StrIndex+" !\n")

    #: Doc Get the file name prefix.
    tileFileNamePrfx= os.path.basename(DHPFile).split(".")[0]

    #: Doc Build the CVS output directory path for the file.
    productCVSFileDirPath= CSVOutputDirectory + "/" + tileFileNamePrfx

    if not os.access(productCVSFileDirPath, os.F_OK) :

      #: Doc Create a sub-directory for each DHP data file in the CSV output directory:
      os.mkdir(productCVSFileDirPath)

    #: Doc Get the lon-lat strings ids. that will be used for indexing:
    llStrIds= prodHDF5FeatureGroup[self.AXIS_NAMES_ID[0]][:]

    #: Doc Avoid hard coding SNAFUs: Use the already defined lat,lon indices for
    #      DHP data files products creation.
    latIdx= int(self.LATPOS_IDX_ID[0].split(",")[0])
    lonIdx= int(self.LONPOS_IDX_ID[0].split(",")[0])

    #: Doc Iterate on the input file timestamps.
    for timeStampIter in tuple(range(0,nbTimeStamps)) :

      #: Doc Build the timestamp HDF5 GROUP data structure string id. key.
      timeStampGroupId= self.TIMESTAMP_GROUP_PREFIX_ID[0] + JsonCfgIO.formatTimeStampGroupNb(timeStampIter+1)

      #: Doc Get the timestamp HDF5 GROUP data structure object.
      timeStampGroup= group01Obj[timeStampGroupId]

      if timeStampGroup is None :
        sys.exit("ERROR "+methID+" Cannot get the timestamp GROUP -> "+
                 timeStampGroupId+" in HDF5 GROUP -> "+group01StrId+" !\n")

      #: Doc Get the timestamp string of the HDF5 data GROUP.
      timeStampString= timeStampGroup.attrs.get(self.TIMESTAMP_METADATA_ID[0])

      #--- NOTE: Need to use Py2And3.getASCIIStr(timeStampString) to get the concatenation working for Python3.
      csvFilePath= productCVSFileDirPath + "/" + tileFileNamePrfx + "_" + Py2And3.getASCIIStr(timeStampString) + ".csv"

      #: Doc Open(zapped if already existing) the csv file with a name which is representative of the S102 tile and the timestamp being processed:
      csvFile= open(csvFilePath, "w")

      sys.stdout.write("INFO "+methID+" Writing CSV file -> "+csvFilePath+"\n")

      #: Doc Write csv file header.

      #--- NOTE: Need to use Py2And3.getASCIIStr(llStrIds[latIdx]) and
      #          Py2And3.getASCIIStr(llStrIds[lonIdx]) to get the concatenation working for Python3.
      csvFile.write( Py2And3.getASCIIStr(llStrIds[latIdx])+
                     "," + Py2And3.getASCIIStr(llStrIds[lonIdx])+
                     "," + DHPMetaDataTuple[1] + "," + DHPMetaDataTuple[2] +"\n")

      #: Doc Get the currents direction,speed or water level,trend combos of
      #      the input data points from the HDF5 H5T_COMPOUND timeStampGroup data structure.
      #
      #      NOTE: The h5py get method returns a DATASET object holding itself a numpy array
      #            of H5T_COMPOUND objects.
      pointsDirCurrData= timeStampGroup.get(self.VALUES_METADATA_ID[0])

      #: lon-lat iteration variable for the data grid points.
      llIter= 0

      #: Doc Iterate on those H5T_COMPOUND two items data ojects to write them in the output csv file.
      for pointDataItem in pointsDirCurrData :

        #: Doc Extract point data two items compound object
        pointData= pointDataItem[0]

        #: Doc Extract lat-lon compound object for this point data.
        llCompoundDataItem= lonLatPosCompoundData[llIter][0]

        #: Doc Write the point data infos. in the CSV file.
        csvFile.write(str(llCompoundDataItem[latIdx]) + "," + str(llCompoundDataItem[lonIdx]) + "," + str(pointData[0]) + "," + str(pointData[1])+"\n")

        llIter += 1

      csvFile.close()

      #print("timeStampString="+timeStampString)
    #--- End for loop

    sys.stdout.write("INFO "+methID+" end\n")
  #---
