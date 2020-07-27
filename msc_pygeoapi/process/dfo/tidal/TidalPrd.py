#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/TidalPrd.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.TidalPrd implementation.
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
import re #--- Regular expressions module
import sys

#---
#from msc_pygeoapi.process.dfo.chs.ICHS import ICHS
from msc_pygeoapi.process.dfo.chs import _CHART_DATUM_CONV_ID
from msc_pygeoapi.process.dfo.tidal.ITidalPrd import ITidalPrd
from msc_pygeoapi.process.dfo.util.TimeMachine import TimeMachine

#----
class TidalPrd(ITidalPrd, TimeMachine) :

  """
  Generic class which must be sub-classed by specific tidal methods classes.
  """

  #---
  def __init__(self) :

    ITidalPrd.__init__(self)
    TimeMachine.__init__(self)

    #--- self.astroInfosFactoryObj generic attribute is supposed to become an
    #    AstroInfosFactory  derived type object instance created by specific
    #    tidal methods sub-classes instances.
    self.astroInfosFactoryObj= None

  #---
  def getTilePredictions( self,
                          TidalPrdFactoryObj,
                          TileDict,
                          DateTimeStampsDict ):
    """
    Generic (a.k.a. "abstract") method for computing
    tidal predictions with tiled data to be implemented
    by sub-classes.

    TODO: Add arguments definitions.
    """

    pass 

  #---
  def validateTidalMethod( self,
                           TidalMethod2Validate) -> bool :

    """
    Instance method validateTidalMethod.

    TidalMethod2Validate (str or enum ??) : A tidal prediction
    method Id. to validate.
    """

    methId= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

    if TidalMethod2Validate is None :
      sys.exit("ERROR "+methId+" TidalMethod2Validate is None ! \n")

    found= False

    for methodAllowed in self.ALLOWED_METHODS:

      if TidalMethod2Validate == methodAllowed : found= True

    if not found :
      sys.stdout.write("WARNING "+methId+
                       " Invalid tidal method -> "+Method2Validate+" !\n")

    return found

  #--- Keep the following method for possible future usage
  ##---
  #def computeTidalPrediction(TimeStampSeconds) :
  #  """
  #    Abstract(A la Java, or virtual in C++ world) method that can be overriden by sub classes.
  #
  #  TimeStampSeconds: A timestamp in seconds since the epoch where we want a single tidal prediction.
  #  """
  #  pass

  #--- Keep for possible future usage
  #def setAstroInfos(self, TidalMethodId, LatitudeInRadians,
  #                  StartTimeSeconds, ConstituentsNamesTuple) :
  #  """
  #    Instance method setAstroInfos. Sub-classes should override this method to implement
  #  specific tidal prediction calculations.
  #
  #  MethodId : The tidal prediction method to use.
  #  LatitudeInRadians : Latitude(in radians) of the point(or average latitude of a region) where we want tidal predictions.
  #  StartTimeSeconds : Time-stamp in seconds since the epoch for the time reference used for initial astronomic arguments computations.
  #  ConstituentsNamesTuple : A tuple of tidal constituents names and data to use for the tidal predictions.
  #  """
  #  methId= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
  #  sys.stdout.write("INFO "+methId+" start\n")
  #  #--- The usual fool-proof checks:
  #  if ConstituentsNamesTuples is None :
  #    sys.stderr.write("ERROR "+methId+" ConstituentsNamesTuples is None ! \n")
  #    sys.exit(1)
  #  if len(ConstituentsNamesTuples) == 0 :
  #    sys.stderr.write("ERROR "+methId+" ConstituentsNamesTuples is empty ! \n")
  #    sys.exit(1)
  #  if not self.validateMethod(TidalMethodId) :
  #    sys.stderr.write("ERROR "+methId+" Invalid tidal method -> "+TidalMethodId+" !\n")
  #    sys.exit(1)
  #   #--- Create the AstroInfosFactoryyObj according to the method wanted:
  #  if TidalMethodId == ITidalPrd.METHODS.FOREMAN :
  #    sys.stdout.write("INFO "+methId+" Will use ->"+self.METHODS.FOREMAN.name+" tidal prediction method\n")
  #
  #sys.stdout.write("INFO "+methId+" end\n")
