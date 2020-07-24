#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dfo/tidal/__init__.py
# Creation        : July/Juillet 2020 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - initialization for dfo/tidal main package.
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
from collections import namedtuple

#---
import enum

#--- 15mins as the default time intervals between
#    successive tidal prediction data.
_DEFAULT_TIMEINCR_SECONDS= ( 900 ,)

#--- Only M. Foreman's method allowed for now
#    XTIDE maybe eventually  , "XTIDE"]
_ALLOWED_METHODS= enum.Enum( str("allowed_methods"), [ str("Foreman") ] )

#--- Strings ids. for amplitudes and phases combos
#    tidal constituents dictionaries indexing:
_PHASE_ID= ( str("phase"), )
_AMPLITUDE_ID= ( str("amplitude") ,)

#--- Two (gaussian) sigma as ad-hoc WL chart datums correction factor:
_ADHOC_CHARTDATUM_CORR_FACTOR= ( 0.979 ,)

_CONSTITUENTS_DATAIN_ID= ( str("ConstituentsData") ,)

#--- Do not allow relative imports.
#from __future__ import absolute_import

#--- Built-in module(s).
#import enum

#---
#from dhp.sfmt.ISFMT import ISFMT
#from dhp.util.ITimeMachine import ITimeMachine
#from dhp.util.IDataIndexing import IDataIndexing

##---
#class ITidalPrd(ITimeMachine, IDataIndexing) :
#  """
#  Class ITidalPrd is used like a Java Interface just to define
#  constants generic parameters for all types of tidal predictions used.
#  """
#
#  FIELDS_IDS= { ISFMT.DATA_TYPES.WATERLEVELS.name : (IDataIndexing.UVZ_IDS.Z.name,),
#                ISFMT.DATA_TYPES.CURRENTS.name    : (IDataIndexing.UVZ_IDS.U.name, IDataIndexing.UVZ_IDS.V.name) }
#
#  ##--- NOTE: TCF data have the tidal consts. periods(in hours)
#  ##          do we have to use it for computing predictions ?
#  #PERIOD_ID= ( str("PERIOD") ,)
#
#  ##---
#  #def __init__(self) : # TimeIncrSeconds= DEFAULT_TIMEINCR_SECONDS[0]) :
#  #  ITimeMachine.__init__(self)
#  #  IDataIndexing.__init__(self)
