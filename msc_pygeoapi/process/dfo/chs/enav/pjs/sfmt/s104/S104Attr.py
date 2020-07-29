#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/s104/S104Attr.py
# Creation        : Octobre/October 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s104.S104Attr implementation.
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
import os
import sys

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.IS104 import IS104

#---
class S104Attr(IS104) :

  """
  Defines the common instance attributes used by all S104*  classes
  """

  #---
  def __init__(self) :

    IS104.__init__(self)

    #: Doc Initialize self._computeWLTrend unary
    #      tuple to False as default. It could be
    #      redefined to True if the water levels
    #      trend needs to be computed.
    self._computeWLTrends= ( False ,)

    #: Doc Will be used to store the time trend offsets.
    self._timeTrendOffsets= None

    #: Doc Set the default lower 1D array limit for the water
    #      levels trends computations.
    self._wlZElevTrendLowIdx= ( self.WLDATA_ARRAYS_BUFFER[0] ,)

    #--- The upper 1D array limit for the water levels
    #    trends computations needs to be set dynamically
    #    using the number of time increments of the input
    #    model data.
    self._wlZElevTrendUppIdx= None

    #--- self._denAccInv will be used for water levels
    #    trends calculation in the main time increments
    #    loop which writes the output products files.
    #    (denominator factor used in the linear regressions)
    self._denAccInv= None
