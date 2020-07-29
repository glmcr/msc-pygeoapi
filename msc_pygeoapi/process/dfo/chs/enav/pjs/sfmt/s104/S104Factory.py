#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/s104/S104.py
# Creation        : Septembre/September 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s104.S104 implementation.
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
import time
import math
import inspect

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.IS104 import IS104
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.S104Attr import S104Attr
from msc_pygeoapi.process.dfo.chs.enav.pjs.util.IDataIndexing import IDataIndexing

#---
class S104Factory(S104Attr) :

  """
  Provide some generic methods for all S104* derived classes.
  """

  def __init__(self) :

    S104Attr.__init__(self)

  #---
  def getWLTrendParams(self) :

    """
    Compute the parameters that will be used for
    the water levels trends.

    TODO: Verify if the algorithm used could
    be used for time incr. intervalls < 900s.

    NOTE: No fool proof checks here for performance reasons.
    """

    #--- Get the moving time window to use for
    #    the WL trends(NOTE: self._timeIncrInterval
    #    must be in seconds and must obviously > 0
    #    here ).
    self._wlZElevTrendLowIdx= \
      int(self.SECONDS_PER_HOUR[0])/int(self._timeIncrInterval)

    #: Doc Set the upper 1D array limit for the
    #  water levels trends computations.
    self._wlZElevTrendUppIdx= \
      ( len(self._dateTimeKeys) - self._wlZElevTrendLowIdx ,)

    #--- TODO: Check if this time trend offsets calculation
    #          could it be done just once instead of setting
    #          the same local tuple for each output file ??

    #: Doc Get the time offsets to calculate the water levels elevations trends.
    timeTrendIncr= \
      ( self._timeIncrInterval * self.SECONDS_PER_HOUR_INV[0] ,)

    self._timeTrendOffsets= ( -timeTrendIncr[0]*2.0,
                              -timeTrendIncr[0],
                              0.0,
                              timeTrendIncr[0],
                              timeTrendIncr[0]*2.0 )

    #: Doc Accumulator for the denominator of the
    #      linear regression slope coefficient that
    #      will be used for the water levels elevations trends.
    denAcc= 0.0

    #--- NOTE: This accumulator computation is done
    #          just once for all time stamps considered
    #          to speed up the exec. of the
    #          getWLZElevationsTrend method that will
    #          be used in the main time increments loop
    #          which writes the output products files.

    for hto in self._timeTrendOffsets :
      denAcc += hto*hto
    #--- end for for hto in timeTrendOffsets

    #--- NOTE: No check here for denAcc being embarassingly close to zero.
    #          Then it's obvious that the timeTrendOffsets contents should
    #          be such that we do no end up with an exploding division
    #          producing a NaN in the ( 1.0/denAcc ,) command below.

    #--- Defines the denominator factor that will be used for
    #    the WL trends calculation(i.e. linear regressions).
    self._denAccInv= ( 1.0/denAcc ,)

    #--- Signals that the water levels trends will be computed.
    self._computeWLTrends= ( True ,)

  #---
  def getWLZElevationsTrend(self, TimeStampsTuple, TimeTrendOffsetsTuple, DenAccInv,
                            PointDataDict, SlopeThreshold= IS104.WL_TREND_THRESHOLD[0]) :
    """
    Calculate an instantaneous temporal WL trend(INCREASING, DECREASING, STEADY) for a given water
    level using the immediate previous time increments neighbors, the actual water level and next time
    increments water levels neighbors. It uses a simple linear regression algorithm to do so.

    TimeStampsTuple (type->tuple): A tuple holding the timestamps indices to use for the PointDataDict indexing.
    NOTE: Normally contains only five items. Could try with only three eventually.

    TimeTrendOffsetsTuple (type->tuple): A tuple holding the time offsets in seconds for the previous timestamps
    the actual timestamp(this one should be 0.0 then) and the next timestamps used in the linear regression algorithm.

    DenAccInv (type->float): Is the constant value of the 1.0/denominator ratio used in the linear regression algorithm.

    PointDataDict (type->dictionary):  A water levels grid point data(webTide, IWLS or NEMO) dictionary.

    SlopeThreshold (type->float) Default-> IS104.WL_TREND_THRESHOLD[0]: A positive floating point value used to 
    discriminate the trend between STEADY and not steady(i.e. INCREASING or DECREASING) water level temporal trend.

    NOTE: No fool-proof checks and also assuming that:

    1). TimeStampsTuple and TimeTrendOffsetsTuple have the same dimensions:

    2). SlopeThreshold is not negative and not 0.0

    3). No check done here for DenAccInv being a NaN then it is the responsibility of the caller to provide a
    valid DenAcc value which is compatible with the timeTrendOffsetsTuple contents and not a NaN.
    """

    #: Doc Default WL trend is UNKNOWN:
    ret= self.WL_TREND_UNKNOWN[0]

    #: Doc Local accumulator for the numerator of the linear regression slope coefficient.
    numAcc= 0.0

    #: Doc Iteration variable for the time increments.
    tsIncr= 0

    #: Doc Loop on the timestamps.
    #      NOTE: TimeStampsTuple normally contains only five items. Could try with only three eventually.
    for timeStamp in TimeStampsTuple :

      numAcc += TimeTrendOffsetsTuple[tsIncr] * PointDataDict[timeStamp][ IDataIndexing.UVZ_IDS.Z.name ]

      #--- The accumulation of denAcc is now done just once in the calling method
      #    instead of computing the same damn thing for each usage of this method.
      #
      #  #tOfst= TimeTrendOffsetsTuple[tsIncr]
      #  #denAcc += tOfst*tOfst
      #  #numAcc += tOfst * PointDataDict[timeStamp][ wlZElevValueId[0] ]
      #
      #  #print "z="+str(PointDataDict[timeStamp][ wlZElevValueId[0] ])

      #--- Increment timestamp iteration variable:
      tsIncr += 1

    #--- NOTE: DenAccInv is an unary tuple:
    slope= ( DenAccInv[0]*numAcc ,)

    #: Doc Set the trend value with the time-window water levels slope.
    if math.fabs(slope[0]) > SlopeThreshold :

      if slope[0] < 0.0 :
        ret= self.WL_TREND_DECREASING[0]
      else :
        ret= self.WL_TREND_INCREASING[0]

    else :
      ret= self.WL_TREND_STEADY[0]

    return ( ret ,)
