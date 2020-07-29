#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/geo/GeoFactory.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.geo.GeoFactory implementation.
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
from msc_pygeoapi.process.dfo.pjs.geo.IGeo import IGeo

#---
class GeoFactory(IGeo) :

  """
  Provide some generic instance methods for the processing of GIS informations-data related
  to the CHS-ENAV SFMT DHP data.
  """

  def __init__(self):

    IGeo.__init__(self)

    self._horizDatumRef= None
    self._horizDatumCode= None

  #---
  def convertDegMinDec2Decimal(self, DegreesMinDecTuple, HemisphereId) :

    """
    Convert an inconvenient-old-school degrees decimal-minutes coordinate
    value (e.g. 50 13.0000N  66 24.0000W) to a more convenient decimal degrees
    coordinate value ( e.g. 50.217, -66.400 )

    DegreesMinDecTuple (type->tuple): A tuple holding the degrees part(string or float)
    of a decimal-minutes coordinate value(e.g. 50) and the decimal-minutes part(string
    or float) of a decimal-minutes coordinate value (e.g. 13.0000)

    HemisphereId (type->string): The letter(as a string) which represent the hemisphere
    of the old-school degrees decimal-minutes coordinate value ( "W", "E", "S" or "N")
 
    return (type->float): The decimal degrees representation of the degrees decimal-
    minutes input.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    if DegreesMinDecTuple is None :
      sys.exit("ERROR "+methID+" DegreesMinDecTuple is None !\n")

    if HemisphereId is None :
      sys.exit("ERROR "+methID+" HemisphereId is None !\n")

    if len(DegreesMinDecTuple) != 2 :
      sys.exit("ERROR "+methID+" len(DegreesMinDecTuple) != 2 !\n")

    if HemisphereId not in self.ALLOWED_HEMI_IDS :
      sys.exit("ERROR "+methID+" Invalid hemisphere id. -> "+HemisphereId+" !\n")

    #: Doc Need float values(in cases where DegreesMinDecTuple contents are strings)
    decimaldegrees= float(DegreesMinDecTuple[0]) + float(DegreesMinDecTuple[1])/self.MINUTES_PER_HOUR[0]

    #: Doc Deal with East or South hemispheres
    #: (i.e. decimaldegrees is < 0 for a Western longitude or a Southern latitude):
    if HemisphereId == self.WEST_HEMI_ID[0] or HemisphereId == self.SOUTH_HEMI_ID[0] :
      decimaldegrees = -decimaldegrees

    return decimaldegrees

  #---
  def insideTwoPointsBoundingBox(self, PointLat, PointLon, TwoPointsBBoxTuple) :

    """
    Check if a lat-lon coordinates combo of a 2D grid point is inside a regular
    cartesian lat-lon bounding box (using only the SW and NE corners of
    the bounding box).

    PointLat (type->float): The latitude(float format) of the 2D grid point to check.

    PointLon (type->float): The longitude(float format) of the 2D grid point to check.

    TwoPointsBBoxTuple (type->tuple): A tuple holding the SW and the NE lat-lon
    coordinates combos of just one cartesian regular bounding box.

    return (type->boolean): True if the point is inside the cartesian regular
    bounding box False otherwise.

    NOTE: No validation for the arguments i.e. assuming that PointLat, PointLon arguments
    are floats and are inside the normal geographical extremums limits +-90, +-180 and 
    assuming that the bounding box coordinates are using the same CRS(Common Reference 
    System a.k.a CRS or SRS) which is EPSG:4326 normally.
    """

    return PointLat > TwoPointsBBoxTuple[ self.TWO_POINTS_BBOX_LAT_MIN[0] ]         \
             and PointLat < TwoPointsBBoxTuple[ self.TWO_POINTS_BBOX_LAT_MAX[0] ]   \
               and PointLon > TwoPointsBBoxTuple[ self.TWO_POINTS_BBOX_LON_MIN[0] ] \
                 and PointLon < TwoPointsBBoxTuple[ self.TWO_POINTS_BBOX_LON_MAX[0] ]

  #---
  def validateOGRLayerSRS(self, OGRLayer) :

    """
    Verify that an OGR class object instance have the right SRS(a.k.a CRS)
    to avoid some awkward-hard-to-debug-SNAFUs inconsistencies for GIS data
    processing related to CHS-ENAV SFMT DHP data.

    OGRLayer (type->ogr.Layer): An OGR Layer class object instance.
    (https://gdal.org/python/osgeo.ogr.Layer-class.html)
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    if OGRLayer is None :
      sys.exit("ERROR "+methID+" OGRLayer is None !\n")
    #---

    #: Doc Get the spatial reference(horiz. datum ref.) from
    #: the OGR class object instance:
    spatialRef= OGRLayer.GetSpatialRef()

    if spatialRef is None :
      sys.exit("ERROR "+methID+" spatialRef is None !\n")
    #---

    #: Doc ESRI SHAPEFILE EPSG stuff not always explicitly defined
    #: so use AutoIdentifyEPSG() on the OGRSpatialReference object
    #: to be sure we do things right here.
    spatialRef.AutoIdentifyEPSG()

    #--- AUTH name: (EPSG normally)
    authName= spatialRef.GetAuthorityName(None)

    #print "authName="+str(authName)

    if authName is None :
      sys.exit("ERROR "+methID+" authName is None !\n")
    #---

    valid= False

    #: Doc Validate the spatial reference which should be
    #: defined in self.ALLOWED_HORIZ_DATUMS dictionary:
    for allowedAuthName in tuple(self.ALLOWED_HORIZ_DATUMS.keys()) :

      if authName == allowedAuthName :
        self._HorizDatumRef= ( authName ,)
        valid= True
        break
      #--- end if block,

    #--- end for loop block.

    if not valid :
      sys.exit("ERROR "+methID+" Invalid horizontal datum reference -> "+
               authName+" Must be one of -> "+str(self.ALLOWED_HORIZ_DATUMS.keys())+" !\n")
    else :
      sys.stdout.write("INFO "+methID+
                       " Will use horizontal datum reference -> "+ self._horizDatumRef[0] + "\n")
    #--- end if-else block.

    #: Doc Validate the spatial reference code (e.g. 4326.
    codeRead= spatialRef.GetAuthorityCode(None)

    if codeRead is None :
      sys.exit("ERROR "+methID+" codeRead is None !\n")
    #---

    valid= False

    #: Doc Check spatial reference code validity.
    for allowedCode in tuple(self.ALLOWED_HORIZ_DATUMS[ self._horizDatumRef[0] ]) :

      if codeRead == allowedCode :
        self._horizDatumCode= ( codeRead ,)
        valid= True
        break
      #--- end if block,

    #--- end for loop block.

    if not valid :
      sys.exit("ERROR "+methID+" Invalid horizontal datum reference code -> "+codeRead+
               " Must be one of -> "+str(self.ALLOWED_HORIZ_DATUMS[ self._horizDatumRef[0] ].keys())+" !\n")
    else :
      sys.stdout.write("INFO "+methID+" Will use horizontal datum code -> "+ self._horizDatumCode[0] +"\n")
    #--- end if-else block.

  #---
  def withinLayerExtent(self, OGRLayer, PointLat, PointLon) :

    """
    Verify if a 2D grid point is included in an OGR(vector) layer.

    OGRLayer (type->ogr.Layer): The OGR Layer class https://gdal.org/python/osgeo.ogr.Layer-class.html object
    instance to use to check if the 2D grid point is included in it. (NOTE: OGRLayer is the python object
    returned by the method GetLayerByName of the GDAL osgeo.ogr python module 
    https://gdal.org/python/osgeo.ogr.DataSource-class.html#GetLayerByName).

    PointLat (type->float): The latitude(float format) of the 2D grid point to check.

    PointLon (type->float): The longitude(float format) of the 2D grid point to check.

    return (type->boolean): True if the point is included in the OGRLayer object instance or False otherwise.

    NOTE: No validation for the arguments i.e. assuming that PointLat, PointLon arguments are inside the
    normal geographical extremums limits +-90, +-180 and assuming that the bounding box coordinates are
    using the same CRS(Common Reference System a.k.a CRS or SRS) which is the EPSG:4326 normally.
    """

    #: Doc Get the list of the lat-lon extremums of the OGR Layer object:
    layerExtent= OGRLayer.GetExtent()

    #--- NOTE: Using >= and <= here:
    return ( PointLat >= layerExtent[2] and PointLat <= layerExtent[3] \
             and PointLon >= layerExtent[0] and PointLon <= layerExtent[1] )
