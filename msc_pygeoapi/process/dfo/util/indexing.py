#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/util/indexing.py
# Creation        : July/Juillet 2020 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: -
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

#---
import enum

#--- U current component string id.
_UUC_ID= ( str("U") ,)

#--- V current component string id.
_VVC_ID= ( str("V") ,)

#--- Doc Z water level string id.
_ZWL_ID= ( str("Z") ,)

#--- Regroup the U,V,Z string ids. in an Enum object
#    for convenience.
_UVZ_IDS= enum.Enum( str("_UVZ_IDS"), [ _UUC_ID[0], _VVC_ID[0], _ZWL_ID[0]])

#---
_DICT_KEYS_SEP= ( str(",") ,)

_LON_ID= ( str("Lon") ,)
_LAT_ID= ( str("Lat") ,)

_POINTS_DATAIN_ID= ( str("POINTS_DATAIN") ,)
_POINTS_DATAOUT_ID= ( str("POINTS_DATAOUT") ,)

#--- Seems odd but it's handy for dictionary indexing:
_NAME_ID= ( str("WhoAmI") ,)

