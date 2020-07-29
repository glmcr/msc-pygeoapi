#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp.models.ModelFactory.py
# Creation        : April/Avril 2020 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.models.ModelFactory implementation.
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

#---
import h5py

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.models.IModel import IModel
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTModelFactory import SFMTModelFactory

#---
class ModelFactory(IModel, SFMTModelFactory) :

  """
  Class that implements some generic verifications
  and processing methods. Normally inherited by all
  specific models sub-classes(like NEMO ECCC or
  NEMO DFO ports models).
  """

  #---
  def __init__(self, SFMTObjInst) :

    """
    SFMTObjInst (type->SFMTObj) : A SFMTObj class instance object.
    """

    IModel.__init__(self)
    SFMTModelFactory .__init__(self, SFMTObjInst)

  #--- TODO: This method assumes that the model input data
  #          results files and the CVD to chart datum data
  #          file are both in the NetCDF4(or HDF5 compatible)
  #          format. We then need to implement a more generic
  #          format agnostic method that will call this specific
  #          method and other methods for different files formats
  #          (if any).
  def applyNC4CVDToCDConvForS104(self, WaterLevelsFieldName) :

    """
    As the method name says, apply the CVD to chart datums
    conversion to a 2D model water levels data(which
    are normally forecasts).

    WaterLevelsFieldName (type->string): The string name id.
    of the model water levels field name. It should be present
    in the model dataset that is present in the self._inputDataDict
    dictionary.

    NOTE: The NC4 string in the method name means that it
    assumes that both the 2D model water levels field data is
    read from a NetCDF4 or an HDF5 input file and that the
    2D CVD to chart datum field data also comes from that kind
    of file format and both must have the same GIS common
    reference system(CRS).

    TODO: Check for both fields data having that same GIS
    common reference system(CRS).
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methId+" start\n")

    if WaterLevelsFieldName is None :
      sys.exit("ERROR "+methId+" WaterLevelsFieldName is None !\n")

    if self._cvd2ChartDatumFile is None :
      sys.exit("ERROR "+methId+" self._cvd2ChartDatumFile is None !\n")

    if not os.access(self._cvd2ChartDatumFile[0],os.F_OK) :
      sys.exit("ERROR "+methId+
               " self._cvd2ChartDatumFile[0] -> "+
               self._cvd2ChartDatumFile[0]+" not found !\n")
    #--- end if block.

    if self._inputDataDict is None :
      sys.exit("ERROR "+methId+" self._inputDataDict is None !\n")
    #---

    #--- Extract the model input data timestamped dictionary.
    modelInputDataTSDict= self._inputDataDict[ self.NC4_TIMESTAMPS_ID[0] ]

    #--- Get the string ids. keys of the modelInputDataTSDict as a tuple.
    timeStampsKeysTuple= tuple( sorted( modelInputDataTSDict.keys() ))

    #--- Extract the model data fields sub-dictionary
    #    for the timestamp 0 only.
    modelInputDataFieldsDict= \
      modelInputDataTSDict[ timeStampsKeysTuple[0] ][ self.INPUT_FIELDS_ID[0] ]

    #--- Extract the string ids. keys names of the data
    #    fields that are present in this modelInputDataFieldsDict.
    modelInputFieldsKeysTuple= tuple ( modelInputDataFieldsDict.keys())

    #--- The model water levels field string id. key name
    #    must be present in the modelInputFieldsKeysTuple.
    if WaterLevelsFieldName not in modelInputFieldsKeysTuple :

      sys.exit("ERROR "+methId+
               " WaterLevelsFieldName string id. -> "+WaterLevelsFieldName+
               " is not present in the modelInputDataTSDict dictionary !\n")
    #--- end if block.

    #--- Extract model water levels NC4(HDF5 compatible)
    #    data field at timestamp 0 only.
    modelWLFieldAtTS0= modelInputDataFieldsDict[ WaterLevelsFieldName ]

    #sys.stdout.write("INFO "+methId+
    #                 " self._cvd2ChartDatumFile[0]="+
    #                 self._cvd2ChartDatumFile[0]+"\n")

    #--- Open the cvd to chart datum data NetCDF4
    #    (or HDF5 compatible) format file.
    h5FRootObj= h5py.File(self._cvd2ChartDatumFile[0],"r")

    #--- Get the string id. keys
    h5FRootObjKeysTuple= tuple( h5FRootObj.keys() )

    #--- The CVD to chart datums string id. key must
    #    be present in the fields keys of the
    #    h5FRootObj object.
    if self._CVD2CD_FIELD_NAME[0] not in h5FRootObjKeysTuple :

      sys.exit("ERROR "+methId+
               " self._CVD2CD_FIELD_NAME[0] -> "+self._CVD2CD_FIELD_NAME[0]+
               " string id. is not present in the CVD to chart datum conversion data file !\n")
    #--- end if block.

    #--- Extract the CVD to chart datums field(i.e. as a HDF5 dataset)
    cvd2cdDataField= h5FRootObj[ self._CVD2CD_FIELD_NAME[0] ]

    #print("h5FRootObjKeysTuple="+str(h5FRootObjKeysTuple))

    #--- Extract the attributes of the CVD to CD static
    #    data file.
    hdf5AttrKeys= tuple( h5FRootObj.attrs.keys() )

    #--- The model product version string attribute MUST also be
    #    defined in the CVD to CD static file attributes.
    if self._modelVersionKeyId[0] not in hdf5AttrKeys :

      sys.exit("ERROR "+methId+
               " Model version attribute: self._modelVersionKeyId[0] -> \""+
               self._modelVersionKeyId[0]+
               "\" string id. is not present in the CVD to chart datum conversion data file !\n")
    #--- end if block.

    #--- Verify if there is no mismatch between the product versions
    #    of both model data and CVD to CD conversion data.
    if h5FRootObj.attrs[ self._modelVersionKeyId[0] ] != \
      self._inputDataDict[ self._modelVersionKeyId[0] ] :

      sys.exit("ERROR "+methId+
               " Mismatch between product versions between the model -> "+
               self._inputDataDict[ self._modelVersionKeyId[0] ]+
               " and the CVD to chart datum conversion static file -> "+
               h5FRootObj.attrs[ self._modelVersionKeyId[0] ]+" !\n")
    #--- end if block.

    sys.stdout.write("INFO "+methId+" Model version -> "+
                     self._inputDataDict[ self._modelVersionKeyId[0] ]+"\n")

    #--- The cvd2cdDataField.shape and modelWLFieldAtTS0[0].shape
    #    MUST be the same, otherwise we have a SNAFU.
    if cvd2cdDataField.shape != modelWLFieldAtTS0.shape :

      sys.exit("ERROR "+methId+
               " cvd2cdDataField.shape != modelWLFieldAtTS0[0].shape !!\n")
    #--- end if block.

    #--- Loop on all model WL input data timestamps
    #    to apply the CVD to chart datum conversion
    #    data.
    for ts in timeStampsKeysTuple :

      #--- Extract(as a 2D numpy array) the model water
      #    levels field for the timestamp being processed.
      modelWLFieldAtTS= \
        modelInputDataTSDict[ts][ self.INPUT_FIELDS_ID[0] ][WaterLevelsFieldName]

      #--- Plain and simple addition of the CVD to chart datums
      #    gridded data to the model WL data.
      modelWLFieldAtTS += cvd2cdDataField

    #--- end for loop.

    h5FRootObj.close()

    sys.stdout.write("INFO "+methId+" CVD to chart datum conversion done !\n")
    sys.stdout.write("INFO "+methId+" end\n")

  #--- FP stands for Fool-Proof.
  def modelFPCheckParams( self,
                          InputParamsDict,
                          InputParamsDictKeys,
                          MainCfgDir,
                          ApplyConversionFlag= False,
                          NbMultiProcesses= 1 ):
    """
    InputParamsDict (type->dictionary) : The dictionary that
    contains the main config. parameters used for the DHP
    conversions. It is normally filled up from a Json
    formatted file.

    InputParamsDictKeys (type->tuple): A tuple that contains
    all the string ids. keys of the InputParamsDict dictionary.

    MainCfgDir (type->string): DHP package main config.
    directory path.

    ApplyConversionFlag (type->boolean) Default->False: A flag to
    signal(or not to)that a numeric conversion of the raw model
    data to something relevant for the DHP data that will be
    produced(ex. m/s to knots conversion for currents or chart
    datums conversions).

    NbMultiProcesses (type->int) <OPTIONAL> Default->1:
    The number of multiprocessing objects to use to speed up exec.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    sys.stdout.write("INFO "+methId+" start\n")

    #--- Usual FP(fool-proof) checks.
    if InputParamsDict is None :
      sys.exit("ERROR "+methId+" InputParamsDict is None !\n")

    if InputParamsDictKeys is None :
      sys.exit("ERROR "+methId+" InputParamsDictKeys is None !\n")

    if MainCfgDir is None :
      sys.exit("ERROR "+methId+" InputParamsDictKeys is None !\n")

    #--- FP checks on NbMultiProcesses.

    #--- Avoid nasty HTD(hard-to-debug) SNAFU behavior
    #    if NbMultiProcesses is passed as a string to
    #    this method.
    self._nbMultiProcesses= int(NbMultiProcesses)

    if self._nbMultiProcesses <= 0 :
      sys.exit("ERROR "+methId+
                       " Invalid NbMultiProcesses value -> "+
                       str(NbMultiProcesses)+" !\n")
    #--- end if block.

    sys.stdout.write("INFO "+methId+" Will use -> "+
                     str(self._nbMultiProcesses)+
                     " multiprocessing object(s).\n")

    #--- NOTE: self.MANDATORY_MDL_JSON_PARAMS holds unary
    #          tuples of strings ids.:
    for strIdItem in self.MANDATORY_MDL_JSON_PARAMS :

      #--- Mandatory string ids. keys checks.
      if strIdItem[0] not in InputParamsDictKeys :

        sys.exit("ERROR "+methId+
                 " string id. -> "+strIdItem[0]+
                 " not defined in mandatory json input config. parameters !\n")
      #---
    #--- end for loop block.

    sys.stdout.write("INFO "+methId+
                     " Mandatory main Json config. parameters are all defined\n")

    #--- Get the model string id. from
    #    the InputParamsDict[ self.JSON_DATAIN_MODEL_ID[0] ]
    #    sub-dictionary which has only one item in it.
    modelId= tuple( InputParamsDict[ self.JSON_DATAIN_MODEL_ID[0] ].keys())[0]

    #--- And this model string id id. key must be
    #    defined in the InputParamsDict dictionary.
    if modelId not in InputParamsDict[ self.JSON_DATAIN_MODEL_ID[0] ] :

      sys.exit("ERROR "+methId+" Model string id. -> "+modelId+
               " not found in InputParamsDict[ self.JSON_DATAIN_MODEL_ID[0] ] !\n")
    #--- End if block.

    sys.stdout.write("INFO "+methId+" modelId -> "+modelId+"\n")

    #--- Get the specific Json cfg parameters dictionary for this model.
    modelParamsDict= InputParamsDict[ self.JSON_DATAIN_MODEL_ID[0] ][ modelId ]

    #--- Extract all the model cfg parameters string ids. keys.
    modelParamsDictKeys= tuple( modelParamsDict.keys() )

    #--- Need to check if self._fieldsVarType is
    #    ISFMT.DATA_TYPES.WATERLEVELS.name for
    #    applying the CVD to chart datum conversion
    #    procedure(obviously, this kind of data
    #    conversion is only for model water levels).
    if ApplyConversionFlag and \
       self._fieldsVarType == ISFMT.DATA_TYPES.WATERLEVELS.name :

      sys.stdout.write("INFO "+methId+
                       " S-104: Checking for CVD to chart datums data for model -> "+
                       modelId+"\n")

      #--- The CVD to chart datums data file string id. key
      #    must be defined in the modelParamsDictKeys tuple.
      if self.JSON_CVD2CD_FILE_ID[0] not in modelParamsDictKeys :

        sys.exit("ERROR "+methId+
                 " CVD to Chart datum data file path string id. -> "+
                 self.JSON_CVD2CD_FILE_ID[0]+" is not defined in the model parameters dictionary !\n")
      #--- end inner if block.

      #--- FP check for the MainCfgDir
      #    existence on disk.
      if not os.access(MainCfgDir,os.F_OK) :

        sys.exit("ERROR "+methId+
                 " MainCfgDir -> "+MainCfgDir+" directory not found !\n")
      #---

      #--- FP check for the MainCfgDir
      #    being a valid directory.
      if not os.path.isdir(MainCfgDir) :

        sys.exit("ERROR "+methId+
                 " MainCfgDir -> "+MainCfgDir+" is not a directory !\n")
      #---

      #--- Need to add the MainCfgDir to the path of the
      #    CVD to chart datum data file to be able to get
      #    its contents.
      self._cvd2ChartDatumFile= \
        ( MainCfgDir + "/" + modelParamsDict[ self.JSON_CVD2CD_FILE_ID[0] ] ,)

      #--- FP check for the CVD to chart datum data file
      #    existence.
      if not os.access(self._cvd2ChartDatumFile[0], os.F_OK) :

        sys.exit("ERROR "+methId+
                 " self._cvd2ChartDatumFile[0] -> "+
                 self._cvd2ChartDatumFile[0]+" not found !\n")
      #--- end if block.

      sys.stdout.write("INFO "+methId+
                       " Will use CVD to chart datums data file -> "+
                       self._cvd2ChartDatumFile[0]+" for conversion to chart datums\n")
    else :

      sys.stdout.write("INFO "+methId+
                       " No conversion related to chart datum(s) will be done for input fields type(s) -> "+
                       self._fieldsVarType+"\n")

    #--- end outer if-else block.

    sys.stdout.write("INFO "+methId+" end\n")

    #--- All checks are done, return the model relevant parameters
    #    to the calling method.
    return (modelId, modelParamsDict, modelParamsDictKeys)
