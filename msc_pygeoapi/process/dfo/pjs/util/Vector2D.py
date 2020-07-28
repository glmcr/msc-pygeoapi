#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/util/Vector2D.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.util.Vector2D implementation.
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
import os
import sys
import math
import inspect

#--- TODO : Add the usual vector operations if needed
#           i.e. dot product, addition, subtraction and so on.
class Vector2D(object) :

  """
    Utility class for 2D vector data.
  """

  def __init__(self) :

    #: Doc 2D vector I(x) and J(y) components:
    self._iComp= self._jComp= 0.0

  #---
  def getIComp(self) :

    return self._iComp

  #---
  def getJComp(self) :

    return self._jComp

  #---
  def set(self, IComp, JComp) :

    """
    Set the 2D vector components:

    IComp (type->float): The I component to set in self.

    JComp (type->float): The J component to set in self.
    """

    self._iComp= IComp
    self._jComp= JComp

    return self

  ##--- Keeping code for possible future usage:
  #def rotateComponentsCounterClockWise(self, CosAngleRot, SinAngleRot) :
  #  tmpIComp= self._iComp
  #  tmpJComp= self._jComp
  #  self._iComp= CosAngleRot*tmpIComp - SinAngleRot*tmpJComp
  #  self._jComp= SinAngleRot*tmpIComp + CosAngleRot*tmpJComp
  #  return self

