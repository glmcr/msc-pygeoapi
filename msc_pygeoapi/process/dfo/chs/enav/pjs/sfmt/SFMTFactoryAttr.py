#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTFactoryAttr.py
# Creation        : September/Septembre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTFactoryAttr implementation.
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
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s102.S102 import S102
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTAttr import SFMTAttr

#---
class SFMTFactoryAttr(SFMTAttr) :

  """
  Class inherited by S<NNN> sub-classes(except S102).
  Declare common attributes used by S<NNN> sub-classes.
  """

  #---
  def __init__( self,
                S102Obj: S102) :

    """
    S102Obj (type->S102): A S102 class instance object.
    """

    #---
    SFMTAttr.__init__(self, S102Obj)

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    sys.stdout.write("INFO "+methId+" start\n")

    #: Doc S104 output object.
    self._s104Obj= None

    #: Doc S111 output object.
    self._s111Obj= None

    self._mainCfgDir= None

    #: Doc The path of the model data input directory.
    self._inputDataDir= None

    #: Doc The path of the main output directory.
    self._mainOutputDir= None

    #: Doc The path of the temporary storage directory.
    self._mainStorageDir= None

    #: Doc The input data type used.
    self._inputDataType= None

    #--- 20200723: self._prodJsonCfgFile attribute
    #              seems to be useless now.
    #    TODO: Remove the following if block when it is sure that
    #          it is indeed useless.
    #
    ##: Doc The specific config. input json file for the wanted product.
    #self._prodJsonCfgFile= None

    #: Doc Alternate output files format(not used for now).
    self._altOutputFormat= None

    #: Doc The path of the specific ECCC Maestro config. directory
    self._maestroCfgDir= None

    #: Doc The config. input dictionary (normally)read from the config. input json file.
    self._inputDataCfgDict= None

    #: Doc Could have a specific input data conversion(ex. m/s to knots for the currents
    #  or chart datum conversion) to do for the DH products.
    self._applyConversion= None

    ##: Doc Holds a list of S102 tiles bounding boxe input files.
    #self._s102TilesBBoxFiles= None

    #: Doc Need to keep track if the code runs under an ECCC Maestro sequencer instance.
    self._ecccMaestroInstance= None

    #: Doc Default minimum number of data points for a S111 and-or 2D S104 tile to be produced:
    #:
    #: NOTE 1: Could be overriden by JSON config. parameter MinNbOfPointsPerTile if defined
    #: in Main JSON config. file.
    #:
    #: NOTE 2: self.MIN_NB_POINTS is an unary tuple.
    self._minNbPointsPerTile= self.MIN_NB_POINTS

    sys.stdout.write("INFO "+methId+" end\n")
