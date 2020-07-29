#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : DFO-CHS-ENAV-DHP
# File/Fichier    : dhp/sfmt/s104/S104.py
# Creation        : Septembre/September 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s104.S104 implementation.
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
import time
import math
import inspect

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMT import SFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.IS104 import IS104
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTData import SFMTData
from msc_pygeoapi.process.dfo.pjs.util.IDataIndexing import IDataIndexing
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.S104Factory import S104Factory

#---
class S104(SFMT, S104Factory) :

  """
  Class S104 defines some methods which are
  to be used by all S104 format flavors.
  It must inherited by the S104DataCodingFmt*
  derived classes.
  """

  #---
  def __init__( self,
                S102TilesObj,
                JsonCommonMetaDataDict,
                JsonTemplatesDir,
                TypeOfWaterLevelData,
                DataCodingFmt,
                GenericModelName,
                OutputDir ) :
    """
    A S104 object instance constructor.

    S102TilesObj (type->S102Tiles): A S102Tiles class instance object.

    JsonCommonMetaDataDict (type->dictionary): A dictionary which
    contains the json formatted common metadata to use for the SFMT DHP data.

    JsonTemplatesDir (type->string): The complete path of the
    directory where to find the S104 DHP data json formatted
    metadata definitions used.

    TypeOfWaterLevelData (type->int): The integer code of the
    type of the water levels data.(See TYPES_OF_DATA dictionary
    defined in ISFMTMetaDataAttr class src file for more details).

    DataCodingFmt (type->Enum.enum): The Enum.enum object instance
    that holds the integer code of the SFMT DHP gridded data type
    (i.e. dataCodingFormat metadata value see last version of the
    official IHO S111 spec. PDF documentation file).

    GenericModelName (type->string): The string name id. of the
    model from which the water levels data used for S104 products
    comes from (ex. "NEMO", "WebTide", "IWLS"). No mention of a
    specific regional name for the model at this point.

    OutputDir (type->string): The output directory where to write
    the HDF5 SFMT DHP data file(s).

    TODO: There is too many args. for this method. Some of those
    args. could be regrouped in a dictionary(or another class).
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methId+" start\n")

    #: Doc Note the ISFMT.PRODUCTS_IDS.S104.name
    #  passed to SFMT.__init__ as the 4th argument.
    SFMT.__init__( self,
                   S102TilesObj,
                   JsonCommonMetaDataDict,
                   JsonTemplatesDir,
                   ISFMT.PRODUCTS_IDS.S104.name,
                   TypeOfWaterLevelData,
                   DataCodingFmt,
                   OutputDir )

    #: Doc S104Factory class object MUST be instantiated after SFMT
    #      class instance object to get the S104 class instance(this)
    #      working as it should(i.e. that the IS104 class instance
    #      object initialized by the S104Factory.__init__(self)
    #      method should be done AFTER the ISFMT class instance object
    #      which is itself initialized by the SFMT.__init__ method).
    S104Factory.__init__(self)

    if TypeOfWaterLevelData is None :
      sys.exit("ERROR "+methId+" TypeOfWaterLevelData is None\n")

    if DataCodingFmt is None :
      sys.exit("ERROR "+methId+" DataCodingFmt is None\n")

    if DataCodingFmt not in ISFMT.ALLOWED_DATA_CODING_FMT :
      sys.exit("ERROR "+methId+\
               " Invalid DataCodingFmt ->"+DataCodingFmt.name+" !\n")
    #---

    if GenericModelName is None :
      sys.exit("ERROR "+methId+" GenericModelName is None\n")

    #--- Set the common S104 metadata values in
    #    the self.HDF5_SET_METADATA_PRODUCT dictionary.
    self.HDF5_SET_METADATA_PRODUCT[ self.TYPEOF_PRODUCT_DATA_ID[0] ]= TypeOfWaterLevelData

    #: Doc DataCodingFmt.value must be of int type.
    self.HDF5_SET_METADATA_PRODUCT[ self.DATA_CODING_FMT_ID[0] ]= DataCodingFmt.value

    self.HDF5_SET_METADATA_PRODUCT[ self.METH_TYPE_PRODUCT_ID[0] ]= GenericModelName

    #: Doc self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ]
    #  list can now be set to a tuple here.
    self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ]= \
      tuple( self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ] )

    sys.stdout.write("INFO "+methId+
                     " Using S104 DHP dataCodingFormat -> "+
                     DataCodingFmt.name+" with int value -> "+
                     str(DataCodingFmt.value)+" for data S104 products outputs\n")

    sys.stdout.write("INFO "+methId+" end\n")

  #---
  def writeCommonHDF5MetaData( self,
                               TileDict,
                               ProductGROUPDataStrId,
                               RegionalModelName= None,
                               INFOLog= False) :
    """
    S104 specific instance method for writing(creating)
    meta data in an HDF5 output file. This method is
    used by S104 sub classes(like S104DataCodingFmt3).

    TileDict (type->dictionary): A dictionary which
    contains model water levels data points for a tile.

    ProductGROUPDataStrId (type->string) : The specific
    S104 DH product string id for HDF5 GROUP data structure.

    RegionalModelName (type->string) <OPTIONAL> Default->None:
    The name of the regional(ex. CIOPS-E) model from which
    the water levels data come from.

    INFOLog (type->boolean) <OPTIONAL> Default->False:
    Flag to put(or not to) the INFO logs on the stdout.

    return (type->h5py file group object)
    """

    #methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    #if INFOLog :
    #  sys.stdout.write("INFO "+methId+" start\n")

    #if INFOLog :
    #  sys.stdout.write("INFO "+methId+" end\n")

    # : Doc Write the common metadata with the SFMT super-class writeCommonHDF5MetaData method.
    super(S104, self).writeCommonHDF5MetaData( TileDict,
                                               self.VERT_DATUM[0],
                                               ProductGROUPDataStrId,
                                               RegionalModelName,
                                               INFOLog )
  #---
  def writeOneTile( self,
                    TileId,
                    TileDict,
                    DateTimeStringsOutDict,
                    RegionalModelName= None,
                    ChartDatumConversion= True,
                    OverWrite= True,
                    InfoLog= False ) :
    """
    Generic S104 writeOneTile method.

    TileId (type->string): A tile string id.

    TileDict (type->dictionary): The properly formatted
    dictionary containing the tile water levels data

    DateTimeStringsOutDict (type->dictionary): Already
    formatted SFMT DHP data date-timestamps strings dictionary.

    RegionalModelName (type->string) <OPTIONAL> Default->None:
    The name of the regional(ex. CIOPS-E) model from which the
    water levels data come from.

    ChartDatumConversion (type->boolean) <OPTIONAL> Default->True:
    To(or not to) apply a chart datum conversion for the water
    levels values.

    OverWrite (type->boolean) <OPTIONAL> Default->True:
    A flag to(ot not to) signal that the already existing
    data products files are to be overwritten with or
    without issuing a WARNING log message to the stdout stream.

    InfoLog (type->boolean) <OPTIONAL> Default->False :
    To put(or not) log INFO messages on the stdout stream.

    return(type->h5py file root object)

    NOTE: No fool-proof checks for performance reasons.
    """

    #: Doc Using SFMT super class writeOneTile
    #      method to do the generic write part.
    super(S104,self).writeOneTile( TileId,
                                   TileDict,
                                   DateTimeStringsOutDict,
                                   RegionalModelName,
                                   ChartDatumConversion,
                                   OverWrite,
                                   InfoLog )

    #: Doc Define self._geoStrId according to the SFMT
    #      DHP water levels type for subsequent usage
    #      by sub classes objects instances.
    self._geoStrId= str(" ") + \
      ISFMT.PRODUCTS_IDS.S104.name + str(" tile ") + TileId

    #: Doc Open the S104 DHP data HDF5 file.
    self._hdf5FileRootObj= SFMTData.openOutFile( IS104.OUT_FILES_PREFIX[0],
                                                 TileId,
                                                 self._outputDir,
                                                 OverWrite,
                                                 InfoLog )

    #--- NOTE: self._hdf5FileRootObj validity check
    #          must have been done by SFMTData.openOutFile.

    #: Doc Get the current product string id.
    #  for the S104 specifig product GROUP HDF5
    #  data structure.
    watLevGROUPDataStrId= \
      self.PRODUCT_FEATURE_IDS[ ISFMT.PRODUCTS_IDS.S104.name ][0]

    #: Doc Write some common meta data in the S104 DHP data HDF5 file.
    self.writeCommonHDF5MetaData( TileDict,
                                  watLevGROUPDataStrId,
                                  RegionalModelName,
                                  InfoLog )

    #: Doc Get the water levels trends(Works only if
    #      timeIncrInterval == IS104.WL_TREND_TIMEINCR_MAX[0]
    #      for now.
    #      NOTE: This if block always need to be executed afer
    #            self.writeCommonHDF5MetaData method call.
    if self._timeIncrInterval == IS104.WL_TREND_TIMEINCR_MAX[0] :
      self.getWLTrendParams()

