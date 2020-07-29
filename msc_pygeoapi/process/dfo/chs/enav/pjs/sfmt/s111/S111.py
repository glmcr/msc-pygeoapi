#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : DFO-CHS-ENAV-DHP
# File/Fichier    : dhp/sfmt/s111/S111.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s111.S111 implementation.
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
import math
import time
import inspect

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMT import SFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s111.IS111 import IS111
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTData import SFMTData
from msc_pygeoapi.process.dfo.chs.enav.pjs.util.Trigonometry import Trigonometry

#---
class S111(IS111, SFMT, Trigonometry) :

  """
  Class S111 defines some methods which are to be used by all S111 format types.
  It is supposed to be inherited by the derived S111DataCodingFmt* classes.
  """

  def __init__(self, S102TilesObj, JsonCommonMetaDataDict, JsonTemplatesDir,
               TypeOfCurrentData, DataCodingFmt, GenericModelName, OutputDir ) :
    """
    S111 object instance constructor.

    S102TilesObj (type->S102Tiles): A S102Tiles class instance object.

    JsonCommonMetaDataDict (type->dictionary): A dictionary holding the json formatted common meta data
    to use for the SFMT DHP data.

    JsonTemplatesDir (type->string): The complete path of the directory where to find the S111 DHP json 
    formatted metadata definitions used.

    TypeOfCurrentData(type->int): The type of the currents data(See TYPES_OF_DATA dictionary defined in 
    ISFMTMetaDataAttr class src file for details).

    DataCodingFmt (type->Enum.enum): The Enum.enum object instance that holds the integer code of the 
    SFMT DHP data gridded data type(i.e. dataCodingFormat metadata value see last version of the
    official IHO S111 spec. PDF doc. file).

    GenericModelName (type->string): A string which is representative of model from which the currents
    input data used for SFMT DHP data comes from (ex. "NEMO", "H2D2" "WebTide"). No mention of a
    regional entity of the model at this point.
    """

    thisMethod= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+thisMethod+" start, OutputDir="+OutputDir+"\n")

    #: Doc SFMT super class MUST be initialized BEFORE IS111 super class.
    #: Doc Note the ISFMT.PRODUCTS_IDS.S111.name passed to SFMT.__init__ as the 4th argument.
    SFMT.__init__(self, S102TilesObj, JsonCommonMetaDataDict, JsonTemplatesDir,
                  ISFMT.PRODUCTS_IDS.S111.name, TypeOfCurrentData, DataCodingFmt, OutputDir)

    IS111.__init__(self)
    Trigonometry.__init__(self)

    if TypeOfCurrentData is None :
      sys.exit("ERROR "+thisMethod+" argument TypeOfCurrentData is None ! \n")

    if DataCodingFmt is None :
      sys.exit("ERROR "+thisMethod+" argument DataCodingFmt is None ! \n")

    if DataCodingFmt not in ISFMT.ALLOWED_DATA_CODING_FMT :
      sys.exit("ERROR "+thisMethod+" Invalid DataCodingFmt ->"+DataCodingFmt.name+" !\n")

    if GenericModelName is None :
      sys.exit("ERROR "+methId+" GenericModelName is None\n")

    #: Set the common S111 metadata values in the self.HDF5_SET_METADATA_PRODUCT generic dictionary.
    self.HDF5_SET_METADATA_PRODUCT[ self.TYPEOF_PRODUCT_DATA_ID[0] ]= TypeOfCurrentData

    #: Doc DataCodingFmt.value must be of int type.
    self.HDF5_SET_METADATA_PRODUCT[ self.DATA_CODING_FMT_ID[0] ]= DataCodingFmt.value

    self.HDF5_SET_METADATA_PRODUCT[ self.METH_TYPE_PRODUCT_ID[0] ]= GenericModelName

    #: Doc self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ] list can now be set to a tuple here.
    self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ]= tuple( self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ] )

    sys.stdout.write("INFO "+thisMethod+" Using S111 DHP dataCodingFormat -> "+ DataCodingFmt.name+
                     " with int value -> "+str(DataCodingFmt.value)+" for data S111 products outputs\n")

    sys.stdout.write("INFO "+thisMethod+" End\n")

  #---
  def setCurrSpeedAndDirection(self, CurrUVPair, ValueIdx, ValuesDataSet, ConvertMs2Knots= True) :

    """
    Set the current speed and direction for one data point in a HDF5 values compound type dataset.

    CurrUVPair (type->dictionary): A dictionary containing the U and V current component for the data point.

    ValueIdx (type->int): The index int values compound type dataset where to set speed and direction.

    ValuesDataSet (type->h5py file compound dataset object): The HDF5 values compound type dataset.

    ConvertMs2Knots (type->boolean) <OPTIONAL>: To convert(or not) meters/seconds to knots if needed(and it normally always the case)
    """

    #--- NOTE: no checks for objects existence or logs here, we need performance:

    uuf= float(CurrUVPair[ self.UUC_ID[0] ])
    vvf= float(CurrUVPair[ self.VVC_ID[0] ])

    speed= math.sqrt(uuf*uuf + vvf*vvf)

    #: Doc Convert m/s to knots if needed:
    if ConvertMs2Knots : speed= self.METERS_SECONDS_2_KNOTS[0]*speed

    #: Doc Set the current velocity in the ValuesDataSet dictionary.
    ValuesDataSet[ValueIdx, IS111.SPEED_METADATA_ID[0] ]= speed

    #: Doc Get the navigation angle (i.e. the direction where the current goes
    #      which is the exact opposite of the meteorological angle)
    navAngle= self.getNavigAngle(uuf,vvf)

    #: Doc Since 360.0 is 0.0 then set navAngle to 0.0 if it is the case:
    if int(navAngle) == 360 : navAngle = 0.0

    #: Set the navigation angle in the ValuesDataSet dictionary.
    ValuesDataSet[ValueIdx, IS111.DIR_METADATA_ID[0] ]= navAngle

  #--- end method setCurrSpeedAndDirection

  #---
  def writeCommonHDF5MetaData(self, TileDict, ProductGROUPDataStrId,
                              RegionalModelName= None, INFOLog= False) :
    """
    S111 specific instance method for writing(creating) metadata in an HDF5 output file.
    This method is used by S111 sub classes(like S111DataCodingFmt3).

    TileDict (type->dictionary): A dictionary holding model currents data points for a tile.

    ProductGROUPDataStrId (type->string) : The specific S111 DHP data string id for the HDF5 GROUP data structure.

    RegionalModelName (type->string) <OPTIONAL> Default->None: The name of the regional(ex. CIOPS-E) model from which the currents data come from.

    INFOLog (type->boolean) <OPTIONAL> Default->False: Flag to put(or not) the INFO logs on the stdout.

    return (type->h5py file group object)
    """

    if INFOLog :
      methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #: Doc Set metadata specific to S111:

    #: Doc depthTypeIndex: Depth type reference at which the currents are valid:
    #      See official IHO document spec. "Surface Current Product Specification" version 1.0.0 May 2018 p.56 section 12.3 table 12.1
    #      https://www.iho.int/mtg_docs/com_wg/IHOTC/S-100_PS/S-111_Surface_Currents_Product_Specification_Documents
    #      1: Layer average(?)
    #      2: Sea surface(The normal case taken as default)
    #      3: Vertical datum
    #      4: Sea bottom
    self.ROOT_GROUP_ATTRS_2SET[ self.DEPTH_TYPE_INDX_ID[0] ][ self.DATAVALUE_ID[0] ]= self.DEFAULT_DEPTH_TYPE_INDEX[0]

    if INFOLog :
      sys.stdout.write("INFO "+methId+" end\n")

    #: Doc Set the common metadata with the SFMT super-class writeCommonHDF5MetaData method.
    #      Note the self.DEFAULT_VERT_DATUM[0] method argument for S111 products.
    super(S111,self).writeCommonHDF5MetaData(TileDict, self.DEFAULT_VERT_DATUM[0],
                                             ProductGROUPDataStrId, RegionalModelName, INFOLog)

  #---
  def writeOneTile(self, TileId, TileDict, DateTimeStringsOutDict,
                   RegionalModelName= None, ConvertMs2Knots= True, OverWrite= True, InfoLog= False) :
    """
    Generic method writing a tiled S111 DHP data HDF5 file.

    TileId (type->dictionary): A tile string id.

    TileDict (type->dictionary): A dictionary holding model currents data points for a tile.

    DateTimeStringsOutDict (type->dictionary): Already formatted SFMT DHP data date timestamps strings dictionary.

    RegionalModelName (type->string) <OPTIONAL> Default->None: The name of the regional(ex. CIOPS-E) model from
    which the water levels data come from.

    ConvertMs2Knots (type->boolean) <OPTIONAL> Default->True: To(or not to) convert meters/seconds to knots if
    needed(and it normally always the case).

    OverWrite (type->boolean) <OPTIONAL> Default->True: A flag to(or not to) signal that the already existing
    data products files are to be overwritten with or without issuing a WARNING log message to the stdout stream.

    INFOLog (type->boolean) <OPTIONAL> Default ->False : To put(or not) log INFO messages on the stdout stream.

    NOTE: No fool-proof checks for performance reasons.
    """

    #: Doc Using SFMT super class writeOneTile for the generic processing.
    super(S111,self).writeOneTile(TileId, TileDict, DateTimeStringsOutDict,
                                  RegionalModelName, ConvertMs2Knots, OverWrite, InfoLog)

    #: Doc Define self._geoStrId according to the S111 DHP data current type
    #      for subsequent usage by sub classes objects instances.
    self._geoStrId= str(" ") + ISFMT.PRODUCTS_IDS.S111.name + str(" tile ") + TileId

    #: Doc Open the S111 DHP data HDF5 file.
    self._hdf5FileRootObj= SFMTData.openOutFile(IS111.OUT_FILES_PREFIX[0], TileId, self._outputDir, OverWrite, InfoLog)

    #--- NOTE: No check on the hdf5FileRootObj validity here for performance reasons.

    #; Doc Get the current product string id. for the GROUP.01 HDF5 data structure.
    currentGROUPDataStrId= self.PRODUCT_FEATURE_IDS[ ISFMT.PRODUCTS_IDS.S111.name ][0]

    #if self._productGroupDataStrSuffix is not None: currentGROUPDataStrId += self._productGroupDataStrSuffix

    #: Doc Write some common meta data with S111 super class writeCommonHDF5MetaData method.
    self.writeCommonHDF5MetaData(TileDict, currentGROUPDataStrId, RegionalModelName, InfoLog)
