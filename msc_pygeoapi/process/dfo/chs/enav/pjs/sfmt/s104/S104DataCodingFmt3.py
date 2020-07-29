#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : DFO-CHS-ENAV-DHP
# File/Fichier    : dhp/sfmt/s104/S104DataCodingFmt3.py
# Creation        : Septembre/September 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.s104.S104DataCodingFmt3 implementation.
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
import time
import math
import inspect

#--- 3rd party h5py package.
import h5py

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.S104 import S104
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.IS104 import IS104

#---
class S104DataCodingFmt3(S104) :

  """
  Class S104DataCodingFmt3 purpose is to produce
  S104 data tiled files in the DataCodingFormat nb.3
  (i.e. water levels data coming from unstructured
  grids models like FVCOM or WebTide models).
  NOTE: Using the same HDF5 file data structures as S111.

  NOTE: We could also use data from models results
  mapped on polar-stereographic or regular lon-lat
  grids as if they were coming from unstructured
  grids provided that it is compatible with the
  de-facto default GIS EPSG:4326 reference
  system spec.
  """

  #---
  def __init__( self,
                S102TilesObj,
                JsonCommonMetaDataDict,
                JsonTemplatesDir,
                TypeOfWaterLevelData,
                GenericModelName,
                OutputDir) :
    """
    Object instance constructor for class S104DataCodingFmt3.

    S102TilesObj (type->S102Tiles): A S102Tiles class instance  object.

    JsonCommonMetaDataDict (type->dictionary): A dictionary holding the common
    json formatted metadata to use for the SFMT DHP data.

    JsonTemplatesDir (type->string): The complete path of the directory where
    to find the SFMT DHP json formatted metadata definitions used.

    TypeOfWaterLevelData (type->int): The type of the water levels data
    (typeOfWaterLevelData metadata value, see TYPES_OF_DATA dictionary
    defined in ISFMTMetaDataAttr class src file for details).

    GenericModelName (type->string): The string name id. of the model from
    which the water levels data used for S104 DHP data comes from (ex. "NEMO",
    "WebTide", "IWLS"). No mention of a specific regional name for the model
    at this point.

    OutputDir (type->string): The output directory where to write the
    S104 products.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    sys.stdout.write("INFO "+methId+" Start: JsonTemplatesDir="+
                     JsonTemplatesDir+", OutputDir="+OutputDir+"\n")

    #: Doc super class __init__ method. Note the
    #      ISFMT.ALLOWED_DATA_CODING_FMT.three argument.
    S104.__init__( self,
                   S102TilesObj,
                   JsonCommonMetaDataDict,
                   JsonTemplatesDir,
                   TypeOfWaterLevelData,
                   ISFMT.ALLOWED_DATA_CODING_FMT.three,
                   GenericModelName,
                   OutputDir )

    sys.stdout.write("INFO "+methId+" end\n")

  #---
  def writeOneTile( self,
                    TileId,
                    TileDict,
                    DateTimeStringsOutDict,
                    RegionalModelName= None,
                    ChartDatumConversion= True,
                    OverWrite= False,
                    InfoLog= False ) :
    """
    Write a tiled S104 DHP data HDF5 file
    using the data coding format 3.

    TileId (type->string): A tile string id.

    TileDict (type->dictionary): The properly
    formatted dictionary which contains the
    tile water levels data.

    DateTimeStringsOutDict (type->dictionary):
    Already formatted HDF5 SFMT DHP spec.
    date-timestamps strings dictionary.

    RegionalModelName (type->string) <OPTIONAL> Default->None :
    A specific regional model name(could be None).

    ChartDatumConversion (type->boolean) <OPTIONAL> Default->True :
    To apply(or not) a chart datum conversion for the water
    levels values.

    OverWrite (type->boolean) <OPTIONAL> Default->False : A flag
    to signal that the already existing data products files are
    to be overwritten with or without issuing a WARNING log message
    to the stdout stream.

    InfoLog (type->boolean) <OPTIONAL> Default->False : To put(or not to)
    log INFO messages on the stdout stream.

    TODO: There is still some slight redundancy between this method and
    the equivalent S111DataCodingFmt3.writeOneTile method so it would be
    more optimal(in terms of OOP paradigm) to implement the common
    processing in the SFMTDataCodingFmt3.writeOneTile super class
    method to get rid of this redundancy.
    """

    #--- NOTE: inspect.stack(0) is faster than
    #          inspect.stack() but with the drawback that
    #          the source file context details are not retreived
    if InfoLog:

      methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

      sys.stdout.write("INFO "+methId+" Start : TileId="+
                       TileId+", self._outputDir="+self._outputDir+
                       ", ChartDatumConversion="+str(ChartDatumConversion)+"\n")
    #--- end if block

    #: Doc Using S104 super class writeOneTile for generic processing.
    super(S104DataCodingFmt3,self).writeOneTile( TileId,
                                                 TileDict,
                                                 DateTimeStringsOutDict,
                                                 RegionalModelName,
                                                 ChartDatumConversion,
                                                 OverWrite,
                                                 InfoLog )

    #--- TODO: This following if block should be done in the
    #          super class S104 writeOneTile method. That would
    #          probably provide a slight performance improvement.

    #: Doc Define the points data array shape just once.
    pointsDataShapeTuple= (self._nbPoints, 1)

    #: Doc To keep track of time stamps for HDF5 outputs formatting:
    timeStampIdx= 0

    #: Doc Loop on all time-stamps available for the tile
    for dateTimeKey in self._dateTimeKeys :

      if InfoLog:
        sys.stdout.write("INFO "+methId+
                         " writing tile "+TileId+
                         " data at dateTime -> "+ dateTimeKey +"\n")
      #---

      #: Doc Get the already and rightly DHP formatted date
      #      time stamp string from DateTimeStringsOutDict.

      #--- NOTE1: Each DateTimeStringsOutDict[dateTimeKey] is an unary tuple.
      #
      #    NOTE2: It seems that we can get a spectacular(about 2.5 times faster!)
      #           performance gain with that already defined DateTimeStringsOutDict
      #           instead of re-doing the string formatting operation for each time
      #           stamp of each output file.
      dateTimeStampStrings= DateTimeStringsOutDict[dateTimeKey][0]

      #--- NOTE: dateTimeStampStrings is a two item tuple:
      timeStampGroup= \
        self._hdf5ProductGroupData.create_group( dateTimeStampStrings[0][0] )

      #: Doc Create time stamp attribute in timeStampGroup:
      timeStampGroup.attrs.create( self.TIMESTAMP_METADATA_ID[0],
                                   dateTimeStampStrings[1][0], dtype= self.TMSTAMP_GRPSTR_DTYPE[0] )

      #: Doc Create speed,direction values dataset compound type in timeStampGroup:

      #--- NOTE: Keep the same (numCOL=self._nbPoints,numROW=1) array mapping as the geometry compound type.
      valuesData= timeStampGroup.create_dataset( self.VALUES_METADATA_ID[0],
                                                 pointsDataShapeTuple, dtype= self.ELEVTREND_TYPEDEF)

      #: Doc Counter for valuesData compound type object loop indexing:
      valueIdx= 0

      #: Doc Need to calculate the WL trends only for timestamps which
      #      are surrounded by two backward-in-time and two forward-in-time
      #      timestamps(i.e. the 1st two and the last two timestamps WL trends
      #      are considered UNKNOWN)
      trendAndTimeStampOk= ( False ,)

      #--- Obviously do that check only if computeWLTrend[0] is True:
      if self._computeWLTrends[0] :

        if timeStampIdx >= self._wlZElevTrendLowIdx[0] \
          and timeStampIdx < self._wlZElevTrendUppIdx[0] :

          #: Doc Ok we can calculate the WL trend.
          trendAndTimeStampOk= ( True ,)

          #: Doc Extract the moving time stamps windows for the WL Z elevations
          #      trend computation with a tuple slicing. Note the + 1 at the
          #      upper index of the tuple slicing operation(the ":" character
          #      string separates the bounds of the self._dateTimeKeys[ tuple
          #      slice wanted) .
          wlZTrendTimeStamps= tuple( self._dateTimeKeys[ timeStampIdx - self._wlZElevTrendLowIdx[0]:
                                     timeStampIdx + self._wlZElevTrendLowIdx[0] + 1 ] )

        #--- end inner if timeStampIdx >= wlZElevTrendLowIdx[0]
      #--- end outer if computeWLTrend[0]

      #: Doc Loop on all tile points:
      for lonLatPairKey in self._pointsDataOutKeysTuple :

        #--- Shortcut to the grid point data dictionary in self._pointsDataOutDict (tile dictionary)
        pointDataDict= self._pointsDataOutDict[lonLatPairKey]

        #: Doc Extract the model grid point water level data from the tile dictionary.
        wlZElev= pointDataDict[dateTimeKey][ self.WLZELEV_VALUEID[0] ]

        #: Doc Set the default WL temporal trend at self.WL_TREND_UNKNOWN[0] as default.
        wlZElevTrend= ( self.WL_TREND_UNKNOWN[0] ,)

        #: Doc Get the WL Z trend but only if we are not at the beginning or at the end of the time stamped data.
        if trendAndTimeStampOk[0] :
          wlZElevTrend= self.getWLZElevationsTrend( wlZTrendTimeStamps,
                                                    self._timeTrendOffsets,
                                                    self._denAccInv,
                                                    pointDataDict )
        #--- end if block.

        #: Doc Assuming here that self.CHART_DATUM_CONV_ID[0]
        #  is a valid key in the pointDataDict:

        #--- NOTE1: pointDataDict[ IS104.CHART_DATUM_CONV_ID[0] ] is an unary tuple:
        #
        #    NOTE2: The conversion to the chart datum could have been already done
        #           at this point. It is the case for ECCC NEMO models.
        if ChartDatumConversion :
          wlZElev += pointDataDict[ IS104.CHART_DATUM_CONV_ID[0] ][0]
        #---

        #: Doc Put WL values in HDF5 compound data structure.
        valuesData[valueIdx, IS104.ELEV_METADATA_ID[0]  ]= wlZElev
        valuesData[valueIdx, IS104.TREND_METADATA_ID[0] ]= wlZElevTrend[0]

        #: Doc Increment compound type array index:
        valueIdx += 1

      #--- End block Loop on tile points:

      #: Doc Increment timeStampIdx for the next dateTimeKey loop item:
      timeStampIdx += 1

    #--- End block Loop on all time-stamps available for the tile

    #: Doc Close the HDF5 python stuff and get outta'here
    self._hdf5FileRootObj.close()

    if InfoLog:
      sys.stdout.write("INFO "+methId+" end \n")
