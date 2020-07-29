#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/s102/S102DataAttr.py
# Creation        : August/Aout 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s102.S102DataAttr implementation.
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

#--- Built-in module(s):
import os
import sys
import inspect

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.IS102 import IS102

#---
class S102DataAttr(IS102):

  """
  Class that defines the common attributes that will be used
  by all S102* classes objects instances.
  """

  #---
  def __init__(self):

    IS102.__init__(self)

    #: Doc self._dataDict(type->dictionary) will contain all tiles data.
    self._dataDict= None

    #: Doc self._baseLevelTiles(type->dictionary) reference to the base level tiles dictionary in self._dataDict only.
    self._baseLevelTiles= None

    #: Doc (type->string) The string id. name for the tiles base level.
    self._baseLevelNameId= None
