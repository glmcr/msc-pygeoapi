#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTObj.py
# Creation        : October/Octobre 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTObj implementation.
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

#--
import os
import sys
import inspect

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTFactory import SFMTFactory
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTModelAttr import SFMTModelAttr

#---
class SFMTObj(SFMTModelAttr) :

  """
  Class used to start the SFMT DHP data crunching production
  with input data coming from a given model results. An object
  instance of this must be created-used from a main python script.
  """

  #---
  def __init__( self,
                MainJsonConfigFile: str,
                MainCfgDir: str = None ) :

    """
    Constructor for class SFMTObj.

    MainJsonConfigFile (type->str): A json format file which
    contains the common config. parameters.

    MainCfgDir (type->str) <OPTIONAL> Default->None :
    DHP package config. directory path.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    sys.stdout.write("INFO "+methId+
                     " start: MainJsonConfigFile="+
                     MainJsonConfigFile+", MainCfgDir="+str(MainCfgDir)+"\n")
    #---

    if MainJsonConfigFile is None :
      sys.exit("ERROR "+methId+" MainJsonConfigFile is None ! \n")

    #: Doc Create the SFMTFactory object that will be used to
    #  start the DHP data crunching.
    sFMTFactoryObj= SFMTFactory(MainJsonConfigFile, MainCfgDir)

    #: Doc Set the SFMTModelAttr super class with newly created
    #      sFMTFactoryObj._s102TilesObj and sFMTFactoryObj
    #      objects for subsequent usage by other classes instances objects.
    SFMTModelAttr.__init__(self, sFMTFactoryObj._s102TilesObj, sFMTFactoryObj)

    sys.stdout.write("INFO "+methId+" end\n")

  #---
  def crunch( self,
              NbMultiProcesses: int = 1,
              OptionalArgs: tuple = None) :
    """
    As its name says: start the SFMT DHP data conversion crunching.

    NbMultiProcesses (type->int) Default==1 : The number of multiprocessing objects to use
    for the possibly parallelized SFMT DHP data outputs.

    OptionalArgs (type->tuple) Default->None : Could have optional args. to deal with.
    (ex. coming from ECCC Maestro oper. env.).
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
    sys.stdout.write("INFO "+methId+" start\n")

    if self._sFMTFactoryObj is None :
      sys.exit("ERROR "+methId+" self._sFMTFactoryObj is None ! \n")

    #: Doc Start the DHP data crunching with method self._sFMTFactoryObj.getProducts
    self._sFMTFactoryObj.getProducts(self, NbMultiProcesses, OptionalArgs)

    sys.stdout.write("INFO "+methId+" end\n")
