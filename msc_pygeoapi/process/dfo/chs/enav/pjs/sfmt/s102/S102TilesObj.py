#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : DFO-CHS-ENAV-DHP
# File/Fichier    : dhp/sfmt/s102/S102TilesObj.py
# Creation        : October/Octobre 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s102.S102TilesObj implementation.
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

#--- Built-in module(s).
import os
import sys
import inspect

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.S102 import S102
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.IS102 import IS102

#---
class S102TilesObj(IS102):

  """
  Simple class providing an access to a reference to a S102 object.
  It seems a bit odd but it allows to have a less convoluted inheritance
  flow between SFMTFactory and SFMTModelFactory sub-classes. We can consider
  it as a kind of a wrapper class.
  """

  #---
  def __init__( self,
                S102ObjInst: S102 ):

    """
    S102ObjInst (type->S102): A S102 class instance object.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    sys.stdout.write("INFO "+methId+" start\n")

    IS102.__init__(self)

    self._s102TilesObj= None

    if S102ObjInst is not None :

      #: Doc S102TilesObj should be an instance object of class S102.
      if not isinstance(S102ObjInst, S102) :
        sys.exit("ERROR "+methId+" S102ObjInst is not an instance object of class S102 !\n")
      #--- end inner if block.

      #: Doc Set self._s102TilesObj reference to S102ObjInst
      #  for subsequent usage by sub-classes.
      self.setS102TilesRef(S102ObjInst)

    #--- end outer inner if block.

    sys.stdout.write("INFO "+methId+" end\n")

  #---
  def setS102TilesRef( self,
                       S102ObjInst: S102) :

    """
    S102ObjInst (type->S102): A S102 class instance object.

    Just set the self._s102TilesObj to a valid S102 class instance object.
    """

    if S102ObjInst is None :
      sys.exit("ERROR "+methId+" S102ObjInst is None !\n")

    if not isinstance(S102ObjInst, S102) :
      sys.exit("ERROR "+methId+" S102ObjInst is not an instance object of class S102 !\n")

    self._s102TilesObj= S102ObjInst

    return self
