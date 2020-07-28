#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/astro/foreman/ForemanFactory.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.astro.foreman.ForemanFactory implementation.
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
import math
import inspect

#---
from msc_pygeoapi.process.dfo.util.JsonCfgIO import JsonCfgIO
from msc_pygeoapi.process.dfo.util.TimeMachine import TimeMachine

#---
from msc_pygeoapi.process.dfo.tidal.astro.foreman.IForeman import IForeman
from msc_pygeoapi.process.dfo.tidal.astro.foreman.SunMoonEphemerides import SunMoonEphemerides
from msc_pygeoapi.process.dfo.tidal.astro.foreman.ForemanAstroFactory import ForemanAstroFactory
from msc_pygeoapi.process.dfo.tidal.astro.foreman.ForemanMainConstituent import ForemanMainConstituent
from msc_pygeoapi.process.dfo.tidal.astro.foreman.ForemanShWtConstituent import ForemanShWtConstituent
from msc_pygeoapi.process.dfo.tidal.astro.foreman.ForemanConstituentAstro import ForemanConstituentAstro
from msc_pygeoapi.process.dfo.tidal.astro.foreman.ForemanMainConstituentDrv import ForemanMainConstituentDrv

#---
class ForemanFactory(ForemanAstroFactory) :

  """
  A class that is inherited by other classes which need to compute tidal predictions
  with Foreman method.
  """

  #---
  def __init__(self, JSONStaticDataFile,
               SecondsSinceEpochStart, SecondsSinceEpochEnd, TimeIncrSeconds= None) :
    """
    JSONStaticDataFile: The JSON format file where to get the static legacy astronomic and tidal constituent input parameters.
    SecondsSinceEpochStart : Seconds since the epoch which will be the initial time-stamp of the time reference of the astronomic informations.
    SecondsSinceEpochEnd   : Seconds since the epoch which will be the final time-stamp of the time reference of the astronomic informations.
    TimeIncrSeconds        : Time increment interval in seconds between successive prediction data.
    """

    ForemanAstroFactory.__init__(self, SecondsSinceEpochStart,
                                 SecondsSinceEpochEnd, TimeIncrSeconds)

    methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

    sys.stdout.write("INFO "+methID+" start\n")

    #--- Usual fool-proof checks:
    if JSONStaticDataFile is None :
      sys.exit("ERROR "+methID+" JSONStaticDataFile is None !\n")

    if not os.access(JSONStaticDataFile,os.F_OK) :
      sys.exit("ERROR "+methID+" JSONStaticDataFile not found !\n")

    sys.stdout.write("INFO "+methID+
                     " Trying to get static data from JSON config. file -> "+JSONStaticDataFile+"\n")

    #--- Get the static legacy astronomic and tidal constituent input parameters from the JSON format file:
    self._staticData= JsonCfgIO.getIt(JSONStaticDataFile)

    if self._staticData is None :
      sys.exit("ERROR "+methID+
               " Problem with getting static data from JSON config. file -> "+JSONStaticDataFile+"\n")

    #--- Extract(in an unary tuple) the astronomic argument constant phase threshold from self.staticData:
    self._phaseThreshold= ( self._staticData[ self.ASTRO_PARAMS_ID[0] ][ self.V_ASTRO_PHASE_INT_THRESHOLD_ID[0] ] ,)

    sys.stdout.write("INFO "+methID+" Got static data from JSON config. file -> "+JSONStaticDataFile+"\n")

    #--- Check that self._secondsSinceEpochStart is a multiple of self.ASTRO_UDPATE_OFFSET_SECONDS for Foreman's method algorithm:
    checkStartTime= \
      TimeMachine.roundPastToTimeIncrSeconds(self.ASTRO_UDPATE_OFFSET_SECONDS[0], self._secondsSinceEpochStart)

    if checkStartTime != self._secondsSinceEpochStart :
      sys.exit("ERROR "+methID+" self._secondsSinceEpochStart is not a multiple of ->"+
               str(self.ASTRO_UDPATE_OFFSET_SECONDS[0])+" Cannot compute astronomic informations !\n")
    #---

    #--- Check that self._secondsSinceEpochEnd is also a multiple of self.ASTRO_UDPATE_OFFSET_SECONDS for Foreman's method algorithm:
    checkEndTime= \
      TimeMachine.roundPastToTimeIncrSeconds(self.ASTRO_UDPATE_OFFSET_SECONDS[0], self._secondsSinceEpochEnd)

    if checkEndTime != self._secondsSinceEpochEnd :
      sys.exit("ERROR "+methID+" self._secondsSinceEpochEnd is not a multiple of ->"+
               str(self.ASTRO_UDPATE_OFFSET_SECONDS[0])+" Cannot compute astronomic informations !\n")
    #---

    sys.stdout.write("INFO "+methID+" self._secondsSinceEpochStart -> "
                      +self.getDateTimeStringZ(self._secondsSinceEpochStart) + "\n")

    sys.stdout.write("INFO "+methID+" self._secondsSinceEpochEnd -> "+
                      self.getDateTimeStringZ(self._secondsSinceEpochEnd) + "\n")

    uppLoopBound= self._secondsSinceEpochEnd

    #--- NOTE: Need to add one self.ASTRO_UDPATE_OFFSET_SECONDS[0] to uppLoopBound
    #          to get all the time-stamp wanted if TimeIncrSeconds != self.ASTRO_UDPATE_OFFSET_SECONDS[0]
    if TimeIncrSeconds != self.ASTRO_UDPATE_OFFSET_SECONDS[0] :
      uppLoopBound += self.ASTRO_UDPATE_OFFSET_SECONDS[0]

    #--- Now populate Moon&Sun ephemerides pre-computed data:
    for timeIncr in range(self._secondsSinceEpochStart, uppLoopBound, self.ASTRO_UDPATE_OFFSET_SECONDS[0]) :

      self._SMEData[timeIncr]= SunMoonEphemerides(self._staticData, timeIncr)

    sys.stdout.write("INFO "+methID+" end\n")

  #---
  def getNewConstituentObj(self, ConstName,
                           FNodalModAdjInit, ForemanConstituentAstroObjects) :

    """
    Create a new ForemanConstituentAstro object for both main and shallow water(if any) tidal constituents.

    ConstName (type->string) : The string id. name of a tidal constituent.
    FNodalModAdjInit (type->float) : The astronomic nodal adjustment factor initialization value.
    ForemanConstituentAstroObjects (type->list): A list object to store the newly created ForemanConstituentAstro objects.
    """

    methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

    ##--- Uncomment fool-proof checks for debugging.
    #if self.staticData is None :
    #  sys.exit("ERROR "+methID+" Problem with getting static data from JSON config. file -> "+JSONStaticDataFile+"\n")
    #
    #if ConstName is None :
    #  sys.exit("ERROR "+methID+" ConstName is None !\n")
    #
    #if FNodalModAdjInit is None :
    #  sys.exit("ERROR "+methID+" FNodalModAdjInit is None !\n")
    #
    #if ForemanConstituentAstroObjects is None :
    #  sys.exit("ERROR "+methID+" ForemanConstituentAstroObjects is None !\n")

    constituentObj= None

    #--- Get the JSON strings indexing ids from the static parameters data:
    mainConstsId= self.JSON_STATIC_DATA_IDS[self.MAIN_CONST_ID[0]]
    shWatConstsId= self.JSON_STATIC_DATA_IDS[self.SHWT_CONST_ID[0]]

    #--- Check if ConstName is a name of a main constituent:
    if ConstName in tuple(self.staticData[mainConstsId].keys()) :

      #--- Create the new ForemanMainConstituent object for the main constituent:
      constituentObj= ForemanMainConstituent(ConstName, FNodalModAdjInit)

      #--- Always put the main constituents objects at the beginning of
      #    the ForemanConstituentAstroObjects list.
      ForemanConstituentAstroObjects.insert(0,constituentObj)

    #--- Check if ConstName is a name of a shallow water constituent:
    elif ConstName in self.staticData[shWatConstsId].keys() :

      #---  Create the new ForemanShWtConstituent object for the shallow water constituent:
      constituentObj= ForemanShWtConstituent(ConstName, FNodalModAdjInit)

      #--- Always put the shallow water constituents objects at the end of
      #    the ForemanConstituentAstroObjects list.
      ForemanConstituentAstroObjects.append(constituentObj)

    #--- end if-elif block.

    #--- Got an unknown constituent name if constituentObj is None at this point.
    if constituentObj is None :
      sys.exit("ERROR "+methID+" Invalid tidal constituent -> "+ ConstName +" !\n")

    #--- return the ForemanConstituentAstro object to the calling method.
    return constituentObj

  #---
  def setShWtDerivationObjectsRfs(self, ForemanConstituentAstroObjects) :

    """
    Set the right main tidal constituent(s) ForemanConstituentAstro
    objects references in a shallow water constituent data dictionary.

    (NOTE: Each shallow water constituent depends on at least one
    main tidal constituent to set itself up before being used
    for tidal computations).

    ForemanConstituentAstroObjects : A tuple of main and shallow water tidal constituents ForemanConstituentAstro objects.

    """

    ##--- No fool-proof checks here for performance reasons:
    #methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
    #sys.stdout.write("INFO "+methID+" start \n")

    #--- Shortcut to the shallow water JSON format static data:
    shWatConstsStaticData= self.staticData[ self.JSON_STATIC_DATA_IDS[ self.SHWT_CONST_ID[0] ] ]

    #--- loop on all ForemanConstituentAstro objects:
    for fcaObj in ForemanConstituentAstroObjects :

      #--- Get the name of the tidal constituent of
      #    the ForemanConstituentAstro object:
      name= fcaObj.getName()

      #--- Check if name is a name of a shallow water constituent:
      if name in shWatConstsStaticData.keys() :

        #--- Extract the main constituents derivation static data tuple
        #    of this shallow water constituent:
        shWtDrvStaticDataTuple= tuple( shWatConstsStaticData[name][ self.SHWAT_MAIN_CONSTS_DERIV_ID[0] ] )

        #--- Loop on the main constituent(s) static data derivation items:
        for mcDrv in shWtDrvStaticDataTuple :

          #--- The name of a main tidal constituent from which a
          #    shallow water constituent depends:
          mcName= mcDrv[ self.SHWAT_MAIN_CONST_ID[0] ]

          #--- Create a new ForemanMainConstituentDrv object in this
          #    shallow water constituent data dictionary :
          #    (Mote the use of method ForemanConstituentAstro.getObj
          #     to retreive the right main tidal constituent ForemanConstituentAstro object)

          newForemanMainConstituentDrv= \
            ForemanMainConstituentDrv( ForemanConstituentAstro.getObj(mcName, ForemanConstituentAstroObjects), mcDrv[ self.SHWAT_MULT_FACT_ID[0] ] )

          #--- Put the new ForemanMainConstituentDrv object in self.__mcDrv list
          fcaObj.addMcDrv( newForemanMainConstituentDrv )

        #--- end for  mcDrv in shWtDrvStaticData
      #--- end if name in shWatConstsStaticData.keys()
    #--- end def setShWtDerivationObjectsRfs(self,ForemanConstituentAstroObjects)

  #---
  def updateTimeRef(self, TimeIncr, LatitudeInRadians, ForemanConstituentAstroObjects) :

    """
    Selectively update the ForemanConstituentAstro objects astronomic informations
    depending on the time increment which needs to be a multiple of self.ASTRO_UDPATE_OFFSET_SECONDS[0].

    TimeIncr : The new time increment in seconds to use for the update.
    LatitudeInRadians : the latitude in radians to use for the update.
    ForemanConstituentAstroObjects : A tuple of ForemanConstituentAstro objects to update.

    NOTE: *** BEWARE *** The local variable timeRefDiff reset at 0 should be done with a double precision
    integer(a.k.a. long long). It's ok by default in python3 but needs to be 0L in python2

    python3: timeRefDiff= 0
    python2: timeRefDiff= 0L

    We could automatically detect if we are running under python2 or python3 but it could
    slow down the execution.
    """

    #--- No args. validation, need performance here.

    #--- Get the time difference between this object and the
    #    new time increment argument.
    #
    #    NOTE: there is no check if this time difference is
    #          positive for performance reasons but we can
    #          also think that the Foreman algorithm can be
    #          used backward in time.
    timeRefDiff= TimeIncr - self._sse

    #--- Check for the TimeIncr being a multiple of self.ASTRO_UDPATE_OFFSET_SECONDS[0]:
    if int( math.fmod(TimeIncr, self.ASTRO_UDPATE_OFFSET_SECONDS[0]) ) == 0 :
      self.updateAstroObjects(TimeIncr, LatitudeInRadians, ForemanConstituentAstroObjects)

      #--- MUST set timeRefDiff at double precision 0.0 after each astronomic informations update.
      timeRefDiff= self._doublePrecZero

      ##--- If not using self._doublePrecZero attribute
      #if sys.hexversion >= 0x3000000 :
      #  #--- Python3
      #  timeRefDiff= 0
      #else :
      #  #--- Python2
      #  timeRefDiff= 0L

      #--- end inner if-else block.
    #--- end outer if block.

    #--- Return the new time reference difference for the tidal predictions:
    #    NOTE: This is the time that sets the frequency offset for the cosinus
    #          argument in the computation of a new tidal amplitude.
    return timeRefDiff
