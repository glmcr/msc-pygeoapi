#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/util/Py2And3.py
# Creation        : April/Avril 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.util.Py2And3 implementation.
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
import inspect

#---
class Py2And3(object) :

  """
  Handle cases where we need to have the same behavior with Python2 and Python3.
  """

  #---
  def __init__(object) :
    pass

  #---
  @staticmethod
  def getASCIIStr(AStr) :

   """
   Get rid of the annoying leading 'b' character prefix if running under Python3.
   """

   ret= str(AStr)

   #: Doc Trick to identify Python3 with sys.hexversion found on stackoverflow again!:
   if sys.hexversion >= 0x3000000 :
     ret= str(AStr,"utf-8")

   return ret


