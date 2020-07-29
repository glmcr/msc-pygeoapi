#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp.models.IModel.py
# Creation        : April/Avril 2020 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.models.IModel implementation.
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
from msc_pygeoapi.process.dfo.pjs.util.ITimeMachine import ITimeMachine
from msc_pygeoapi.process.dfo.pjs.util.IDataIndexing import IDataIndexing

#---
class IModel(ITimeMachine, IDataIndexing) :

  """
  Class used to define various constant parameters(as unary tuples) which are
  common to all dhp.models.* sub-packages for specific models.
  """

  def __init__(self) :

    ITimeMachine.__init__(self)
    IDataIndexing.__init__(self)

    ##--- This _MODEL_VERSION_KEYID need
    ##    to de defined by the classes
    ##    that inherits from this IModel
    ##    super class.
    #self._MODEL_VERSION_KEYID= None

    #--- CVD to CV field name id. that will be used for
    #    the conversion once transformed from raw CVD to chart datum
    #    data. Unary tuple since it is constant.
    self._CVD2CD_FIELD_NAME= ( str("chartdatumconv") ,)

    self.INPUT_FILES_DICT_ID= ( str("InputFiles") ,)
    self.TILES_MDLINDICES_DICT_ID= ( str("TilesModelJIArrIndices") ,)

    self.JSON_DATAIN_FMT_ID= ( str("FileFmt") ,)
    self.JSON_DATAIN_GRTYPE_ID= ( str("GridType") ,)
    self.JSON_NB_TOTAL_HOURS_ID= ( str("NbTotalHours") ,)
    self.JSON_DATAIN_XFER_MACH_ID= ( str("XFerMachIn") ,)
    self.JSON_DATAOUT_XFER_MACH_ID= ( str("XFerMachOut") ,)
    self.JSON_DATAIN_DIR_ID=  ( str("MainDataDir") ,)
    self.JSON_DATAIN_FEXT_ID= ( str("FileExt") ,)
    self.JSON_DATAIN_MDLDIR_ID= ( str("MdlDir") ,)
    self.JSON_DATAIN_FSFX_ID= ( str("FileSuffix") ,)
    self.JSON_DATAIN_FLIST_ID= ( str("FilesListFName") ,)
    self.JSON_DATAIN_TYPEDIR_ID= ( str("DataType") ,)
    self.JSON_DATAIN_MODEL_ID= ( str("WhichModel") ,)
    self.JSON_FIELDSNAMES_ID= ( str("FieldsVariablesNames") ,)
    self.JSON_TILES_MDLINDICES_ID= ( str ("TilesModelIndicesFName") ,)
    self.JSON_CVD2CD_FILE_ID= ( str("CVD2ChartDatumFile") ,)

    #: Doc Define common mandatory parameters strings ids. that should be present
    #      in the Json formatted config. file for all models.
    self.MANDATORY_MDL_JSON_PARAMS= ( self.JSON_DATAIN_FMT_ID,
                                      self.JSON_NB_TOTAL_HOURS_ID,
                                      self.JSON_DATAIN_DIR_ID,
                                      self.JSON_DATAIN_FEXT_ID,
                                      self.JSON_DATAIN_TYPEDIR_ID,
                                      self.JSON_DATAIN_MODEL_ID,
                                      self.JSON_TILES_MDLINDICES_ID )
