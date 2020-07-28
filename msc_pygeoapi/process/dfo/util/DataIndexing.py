#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/util/DataIndexing.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.util.DataIndexing implementation.
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
import numpy

#---
from msc_pygeoapi.process.dfo.util.IDataIndexing import IDataIndexing

#---
class DataIndexing(IDataIndexing) :

  """
  Utility class used to define some generic data indexing methods.
  """

  #---
  def __init__(self) :

    IDataIndexing.__init__(self)

  #---
  @staticmethod
  def getNumpyDataSlice( NumpyDataArray, LowUppRangeTuple= None) :

    """
    NumpyDataArray (type->numpy darray): 2D or 3D

    LowUppRangeTuple (type->tuple of two type->int) <OPTIONAL> default->None:
    If it is not None it must be a two items tuple holding the lower and upper NC4 3D
    data slicing integer indices. The low 3D slicing index could be zero and the upp
    3D slicing index must be > 0. Assuming 2D input data if None.
    """

    retData= None

    if LowUppRangeTuple is None :
      retData= NumpyDataArray
    else :

      #nbLevels= LowUppRangeTuple[1] - LowUppRangeTuple[0]
      #retData= numpy.empty([nbLevels,:,:])

      #retData= numpy.empty([nbLevels, NumpyDataArray.shape[1], NumpyDataArray.shape[2]])
      #print("retData.shape="+str(retData.shape))
      retData= {}

      for levelIter in tuple(range(LowUppRangeTuple[0], LowUppRangeTuple[1])) :

        retData[levelIter]= NumpyDataArray[levelIter]

      #retData= NumpyDataArray[LowUppRangeTuple[0]:LowUppRangeTuple[1]]

      print("retData[1].shape="+str(retData[1].shape))

    return retData
