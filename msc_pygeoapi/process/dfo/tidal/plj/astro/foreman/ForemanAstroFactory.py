#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/astro/foreman/ForemanAstroFactory.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.astro.foreman.ForemanAstroFactory implementation.
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
from msc_pygeoapi.process.dfo.tidal.astro.foreman.IForeman import IForeman
from msc_pygeoapi.process.dfo.tidal.astro.AstroInfosFactory import AstroInfosFactory
from msc_pygeoapi.process.dfo.tidal.astro.foreman.ForemanConstituentAstro import ForemanConstituentAstro

#---
class ForemanAstroFactory(IForeman, AstroInfosFactory) :

  """
  Class dealing with astronomic informations in the
  context of the Foreman tidal prediction method
  and also used to try to get a better modularization
  of the code.
  """

  def __init__( self,
                SecondsSinceEpochStart,
                SecondsSinceEpochEnd,
                TimeIncrSeconds= None ) :

    IForeman.__init__(self)
    AstroInfosFactory.__init__( self,
                                SecondsSinceEpochStart,
                                SecondsSinceEpochEnd,
                                TimeIncrSeconds )

    #---
    self._SMEData= {}
    self._staticData= None
    self._phaseThreshold= None

    #---
    self._doublePrecZero= 0

    #--- Check for Python2 interpreter:
    if sys.hexversion < 0x3000000 :

      #--- Need to use long(0) for Python2
      self._doublePrecZero= long(0)
    #---

  #---
  def getMainConstCosSinAcc( self,
                             LatitudeInRadians,
                             SunMoonEphemeridesObj,
                             SatellitesDataTuple ) :
    """
    Instance method which computes the astronomic
    lunar nodal modulation adjustment(correction)
    factor for a main tidal constituent.

    LatitudeInRadians : Latitude in radians of a given
    location(a WL station OR a grid point).

    SunMoonEphemeridesObj : An already set SunMoonEphemerides
    object used(but not modified) in the computations.

    SatellitesDataTuple : A tuple of a Main constituent
    satellites static data.

    REMARK: No arguments validation, need performance.
    """

    #--- No args. validation, need performance:

    #--- Uncomment for debugging:
    #methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

    #--- Shortcut to the astro parameters static data dictionary:
    astroParamsStaticDataDict= self._staticData[ self.ASTRO_PARAMS_ID[0] ]

    #--- Local cos,sim array constant indices:
    COS_IDX= ( astroParamsStaticDataDict[ self.COS_IDX_ID[0] ] ,)
    SIN_IDX= ( astroParamsStaticDataDict[ self.SIN_IDX_ID[0] ] ,)

    #--- Accumulators which will be returned by the method:
    cosSinAcc= [ astroParamsStaticDataDict[ self.COS_ACC_INIT_ID[0] ],
                 astroParamsStaticDataDict[ self.SIN_ACC_INIT_ID[0] ] ]

    #--- Use unary tuples for sinLatRad and adj1Fact which must stay constant after being set:
    sinLatRad= ( math.sin(LatitudeInRadians), )
    adj1Fact= ( (1.0 - 5.0 * sinLatRad[0] * sinLatRad[0])/sinLatRad[0], )

    #--- Shortcuts to the FV_NODAL_ADJ static parameters data:
    FV_NODAL_ADJ_FLAGSTuple= tuple( astroParamsStaticDataDict[ self.FV_NODAL_ADJ_FLAGS_ID[0] ] )
    FV_NODAL_ADJ_CONSTANTSTuple= tuple( astroParamsStaticDataDict[ self.FV_NODAL_ADJ_CONSTANTS_ID[0] ] )

    #--- Loop on the satellites static data for a main constituent:
    for satellite in SatellitesDataTuple :

      doodsonNumChangesTuple= tuple( satellite[ self.SAT_DOODNUM_CHANGES_ID[0] ] )

      cosSinArg= satellite[ self.SAT_PHASECORR_ID[0] ] + \
                 doodsonNumChangesTuple[0] * SunMoonEphemeridesObj.moonP + \
                 doodsonNumChangesTuple[1] * SunMoonEphemeridesObj.meanAscModeNP + doodsonNumChangesTuple[2]*SunMoonEphemeridesObj.sunPP

      #--- Need only the decimal part of cosSinArg to be multiplied by self.TWO_PI[0]:
      cosSinArg= self.TWO_PI[0] * (cosSinArg - int(cosSinArg))

      #---
      amplitudeRatioFlag= satellite[ self.SAT_AMP_RATIO_FLAG_ID[0] ]

      #--- Default value for cosSinFact:
      cosSinFact= satellite[ self.SAT_AMP_RATIO_ID[0] ]

      #print "amplitudeRatioFlag="+str(amplitudeRatioFlag)
      #print "cosSinFact 1="+str(cosSinFact)
      #print "FV_NODAL_ADJ_FLAGSTuple="+str(FV_NODAL_ADJ_FLAGSTuple)

      adjFactor= 1.0

      if amplitudeRatioFlag > 0 :

        if amplitudeRatioFlag == 1 :
          adjFactor *= adj1Fact[0] * FV_NODAL_ADJ_CONSTANTSTuple[1]
        else :
          adjFactor *= sinLatRad[0] * FV_NODAL_ADJ_CONSTANTSTuple[2]

        #--- end inner if block.
      #--- end outer if block.

      cosSinFact *= adjFactor

      #--- M. Foreman's Fortran source code for cos,sin accumulators :
      #
      #    sumc=sumc+rr*cos(uu*twopi)
      #    sums=sums+rr*sin(uu*twopi)
      #

      #print "cosSinFact 2="+str(cosSinFact)
      #print "cosSinArg= "+str(cosSinArg)+"\n"

      #--- Fill-up the cos,sin accumulators :
      cosSinAcc[ COS_IDX[0] ] += cosSinFact * math.cos(cosSinArg)
      cosSinAcc[ SIN_IDX[0] ] += cosSinFact * math.sin(cosSinArg)

    #--- Return the cos,sin accumulators to the calling method.
    return tuple(cosSinAcc)

  #---
  def getStaticDataForConst(self, ConstName) :

    """
    Extract the static data from the self.staticData dictionary retreived from the JSON formatted file.

    ConstName : The name(String) of the constituent.
    """

    #--- Uncomment for debugging:
    #methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
    #if self.staticData is None :
    #  sys.stderr.write("ERROR "+methID+" self.staticData is None !\n")
    #  sys.exit(1)

    constDataRet= None

    mainConstsId= self.JSON_STATIC_DATA_IDS[ self.MAIN_CONST_ID[0] ]
    shWatConstsId= self.JSON_STATIC_DATA_IDS[ self.SHWT_CONST_ID[0] ]

    if ConstName in self._staticData[mainConstsId] :
      constDataRet= self._staticData[mainConstsId][ConstName]

    elif ConstName in self._staticData[shWatConstsId] :
      constDataRet= self._staticData[shWatConstsId][ConstName]

    #--- end if-elif block.

    #--- constDataRet must be not None at this point otherwise we have a SNAFU.
    if constDataRet is None :
      sys.exit("ERROR "+methID+" Invalid tidal constituent -> "+ ConstName +" !\n")

    return constDataRet

  #---
  def updateAstroObjects(self, TimeIncr, LatitudeInRadians, ForemanConstituentAstroObjects) :

    """
    Update the astronomic informations ForemanConstituentAstro objects with a new time increment.

    TimeIncr : The new time increment in seconds to use for the update.
    LatitudeInRadians : The latitude(of a WL station OR a grid point) in radians to use for the update.
    ForemanConstituentAstroObjects : A tuple of ForemanConstituentAstro objects to update.
    """

    #--- No args. validation, need performance here.

    for fcaObj in ForemanConstituentAstroObjects :

      #print("name="+fcaObj.getName())

      #--- NOTE: Polymorphic object call here since main and shallow water
      #          constituents astro. infos. update methods are different.
      fcaObj.updateAstroData( LatitudeInRadians, self._SMEData[TimeIncr], self)

    #--- Set self._sse to the time increment used for the update:
    self._sse= TimeIncr

    #--- ForemanConstituentAstro.applyZero2PISandwich static method must
    #    always be applied immediately after the fcaObj.updateAstroData
    #    method have itself been used for all ForemanConstituentAstro objects:

    ForemanConstituentAstro.applyZero2PISandwich(ForemanConstituentAstroObjects)

  ##--- Keep for possible future usage:
  #def getMainConstTidalFrequency(self, SMEDataObj, DoodsonNumbers) :
  #
  #  #--- Uncomment for debugging:
  #  #methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
  #  #if SMEDataObj is None :
  #  #  sys.exit("ERROR "+methID+" SMEDataObj is None !\n")
  #
  #  return ( DoodsonNumbers[0] * SMEDataObj.dtau   +
  #           DoodsonNumbers[1] * SMEDataObj.moonDS +
  #           DoodsonNumbers[2] * SMEDataObj.sunDH  +
  #           DoodsonNumbers[3] * SMEDataObj.moonDP         +
  #           DoodsonNumbers[4] * SMEDataObj.meanAscModeDNP +
  #           DoodsonNumbers[5] * SMEDataObj.sunDPP          ) * self.HOURS_PER_NORMAL_YEAR_INV
