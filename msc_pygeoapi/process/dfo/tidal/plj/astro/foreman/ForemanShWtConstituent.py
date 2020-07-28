#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/astro/foreman/ForemanShWtConstituent.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.astro.foreman.ForemanShWtConstituent implementation.
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
from msc_pygeoapi.process.dfo.tidal.astro.foreman.ForemanConstituentAstro import ForemanConstituentAstro
from msc_pygeoapi.process.dfo.tidal.astro.foreman.ForemanMainConstituentDrv import ForemanMainConstituentDrv

#---
class ForemanShWtConstituent(IForeman, ForemanConstituentAstro) :

  """
  Class dealing with shallow water tidal constituents(if any) static and dynamic data
  in the context of the Foreman tidal prediction method.
  """

  #---
  def __init__(self, Name= None, FNodalModAdjInit= None) :

    IForeman.__init__(self)
    ForemanConstituentAstro.__init__(self, Name, 0.0, FNodalModAdjInit, 0.0)

    #methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

    #sys.stdout.write("INFO "+methID+" start\n")

    #--- List that will hold the ForemanMainConstituentDrv objects
    #    wrapped in unary tuples.
    self.__mcDrv= []

    #sys.stdout.write("INFO "+methID+" end\n")

  #---
  def addMcDrv(self, ForemanMainConstituentDrvObj) :

    """
    Simple method to add a ForemanMainConstituentDrv object(wrapped in an unary tuple) to the self.__mcDrv list.

    ForemanMainConstituentDrvObj (type->ForemanMainConstituentDrv): The ForemanMainConstituentDrv object to add to the self.__mcDrv list.
    """

    #--- Set the ForemanMainConstituentDrv object as a unary tuple in self.__mcDrv list:
    self.__mcDrv.append( (ForemanMainConstituentDrvObj, ) )

  #---
  def updateAstroData(self, LatitudeinRadians, SMEDataObj, ForemanAstroFactoryObj) :

    """
    Update the astronomic informations of a shallow water constituent.

    LatitudeInRadians (type->float) : The latitude(of a WL station OR a grid point) in radians to use for the update.

    SMEDataObj (type->SunMoonEphemerides) : The SunMoonEphemerides object used to update the astronomic informations
    of the main constituent.

    ForemanAstroFactoryObj (type->ForemanAstroFactory): The ForemanAstroFactory object used to update the astronomic
    informations of the main constituent.
    """

    #--- No args. validation, need performance.

    #--- Uncomment for debugging:
    #methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
    #sys.stdout.write("INFO "+methID+" start, sh. wat. const name="+self._name+"\n")

    #--- Always reset object numeric data:
    self.reset()

    #--- Iterate on all ForemanMainConstituentDrv objects in self.__mcDrv to update this
    #    shallow water constituent astronomic infos. with the already updated astronomic
    #    infos. of the main constituents from which it depends.
    for mcDrv in tuple(self.__mcDrv) :

      mcObj= mcDrv[0]._foremanMainConstituentObjRf
      mcMultFactor= mcDrv[0]._multFactor

      self._tidalFrequency += mcMultFactor*mcObj._tidalFrequency

      self._fNodalModAdj *= math.pow(mcObj._fNodalModAdj, mcMultFactor)

      self._astroArgument += mcMultFactor*mcObj._astroArgument

    #print self.asString()
    #sys.stdout.write("INFO "+methID+" exit 0 \n")
    #sys.exit(0)
    #sys.stdout.write("INFO "+methID+" end,  sh. wat. const name="+self._name+"\n\n")

