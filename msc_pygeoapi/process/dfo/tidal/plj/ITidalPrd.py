#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/ITidalPrd.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.ITidalPrd implementation.
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

#--- Built-in module(s).
import enum

#---
from msc_pygeoapi.process.dfo.IDFO import IDFO
from msc_pygeoapi.process.dfo.util.ITimeMachine import ITimeMachine
from msc_pygeoapi.process.dfo.util.IDataIndexing import IDataIndexing

#---
class ITidalPrd(ITimeMachine, IDataIndexing) :

  """
  Class ITidalPrd is used like a Java Interface just to define
  constants generic parameters for all types of tidal predictions used.
  """

  #--- 15mins as the default time intervals between successive
  #    tidal prediction data.
  DEFAULT_TIMEINCR_SECONDS= ( 900 ,)

  #: Doc Only M. Foreman's method allowed for now
  #      XTIDE maybe eventually  , "XTIDE"]
  ALLOWED_METHODS= \
      enum.Enum( str("ALLOWED_METHODS"), [ str("FOREMAN") ] )

  FIELDS_IDS= {

      IDFO._DATA_TYPES.WATERLEVELS.name : (IDataIndexing.UVZ_IDS.Z.name,),
      IDFO._DATA_TYPES.CURRENTS.name    : (IDataIndexing.UVZ_IDS.U.name,
                                           IDataIndexing.UVZ_IDS.V.name)
  }

  #--- Strings ids. for amplitudes and phases combos tidal constituents dictionaries indexing:
  PHASE_ID= ( str("PHASE"), )
  AMPLITUDE_ID= ( str("AMPLITUDE") ,)

  #--- NOTE: TCF data have the tidal consts. periods(in hours)
  #          do we have to use it for computing predictions ?
  PERIOD_ID= ( str("PERIOD") ,)

  #--- Two (gaussian) sigma as ad-hoc chart datums correction factor:
  ADHOC_CHARTDATUM_CORR_FACTOR= ( 0.979 ,)

  #---
  def __init__(self) :

    ITimeMachine.__init__(self)
    IDataIndexing.__init__(self)

    self.CONSTITUENTS_DATAIN_ID= ( str("ConstituentsData") ,)
