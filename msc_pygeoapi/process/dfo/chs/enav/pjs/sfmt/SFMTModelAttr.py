#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTModelAttr.py
# Creation        : September/Septembre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTModelAttr implementation.
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
class SFMTModelAttr(ISFMT, S102TilesObj) :

  """
  Defines specific SFMTModel attributes.
  """

  #---
  def __init__( self,
                S102Obj: S102,
                SFMTFactoryObj ) :
    """
    S102Obj (type->S102): A S102 class instance object.

    SFMTFactoryObj (type->SFMTFactory): A SFMTFactory class instance object.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    sys.stdout.write("INFO "+methId+" start.\n")

    ISFMT.__init__(self)
    S102TilesObj.__init__(self, S102Obj)

    if SFMTFactoryObj is None :
      sys.exit("ERROR "+methId+" SFMTFactoryObj is None !\n")

    if SFMTFactoryObj._mainOutputDir is None :
      sys.exit("ERROR "+methId+" SFMTFactoryObj._mainOutputDir is None \n")

    if not os.access(SFMTFactoryObj._mainOutputDir, os.F_OK) :
      sys.exit("ERROR "+methId+
               " SFMTFactoryObj._mainOutputDir -> "+
               SFMTFactoryObj._mainOutputDir+" not found !\n")
    #---

    if SFMTFactoryObj._mainStorageDir is None :
      sys.exit("ERROR "+methId+" SFMTFactoryObj._mainStorageDir is None \n")

    if not os.access(SFMTFactoryObj._mainStorageDir, os.F_OK) :
      sys.exit("ERROR "+methId+
               " SFMTFactoryObj._mainStorageDir -> "+
               SFMTFactoryObj._mainStorageDir+" not found !\n")
    #---

    #: Doc Use self._sFMTFactoryObj for subsequent usage by sub-classes.
    self._sFMTFactoryObj= SFMTFactoryObj

    #: Doc Use ISFMT.ALLOWED_DATA_CODING_FMT.three  as the default data coding format.
    self._dataCodingFmt= ISFMT.ALLOWED_DATA_CODING_FMT.three

    #: Doc Define the default number of multiprocessing objects
    #      which is 1 obviously.
    self._nbMultiProcesses= 1

    #: Doc The self._cvd2ChartDatumFile is used for S104 made
    #      with 2D models(like NEMO models) to convert the raw
    #      models WL results to the specific chart datum for
    #      each 2D model valid grid points. It is obviously
    #      not used for models data other than water levels.
    self._cvd2ChartDatumFile= None

    #--- TODO: Test the possibility of using a dictionary of
    #          methods pointers to dispatch the output objects
    #          creations with it instead of using an if-else block

    sys.stdout.write("INFO "+methId+" end\n")
