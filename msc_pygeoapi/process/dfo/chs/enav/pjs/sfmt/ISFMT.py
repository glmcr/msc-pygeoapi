#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/ISFMT.py
# Creation        : September/Septembre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.ISFMT implementation. It is used like a Java Interface.
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
import enum

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.IS102 import IS102
from msc_pygeoapi.process.dfo.pjs.util.IDataIndexing import IDataIndexing
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMTMetaDataAttr import ISFMTMetaDataAttr

#---
class ISFMT(ISFMTMetaDataAttr, IS102) :

  """
  Class ISFMT defines some constants(hence the use of unary tuples
  to do so) parameters for its derived S<NNN> sub-classes(except S102)
  It's something loosely related to the use of an interface in Java.
  """

  #: Doc DHP main config. directory should be named "cfg"
  MAIN_CFG_DIR= ( "cfg" ,)

  #: Doc Official HDF5 file format extension
  OUT_FILES_EXTENSION= ( str(".h5") ,)

  #: Doc Define the IO data types strings ids.
  DATA_TYPES= enum.Enum( str("DATA_TYPES"), [ str("WATERLEVELS"), str("CURRENTS") ])
  #DATA_TYPES= enum.Enum( str("DATA_TYPES"),
  #[ str("WATERLEVELS"), str("CURRENTS"), str("WAVES"), str("ICE_CONCENTRATION") ])

  #: Doc Json string id. for the path of the temporary work directory.
  JSON_WRKDIR_ID= ( str("WorkDir") ,)

  #: Doc Json string id. for the path of the temporary main storage directory.
  JSON_MAIN_STORAGEDIR_ID= ( str("MainStorageDir") ,)

  #: Doc Nb. of hours to go back in the past relative
  #      to the time at which the SFMT DHP data files
  #      production is automagically started. It is
  #      used to get a slight cushion in the past for
  #      the SFMT DHP data.
  #
  #      TODO: Define it in the main script json config. file instead ??
  HOURS_IN_PAST_START= ( 6, )

  #: Doc Nb. of hours to go in the future for the SFMT DHP data.
  DEFAULT_FUTURE_HOURS= ( 48 ,)

  #: Doc Official IHO id. for the CHS SFMT DHP data.
  PRODUCTS_CHS_TAG= ( str("CA00") ,)

  #: Doc The string ids. for the SFMT DHP data
  #      (Note that the hyphen character is dropped here)
  PRODUCTS_IDS= enum.Enum( str("PRODUCTS_IDS"), [ str("S104"), str("S111") ] )
  #PRODUCTS_IDS= enum.Enum( str("PRODUCTS_IDS"), [ str("S104"), str("S111"), str("S412") ] )

  #: Doc The string id. for WebTide input data:
  WEBTIDE_STR_ID= ( str("WebTide") ,)

  #: Doc The string id. for ECCC NEMO models.
  ECCCNEMO_STR_ID= ( str("ECCC-NEMO") ,)

  #: Doc The string id. for ECCC H2D2 model.
  ECCCH2D2_STR_ID= ( str("ECCC-H2D2") ,)

  #: Doc The string id. for DFO NEMO models.
  DFOEMO_STR_ID= ( str("DFO-NEMO") ,)

  #: Doc The string id. for DFO-IWLS RT database system.
  DFOIWLS_STR_ID= ( str("DFO-IWLS") ,)

  #: Doc The allowed input data formats as of 2018-11-23:
  ALLOWED_INPUT_DATA_TYPES= enum.Enum( str("ALLOWED_INPUT_DATA_TYPES"), [ WEBTIDE_STR_ID[0]  ,
                                                                          DFOIWLS_STR_ID[0]  ,
                                                                          ECCCNEMO_STR_ID[0] ,
                                                                          ECCCH2D2_STR_ID[0] ])

  #--- TODO: Use a named tuple instead of an enum.Enum here for ALLOWED_DATA_CODING_FMT.
  #: Doc The allowed S104 and S111 data coding formats allowed as of 2019-07-30:
  ALLOWED_DATA_CODING_FMT= enum.Enum("ALLOWED_DATA_CODING_FMT", [ ( str("three"), 3) ] )

  #---
  def __init__(self) :

    IS102.__init__(self)
    ISFMTMetaDataAttr.__init__(self)

    #: Doc Default minimum number of data points for a S102 tile to be produced
    #      (i.e. tiles which enclose less than self.MIN_NB_POINTs are skipped and not written as a final product)
    #      NOTE: Could be overriden by json config. parameter MinNbOfPointsPerTile if defined.
    self.MIN_NB_POINTS= ( 3,)

    #: Doc ECCC data only available at 3 hours(== 10800 seconds) intervalls.
    #      TODO: Add simple linear time interpolation to at least get the ECCC NEMO data at 1 hours intervalls ??
    self.MAXTIME_INTERVALL_SEC= ( 10800 ,)

    #: Doc Ids. of the main script config. params retreived from the main script config. JSON file:
    #      See the *.json files located in cfg/Main sub-directory.
    self.JSON_FIELDSVARS_ID= ( str("FieldsVariables") ,)
    self.JSON_APPLY_CONV_ID= ( str("ApplyConversion") ,)
    self.JSON_MIN_NB_POINTS_ID= ( str("MinNbOfPointsPerTile") ,)

    #---
    self.JSON_INPUT_DATA_ID= ( str("Input"), )

    #: Doc Json string id. for the path of the model data input directory.
    self.JSON_MODELDATA_INPUT_DIR= ( str("ModelDataInputDir"), )

    #--- TODO :
    self.JSON_META_DATA_DIR_ID= ( str("SFMTMetaDataDir") ,)
    self.JSON_INPUT_DATATYPE_ID= ( str("Type") ,)
    self.JSON_TILES_SHP_FILES_ID= ( str("TilesLevelsShapeFiles") ,)
    self.JSON_CFG_OUTPUT_FMT_ID= ( str("OutputFormat") ,)
    self.JSON_PRODUCTS_OUTDIR_ID= ( str("ProductsOutputDir") ,)
    self.JSON_INPUT_DATAPARAMS_ID= ( str("Params") ,)

    #: Doc Could have to reject some S102 tiles that are considered
    #      useless. We use regular bounding boxes (ex. [SW lat,SW lon, NE lat, NE lon])
    #      to define those regular bounding boxes.
    self.JSON_EXCLUDE_TILES_ID= ( str("TilesExcludeBBox") ,)

    #---
    self.JSON_INPUT_CFGFILE_ID= ( str("CfgFile") ,)

    #: Doc The Mandatory config. parameters strings ids. which
    #      must be present in the Main configs. JSON files:
    self.JSON_MAINPARAMS_IDS= ( self.JSON_INPUT_DATA_ID[0],
                                self.JSON_META_DATA_DIR_ID[0],
                                self.JSON_PRODUCTS_OUTDIR_ID[0],
                                self.JSON_TILES_SHP_FILES_ID[0],
                                ISFMT.JSON_MAIN_STORAGEDIR_ID[0])

    self.PRODUCT_FEATURE_IDS= { ISFMT.PRODUCTS_IDS.S104.name : ( str("WaterLevel") ,) ,
                                ISFMT.PRODUCTS_IDS.S111.name : ( str("SurfaceCurrent"),) }
