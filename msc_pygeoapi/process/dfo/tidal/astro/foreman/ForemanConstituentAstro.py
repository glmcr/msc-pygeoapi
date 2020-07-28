#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/astro/foreman/ForemanConstituentAstro.py
# Creation        : August/Aout 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.astro.foreman.ForemanConstituentAstro implementation.
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
import sys
import math
import inspect

#---
from msc_pygeoapi.process.dfo.util.Trigonometry import Trigonometry
from msc_pygeoapi.process.dfo.tidal.astro.ConstituentAstroFactory import ConstituentAstroFactory

#---
class ForemanConstituentAstro(ConstituentAstroFactory, Trigonometry) :

  #---
  def __init__(self,Name, TidalFrequency, FNodalModAdj, AstroArgument) :

    Trigonometry.__init__(self)
    ConstituentAstroFactory.__init__(self, Name)

    methId= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

    #--- Usual FP(Fool-Proof) checks.
    if Name is None :
      sys.exit("ERROR "+methId+" Name is None ! \n")

    if TidalFrequency is None :
      sys.exit("ERROR "+methId+" TidalFrequency is None ! \n")

    if FNodalModAdj is None :
      sys.exit("ERROR "+methId+" FNodalModAdj is None ! \n")

    if AstroArgument is None :
      sys.exit("ERROR "+methId+" AstroArgument is None ! \n")

    #--- Need to keep the intial FNodalModAdj in self._fNodalModAdjInit for
    #    a possible subsequent object reset.
    self._fNodalModAdjInit= FNodalModAdj

    self.init(TidalFrequency, FNodalModAdj, AstroArgument)

  #---
  @staticmethod
  def applyZero2PISandwich(ForemanConstituentAstroObjs) :

    """
    Apply the self.getZero2PISandwich method to the astronomical arguments attributes
    of each ForemanConstituentAstro objects contained in a tuple(or list).

    ForemanConstituentAstroObjs : A tuple(or list) of ForemanConstituentAstro objects.

    return ForemanConstituentAstroObjs
    """

    #--- NOTE : No validation done on ForemanConstituentAstroObjs.
    #           We need performance here.

    #--- self.getZero2PiSandwichWithConv method must always be applied after
    #    each individual ForemanConstituentAstro objects update method calls

    for fcObj in ForemanConstituentAstroObjs :
      fcObj._astroArgument= fcObj.getZero2PiSandwichWithConv(fcObj._astroArgument, True)

    return ForemanConstituentAstroObjs

  #---
  def asString(self):

    """
    As the name says, return a string built with this self(object) contents
    """

    return  str(__name__) + ": Name="+ self.getName() + \
            ": self._tidalFrequency="+ str(self._tidalFrequency) + \
            ": self._fNodalModAdj="+ str(self._fNodalModAdj) + \
            ": self._astroArgument="+ str(self._astroArgument)
  #---
  def computeTidalAmplitude(self,ConstAmplitude,ConstGreenwichPhaseLag) :

    """
    Compute the tidal amplitude of a constituent.

    ConstAmplitude: The static amplitude of a constituent.
    ConstGreenwichPhaseLag:  The Greenwich phase lag(Must be in radians)

    return the computed tidal amplitude.
    """

    #--- NOTE : No validation done on arguments.
    #           We need performance here.

    return self._fNodalModAdj * ConstAmplitude * \
           math.cos(self._astroArgument - ConstGreenwichPhaseLag)

  #---
  def computeTidalAmplitudeAt(self, ConstAmplitude, ConstGreenwichPhaseLag, IncrSeconds) :

    """
    Compute the tidal amplitude of a constituent at a time offset since the
    last update of the self._astroArgument.

    ConstAmplitude: The static amplitude of a constituent.
    ConstGreenwichPhaseLag:  The Greenwich phase lag(Must be in radians)
    IncrSeconds : The seconds(in double precision) since the last update of the self._astroArgument.

    return the computed tidal amplitude at the time offset since the last update of the self._astroArgument.
    """

    #--- NOTE : No validation done on arguments.
    #           We need performance here.

    return self._fNodalModAdj * ConstAmplitude * \
           math.cos( (self._astroArgument + IncrSeconds*self._tidalFrequency) - ConstGreenwichPhaseLag)
  #---
  @staticmethod
  def getObj(Name, ForemanConstituentAstroObjects) :

    """
    Return the ForemanConstituentAstro type object that has the string Name
    as an id.

    Name (type->string) : The string id. to search for in the ForemanConstituentAstroObjects tuple(or list)
    ForemanConstituentAstroObjects (type->tuple(or list) : of ForemanConstituentAstro type objects.

    REMARK : No fool proof checks here, need performance.
    """

    retObj= None

    for fcaObj in ForemanConstituentAstroObjects :

      if fcaObj._name == Name :
        retObj= fcaObj
        break

    return retObj

  #---
  def init(self, TidalFrequencyInitVal, FNodalModAdjInitVal, AstroArgumentInitVal) :

    """
    self._tidalFrequency (type->float) : A constituent tidal frequency IN RADIANS/SECONDS.
    """

    self._tidalFrequency= TidalFrequencyInitVal

    """
    self._astroArgument (type->float) : It is the astronomical argument (named "v" in Foreman's Fortran src code,
    named "Vj" in his documents) adjustment for phase PLUS the nodal modulation adjustment factor for phase
    (named "u" in Foreman's Fortran src code, named "uj" in his documents). MUST be in radians.
    """

    self._astroArgument= AstroArgumentInitVal

    """
    self._fNodalModAdj (type->float ?) : It is the dimensionless nodal modulation adjustment factor for amplitude
    ( named "f" in Foreman's Fortran src code, named fj in his documents ).
    """

    self._fNodalModAdj= FNodalModAdjInitVal;

  #---
  def reset(self) :

    self.init(0.0, self._fNodalModAdjInit, 0.0)

  #--- Abstract method to be implemented by sub-classes:
  def updateAstroData(self, LatitudeinRadians, SMEDataObj, ForemanAstroFactoryObj) :

    pass

    #methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
