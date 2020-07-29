#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/ISFMTMetaDataAttr.py
# Creation        : September/Septembre 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.ISFMTMetaDataAttr implementation.
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
import sys
import h5py
import inspect

#---
from msc_pygeoapi.process.dfo.pjs.util.IDataIndexing import IDataIndexing

#---
class ISFMTMetaDataAttr(IDataIndexing) :

  """
  Class ISFMTMetaDataAttr defines some class instance constants parameters
  for ISFMTMetaData and other SFMT derived classes.
  """

  #---
  def __init__(self) :

    IDataIndexing.__init__(self)

    #---
    self.NORMAL_JSON_FILE_EXT= ( str(".json") ,)

    #: Doc The mandatory Json format file name which defines the common
    #      HDF5 metadata used for the SFMT DHP data. This file is
    #      normally found in the cfg/SFMTMetaData/JSON sub-directory.
    #      of the DFO-CHS-ENAV-DHP python package.
    self.COMMON_METADATA_FILENAME= ( str("SFMTMetaData") + self.NORMAL_JSON_FILE_EXT[0] ,)

    self.HDF5_DC3_GRP01_ID= ( str(".01") ,)

    #: Doc The metadata string id. for the data coding format used:
    self.DATA_CODING_FMT_ID= ( str("dataCodingFormat") ,)

    #: Doc The metadata string ids. for indexing in
    #      the self.TYPES_OF_DATA dictionary(defined just below):
    self.MOD_HINDCAST_ID=  ( str("MODEL_HINDCAST") ,)
    self.MOD_FORECAST_ID=  ( str("MODEL_FORECAST") ,)
    self.ASTRO_PRED_ID=    ( str("ASTRO_PREDICTION") ,)
    self.ANL_HYB_METH_ID=  ( str("ANL_OR_HYB_METHOD") ,)
    self.REAL_TIME_OBS_ID= ( str("REAL_TIME_OBSERVATION") ,)
    self.HISTORIC_OBS_ID=  ( str("HISTORICAL OBSERVATION") ,)

    #: Doc Official IHO SFMT DHP data types to be used in the metadata.
    self.TYPES_OF_DATA= { self.HISTORIC_OBS_ID[0]  : 1,
                          self.REAL_TIME_OBS_ID[0] : 2,
                          self.ASTRO_PRED_ID[0]    : 3,
                          self.ANL_HYB_METH_ID[0]  : 4,
                          self.MOD_HINDCAST_ID[0]  : 5,
                          self.MOD_FORECAST_ID[0]  : 6 }

    #: Doc Must use bytes as argument to h5py dtype=h5py.special_dtype() function
    #      to get a CSET H5T_CSET_ASCII type. If we use dtype=h5py.special_dtype(str)
    #      then we end up with a CSET H5T_CSET_UTF8 type which we are supposed to avoid.
    #
    #      See the HDF5Group.create_dataset function usage in the SFMTMetaData class
    #      instance method and createAutoMetaDataSetsInHDF5Group and also used in SFMTData
    #      class method writeCommonHDF5MetaData.
    #
    self.H5PY_STRING_SPECIAL_DTYPE= ( bytes, )

    #: Doc The HDF5 string id. for the file structure root GROUP.
    self.ROOT_GROUP_ID= ( str("/") ,)

    #: Doc The HDF5 string id. for the data structures inside GROUPs ATTRIBUTEs:
    self.DTYP_ID= ( str("DATATYPE") ,)
    self.DSET_ID= ( str("DATASPACE") ,)

    #: Doc String id. for the timestamps HDF5 GROUPs
    self.TIMESTAMP_GROUP_PREFIX_ID= ( str("Group_") ,)

    #: Doc The HDF5 string id. specific for the SFMT DHP Group_F HDF5 GROUP:
    self.GRPF_ID= ( self.TIMESTAMP_GROUP_PREFIX_ID[0] + str("F") ,)

    #: Doc String id. used to gather some sub-GROUP metadata together in a dict.
    #      (many GROUP data structure inside one GROUP) both used for JSON
    #      formatted metadata strings ids. definitions and for HDF5 files.
    self.JSON_GROUPS_ID= ( str("GROUPS") ,)

    #: Doc The HDF5 string id. for the ATTRIBUTES metadata
    #      used both for JSON formatted metadata strings ids.
    #      definitions and for HDF5 files.
    self.JSON_ATTRS_ID= ( str("ATTRIBUTES") ,)

    #: Doc The HDF5 string id. for the DATASETS metadata
    #      used both for JSON formatted metadata strings ids.
    #      definitions and for HDF5 files.
    self.JSON_DATASETS_ID= ( str("DATASETS") ,)

    #: Doc SFMT DHP common HDF5 metadata strings ids. for all S<NNN> formats types.
    self.AUTO_METADATA_ROOT= [ str("epoch"), str("metaFeatures"), str("productSpecification") ]

    #: Doc Some more SFMT DHP HDF5 metadata string ids.
    self.DATETIME_SEP_ID= ( str("HDF5_DATE_TIME_SEP") ,)
    self.GEO_ATTR_ID= ( str("HDF5_GEOGRAPHIC_ATTR_ID") ,)
    self.GEO_PREFIX_ID= ( str("HDF5_GEOGRAPHIC_ID_PREFIX") ,)

    #: Doc Regroup some HDF5 metadata string ids. in at tuple for checks done in loops:
    self.JSON_STRIDS_CHECKS= ( self.GEO_PREFIX_ID[0], self.GEO_ATTR_ID[0], self.DATETIME_SEP_ID[0] )

    #: Doc Define various HDF5 ATTRIBUTEs constant strings ids. for all S<NNN> formats types.

    #: Doc Date-time ATTRIBUTE ids. in the ROOT GROUP
    self.ISSUE_DATE_ID= ( str("issueDate") ,)
    self.ISSUE_TIME_ID= ( str("issueTime") ,)

    #: Doc "depthTypeIndex" HDF5 ATTRIBUTE id. is only used for
    #      S111 DH products in the ROOT GROUP. See the IHO S111
    #      official spec. version 1.0.0 for details on that ATTRIBUTE.
    self.DEPTH_TYPE_INDX_ID= ( str("depthTypeIndex") ,)

    #: Doc geo-ref. ATTRIBUTE ids. in the ROOT GROUP.
    self.HORIZ_DATUM_VAL_ID= ( str("horizDatumValue") ,)
    self.HORIZ_DATUM_REF_ID= ( str("horizontalDatumReference") ,)

    #: Doc HDF5 ATTRIBUTE ids. for the "WaterLevel.01" sub GROUP:
    self.NUM_GRP_ID= ( str("numGRP") ,)
    self.NUM_NODES_ID= ( str("numberOfNodes") ,)
    self.NUM_TIMES_ID= ( str("numberOfTimes") ,)

    #: Doc HDF5 ATTRIBUTE id. for the "WaterLevel" sub GROUP:
    #      (Same value as "numberOfNodes" in the "WaterLevel.01" sub GROUP)
    self.NUM_INSTANCES_ID= ( str("numInstances") ,)

    #: Doc HDF5 DATASET id. of the  "WaterLevel" sub GROUP:
    #      which definesthe coordinates names used in the
    #      "Positioning" HDF5 compound data type
    self.AXIS_NAMES_ID= ( str("AxisNames") ,)

    #: Doc HDF5 ATTRIBUTE id. in "<productType>.01" sub GROUP
    #      for the time in seconds between two temporally successive
    #      "Group_***" sub GROUPs of "<productType>.01"
    self.TIME_REC_INTRV_ID= ( str("timeRecordInterval") ,)
    self.DATETIME_FRST_REC_ID= ( str("dateTimeOfFirstRecord") ,)
    self.DATETIME_LAST_REC_ID= ( str("dateTimeOfLastRecord") ,)

    #: Doc HDF5 ATTRIBUTE ids. for the coordinates limits of
    #      the data. Used in both ROOT and "SurfaceCurrent.01" GROUPs
    #      (and their values are the same when using S102 tiles)
    self.EAST_BOUND_LON_ID=  ( str("eastBoundLongitude") ,)
    self.WEST_BOUND_LON_ID=  ( str("westBoundLongitude") ,)
    self.NORTH_BOUND_LAT_ID= ( "northBoundLatitude" ,)
    self.SOUTH_BOUND_LAT_ID= ( "southBoundLatitude" ,)

    #: Doc Put the HDF5 ATTRIBUTE ids. for the coordinates limits in
    #    a tuple to use loop processing:
    self.BBOX_LLLIMITS_IDS= ( self.EAST_BOUND_LON_ID[0] ,
                              self.WEST_BOUND_LON_ID[0] ,
                              self.NORTH_BOUND_LAT_ID[0],
                              self.SOUTH_BOUND_LAT_ID[0] )

    #: Doc HDF5 ATTRIBUTE ids. for lon-lat coordinates in S<NNN> DHP data files.
    self.LLPOS_ID= ( str("Positioning") ,)

    #: Doc lon-lat coordinates indices for the HDF5 compound data
    #      type creation of the "Positioning" GROUP.
    self.LONPOS_IDX_ID= ( str("0,0") ,)
    self.LATPOS_IDX_ID= ( str("1,0") ,)

    #: Doc Id. of the HDF5 DATASET located in the "Positioning" GROUP.
    self.GEOMVALUES_ID= ( str("geometryValues"), )

    #: Doc HDF5 ATTRIBUTE id. for the vertical datum used:
    self.VERT_DATUM_ID= ( str("verticalDatum") ,)

    #: Doc No vertical datum as default(It is normally the case for S111 data).
    self.DEFAULT_VERT_DATUM= ( -1 ,)

    #: Doc IHO official lowerLowWaterLargeTide integer code (a.k.a. chart datum).
    #      for the S104 DHP data.
    self.LLWLT_VERT_DATUM= ( 27 ,)

    #: Doc HDF5 DATASET id. for the HDF5 compound data type
    #      which holds the currents or water levels data located
    #      in the Group_*** sub GROUPs
    self.VALUES_METADATA_ID= ( str("values") ,)

    #: Doc HDF5 ATTRIBUTE id. for the time stamp of each
    #      Group_*** sub GROUPs
    self.TIMESTAMP_METADATA_ID= ( str("timePoint") ,)

    #: Doc HDF5 SPACE string id.
    self.HDF5_SIMPLE_SPACE_ID= ( str("SIMPLE") ,)

    #: Doc HDF5 DATATYPEs string ids.
    self.HDF5_STR_TYPE_ID= ( str("H5T_STRING") ,)
    self.HDF5_INT_TYPE_ID= ( str("H5T_NATIVE_INT") ,)
    self.HDF5_FLOAT_TYPE_ID= ( str("H5T_NATIVE_FLOAT") ,)

    #: Doc self.METH_TYPE_PRODUCT_ID and self.TYPEOF_PRODUCT_DATA_ID
    #      have to be set by the specific products classes.
    self.METH_TYPE_PRODUCT_ID= None
    self.TYPEOF_PRODUCT_DATA_ID= None

    #: Doc Dictionary for HDF5 DATATYPEs creation usage in loops:
    self.HDF5_AUTO_DTYPES= { self.HDF5_INT_TYPE_ID[0]   : ( h5py.h5t.NATIVE_INT32 ,),
                             self.HDF5_FLOAT_TYPE_ID[0] : ( h5py.h5t.NATIVE_FLOAT ,),
                             self.HDF5_STR_TYPE_ID[0]   : ( h5py.special_dtype( vlen= self.H5PY_STRING_SPECIAL_DTYPE[0] ) ,) }

    #: Doc HDF5 Meta-data that need to be set by each S<NNN> class instances objects.
    self.ROOT_GROUP_ATTRS_2SET= { self.ISSUE_DATE_ID[0]      : { self.DTYP_ID[0] : self.HDF5_STR_TYPE_ID[0] } ,
                                  self.ISSUE_TIME_ID[0]      : { self.DTYP_ID[0] : self.HDF5_STR_TYPE_ID[0] } ,
                                  self.VERT_DATUM_ID[0]      : { self.DTYP_ID[0] : self.HDF5_INT_TYPE_ID[0] } ,
                                  self.HORIZ_DATUM_REF_ID[0] : { self.DTYP_ID[0] : self.HDF5_STR_TYPE_ID[0] } ,
                                  self.HORIZ_DATUM_VAL_ID[0] : { self.DTYP_ID[0] : self.HDF5_INT_TYPE_ID[0] } }

    #: Doc dataCodingFormat nb. 3 GROUP01 meta-data to set by each S<NNN> class instances objects.
    self.DC3_GROUP01_ATTRS_2SET= { self.NUM_GRP_ID[0]           : { self.DTYP_ID[0] : self.HDF5_INT_TYPE_ID[0] } ,
                                   self.NUM_NODES_ID[0]         : { self.DTYP_ID[0] : self.HDF5_INT_TYPE_ID[0] } ,
                                   self.NUM_TIMES_ID[0]         : { self.DTYP_ID[0] : self.HDF5_INT_TYPE_ID[0] } ,
                                   self.TIME_REC_INTRV_ID[0]    : { self.DTYP_ID[0] : self.HDF5_INT_TYPE_ID[0] } ,
                                   self.DATETIME_FRST_REC_ID[0] : { self.DTYP_ID[0] : self.HDF5_STR_TYPE_ID[0] } ,
                                   self.DATETIME_LAST_REC_ID[0] : { self.DTYP_ID[0] : self.HDF5_STR_TYPE_ID[0] } }

    #: Doc Create generic dictionary HDF5_SET_METADATA_PRODUCT and
    #      initialize it with keys which are common for all products types.
    self.HDF5_SET_METADATA_PRODUCT= { self.NUM_INSTANCES_ID[0]   : None,
                                      self.DATA_CODING_FMT_ID[0] : None }

    #: Doc Create generic dictionary HDF5_AUTO_METADATA_PRODUCT and
    #  initialize it keys which are common for all products types.
    #  Note that self.DATA_CODING_FMT_ID[0] is also used in this dictionary
    #  even if it is also used in self.HDF5_SET_METADATA_PRODUCT. This is
    #  necessary because the IHO (in fact the S111 spec. only as of 20190925)
    #  DHP spec require using this parameter in two places(two HDF5 GROUPs) in
    #  the products files metadata.
    self.HDF5_AUTO_METADATA_PRODUCT= { self.JSON_DATASETS_ID[0] : [ self.AXIS_NAMES_ID[0] ],
                                       self.JSON_ATTRS_ID[0]    : [ str("dimension"),
                                                                    str("commonPointRule"),
                                                                    str("timeUncertainty"),
                                                                    str("interpolationType"),
                                                                    str("verticalUncertainty"),
                                                                    str("horizontalPositionUncertainty"),
                                                                    self.DATA_CODING_FMT_ID[0],
                                                                    self.NUM_INSTANCES_ID[0] ] }
