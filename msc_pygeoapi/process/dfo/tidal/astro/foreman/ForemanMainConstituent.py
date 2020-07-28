#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/astro/foreman/ForemanMainConstituent.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.astro.foreman.ForemanMainConstituent implementation.
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
from msc_pygeoapi.process.dfo.tidal.astro.foreman.ForemanAstroFactory import ForemanAstroFactory
from msc_pygeoapi.process.dfo.tidal.astro.foreman.ForemanConstituentAstro import ForemanConstituentAstro

#---
class ForemanMainConstituent(IForeman, ForemanConstituentAstro) :

  """
  class dealing with main tidal constituents static and dynamic data
  in the context of the Foreman tidal prediction method.
  """

  #---
  def __init__(self, Name= None, FNodalModAdjInit= None) :

    IForeman.__init__(self)
    ForemanConstituentAstro.__init__(self,Name,0.0,FNodalModAdjInit,0.0)

    #methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
    #sys.stdout.write("INFO "+methID+" start\n")
    #sys.stdout.write("INFO "+methID+" end\n")

  #---
  def updateAstroData(self, LatitudeinRadians, SMEDataObj, ForemanAstroFactoryObj) :

    """
    Update the astronomic informations of a main constituent.

    LatitudeInRadians (type->float): The latitude(of a WL station OR a grid point) in radians to use for the update.

    SMEDataObj (type->SunMoonEphemerides): The SunMoonEphemerides object used to update the astronomic informations
    of the main constituent.

    ForemanAstroFactoryObj (type->ForemanAstroFactory): The ForemanAstroFactory object used to update the astronomic
    informations of the main constituent.
    """

    #--- No args. validation, need performance.

    #--- Uncomment for debugging:
    #methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
    #sys.stdout.write("INFO "+methID+" start, self._name="+self._name+"\n")

    #--- Always reset object numeric data:
    self.reset()

    #--- No args. validation, need performance.
    mainConstStaticDataDict= ForemanAstroFactoryObj.getStaticDataForConst(self._name)

    #--- Extract the Doodson numbers data from MainConstStaticDataDict
    doodsonNumbers= tuple(mainConstStaticDataDict[ self.MAIN_CONST_DOODNUMS_ID[0] ])

    #--- NOTE: self.CYCLES_HOUR_2_RADIANS_SECONDS and self.HOURS_PER_NORMAL_YEAR_INV are both one item tuples.
    freqArgFactor= ( self.CYCLES_HOUR_2_RADIANS_SECONDS[0]*self.HOURS_PER_NORMAL_YEAR_INV[0] ,)

    #--- TODO: Use python lambda stuff here for the following inlined multiplications ??
    #          Possibly slower than this inlining of multiplications ??

    self._tidalFrequency= freqArgFactor[0] * ( doodsonNumbers[0] * SMEDataObj.dTau   +
                                               doodsonNumbers[1] * SMEDataObj.moonDS +
                                               doodsonNumbers[2] * SMEDataObj.sunDH  +
                                               doodsonNumbers[3] * SMEDataObj.moonDP +
                                               doodsonNumbers[4] * SMEDataObj.meanAscModeDNP +
                                               doodsonNumbers[5] * SMEDataObj.sunDPP   )

    #--- M. Foreman's Fortran source code for the V astronomical argument:
    #
    #      dbl=ii(k)*tau+jj(k)*s+kk(k)*h+ll(k)*p+mm(k)*enp+nn(k)*pp+semi(k)
    #
    #     !WITH s,h,p,enp,pp -> SUN MOON EPHEMERIDES
    #     !WITH ii(k),jj(k),kk(k),ll(k),mm(k),nn(k) -> DOODSON NUMBERS FOR CONSTITUENT k
    #     !WITH semi -> PHASE CORRECTION
    #

    #--- TODO: Also use python lambda stuff here for the following inlined multiplications ??:

    self._astroArgument= ( doodsonNumbers[0] * SMEDataObj.tau   +
                           doodsonNumbers[1] * SMEDataObj.moonS +
                           doodsonNumbers[2] * SMEDataObj.sunH  +
                           doodsonNumbers[3] * SMEDataObj.moonP +
                           doodsonNumbers[4] * SMEDataObj.meanAscModeNP +
                           doodsonNumbers[5] * SMEDataObj.sunPP +
                           mainConstStaticDataDict[ self.MAIN_CONST_PHASECORR_ID[0] ] )

    #--- Only the fractional part of vAstro is needed if it is superior to constant int phase threshold.
    self._astroArgument -= ForemanAstroFactoryObj._phaseThreshold[0] * \
                             int( self._astroArgument/ForemanAstroFactoryObj._phaseThreshold[0] )

    #--- Uncomment for debugging:
    #print self.asString()
    #print("self._astroArgument bef. satellites="+str(self._astroArgument))
    #print("self._fNodalModAdj bef. satellites="+str(self._fNodalModAdj))

    #--- Get main constituent satellites data if any.
    satellitesDataTuple= tuple( mainConstStaticDataDict[ self.MAIN_CONST_SATS_ID[0] ] )

    if len(satellitesDataTuple) > 0 :

      #--- Got satellites data to process.
      #    TODO: Use a double item tuple as returned object here ? performance impact ?
      mainCosSinAcc= ForemanAstroFactoryObj.getMainConstCosSinAcc(LatitudeinRadians, SMEDataObj, satellitesDataTuple)

      #print "mainCosSinAcc="+str(mainCosSinAcc)

      #--- Shortcut to the astro parameters static data dictionary:
      astroParamsStaticDataDict= ForemanAstroFactoryObj._staticData[ self.ASTRO_PARAMS_ID[0] ]

      COS_IDX= ( astroParamsStaticDataDict[ self.COS_IDX_ID[0] ] ,)
      SIN_IDX= ( astroParamsStaticDataDict[ self.SIN_IDX_ID[0] ] ,)

      self._fNodalModAdj= \
        math.sqrt(mainCosSinAcc[ COS_IDX[0] ]*mainCosSinAcc[ COS_IDX[0] ] + mainCosSinAcc[ SIN_IDX[0] ]*mainCosSinAcc[ SIN_IDX[0] ])

      self._astroArgument += self.TWO_PI_INV[0]*math.atan2(mainCosSinAcc[ SIN_IDX[0] ], mainCosSinAcc[ COS_IDX[0] ])

    #--- end block if len(satellitesDataTuple) > 0

    #--- Uncomment for debugging:
    #print("self._astroArgument aft. satellites="+str(self._astroArgument))
    #print("self._fNodalModAdj aft. satellites="+str(self._fNodalModAdj))
    #print(self.asString())
    #print(str(self))

    #sys.stdout.write("INFO "+methID+" end\n")

  #--- end block method updateAstroData
