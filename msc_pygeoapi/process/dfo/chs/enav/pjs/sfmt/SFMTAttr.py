#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTAttr.py
# Creation        : September/Septembre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTAttr implementation.
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
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.S102 import S102
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.S102TilesObj import S102TilesObj

#---
class SFMTAttr(ISFMT, S102TilesObj) :

  """
  Declare SFMT DHP common attributes used
  by S<NNN> sub-classes(except S102).
  """

  #---
  def __init__( self,
                S102Obj: S102) :

    """
    S102Obj (type->S102): A S102 class instance object.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    sys.stdout.write("INFO "+methId+" start\n")

    ISFMT.__init__(self)
    S102TilesObj.__init__(self, S102Obj)

    #: Doc (type->int): The number of data points
    #      contained in a given DHP data tile.
    self._nbPoints= None

    #: Doc (type->string): The geographic string identifier
    #      (the name of a tile normally) for the HDF5 fileroot group.
    self._geoStrId= None

    #: Doc (type->string): The output directory where to write
    #      the S104 products.
    self._outputDir= None

    #: Doc (type->int): The time interval in seconds between two
    #      successive timestamps of the input data timestamps.
    self._timeIncrInterval= None

    #: Doc (type->dictionary): A dictionary holding DH
    #      product model results data points.
    self._pointsDataOutDict= None

    #: Doc (type->tuple): Tuple holding the keys of
    #      the self._pointsDataOutDict dictionary.
    self._pointsDataOutKeysTuple= None

    sys.stdout.write("INFO "+methId+" end\n")
