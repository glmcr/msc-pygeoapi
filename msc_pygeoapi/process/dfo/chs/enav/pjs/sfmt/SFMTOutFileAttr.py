#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTOutFileAttr.py
# Creation        : October/Octobre 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTOutFileAttr implementation.
#
# Remarks :
#
# License :
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
#==============================================================================

#--- Do not allow relative imports.
from __future__ import absolute_import

#---
import os
import sys

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTAttr import SFMTAttr

#---
class SFMTOutFileAttr(SFMTAttr) :

  """
  Regroup all SFMT DHP HDF5 data file structures in one class.
  """

  #---
  def __init__(self, S102Obj):

    """
    S102Obj (type->S102): A S102 class instance object.
    """

    SFMTAttr.__init__(self, S102Obj)

    #: Doc Reference to the ROOT GROUP data structure
    #      in a HDF5 output file.
    self._hdf5FileRootObj= None

    #: Doc Generic HDF5 GROUP data structure for all SFMT DHP data
    #      format types It is the 1st GROUP data structure just under
    #      the ROOT GROUP data structure in a HDF5 output file.
    self._hdf5ProductGroup= None

    #--- TODO: We will probably have to create new classes
    #          which will inherits from this class for each
    #          data coding formats used. Now(2019-10-02) we
    #          only have to deal with data coding format 3.

    #: Doc The specific product HDF5 GROUP DATA structure which have
    #      to be created inside the self._hdf5ProductGroup GROUP data
    #      structure itself(ex. <product>.01 in data coding format 3 files).
    self._hdf5ProductGroupData= None

    #: Doc To keep a reference to the date-timestamps strings ids. keys
    #     coming from the input model data and used for the product output files.
    self._dateTimeKeys= None

    #: Doc To keep a reference to the time interval between the input model data
    #      NOTE: Only used for S104 data
    self._timeIncrIntrv= None

    #: Doc To keep a reference to the dictionary for the setup of the HDF5 metadata
    #      for the specific DH product data coding format #
    self._productGroupAttrDict2Set= None

    #: Doc To keep a reference to the product HDF5 GROUP DATA string id suffix(if any).
    self._productGroupDataStrSuffix= None
