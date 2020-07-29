#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/models/ModelDataAttr.py
# Creation        : April/Avril 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.models.ModelDataAttr.py implementation.
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
#import os
#import sys
#import inspect

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.IS102 import IS102

#---
class ModelDataAttr(object) :

  """
  Declare all the common self._* objects attributes inherited by all the
  sub-classes of the dhp.models.* sub-packages.
  """

  def __init__(self) :

    #---
    #methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    #sys.stdout.write("INFO "+methId+" start\n")

    #self._nbMultiProcesses= 1

    #: Doc ModelsDataAttr class attributes:

    #: Doc self._workDir will hold the working directory path(normally used for models input data)
    self._workDir= None

    #--- TODO: Add comments for all the following attributes.
    self._inputFiles= None
    self._fieldsNames= None
    self._inputDataDict= None
    self._tilesWithData= None
    self._inputGridType= None
    self._fieldsVarType= None
    self._inputFilesFmt= None
    self._inputFilesFDef= None
    self._nbTotalHoursOper= None
    #self._noDataValueFFlag= None
    self._modelVersionKeyId= None
    self._currentsFieldNames= None
    self._tilesMdlArrIndices= None
    self._tilesMdlIndicesFDef= None
    self._noDataValueFFlagInv= None
    self._waterLevelsFieldName= None
    self._secondsSinceEpochEnd= None
    self._secondsSinceEpochStart= None
    self._twoPointsExcludeBBoxTuple= None

    #: Doc _inputSetupDone: Boolean flag to signal that
    #      the initial input data setup have already been
    #      done by a previous Maestro instance of the main script.
    self._inputSetupDone= False

    self._s102Level2Use= IS102.DEFAULT_TILES_BASE_LEVEL[0]

    #sys.stdout.write("INFO "+methId+" end\n")
