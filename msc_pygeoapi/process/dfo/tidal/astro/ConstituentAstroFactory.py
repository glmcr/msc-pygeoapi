#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/astro/ConstituentAstroFactory.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.astro.ConstituentAstroFactory implementation.
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
from msc_pygeoapi.process.dfo.tidal.ITidalPrd import ITidalPrd
from msc_pygeoapi.process.dfo.tidal.astro.AstroInfosFactory import AstroInfosFactory

#---
class ConstituentAstroFactory(ITidalPrd) :

  """
  Class ConstituentAstroFactory: Generic super class representing
  one constituent astronomic information object.
  """

  #---
  def __init__(self, Name= None) :

    """
    Name: The name(string) of a specific tidal constituent ex. M2, O1, S2 and so on.
    """

    ITidalPrd.__init__(self)

    self._name= Name

  #---
  def computeTidalAmplitude(self, ConstAmplitude, ConstGreenwichPhaseLag) :

    """
    Abstract instance method computeTidalAmplitude to be implemented by sub-classes:
    """

    pass

  #--- Abstract method computeTidalAmplitude to be implemented by sub-classes:
  def computeTidalAmplitudeAt(self, ConstAmplitude, ConstGreenwichPhaseLag, IncrSeconds) :

    """
    Another abstract instance method computeTidalAmplitude to be implemented by sub-classes:
    """

    pass

  #--- Instance method getName:
  def getName(self) :

    return self._name

  #---
  def reset(self):

    """
    Abstract instance method to be implemented by sub-classes.
    """

    pass

  #---
  def updateAstroData(self, TimeIncr, LatitudeinRadians, SMEDataObj, ConstStaticDataDict) :

    """
    Abstract instance method to be implemented by sub-classes:
    """

    pass

    #methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
    #sys.stdout.write("INFO "+methID+" start\n")
    #sys.stdout.write("INFO "+methID+" end\n")

  ## Keep for possible future usage
  ##--- Instance method setName:
  #def setName(self, Name) :
  #  self._name= Name

  ## Keeping it for possible future usage
  ##---
  #@staticmethod
  #def get(AName, ConstituentAstroFactoryList) :
  #  """
  #  static method get:
  #  AName: The name of a specific tidal constituent ex. M2, O1, S2.
  #  ConstituentAstroFactoryList : A list of ConstituentAstroFactory objects.
  #  return : The ConstituentAstroFactory object wanted if it is found in ConstituentAstroFactoryList, None otherwise.
  #  """
  #  thisMethod= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
  #  #thisMethod= thisClassId+".get"
  #  if AName is None :
  #    sys.exit("ERROR "+thisMethod+" method: AName is None !\n")
  #  if ConstituentAstroFactoryList is None :
  #    sys.exit("ERROR "+thisMethod+" method: ConstituentAstroFactoryList is None !\n")
  #  ret= None
  #  for cfo in ConstituentAstroFactoryList :
  #    if cfo._name == AName :
  #      ret= cfo
  #      break
  #  if ret is None :
  #    sys.exit("ERROR "+thisMethod+" method : invalid tidal constituent name -> " + AName + " !\n")
  #  return ret

  ## Keeping it for possible future usage
  ##--- Class method getSubsetTuple:
  ##
  ##    ConstNamesList: A list of tidal constituents (String) names that we want to validate.
  ##    ValidConstsNamesList: A list of all the valid tidal constituents (String) names.
  ##    ConstituentAstroFactoryStaticSetList : An already existing list of valid ConstituentAstroFactory objects
  ##
  ##    return: A tuple of ConstituentFactory objects which is a subset of the ConstituentFactory objects contained in the ConstituentFactoryStaticSetList
  ##
  #def getSubsetTuple(ConstNamesList, ValidConstsNamesList, ConstituentAstroFactoryStaticSetList) :
  #
  #  thisMethod= thisClassId+".getSubsetTuple"
  #
  #  if ConstNamesList is None :
  #    sys.exit("ERROR "+thisMethod+" method: ConstNamesList is None !\n")
  #
  #  if ValidConstsNamesList is None :
  #    sys.exit("ERROR "+thisMethod+" method: ValidConstsNamesList is None !\n")
  #
  #  if ConstituentAstroFactoryStaticSetList is None :
  #    sys.exit("ERROR "+thisMethod+" method: ConstituentAstroFactoryStaticSetList is None !\n")
  #
  #  if len(ValidConstsNamesList) < len(ConstNamesList) :
  #    sys.exit("ERROR "+thisMethod+
  #             " method: len(ValidConstsNamesList) < len(ConstNamesList) ! ValidConstsNamesList should always be larger than ConstNamesList\n")
  #  #---
  #
  #  tmpList= []
  #
  #  for cn in ConstNamesList :
  #
  #    if not AstroInfos.validateConstName(cn,ValidConstsNamesList) :
  #      sys.exit("ERROR "+thisMethod+" method: Invalid tidal constituent name -> " + cn + " !\n")
  #    #---
  #
  #    for cst in ConstituentAstroFactoryStaticSetList :
  #
  #      if cn == cst.getName() :
  #
  #        tmpList.append(cst)
  #        break
  #
  #  return tuple(tmpList)
