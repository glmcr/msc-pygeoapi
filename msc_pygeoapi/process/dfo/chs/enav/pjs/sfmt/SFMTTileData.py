#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTTileData.py
# Creation        : May/Mai 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTTileData implementation.
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

#---
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.IS104 import IS104
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTMetaData import SFMTMetaData
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTDataFactory import SFMTDataFactory

#---
class SFMTTileData(SFMTDataFactory, SFMTMetaData) :

  """
  Class implementing utility instance method writeCommonTileData.
  """

  #---
  def __init__(self, S102Obj, JsonCommonMetaDataDict) :

    """
    Constructor for class SFMTTileData.

    S102Obj (type->S102) : A S102 class instance object.

    JsonCommonMetaDataDict (type->dictionary) : A dictionary holding the common json formatted meta data to use for all the SFMT DHP data types.
    """

    SFMTDataFactory.__init__(self, S102Obj)
    SFMTMetaData.__init__(self, JsonCommonMetaDataDict)

  #---
  def writeCommonTileData( self,
                           RootJSONGroupAttrs,
                           InfoLog= False) :
    """
    Method used to write the common DH product
    tile metadata in its output file.

    RootJSONGroupAttrs (type->h5py file group object):
    The SFMT DHP HDF5 data root group object for the
    main attributes.

    INFOLog (type->boolean) <OPTIONAL> Default->False:
    Flag to put(or not to) the INFO logs on the stdout.

    NOTE: No fool-proof checks for performance reasons.
    """

    #---
    if InfoLog :
      thisMeth= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #: Doc Create the tile bounding box meta-data
    #      BUT in surfCurrent01Group GROUP this time:
    self.createAutoMetaDataAttrsInHDF5Group( RootJSONGroupAttrs,
                                             tuple(self.BBOX_LLLIMITS_IDS),
                                             self.DTYP_ID[0],
                                             self._hdf5ProductGroupData )

    #: Doc Set the attribute for the numbers of model
    #      data points enclosed by the tile:
    self._productGroupAttrDict2Set[ self.NUM_NODES_ID[0] ][ self.DATAVALUE_ID[0] ]= self._nbPoints

    #: Doc Extract 1st grid point data dictionary
    #  key from self._pointsDataOutKeysTuple.
    pointData0Key= self._pointsDataOutKeysTuple[0]

    #: Doc Need to verify that the timestamps strings keys are ok.
    pointData0TimeStampsList= \
      list( self._pointsDataOutDict[pointData0Key].keys() )

    #--- TODO: Check if the following if could be moved in
    #          one of the S104 methods.
    #
    #: Doc Remove chart datum item(if any) from
    #      pointData0TimeStampsList keys list
    #      for getting the timestamps right.
    if IS104.CHART_DATUM_CONV_ID[0] in pointData0TimeStampsList :
      pointData0TimeStampsList.remove(self.CHART_DATUM_CONV_ID[0])

    #:Doc Extract date-time keys from 1st point data dictionary.

    #--- NOTE: Do not assume that date-time keys
    #          are already sorted in ascending order.
    self._dateTimeKeys= \
      tuple( sorted( pointData0TimeStampsList, reverse= False) )

    #: Doc Get the time increment interval in seconds
    #      between 2nd and 1st dateTimes.
    self._timeIncrInterval= self.getDTStringsSecondsDiff( self._dateTimeKeys[1],
                                                          self._dateTimeKeys[0],
                                                          self.DEFAULT_GET_SECONDS_FMT[0])

    #--- TODO: The self.setDateTimeHDF5MetaData method could
    #          be used just once and for all output files
    #          (but will the performance gain be really significant ??)
    self.setDateTimeHDF5MetaData( self._timeIncrInterval,
                                  self._dateTimeKeys,
                                  self._productGroupAttrDict2Set)

    prodGrpAttrDict2SetKeys= \
      tuple(self._productGroupAttrDict2Set.keys())

    #: Doc Create the HDF5 ATTRIBUTEs we have just set
    #      in the self._hdf5ProductGroupData:
    self.createAutoMetaDataAttrsInHDF5Group( self._productGroupAttrDict2Set,
                                             prodGrpAttrDict2SetKeys,
                                             self.DTYP_ID[0],
                                             self._hdf5ProductGroupData)

    #: Doc Create coordinates positioning Group in
    #      surfCurrent01Group and populate it with
    #      tile lat/long dataset.
    coordinatesPosGroup= \
      self._hdf5ProductGroupData.create_group(self.LLPOS_ID[0])

    #: Doc Extract the metadata axis names dictionary
    #      in self.__productJSONMetaDataDict.
    axisNameDSetDict= \
      self._jsonProductMetaDataDict[ self.JSON_DATASETS_ID[0] ][ self.AXIS_NAMES_ID[0] ]

    #: Doc Set the coordinates positioning Group
    #      in the HDF5 file data structure:
    self.setCoordinatesHDF5MetaData( self._nbPoints,
                                     axisNameDSetDict,
                                     self._pointsDataOutKeysTuple,
                                     coordinatesPosGroup )
