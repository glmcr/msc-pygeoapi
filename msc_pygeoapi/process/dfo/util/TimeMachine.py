#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/util/TimeMachine.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.util.TimeMachine implementation.
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
import sys
import time
import inspect
import calendar

#---
from dhp.util.ITimeMachine import ITimeMachine

#---
class TimeMachine(ITimeMachine) :

  """
  Utility class dealing with date-time processing stuff.
  Inherits from super class ITimeMachine.
  """

  #: Doc Need to pump up the default recursion limit of 1000 to 50000 to get
  #      the recursive static method roundPastToTimeIncrSeconds to work as expected.
  sys.setrecursionlimit(50000)

  #---
  def __init__(self) :

    ITimeMachine.__init__(self)

    #methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

  #--- Instance method getDateTimeString :
  def getDateTimeStringZ(self, SecondsSE, DateTimeStringFormat= None) :

    """
    Returns a date-time string built from the SecondsSE argument
    and formatted with the DateTimeStringFormat argument if any.

    SecondsSE (type->int): Seconds since the UNIX epoch start.

    DateTimeStringFormat (type->string) <OPTIONAL> default->None : The string format to use for the date-time
    string to built from the SecondsSE argument.

    return (type->string)
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    ##--- Uncomment for debugging
    ##--- The usual fool-proof checks:
    #if SecondsSE is None :
    #  sys.exit("ERROR "+methId+" SecondsSE is None! \n")
    #
    #if SecondsSE < 0 :
    #  sys.exit("ERROR "+methId+" SecondsSE < 0! \n")

    if DateTimeStringFormat is None :
      DateTimeStringFormat= self.DEFAULT_GET_SECONDS_FMT[0]

    #: Doc Use the old-school basic time.strftime method to get what we want:
    return time.strftime(DateTimeStringFormat, time.gmtime(SecondsSE) )

  #---
  def getYYYYMMDDYesterday(self, YYYYMMDDToday) :

    """
    Build Yesterday' YYYYMMDD string using today's YYYYMMDD string.

    YYYYMMDDToday (type->string) : Today's YYYYMMDD string.

    return (type->string) : Yesterday's YYYYMMDD string.
    """

    #: Doc Need to go back 24 hours in the past to also consider yesterday's NEMO data
    #      if this script have been started by the 18Z ORJI run(i.e. 18Z NEMO outputs
    #      for a given day are produced the following day around 01:20Z)

    #    NOTE: No need to do that when running inside in the ECCC Maestro oper. env.
    #          system using DATEO variable which is the synoptic hour 00Z, 06Z, 12Z and 18Z.
    seconds24HInPast= self.getSeconds(YYYYMMDDToday, self.YYYYMMDDFmt[0]) - self.SECONDS_PER_DAY[0]

    #: Doc Using getDateTimeStringZ from super class TimeMachine to return yesterday's YYYYMMDD string.
    return self.getDateTimeStringZ(seconds24HInPast).split( self.DATE_TIME_SPLIT_STR[0] )[0]

  #--- Instance method getSeconds
  def getSeconds(self, YYYYMMDDhhmmss, DateTimeStringFormat) :

    """
    Instance method returning the conversion to seconds since
    the UNIX epoch start of a date-time string.

    YYYYMMDDhhmmss (type->string): The date-time string to convert.

    DateTimeStringFormat (type->string): The Python time.strptime method string format to use for the conversion.
    (https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    ##--- Uncomment for debugging
    ##--- The usual fool-proof checks:
    #if YYYYMMDDhhmmss is None :
    #  sys.exit("ERROR "+methId+" YYYYMMDDhhmmss is None! \n")
    #
    #if DateTimeStringFormat is None :
    #  sys.exit("ERROR "+methId+" DateTimeStringFormat is None! \n")

    return int( time.mktime( time.strptime( YYYYMMDDhhmmss, DateTimeStringFormat ) ) )

  #---
  @staticmethod
  def roundPastToTimeIncrSeconds(IncrSeconds, Seconds) :

    """
    Class method which round a date-time in seconds since the epoch
    to the nearest date-time in seconds since the epoch in the past
    which have an exact difference of -IncrSeconds with it.

    IncrSeconds (type->int): A time increment in seconds (usually 900,1800,3600,...)
    Seconds (type->int):  A date-time in seconds since the UNIX epoch start.

    Remark: Using tail recursion.

    NOTE1: No checks if Seconds is larger than IncrSeconds. It is the responsibility
    of the calling method to pass values as Seconds > IncrSeconds.

    NOTE2: No checks if the arguments are negative. It is the responsibility
    of the calling method to pass positive values.
    """

    ret= Seconds

    if ret%IncrSeconds != 0 :

      #: Doc recursive call here !
      ret= TimeMachine.roundPastToTimeIncrSeconds(IncrSeconds, Seconds - 1)

    return ret
