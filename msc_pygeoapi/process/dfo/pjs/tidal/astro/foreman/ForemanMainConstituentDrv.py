#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/astro/foreman/ForemanMainConstituentDrv
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.astro.foreman.ForemanMainConstituentDrv implementation.
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
##==============================================================================

#---
import os
import sys
import inspect

#---
from msc_pygeoapi.process.dfo.tidalprd.astro.foreman.IForeman import IForeman

#---
class ForemanMainConstituentDrv(IForeman) :

  """
  Small class for storing main constitents static satellites derivation data.

  Used by ForemanShWtConstituent objects in the specific updateAstroData method
  of this class.

  TODO: Check if we can use a python dictionary to do the job.
  """

  #---
  def __init__(self, ForemanMainConstituentObjRf, MultFactor) :

    """
    ForemanMainConstituentObjRf: Reference to an already existing ForemanMainConstituent object:
    MultFactor : The Multiplicative factor to apply to the satellite data of the ForemanMainConstituent object:
    """

    IForeman.__init__(self)

    #--- Reference to an already existing ForemanMainConstituent object:
    self._foremanMainConstituentObjRf= ForemanMainConstituentObjRf

    #--- The Multiplicative factor to apply to the data of the ForemanMainConstituent object:
    self._multFactor= MultFactor
