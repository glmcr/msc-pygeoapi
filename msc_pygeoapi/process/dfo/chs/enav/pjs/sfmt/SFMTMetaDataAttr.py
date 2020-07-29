#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTMetaDataAttr.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTMetaDataAttr implementation
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
import inspect

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT

#---
class SFMTMetaDataAttr(ISFMT) :

  """
  Class having some specific SFMT DHP metadata attributes.
  """

  def __init__(self) :

    ISFMT.__init__(self)

    #: Doc (type->dictionary): Generic json metadata dictionary for SFMT DHP data
    self._jsonProductMetaDataDict= None

    #: Doc (type->dictionary): A dictionary holding the Json formatted HDF5 root metadata.
    self._jsonRootTypeMetaDataDict= None

    #: Doc (type->dictionary): A dictionary holding common metadata coming from a json formatted file.
    self._jsonCommonMetaDataDict= None
