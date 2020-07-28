#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/astro/AstroInfosFactory.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.astro.AstroInfosFactory implementation.
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
import os
import sys
import time
import inspect

#----
from msc_pygeoapi.process.dfo.tidal.TidalPrd import TidalPrd
from msc_pygeoapi.process.dfo.tidal.ITidalPrd import ITidalPrd
from msc_pygeoapi.process.dfo.util.TimeMachine import TimeMachine

#---
class AstroInfosFactory(ITidalPrd, TimeMachine) :

  """
  Generic class for astronomic informations. The only tidal prediction method used
  for now(2018-11-20) is the method of M. Foreman's but we can think that other methods
  could eventually be used in the future.
  """

  #---
  def __init__(self, SecondsSinceEpochStart,
               SecondsSinceEpochEnd, TimeIncrSeconds= None) :

    """
    SecondsSinceEpochStart : Seconds since the epoch which will be the initial time-stamp of the time reference of the astronomic informations.
    SecondsSinceEpochEnd   : Seconds since the epoch which will be the final time-stamp of the time reference of the astronomic informations.
    TimeIncrSeconds        : Time increment interval in seconds between successive prediction data.
    """

    ITidalPrd.__init__(self)
    TimeMachine.__init__(self)

    methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

##    #--- Foreman's tidal method as default method to use
##     self.Method= "FOREMAN"
##     if Method2Use is not None :
##       if not self.validateTidalMethod(Method2Use) :
##         sys.stderr.write("ERROR "+methID+ Invalid tidal prediction method requested -> " + Method2Use +"\n")
##         sys.exit(1)
##       self.Method= Method2Use
##     sys.stdout.write("INFO "+methID+" Will use method -> " + self.Method +"\n")

    #--- Start from scratch.
    self.clear()

    #--- Some fool-proof checks:
    if SecondsSinceEpochStart is None or \
         SecondsSinceEpochStart == 0 or SecondsSinceEpochStart < 0 :

      sys.exit("ERROR "+methID+
               " Invalid SecondsSinceEpochStart -> "+ str(SecondsSinceEpochStart) + " !\n")
    #---

    self._secondsSinceEpochStart= SecondsSinceEpochStart

    if SecondsSinceEpochEnd is None or \
         SecondsSinceEpochEnd <= self._secondsSinceEpochStart :

      sys.exit("ERROR "+methID+" Invalid SecondsSinceEpochEnd -> "+
               str(SecondsSinceEpochEnd) + " <= self._secondsSinceEpochStart !\n")
    #---

    #--- Store time stamps in the object:
    self._secondsSinceEpochEnd= SecondsSinceEpochEnd

    #--- Default time increment between successive tidal predictions data.
    #    (a.k.a. we can call it "time nodes")
    self._timeIncrSeconds= ITidalPrd.DEFAULT_TIMEINCR_SECONDS[0]

    #--- Use the time increment if defined in the args.:
    if TimeIncrSeconds is not None :

      #--- Forget about tidal predictions with time increment > self.SECONDS_PER_HOUR
      if TimeIncrSeconds > self.SECONDS_PER_HOUR[0] :

        sys.exit("ERROR "+methID+" TimeIncrSeconds -> "+str(TimeIncrSeconds)+
                 " > self.SECONDS_PER_HOUR[0] ! TimeIncrSeconds must be <=  self.SECONDS_PER_HOUR[0] !\n")
      #---

      self._timeIncrSeconds= TimeIncrSeconds

    sys.stdout.write("INFO "+methID+" Will use -> "+
                     str( self._timeIncrSeconds)+" seconds for time increment between prediction data\n")

    #--- self.sse to keep track of where we are in time.
    self._sse= self._secondsSinceEpochStart

  #--- Instance method clear
  def clear(self) :

    """
    Just for starting from scratch for date-time attributes of self.
    """

    self._secondsSinceEpochStart= self._secondsSinceEpochEnd= self._timeIncrSeconds= self.sse= None

  ##--- Keep for possible future usage.
  ##---
  #@staticmethod
  #def validateConstName(AConstName, ValidConstsNames) :
  #  """
  #  Class method validateConstName.
  #  AConstName : A tidal constituent name to validate.
  #  ValidConstsNames : Array of valid tidal constituents names to use for the validation.
  #  """
  #  methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
  #  if AConstName is None :
  #    sys.exit("ERROR "+methID+" AConstName is None ! \n")
  #  if ValidConstsNames is None :
  #    sys.exit("ERROR "+methID+" ValidConstsNames is None ! \n")
  #  if len(ValidConstsNames) < 2 :
  #    sys.exit("ERROR "+methID+" len(ValidConstsNames) < 2 ! \n")
  #  found= False
  #  for cn in ValidConstsNames :
  #    if AConstName == cn :
  #      found= True
  #      break
  #  return found

  ##--- Keep for possible future usage.
  #def computeTidalPrediction(self, timeStampSeconds, constituent1DDataObj) :
  #  """
  #  Instance method computeTidalPrediction.
  #  timeStampSeconds: Time offset from self.SecondsSinceEpoch. It is not the real time stamp
  #  of the prediction which is self.SecondsSinceEpoch + timeStampSeconds
  #  NOTE: timeStampSeconds could be < 0 if time is going backwards.
  #  constituent1DData: A constituent1DData object containing all informations for a tidal constituent.
  #  NOTE: No arguments validation done in order to ensure to get the best performance.
  #  """
  #  #--- Get the time offset since last astronomic infos. update:
  #  #    NOTE: updateTimeDiff could be 0 if time is going backwards.
  #  updateTimeDiff= timeStampSeconds - self.SecondsSinceEpoch
  #  #--- Update astronomic informations only if the absolute value of updateTimeDiff is equal to self.ASTRO_UDPATE_OFFSET_SECOND
  #  #    TODO: Is this relevant for other tidal methods than Foreman's method ?
  #  if int(math.fabs(updateTimeDiff)) == self.ASTRO_UDPATE_OFFSET_SECONDS :
  #    self.SecondsSinceEpoch += updateTimeDiff
  #    updateTimeDiff= 0
  #  #--- Local accumulator for the computed tidal amplitudes of every tidal constituents:
  #  tidalAmplitudeAcc= 0.0
  #  #--- Loop on the constituent1DDataObj contents and accumulate tidal amplitudes
  #  #    for all constituents contained by this object.
  #  for c1d in constituent1DDataObj :
  #    tidalAmplitudeAcc += c1d.getTidalAmplitude(updateTimeDiff)
  #  return tidalAmplitudeAcc

  ##--- Keep it for possible future usage.
  #---
  #def updateTimeReference(self,timeIncrement) :
  #  """
  #  Instance method updateTimeReference. To be inherited by child classes.
  #  timeIncrement: A time increment in seconds to add to self.SecondsSinceEpoch.
  #  NOTE: Could be < 0 if time is going backwards.
  #  NOTE: No arguments validation done in order to ensure to get the best performance.
  #  """
  #  #if self.SecondsSinceEpoch is None :
  #  #  sys.stderr.write("ERROR tidalprd.astro.AstroInfos.updateTimeReference(self,timePosIncr): self.SecondsSinceEpoch == None" + " !\n")
  #  #  sys.exit(1)
  #  self._secondsSinceEpoch += timeIncrement

