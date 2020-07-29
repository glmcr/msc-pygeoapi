#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/geo/GeoLandWaterMasks.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.geo.GeoLandWaterMasks implementation.
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

#--- 3rd party ogr module from gdal osgeo python bundle:
from osgeo import ogr

#---
from msc_pygeoapi.process.dfo.pjs.geo.GeoFactory import GeoFactory
from msc_pygeoapi.process.dfo.pjs.geo.IGeoLandWaterMasks import IGeoLandWaterMasks

#---
class GeoLandWaterMasks(IGeoLandWaterMasks, GeoFactory) :

  """
  Class dealing with the usage of geo-referenced land-water masks polygons
  for the CHS-ENAV SFMT DHP data in canadian coastal and inland waters.
  """

  #---
  def __init__(self, CanCoastLinesLandDataDir,
               CanCoastLinesLandFilesTuple, FileFormat= None) :
    """
    Create a new GeoLandWaterMasks object instance.

    CanCoastLinesLandDataDir (type->string): The parent directory where to find the
    land-water masks input file(s).

    CanCoastLinesLandFilesTuple (type->tuple): A tuple holding the land-water masks
    input file(s) name(s).

    FileFormat (type->string) <OPTIONAL> Default->None: The land-weater file format
    to use. If None then it is assumed that it is the ESRI_SHAPEFILE format.
    """

    GeoFactory.__init__(self)
    IGeoLandWaterMasks.__init__(self)

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methID+
                     " Start, CanCoastLinesLandFilesTuple="+str(CanCoastLinesLandFilesTuple)+"\n")

    if CanCoastLinesLandDataDir is None :
      sys.exit("ERROR "+methID+" CanCoastLinesLandDataDir is None !\n")
    #---

    #: Doc Check if parent directory exists and is readable:
    if not os.access(CanCoastLinesLandDataDir, os.F_OK) :
      sys.exit("ERROR "+methID+
               " Cdn coastal land polygons parent directory -> "+CanCoastLinesLandDataDir+" not found !\n")
    #---

    if CanCoastLinesLandFilesTuple is None :
      sys.exit("ERROR "+methID+" CanCoastLinesLandFilesTuple is None !\n")
    #---

    #: Doc Don't assume that the FileFormat is ok.
    fileFormatOk= False

    #: Doc FileFormat could indeed be None.
    if FileFormat is None :

      #: Doc Assuming ESRI SHAPEFILE format if FileFormat is None:
      FileFormat= self.ALLOWED_FORMATS.ESRI_SHAPEFILE.name

    #: Doc Validate the FileFormat.
    for allowedFormat in tuple(self.ALLOWED_FORMATS) :

      #: Doc Recall that self.ALLOWED_FORMATS is an Enum then extract the string
      #: representation with the name attribute:
      if FileFormat == allowedFormat.name:
        fileFormatOk= True
        break
      #--- end inner if block

    #--- end for loop block

    if not fileFormatOk :
      sys.stderr.write("ERROR "+methID+" Invalid land-water masks file format -> "+FileFormat+" !\n")
      sys.exit(1)

    #: Doc Generic method reference depending on the GIS format type used.
    #: (a.k.a. function-method pointer in C.C++ world)
    self.isPoint2DWet= None

    self._ogrDFRef= {}

    #: Doc Only ESRI_SHAPEFILE format used as of 2018-12-12 but
    #: we could have other formats types in the future.
    if FileFormat == self.ALLOWED_FORMATS.ESRI_SHAPEFILE.name :

      #: Doc Set the self.isPoint2DWet method reference to the OGR(vector) one
      self.isPoint2DWet= self.isOGRPoint2DWet

      self.getSHPOGRData(CanCoastLinesLandDataDir, CanCoastLinesLandFilesTuple) 

  #--- End block method __init__

  #--- TODO: Move this method in a new GeoOGR generic class to improve code modularization:
  def getSHPOGRData(self, CanCoastLinesLandHShpDataDir, CanCoastLinesLandShpFilesTuple) :

    """
    Read ESRI SHAPEFILE land-water mask(s) polygons data.

    CanCoastLinesLandHShpDataDir (type->string): The parent directory where to find the
    land-water masks input shapefile(s).

    CanCoastLinesLandShpFilesTuple (type->tuple): A tuple holding the land-water masks
    input shapefile(s) name(s).
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methID+
                     " Start, CanCoastLinesLandShpFilesTuple="+str(CanCoastLinesLandShpFilesTuple)+"\n")

    ##--- Some fool-proof checks should have been done already by the __init_method:
    #if CanCoastLinesLandHShpDataDir is None :
    #  sys.exit("ERROR "+methID+" CanCoastLinesLandHShpDataDir is None !\n")
    #
    #--- Check if parent directory exists and is readable:
    #if not os.access(CanCoastLinesLandHShpDataDir,os.F_OK) :
    #  sys.exit("ERROR "+methID+
    #                   " Cdn coastal land polygons shapefiles directory -> "+CanCoastLinesLandHShpDataDir+" not found !\n")
    #if CanCoastLinesLandShpFilesTuple is None :
    #  sys.exit("ERROR "+methID+" CanCoastLinesLandShpFilesTuple is None !\n")
    ##---

    #: Doc Create the dictionary to fill up with OGR layer(s) definition data:
    self._ogrDFRef= {}

    #: Doc Loop on the shapefile(s) name(s) defined in CanCoastLinesLandShpFilesTuple:
    for canCoastLinesLandShpFile in CanCoastLinesLandShpFilesTuple : 

      #: Doc Complete path of the shapefile being processed:
      shapeFileFullPath= CanCoastLinesLandHShpDataDir + "/" + canCoastLinesLandShpFile

      #--- Check if the shapefile exists and if it's readable:
      if not os.access(shapeFileFullPath, os.F_OK) :
        sys.exit("ERROR "+methID+
                  " Cdn coastal land polygons shapefile -> "+shapeFileFullPath+" not found !\n")
      #---

      #: Doc Get the name of the land-water masj file from its complete path.
      landMasksOGRDataFileNamePrfx= os.path.basename(canCoastLinesLandShpFile).split(".")[0]

      sys.stdout.write("INFO "+methID+" Reading OGR land mask data layer -> "+
                       landMasksOGRDataFileNamePrfx+" from file -> "+shapeFileFullPath+"\n")

      #: Doc The OGR layer to get from the shapefile should have its name
      #    defined as the file name(without the extension):
      ogrLayerName= os.path.basename(landMasksOGRDataFileNamePrfx).split(".")[0]

      #: Doc The 0 arg. signal that the file is opened in read mode only.
      self._ogrDFRef[ogrLayerName]= ogr.Open(shapeFileFullPath, 0)

      #--- Check if the ogr.Open returned something usable:
      if self._ogrDFRef[ogrLayerName] is None :
        sys.exit("ERROR "+methID+" Unable to open file -> "+shapeFileFullPath+" with ogr.Open !\n")

      #--- Could be an unicode string problem here ? need to use str(ogrLayerName) to get ogrDFRef.GetLayerByName working properly.
      #layerDict[self.OGR_LAYERS_ID[0]]= self._ogrDFRef[ogrLayerName].GetLayerByName(str(ogrLayerName))

      #: Doc Seems an unicode string stuff problem here ? need to use str(ogrLayerName) to
      #      get ogrDFRef.GetLayerByName working properly.
      layerRef= self._ogrDFRef[ogrLayerName].GetLayerByName(str(ogrLayerName))

      #: Doc Check if the OGR layer reference is ok:
      if layerRef is None :
        sys.exit("ERROR "+methID+" Unable to get layer ->"+ogrLayerName+
                 " from -> "+shapeFileFullPath+" with ogrDFRef.GetLayerByName !\n")
      #---

      #: Doc Validate the OGR layer SRS:
      self.validateOGRLayerSRS(layerRef)

      #: Doc Check if the OGR data have the right geometry using its feature 0.
      featureZero= layerRef.GetFeature(0)

      if featureZero is None :
        sys.exit("ERROR "+methID+
                 " Cannot get feature 0 with layerRef.GetFeature(0) from file -> "+shapeFileFullPath+"!\n")
      #---

      featureZeroGRef= featureZero.GetGeometryRef()

      if featureZeroGRef is None :
        sys.exit("ERROR "+methID+
                 " Cannot get feature 0 geometry object with feature0.GetGeometryRef() from file -> "+shapeFileFullPath+"!\n")
      #---

      geomTypeName= featureZeroGRef.GetGeometryName()

      if geomTypeName not in self.OGR_ALLOWED_GEOMETRIES_NAMES :
        sys.exit("ERROR "+methID+" Invalid geometry type -> "+
                 str(geomTypeName)+" found in file -> "+shapeFileFullPath+"!\n")
      #---

      sys.stdout.write("INFO "+methID+" Will use OGR geometry type -> "+str(geomTypeName)+" \n")

    #--- end block for canCoastLinesLandShpFile in CanCoastLinesLandShpFilesTuple

    sys.stdout.write("INFO "+methID+" end \n")

  #--- isOGRPoint2DWet method still need to be tested-validated
  #    TODO: Move this method in a new GeoOGR generic class to improve code modularization:
  def isOGRPoint2DWet(self, PointLon, PointLat) :

    """
    Verify if a 2D grid point is not a "dry" point i.e. that it is
    a "wet" grid point which is outside of all OGR land-water mask
    polygons of an OGR layer.

    PointLat (type->float): The latitude(float format) of the 2D grid point for the dryness check.

    PointLon (type->float): The longitude(float format) of the 2D grid point for the dryness check.

    return (type->float): The boolean verdict of wetness for the (PointLon, PointLat).

    NOTE: No validation on arguments i.e. assuming that PointLat, PointLon arguments
    are inside the normal geographical extremums limits +-90, +-180 and assuming
    that the bounding box coordinates are using the same CRS(a.k.a SRS) which is
    EPSG:4326 normally.
    """

    #methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #: Doc Need to create an tmp. OGR point geometry object.
    ogrPoint= ogr.Geometry(ogr.wkbPoint)

    #: Doc Set the tmp. point lon-lat
    ogrPoint.SetPoint_2D(0, PointLon, PointLat)

    #: Doc We assume first that the point is not on land:
    isWet= True

    #: Doc Loop on all OGR layers:
    for layerId in tuple(self._ogrDFRef.keys()) :

      #: Doc Extract the layer reference.
      layerRef= self._ogrDFRef[layerId].GetLayerByName(str(layerId))

      #: Doc Check for the point inclusion in the layer extent:
      if not self.withinLayerExtent(layerRef, PointLat, PointLon) :

        #: Doc Point not included in current layer extent,
        #    continue with the next layer if any:
        continue
      #--- end if block.

      #: Doc Point inside layer extent, need to reset OGR file
      #      reading each time we have to loop on all features
      layerRef.ResetReading()

      #: Doc Set the spatial filter of the layer with the ogrPoint geometry
      #    to speed up the search:
      layerRef.SetSpatialFilter(ogrPoint)

      #: Doc Try to find a land polygon feature enclosing the grid point.
      polyRet= layerRef.GetNextFeature()

      if polyRet is not None:

        #: Doc Got a land polygon enclosing the point so it is a dry grid point.
        isWet= False
        break
      #--- end if block.
    #--- end block loop for layerId in self._ogrDFRef.keys()

    return isWet
