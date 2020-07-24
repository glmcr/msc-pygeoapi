#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : dfo msc-pygeoapi process plugins
# File/Fichier    : dfo/util/itime_machine.py
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
from collections import namedtuple

#--- Define some constants(a.k.a. variables that are not allowed to vary).
#    Unfortunately, there is no such thing as real constant objects in Python.

_PREPEND_ZER0_2DIGITS_FMT= ( "%02d" ,)

#--- No need for lengthy comments here, the names of
#    some constants are a kind of self-documenting code.
_HOURS_PER_DAY= ( 24 ,)
_HOURS_PER_DAY_INV= ( 1.0/_HOURS_PER_DAY[0] ,)

_MINUTES_PER_HOUR= ( 60 ,)
_SECONDS_PER_MINUTE= ( 60 ,)

_SECONDS_PER_HOUR= ( _MINUTES_PER_HOUR[0] * _SECONDS_PER_MINUTE[0] ,)

#--- Use a product by 1.0/_SECONDS_PER_HOUR[0] instead of a
#    division by _SECONDS_PER_HOUR[0] for operations. Can
#    get some significant exec speedup when doing so.
_SECONDS_PER_HOUR_INV= ( 1.0/_SECONDS_PER_HOUR[0] ,)

_SECONDS_PER_15_MINS= ( 15 * _SECONDS_PER_MINUTE[0] ,)

_DAYS_PER_NORMAL_YEAR= ( 365 ,)

_SECONDS_PER_DAY= ( _HOURS_PER_DAY[0] * _SECONDS_PER_HOUR[0] ,)

#--- Same reason as for _SECONDS_PER_HOUR_INV.
_SECONDS_PER_DAY_INV= ( 1.0/_SECONDS_PER_DAY[0] ,)

_HOURS_PER_NORMAL_YEAR= ( _HOURS_PER_DAY[0] * _DAYS_PER_NORMAL_YEAR[0] ,)

#--- Same reason as for _SECONDS_PER_HOUR_INV.
_HOURS_PER_NORMAL_YEAR_INV= ( 1.0/_HOURS_PER_NORMAL_YEAR[0], )

#--- INF_YEAR_LIMIT: Past time limit for tidal predictions
#    TODO: Test if we can go before December 31 1899 at noon for
#          tidal predictions with M. Foreman's method.
#
_INF_YEAR_LIMIT= ( 1900 ,)

_DATE_TIME_FMT_LEN= ( 6 ,)

#--- No it is not related to the thermodynamic
#    arrow-of-time unfortunately.
_ARROW_OF_TIME= { str("FORWARD") : 1.0,
                  str("BACKWARD") : -1.0 }

#--- Year-Month-Day string conversion format:
#_YYYYMMDDFmt= ( str("%Y%m%d") ,)
_YYYYMMDDFMT= ( str("%Y%m%d") ,)

#--- hour-minutes-seconds string conversion format:
#_hhmmssFmt= (str("%H%M%S") ,)
_HHMMSSFMT= (str("%H%M%S") ,)

_DATE_TIME_SPLIT_STR= ( str(".") ,)
_DATE_TIME_UTC_SUFFIX= ( str("Z") ,)

#--- NOTE: Need to use "".join() to get what we want i.e. a one
#          string tuple which is equivalent of a constant string:
_DEFAULT_GET_SECONDS_FMT= ( str( "".join(_YYYYMMDDFMT[0] + \
                                         _DATE_TIME_SPLIT_STR[0] + \
                                         _HHMMSSFMT[0] + _DATE_TIME_UTC_SUFFIX[0]) ) ,)

_DATE_TIME_ARRAY_INDICES= namedtuple( str("idx"),
                                      str("YEAR MONTH MDAY HOUR MINUTES SECONDS") ) (0, 1, 2, 3, 4, 5)

