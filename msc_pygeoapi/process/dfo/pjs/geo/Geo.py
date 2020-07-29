#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/geo/Geo.py
# Creation        : November/Novembre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.geo.Geo implementation.
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
import inspect

#--- 3rd party numpy package:
import numpy

#---
from msc_pygeoapi.process.dfo.pjs.geo.IGeo import IGeo
from msc_pygeoapi.process.dfo.pjs.geo.GeoFactory import GeoFactory

#---
class Geo(GeoFactory) :

  """
  Provide some generic methods for the processing of GIS informations-data related
  to the CHS-ENAV SFMT DHP data.
  """

  def __init__(self) :

    GeoFactory.__init__(self)

  #---
  def getDecimalCoordinate(self, DegreesStr, DecMinValHemiStr) :

    """
    Convert an inconvenient-old-school degrees decimal-minutes
    coordinate value (e.g. 69 24.0000W) to a more convenient
    decimal degrees coordinate value ( e.g. -69.400 )

    DegreesStr (type->string): The degrees part(string for now) of a decimal-minutes coordinate value(e.g. 69).

    DecMinValHemiStr (type->string): The decimal-minutes part(string for now) of a decimal-minutes coordinate value (e.g. 24.0000W).

    return (type->float): The decimal degrees representation of the degrees decimal-minutes input.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    if DegreesStr is None :
      sys.exit("ERROR "+methId+" DegreesStr is None \n")

    if DecMinValHemiStr is None :
      sys.exit("ERROR "+methId+" DecMinValHemiStr is None \n")

    #: Doc Extract the minutes decimals from its string definition which have the
    #: hemisphere flag glued at the end of the string.
    decMinVal= float( DecMinValHemiStr[:len(DecMinValHemiStr)-1] )

    #: Doc Now get the hemisphere flag glued at the end of the string.
    decMinHemiStr= DecMinValHemiStr[ len(DecMinValHemiStr)-1 ]

    #: Doc Get a tuple holding the degrees(numeric float) value part and the numeric values of the minutes decimal.
    decMinLatTuple= ( float(DegreesStr), decMinVal )

    #: Doc The rest of the conversion is done by the inherited method convertDegMinDec2Decimal from super class GeoFactory:
    return self.convertDegMinDec2Decimal( decMinLatTuple, decMinHemiStr )

  #---
  @staticmethod
  def getWestHemi2DLongitudes(LonValues) :

    """
    Convert longitudes data values to the [-180,180] bracket format
    (i.e. W-E hemispheres) from the [0,360] bracket format.

    LonValues (type->float) : numpy array of [0,360] bracket format longitudes.

    return (type->float): numpy array of [-180,180] bracket format longitudes
    converted from LonValues argument.
    """

    lonValuesWH= numpy.zeros((LonValues.shape[0], LonValues.shape[1]))

    lonValuesWH= LonValues[:,:] - 360.0

    return lonValuesWH

  #---
  def needToExcludePoint(self, PointLat, PointLon, TwoPointsBBoxesTuple) :

    """
    Check if a lat-lon coordinates combo of a point is inside a regular
    cartesian lat-lon exclusion bounding box (using only the SW and NE
    corners of the bounding box).

    PointLat (type->float): The latitude of the point to exclude(or not).

    PointLon (type->float): The longitude of the point to exclude(or not).

    TwoPointsBBoxesTuple (type->tuple): A tuple holding the South-West and 
    the North-East lat-lon coordinates combos of some (at least one) regular
    cartesian bounding box(es).

    return (type->boolean): True if the point is inside one of the bounding 
    boxes to signal to the calling method that the point need to be excluded.
    False otherwise meaning that the point is not to be excluded.

    NOTE: No validation for the arguments i.e. assuming that PointLat, PointLon
    arguments are indeed of float type and are inside the normal geographical
    extremums limits +-90, +-180 and assuming that the bounding box coordinates
    are using the  same CRS(Common Reference System a.k.a CRS or SRS) which is 
    EPSG:4326 normally.
    """

    excludePoint= False

    #: Doc Loop on all the bounding boxe(s) of the TwoPointsBBoxesTuple
    for bBoxList in TwoPointsBBoxesTuple :

      #: Doc NOTE: insideTwoPointsBoundingBox method is inherited from GeoFactory class:
      if self.insideTwoPointsBoundingBox(PointLat, PointLon, tuple(bBoxList) ) :

        excludePoint= True
        break

      #--- End if block.
    #--- End for loop block

    #: Doc Return the boolean verdict to the calling method.
    return excludePoint
