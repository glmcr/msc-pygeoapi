#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTData.py
# Creation        : May/Mai 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTData implementation.
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
import time
import inspect
import multiprocessing

#--- 3rd party h5py package:
import h5py

#---
from msc_pygeoapi.process.dfo.pjs.util.JsonCfgIO import JsonCfgIO
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTTileData import SFMTTileData
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.S102TilesFactory import S102TilesFactory

#---
class SFMTData(SFMTTileData) :

  """
  Provide some utility instance methods implementations to S<NNN> sub-classes.
  """

  #---
  def __init__(self, S102Obj, JsonCommonMetaDataDict) :

    """
    S102Obj (type->S102): A S102 class instance object.

    JsonCommonMetaDataDict (type->dictionary) : A dictionary holding the json common
    metadata to use for the SFMT DHP data.
    """

    SFMTTileData.__init__(self, S102Obj, JsonCommonMetaDataDict)

  #---
  @staticmethod
  def openOutFile(OutFilePrefix, TileId, OutDir,
                  OverWriteWarn= False, INFOLog= False) :
    """
    staticmethod which opens a HDF5 DHP data output file.

    OutFilePrefix (type->string): The prefix(string) of the file name to open.

    TileId (type->string): The string id. of the tile holding the data to write.

    OutDir (type->string): The Directory where to write the output file.

    OverWriteWarn (type->boolean) <OPTIONAL> Default->False: A flag to(ot not to) signal
    that the already existing DHP data files are to be overwritten with or without
    issuing a WARNING log message to the stdout stream.

    INFOLog (type->boolean) <OPTIONAL> Default->False: To(or not to) put log INFO messages
    on the stdout stream.

    return (type->h5py file root GROUP data structure object)

    NOTE: Fool-proof checks are minimal for performance reasons.
    """

    if INFOLog :
      methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #: Doc Complete path of the specific HDF5 file for the tile being processed.

    #    (NOTE: The check for self.OutDir existence and write access should have already been done)
    oFilePath= OutDir + "/" + S102TilesFactory.getTileOutFileName(OutFilePrefix, TileId, ISFMT.OUT_FILES_EXTENSION[0])

    if OverWriteWarn and os.access(oFilePath, os.F_OK) :
      methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
      sys.stdout.write("WARNING "+methId+" Will overwrite already existing file -> "+oFilePath+" !\n")
    #---

    if INFOLog:
      sys.stdout.write("INFO "+methId+" Writing tile "+TileId+" data in file "
                       +oFilePath+", process id="+str(multiprocessing.current_process())+"\n")
    #---

    #: Doc Open HDF5 output file in write mode (NOTE: contents erased if oFilePath already exists).
    hdf5FileRootObj= h5py.File(oFilePath, "w")

    if hdf5FileRootObj is None :
      methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
      sys.exit("ERROR "+methId+" hdf5FileRootObj is None !, h5py.File(oFilePath, \"w\") failure !\n")
    #---

    #: Doc Return the result of h5py.File method which
    return hdf5FileRootObj

  #---
  def writeCommonHDF5MetaData(self, TileDict, VerticalDatumCode,
                              ProductGROUPDataStrId, RegionalModelName= None, INFOLog= False) :
    """
    Common instance method for writing(creating) HDF5 meta data for SFMT DHP data formats.

    TileDict (type->dictionary) : A tile data dictionary.

    VerticalDatumCode (type->int) : The SFMT DHP integer code(Official IHO spec.) for the vertical
    datum to use for the data.

    ProductGROUPDataStrId (type->string) : The specific SFMT DHP string id. for HDF5 GROUP data structure.

    RegionalModelName (type->string) <OPTIONAL> Default->None: The name of the regional(ex. CIOPS-E) model
    from which the product input data come from.

    INFOLog (type->boolean) <OPTIONAL> Default->False: Flag to put(or not to) the INFO logs on the stdout.

    return (type->h5py file group object)

    NOTE: Fool-proof checks are commented for performance reasons.
    """

    if INFOLog :
      sys.stdout.write("INFO "+str(__name__)+"."+ str(inspect.stack(0)[0][3])+" method: Start\n")

    ##--- Uncomment for debugging
    #if TileDict is None :
    #  sys.exit("ERROR "+methId+" TileDict is None !\n")

    ##--- Uncomment for debugging
    #if ProductGROUPStrId is None :
    #  sys.exit("ERROR "+methId+" Product01GROUPStrId is None !\n")

    ##--- Uncomment for debugging
    #if self._hdf5FileRootObj is None :
    #  sys.exit("ERROR "+methId+" self._hdf5FileRootObj is None !\n")

    ##--- Uncomment for debugging
    #if self._hdf5FileRootObj.name != self.ROOT_GROUP_ID[0] :
    #  sys.exit("ERROR "+methId+" Need the HDF5 root group object \""+
    #           self.ROOT_GROUP_ID[0]+"\" not this -> "+self._hdf5FileRootObj.name  +"! \n")

    ##--- Uncomment for debugging
    #if not self.ROOT_GROUP_ID[0] in self._jsonCommonMetaDataDict :
    #  sys.exit("ERROR "+methId+" HDF5 root group object id \""+
    #           self.ROOT_GROUP_ID[0]+"\" not in self._JSONCommonMetaDataDict! \n")

    ##--- Uncomment for debugging
    #if self._s102TilesObj is None :
    #  sys.exit("ERROR "+methId+" self._s102TilesObj cannot be None at this point !\n")

    #: Doc Shortcut to the S102 tiles object
    s102TilesObj= self._s102TilesObj

    #; Doc Append a specific data coding format string suffix(if any) to the product HDF5 GROUP DATA string id.
    if self._productGroupDataStrSuffix is not None: ProductGROUPDataStrId += self._productGroupDataStrSuffix

    #: Doc Get the common json defined root group attributes auto metadata;
    rootJSONGroupAttrs= \
      self._jsonCommonMetaDataDict[ self.ROOT_GROUP_ID[0] ][ self.JSON_ATTRS_ID[0] ]

    self.ROOT_GROUP_ATTRS_2SET[ self.VERT_DATUM_ID[0] ][ self.DATAVALUE_ID[0] ]= VerticalDatumCode

    #: Doc Combine both json root group attributes auto metadata from common and specific
    #      (S111,S104 and other) DH product files in rootJSONGroupAttrs dictionary.
    JsonCfgIO.mergeNestedDicts(self._jsonRootTypeMetaDataDict[ self.JSON_ATTRS_ID[0] ], rootJSONGroupAttrs)

    #: Doc Create auto meta-data attributes in HDF5 root group:
    self.createAutoMetaDataAttrsInHDF5Group(rootJSONGroupAttrs,
                                            tuple(self.AUTO_METADATA_ROOT), self.DTYP_ID[0], self._hdf5FileRootObj)

    #: Doc Horizontal datum authority(Which is EPSG normally)
    self.ROOT_GROUP_ATTRS_2SET[ self.HORIZ_DATUM_REF_ID[0] ][ self.DATAVALUE_ID[0] ]= s102TilesObj._horizDatumRef[0]

    #: Doc Horizontal datum authority value(Which is 4326 normally
    self.ROOT_GROUP_ATTRS_2SET[ self.HORIZ_DATUM_VAL_ID[0] ][ self.DATAVALUE_ID[0] ]= int( s102TilesObj._horizDatumCode[0] )

    #: Doc What time is it now in the UTC(a.k.a ZULU) time zone please ?
    dtNowUtc= ( time.gmtime() ,)

    #: Doc Date(YYYYMMDD format) of file creation:
    self.ROOT_GROUP_ATTRS_2SET[ self.ISSUE_DATE_ID[0] ][ self.DATAVALUE_ID[0] ]= time.strftime(self.YYYYMMDDFmt[0], dtNowUtc[0])

    #: Doc Time of day(hhmmss format) of file creation:
    self.ROOT_GROUP_ATTRS_2SET[ self.ISSUE_TIME_ID[0] ][ self.DATAVALUE_ID[0] ]= time.strftime(self.hhmmssFmt[0], dtNowUtc[0])

    #--- NOTE: Using str here just to be sure that we pass an ASCII string
    #    to hdf5FileRootObj.attrs.create h5py method:
    geoIdStrValue= str(self._jsonCommonMetaDataDict[ self.GEO_PREFIX_ID[0] ] + self._geoStrId)

    #: Doc Use the string id self._jsonCommonMetaDataDict[self.GEO_ATTR_ID[0]]
    #      plus the tile string Id for the geographicIdentifier attribute:
    self._hdf5FileRootObj.attrs.create(self._jsonCommonMetaDataDict[ self.GEO_ATTR_ID[0] ],
                                       geoIdStrValue, dtype= h5py.special_dtype(vlen= self.H5PY_STRING_SPECIAL_DTYPE[0]) )

    #: Doc Write tile bounding box meta-data in the root group:

    #--- NOTE: This will be done again(see below) in the GROUP "SurfaceCurrent.01" data section which is somewhat redundant
    #          when using S102 tiles but it was designed for cases where we can have some sub-domains enclosed in one large
    #          domain.

    #: Doc Recall that self.S102Tiles.dataDict[tile][self.S102Tiles.BOUNDING_BOX_ID] is a list containing the
    #      S102 tile regular bounding box limits(4 lon-lat points)
    boundingBoxNorthEastLLList= TileDict[ s102TilesObj.BOUNDING_BOX_ID[0] ][ s102TilesObj.BBOX_NORTH_EAST_CORNER[0] ]
    boundingBoxSouthWestLLList= TileDict[ s102TilesObj.BOUNDING_BOX_ID[0] ][ s102TilesObj.BBOX_SOUTH_WEST_CORNER[0] ]

    #: Doc Shortcut to the common json defined root group attributes auto meta-data;
    rootJSONGroupAttrs= self._jsonCommonMetaDataDict[ self.ROOT_GROUP_ID[0] ][ self.JSON_ATTRS_ID[0] ]

    #: Doc Set the lat-lon infos. used for the HDF5 metadata :
    rootJSONGroupAttrs[ self.EAST_BOUND_LON_ID[0]  ][ self.DATAVALUE_ID[0] ]= boundingBoxNorthEastLLList[ s102TilesObj.TILES_LON_IDX[0] ]
    rootJSONGroupAttrs[ self.WEST_BOUND_LON_ID[0]  ][ self.DATAVALUE_ID[0] ]= boundingBoxSouthWestLLList[ s102TilesObj.TILES_LON_IDX[0] ]

    rootJSONGroupAttrs[ self.NORTH_BOUND_LAT_ID[0] ][ self.DATAVALUE_ID[0] ]= boundingBoxNorthEastLLList[ s102TilesObj.TILES_LAT_IDX[0] ]
    rootJSONGroupAttrs[ self.SOUTH_BOUND_LAT_ID[0] ][ self.DATAVALUE_ID[0] ]= boundingBoxSouthWestLLList[ s102TilesObj.TILES_LAT_IDX[0] ]

    #: Doc Create tile bounding box meta-data in hdf5FileRootObj:
    self.createAutoMetaDataAttrsInHDF5Group(rootJSONGroupAttrs,
                                            tuple(self.BBOX_LLLIMITS_IDS), self.DTYP_ID[0], self._hdf5FileRootObj)

    #: Doc Get the json defined GROUP_F auto metadata (which are of HDF5 DATASET type):
    groupFJSONMetaData= self._jsonRootTypeMetaDataDict[ self.JSON_GROUPS_ID[0] ][ self.GRPF_ID[0] ]

    #: Doc Create auto meta-data Group_F HDF5 GROUP datasets in root group:

    #--- NOTE : HDF5RootGroup.create_group(self.GRPF_ID[0]) usage related to
    #           IHO spec. document "Surface Current Product Specification" version 1.0.0 May 2018 p.46, section 10.2.1
    self.createAutoMetaDataSetsInHDF5Group(groupFJSONMetaData[ self.JSON_DATASETS_ID[0] ],
                                           tuple(self.HDF5_AUTO_METADATA_GROUP_F), self._hdf5FileRootObj.create_group(self.GRPF_ID[0]) )

    #: Doc Create(write) the HDF5 ATTRIBUTEs defined in self.ROOT_GROUP_ATTRS_2SET in the HDF5RootGroup:
    self.createAutoMetaDataAttrsInHDF5Group(self.ROOT_GROUP_ATTRS_2SET,
                                            tuple( self.ROOT_GROUP_ATTRS_2SET.keys() ), self.DTYP_ID[0], self._hdf5FileRootObj)

    #: Doc Get the name string id. of the product.
    prodStrId= self.HDF5_AUTO_METADATA_PRODUCT[ self.NAME_ID[0] ]

    #: Doc Create the product HDF5 GROUP data structure in the root GROUP:
    self._hdf5ProductGroup= self._hdf5FileRootObj.create_group(prodStrId)

    #: Doc Shortcut to the json formatted specific S*** DH product metadata dictionary:
    self._jsonProductMetaDataDict= self._jsonRootTypeMetaDataDict[ self.JSON_GROUPS_ID[0] ][prodStrId]

    #: Doc Shortcut to the json surface current meta-data attributes dictionary:
    productJSONMetaDataAttrsDict= self._jsonProductMetaDataDict[ self.JSON_ATTRS_ID[0] ]

    #: Doc Set the NUM_INSTANCES_ID in the surface current metadata bundle dictionary:
    self.HDF5_SET_METADATA_PRODUCT[ self.NUM_INSTANCES_ID[0] ]= self._nbPoints

        #: Doc Local copy of the generic model name in case we have a regional model name to add
    #      to the meta data:
    genericModelName= self.HDF5_SET_METADATA_PRODUCT[ self.METH_TYPE_PRODUCT_ID[0] ]

    #: Doc Concatenate the RegionalModelName(if any) to the already defined
    #      generic model name defined in self.HDF5_SET_METADATA_PRODUCT:
    if RegionalModelName is not None :
      genericModelNameSuffix= ": "+RegionalModelName
    else :
      genericModelNameSuffix= ""

    #: Doc Redefine self.HDF5_SET_METADATA_PRODUCT[ self.METH_TYPE_PRODUCT_ID[0] ] properly with the
    #      genericModelNameSuffix(if any)
    self.HDF5_SET_METADATA_PRODUCT[ self.METH_TYPE_PRODUCT_ID[0] ]= genericModelName + genericModelNameSuffix

    #: Doc Retreive the specific currents type infos values we have in self.HDF5_SET_METADATA_PRODUCT.
    #      dictionary and update the surfCurrentsJSONMetaDataAttrsDict with it:
    for strId in tuple(self.HDF5_SET_METADATA_PRODUCT.keys()) :
      productJSONMetaDataAttrsDict[strId][ self.DATAVALUE_ID[0] ]= self.HDF5_SET_METADATA_PRODUCT[strId]

    #: Doc Create meta-data attributes for surface current HDF5 GROUP data structure:
    self.createAutoMetaDataAttrsInHDF5Group(productJSONMetaDataAttrsDict,
                                            tuple(self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_ATTRS_ID[0] ]), self.DTYP_ID[0], self._hdf5ProductGroup)

    #: Doc Need to reset self.HDF5_SET_METADATA_PRODUCT[ self.METH_TYPE_PRODUCT_ID[0] ] to genericModelName
    #      in case RegionalModelName was appended to it otherwise we end up with a repetition of the genericModelNameSuffix
    #      in the string written in the output files.
    self.HDF5_SET_METADATA_PRODUCT[ self.METH_TYPE_PRODUCT_ID[0] ]= genericModelName

    #: Doc Create AxisNames dataset in metadata Level 2 content (under SurfaceCurrent GROUP)
    self.createAutoMetaDataSetsInHDF5Group(self._jsonProductMetaDataDict[ self.JSON_DATASETS_ID[0] ],
                                           tuple(self.HDF5_AUTO_METADATA_PRODUCT[ self.JSON_DATASETS_ID[0] ]), self._hdf5ProductGroup)

    #: Doc Create the product HDF5 Level3 and level4(No relation to S102 levels stuff) data structure
    #      in the product HDF5 GROUP file data structure itself and retrieve a local reference to its content.
    self._hdf5ProductGroupData= self._hdf5ProductGroup.create_group(ProductGROUPDataStrId)

    #: Doc Write common DataCodingFmt3 HDF5 metadata(using super-class SFMTTileData writeCommonTileData method).
    self.writeCommonTileData(rootJSONGroupAttrs)

    if INFOLog :
      sys.stdout.write("INFO "+str(__name__)+"."+ str(inspect.stack(0)[0][3])+" method: End.\n")
