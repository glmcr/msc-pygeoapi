#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/util/ITimeMachine.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.util.ITimeMachine implementation.
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
from collections import namedtuple

#---
class ITimeMachine(object) :

  """
  Class defining some constants(a.k.a. variables that are not allowed to vary)
  values used by its child class TimeMachine or any other class inheriting from it.
  """

  def __init__(self) :

    self.PREPEND_ZER0_2DIGITS_FMT= ( "%02d" ,)

    #--- No need for lengthy comments here, the names of
    #    some constants are a kind of self-documenting code.
    self.HOURS_PER_DAY= ( 24 ,)
    self.HOURS_PER_DAY_INV= ( 1.0/self.HOURS_PER_DAY[0] ,)

    self.MINUTES_PER_HOUR= ( 60 ,)
    self.SECONDS_PER_MINUTE= ( 60 ,)

    self.SECONDS_PER_HOUR= ( 3600 ,)
    self.SECONDS_PER_HOUR_INV= ( 1.0/self.SECONDS_PER_HOUR[0] ,)

    self.SECONDS_PER_15_MINS= ( 15*self.SECONDS_PER_MINUTE[0] ,)

    self.DAYS_PER_NORMAL_YEAR= ( 365 ,)

    self.SECONDS_PER_DAY= ( self.HOURS_PER_DAY[0] * self.SECONDS_PER_HOUR[0] ,)
    self.SECONDS_PER_DAY_INV= ( 1.0/self.SECONDS_PER_DAY[0] ,)

    self.HOURS_PER_NORMAL_YEAR= ( self.HOURS_PER_DAY[0] * self.DAYS_PER_NORMAL_YEAR[0] ,)

    self.HOURS_PER_NORMAL_YEAR_INV= ( 1.0/self.HOURS_PER_NORMAL_YEAR[0], )

    #--- INF_YEAR_LIMIT: Past time limit for tidal predictions
    #    TODO: Test if we can go before December 31 1899 at noon for
    #          tidal predictions with M. Foreman's method.
    #
    self.INF_YEAR_LIMIT= ( 1900 ,)

    self.DATE_TIME_FMT_LEN= ( 6 ,)

    #: Doc It is not related to the thermodynamic arrow-of-time.
    self.ARROW_OF_TIME= { str("FORWARD") : 1.0,
                          str("BACKWARD") : -1.0 }

    #: Doc Year-Month-Day string conversion format:
    self.YYYYMMDDFmt= ( str("%Y%m%d") ,)

    #: Doc hour-minutes-seconds string conversion format:
    self.hhmmssFmt= (str("%H%M%S") ,)

    self.DATE_TIME_SPLIT_STR= ( str(".") ,)
    self.DATE_TIME_UTC_SUFFIX= ( str("Z") ,)

    #--- NOTE: Need to use "".join() to get what we want i.e. a one
    #          string tuple which is equivalent of a constant string:
    self.DEFAULT_GET_SECONDS_FMT= ( str( "".join(self.YYYYMMDDFmt[0] + \
                                         self.DATE_TIME_SPLIT_STR[0] + \
                                         self.hhmmssFmt[0] + self.DATE_TIME_UTC_SUFFIX[0]) ) ,)

    self.DATE_TIME_ARRAY_INDICES= namedtuple( str("idx"),
                                              str("YEAR MONTH MDAY HOUR MINUTES SECONDS") ) (0, 1, 2, 3, 4, 5)

    #self.NORMAL_NUM_OF_DAYS_PER_MONTH= \
    # namedtuple( str("days"),\
    #   str("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC") )\
    #(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    #self.NORMAL_NUM_OF_DAYS_PER_MONTH= { str("01") : 31,
    #                                     str("02") : 28,
    #                                     str("03") : 31,
    #                                     str("04") : 30,
    #                                     str("05") : 31,
    #                                     str("06") : 30,
    #                                     str("07") : 31,
    #                                     str("08") : 31,
    #                                     str("09") : 30,
    #                                     str("10") : 31,
    #                                     str("11") : 30,
    #                                     str("12") : 31  }

