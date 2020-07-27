#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/util/IDataIndexing.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.util.IDataIndexing implementation.
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
import enum

#---
class IDataIndexing(object) :

  """
  Generic utility class used to define common constants parameters
  (A la Python i.e. with unary tuples). This class can simply
  be inherited by sub-classes which wants to have a direct
  access to its definitions.

  """

  #: Doc U current component string id.
  UUC_ID= ( str("U") ,)

  #: Doc V current component string id.
  VVC_ID= ( str("V") ,)

  #: Doc Z water level string id.
  ZWL_ID= ( str("Z") ,)

  #: Doc Regroup the U,V,Z string ids. in an Enum object
  #      for convenience.
  UVZ_IDS= enum.Enum( str("UVZ_IDS"), [ UUC_ID[0], VVC_ID[0], ZWL_ID[0] ])

  #---
  def __init__(self) :

    #: Doc Use unary tuple for constants definitions:
    self.DICT_KEYS_SEP= ( str(",") ,)

    self.LON_ID= ( str("Lon") ,)
    self.LAT_ID= ( str("Lat") ,)

    self.POINTS_DATAIN_ID= ( str("POINTS_DATAIN") ,)
    self.POINTS_DATAOUT_ID= ( str("POINTS_DATAOUT") ,)

    #: Doc Seems odd but it's handy for dictionary indexing:
    self.NAME_ID= ( str("WhoAmI") ,)
    self.MODEL_NAME_ID=( str("DataSetId") ,)

    #: Doc Do not change this self.DATAVALUE_ID parameter
    #      because it is also used for HDF5 file structure
    #      indexing. 
    self.DATAVALUE_ID= ( str("DATA") ,)
