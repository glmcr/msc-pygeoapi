#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : dfo msc-pygeoapi process plugins
# File/Fichier    : dfo/tidal/prediction.py
# Creation        : July/Juillet 2020 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dfo.tidal.prediction implementation.
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

#--- Avoid namespace pollution SNAFUs with explicit imports:
from msc_pygeoapi.process.dfo.tidal import (
    _ADHOC_CHARTDATUM_CORR_FACTOR
)

from msc_pygeoapi.process.dfo.util.time_machine import time_machine

#---
class prediction(time_machine) :

  """
  Generic class which must be inherited
  by specific tidal methods classes.
  """

  #---
  def __init__(self) :

    #ITidalPrd.__init__(self)
    time_machine.__init__(self)

    #--- self._astroInfosFactoryObj generic attribute is supposed to become an
    #    AstroInfosFactory  derived type object instance created by specific
    #    tidal methods sub-classes instances.
    self._astroInfosFactoryObj= None

  #---
  @staticmethod
  def getAdHocChartDatumCorrection( WLZAmplitudeStrId: str,
                                    CDCorrFactor: float = _ADHOC_CHARTDATUM_CORR_FACTOR) -> tuple :
    """
    Apply an ad-hoc chart datum correction computed from the water levels
    tidal constituents amplitudes.

    NOTE: This ad-hoc chart datum correction using tidal constituents amplitudes
    is temporary and is supposed to be eventually replaced by a more accurate
    and rigourous procedure.

    WLZAmplitudeStrId : The string key id. to index the WLs tidal
    constiuents amplitudes in PointDataDict.

    CDCorrFactor<OPTIONAL, default== _ADHOC_CHARTDATUM_CORR_FACTOR> :
    A correction factor to apply to the computed ad-hoc CD.

    return a unary tuple which contains the adhoc chart datum correction
    for a grid point.
    """

    #methId= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

    #--- No fool-proof checks her for performance reasons:
    #    Assuming that WLZAmplitudeStrId string identificators
    #    are present in the dictionary keys of PointDataDict

    rgx= re.compile(".*"+WLZAmplitudeStrId[0])
    wlzDataIdsTuple= tuple( filter(rgx.match, PointDataDict.keys()) )

    wlzAmpsAcc= 0.0

    for wlzAmpId in wlzDataIdsTuple :

      wlzAmpsAcc += float(PointDataDict[wlzAmpId])

    #--- NOTE: PointDataDict[ IS104.CHART_DATUM_CONV_ID[0] ] is an unary tuple.
    #PointDataDict[ IS104.CHART_DATUM_CONV_ID[0] ]= ( CDCorrFactor[0] * wlzAmpsAcc ,)

    return ( CDCorrFactor[0] * wlzAmpsAcc ,)

  #---
  def getTilePredictions(self, TidalPrdFactoryObj, TileDict, DateTimeStampsDict) :

    """
    Generic (a.k.a. "abstract") method for computing tidal predictions with tiled data
    to be implemented by sub-classes.

    TODO: Add arguments definitions.
    """

    pass 

  #---
  def validateTidalMethod(self, TidalMethod2Validate) :

    """
    Instance method validateTidalMethod.

    TidalMethod2Validate : A tidal prediction method Id. to validate.
    """

    methId= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

    if TidalMethod2Validate is None :
      sys.exit("ERROR "+methId+" TidalMethod2Validate is None ! \n")

    found= False

    for methodAllowed in _ALLOWED_METHODS:

      if TidalMethod2Validate == methodAllowed : found= True

    if not found :
      sys.stdout.write("WARNING "+methId+" Invalid tidal method -> "+Method2Validate+" !\n")

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
