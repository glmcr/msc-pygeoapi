#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/sfmt/SFMTMetaData.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.sfmt.SFMTMetaData implementation
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
import sys
import inspect

#---
from msc_pygeoapi.process.dfo.pjs.util.JsonCfgIO import JsonCfgIO
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTMetaDataAttr import SFMTMetaDataAttr

#---
class SFMTMetaData(SFMTMetaDataAttr) :

  """
  Class SFMTMetaData create-write common HDF5 metadata for all S<NNN>
  products in an automated fashion. By doing so, we avoid to repeat(i.e.
  copy-pasting codes which we try to avoid as much as we can) the exact
  same coding for each S<NNN> formats flavors.
  """

  #---
  def __init__(self, JsonCommonMetaDataDict) :

    """
    JsonCommonMetaDataDict (type->dictionary) : A dictionary holding the common HDF5
    json formated metadata to use for the SFMT DHP data.
    """

    SFMTMetaDataAttr.__init__(self)

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    if JsonCommonMetaDataDict is None :
      sys.exit("ERROR "+thisMethod+" JsonCommonMetaDataDict is None ! \n")

    #: Doc (type->dictionary): Keep a reference to the JsonCommonMetaDataDict in self object
    #                          for subsequent usage by sub classes.
    self._jsonCommonMetaDataDict= JsonCommonMetaDataDict

  #---
  def createAutoMetaDataAttrsInHDF5Group(self, JsonGroupAttrsDict,
                                         AutoMetaDataStrIdsTuple, HDF5TypeKeyId, HDF5Group, INFOLog= False) :
    """
    Create-write HDF5 SFMT DHP data ATTRIBUTEs contained in the dictionary JsonGroupAttrsDict with their
    strings ids. defined in the AutoMetaDataStrIdsTuple tuple. The ATTRIBUTEs are created in the HDF5 group
    identified with the HDF5Group argument(which should already exists).

    JsonGroupAttrsDict (type->dictionary): The json formatted dictionary indexing the SFMT DHP HDF5 metadata ATTRIBUTEs.

    AutoMetaDataStrIdsTuple (type->tuple): Tuple holding the strings ids. to use as loop iteration indexing items
    in JsonGroupAttrsDict.

    HDF5TypeKeyId (type->string): The string key id. for the HDF5 type(used to do indexing in JsonGroupAttrsDict
    metadata dictionary).

    HDF5Group (type->HDF5 file GROUP data structure object): The HDF5 GROUP data structure object to fill up with
    dynamic metadata ATTRIBUTEs.

    INFOLog (type->boolean) <OPTIONAL> Default->False: To log or not to log INFO messages on stdout file stream.

    NOTE: Fool-proof checks are commented for performance reasons.
    """

    if INFOLog :
      thisMethod= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
      sys.stdout.write("INFO "+thisMethod+" Start: AutoMetaDataStrIdsTuple="+
                       str(AutoMetaDataStrIdsTuple)+", HDF5TypeKeyId="+str(HDF5TypeKeyId)+"\n")

    ##--- Uncomment for debugging
    #if JsonGroupAttrsDict is None :
    #  sys.exit("ERROR "+thisMethod+" JsonGroupAttrsDict is None ! \n")

    ##--- Uncomment for debugging
    #if HDF5TypeKeyId not in JsonGroupAttrsDict.keys() :
    #  sys.exit("ERROR "+thisMethod+" HDF5TypeKeyId not in JsonGroupAttrsDict.keys()! \n")

    ##--- Uncomment for debugging
    #if AutoMetaDataStrIdsTuple is None :
    #  sys.exit("ERROR "+thisMethod+" AutoMetaDataStrIdsTuple is None ! \n")

    ##--- Uncomment for debugging
    #if len(AutoMetaDataStrIdsTuple) == 0 :
    #  sys.exit("ERROR "+thisMethod+" len(AutoMetaDataStrIdsTuple) == 0 ! \n")

    ##--- Uncomment for debugging
    #if HDF5Group is None :
    #  sys.exit("ERROR "+thisMethod+" HDF5Group is None ! \n")

    #: Doc Just need to loop on auto metadata list items to create HDF5 attributes to create them
    #      in the h5py file GROUP data structure object.
    for autoMetaDataId in AutoMetaDataStrIdsTuple :

      if INFOLog :
        sys.stdout.write("INFO "+thisMethod+" processing attribute -> "+autoMetaDataId+"\n")

      #: Doc Extract the DATATYPE string id. key from the JsonGroupAttrsDict:
      dTypeId= JsonGroupAttrsDict[autoMetaDataId][HDF5TypeKeyId]

      ##--- Uncomment for debugging
      #if hdf5DTypeId not in self.HDF5_AUTO_DTYPES.keys() :
      #  sys.exit("ERROR "+thisMethod+" Invalid DATATYPE -> "+hdf5DTypeId+" !\n")

      #: Doc Extract the value of the DATATYPE from JsonGroupAttrsDict:
      dataValue= JsonGroupAttrsDict[autoMetaDataId][ self.DATAVALUE_ID[0] ]

      #: Doc Create the ATTRIBUTE with the right DATATYPE argument extracted from self.HDF5_AUTO_DTYPES dictionary:
      HDF5Group.attrs.create(autoMetaDataId, dataValue, dtype= self.HDF5_AUTO_DTYPES[dTypeId][0])

    #--- End block loop for autoMetaDataId in AutoMetaDataStrIdsTuple.

    if INFOLog :
      sys.stdout.write("INFO "+thisMethod+" end\n")

  #---
  def createAutoMetaDataSetsInHDF5Group(self, JsonGroupDataSetsDict,
                                        AutoMetaDataStrIdsTuple, HDF5Group, INFOLog= False) :
    """
    Create-write HDF5 SFMT DHP data common DATASETs contained in the dictionary
    JsonGroupDataSetsDict with their strings ids defined in the AutoMetaDataStrIdsTuple
    tuple. The attributes are created in the HDF5 group identified with the HDF5Group
    argument (which should already exists).

    JsonGroupDataSetsDict (type->dictionary): A json formatted dictionary of HDF5 DATASETs
    metadata to be created in the HDF5Group data structure.

    AutoMetaDataStrIdsTuple (type->tuple): A tuple holding the DATASETs strings ids. keys
    to use for indexing in the JsonGroupDataSetsDict dictionary.

    HDF5Group (type->HDF5 file GROUP data structure object): The HDF5 GROUP data structure
    to fill up with dynamic DATASETs metadata.

    INFOLog (type->boolean) <OPTIONAL> Default->False: To(or not to) log INFO level messages
    on stdout file stream.

    NOTE: Fool-proof checks are commented for performance reasons.
    """

    if INFOLog :
      thisMethod= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"
      sys.stdout.write("INFO "+thisMethod+
                       " Start: AutoMetaDataStrIdsTuple="+str(AutoMetaDataStrIdsTuple)+"\n")

    ##--- Uncomment for debugging
    #if JsonGroupDataSetsDict is None :
    #  sys.exit("ERROR "+thisMethod+" JsonGroupDataSetsDict is None ! \n")

    ##--- Uncomment for debugging
    #if AutoMetaDataStrIdsTuple is None :
    #  sys.exit("ERROR "+thisMethod+" AutoMetaDataStrIdsTuple is None ! \n")

    ##--- Uncomment for debugging
    #if len(AutoMetaDataStrIdsList) == 0 :
    #  sys.exit("ERROR "+thisMethod+" len(AutoMetaDataStrIdsList) == 0 ! \n")

    ##--- Uncomment for debugging
    #if HDF5Group is None :
    #  sys.exit("ERROR "+thisMethod+" HDF5Group is None ! \n")

    #: Doc Just need to loop on auto metadata list items to create HDF5 DATASETs in
    #      the HDF5 file GROUP data structure object
    for autoMetaDataId in AutoMetaDataStrIdsTuple :

      if INFOLog :
        sys.stdout.write("INFO "+thisMethod+" processing HDF5 DATASET -> "+ autoMetaDataId + "\n")

      #: Doc Extract the DATASPACE sub-dictionary of the DATASET from JsonGroupDataSetsDict dictionary
      dataSpace= JsonGroupDataSetsDict[autoMetaDataId][ self.DSET_ID[0] ]

      ##--- Uncomment for debugging
      #if not self.HDF5_SIMPLE_SPACE_ID[0] in dataSpace :
      #  sys.exit("ERROR "+thisMethod+
      #           " The HDF5 data space must be "+self.HDF5_SIMPLE_SPACE_ID[0]+" here ! \n")
      ##---

      #: Doc DATASET column iteration counter.
      nbCols= 0

      #: Doc To store the DATASPACE values in a temp. dictionary:
      itemsDictTmp= {}

      #: Doc Iterate on the DATASPACE items values of the DATASET.
      for itemKey in tuple( sorted(dataSpace[ self.DATAVALUE_ID[0] ].keys()) ) :

        #: Doc The string item should be like "rowIdx,colIdx".
        #      rowIdx is the row index of the the data and
        #      colIdx is the column index of the data in the
        #      DATASET structure.
        indices= itemKey.split(",")

        ##--- Uncomment for debugging
        ##--- Max. two dimensions allowed here !
        #if len(indices) != 2 :
        #  sys.exit("ERROR "+thisMethod+": Invalid JSON itemKey -> "+ itemKey + " ! \n")
        ##---

        rowIdx= indices[0]
        colIdx= indices[1]

        #: Doc Need to increment nbCols if necessary.
        if int(colIdx) == nbCols : nbCols += 1

        #: Doc Create row entry in itemsDictTmp if not already created.
        if not rowIdx in itemsDictTmp :
          itemsDictTmp[rowIdx]= {}

        #: Add the DATASPACE value in the itemsDictTmp for subsequent usage.
        itemsDictTmp[rowIdx].update( { colIdx : dataSpace[ self.DATAVALUE_ID[0] ][itemKey] })

      #--- End block for loop.

      #: Doc Get the itemsDictTmp dictionary keys in a tuple.
      itemsDictTmpKeys= tuple(itemsDictTmp.keys())

      #: Doc Get the nb. of rows for the DATASPACE values.
      nbRows= len(itemsDictTmpKeys)

      #--- Use an unary tuple here for hdf5StrDType ???
      hdf5StrType= self.HDF5_AUTO_DTYPES[ self.HDF5_STR_TYPE_ID[0] ][0]

      #: Doc Could have 2D arrays in case nbCols is > 1 at this point.
      if nbCols > 1 :

        #: Doc Create the HDF5 DATASET having a 2D array(nbRows, nbCols).
        dsp= HDF5Group.create_dataset(autoMetaDataId, (nbRows, nbCols), dtype= hdf5StrType )

        #: Doc Loop on itemsDictTmp rows,cols to fill up the DATASET 2D array
        #      with the metadata coming from the Json config. file.
        for row in itemsDictTmpKeys :
          for col in tuple(itemsDictTmp[row].keys()) :

            dsp[int(row), int(col)]= itemsDictTmp[row][col]

            #print(row+","+col+": "+ itemsDictTmp[row][col])

      #: Doc Or could have 1D arrays:
      else :

        #: Doc Create the HDF5 DATASET having a 1D array(of nbRows items).
        dsp= HDF5Group.create_dataset(autoMetaDataId, ( nbRows ,), dtype= hdf5StrType )

        #: Doc Loop on itemsDictTmp rows to fill up the DATASET 1D array
        #      with the metadata coming from the Json config. file.
        for row in itemsDictTmpKeys :
          dsp[int(row)]= itemsDictTmp[row]["0"]

      #--- end block if-else.

    #---
    if INFOLog :
      sys.stdout.write("INFO "+thisMethod+" end\n")

  #---
  @staticmethod
  def getDateTimeStampStrTuple(TimeStampHDF5GroupPrefix, TimeStampIdx,
                               DateTimeKey, DateTimeKeySplitStr, HDF5DateTimeSep) :
    """
    Build the required name of the "<TimeStampHDF5GroupPrefix>_***" HDF5 GROUP and it's date timestamp
    string with the right format(Ex. "20180720T064500Z") for the SFMT DHP data.

    TimeStampHDF5GroupPrefix (type->tuple): An unary tuple holding the string prefix to use for the
    GROUPs names.

    TimeStampIdx (type->int): The time stamp counter needed for the name of the "Group_***" GROUP.
    if TimeStampIdx == 69 then we end up with "Group_069"

    DateTimeKey (type->string): The date timestamp string in YYYYMMDD.hhmmssZ format.

    DateTimeKeySplitStr (type->string): String used to split the DateTimeKey string.

    HDF5DateTimeSep (type->string): Ths string separator for the SFMT DHP data timestamp format.

    return (type->tuple): A tuple holding the "<TimeStampHDF5GroupPrefix>_***" string and the SFMT
    DHP data format timestamp.

    NOTE: No fool-proof checks for performance reasons.
    """

    #: Doc Split the YYYYMMDD.hhmmssZ formatted DateTimeKey string in two parts:
    dateTimeSplit= tuple( DateTimeKey.split(DateTimeKeySplitStr) )
    #dateTimeSplit= tuple( DateTimeKey.split(self.DATE_TIME_SPLIT_STR[0]) )

    #: Doc Get the official SFMT DHP data format for the time stamp.
    dateTimeOutStr= ( dateTimeSplit[0] + HDF5DateTimeSep[0] + dateTimeSplit[1] ,)

    #: Doc Need to convert the concatenation of TimeStampHDF5GroupPrefix[0] and
    #      JsonCfgIO.formatTimeStampGroupNb(TimeStampIdx) to an inner tuple in the returned tuple.
    return ( ( TimeStampHDF5GroupPrefix[0] + JsonCfgIO.formatTimeStampGroupNb(TimeStampIdx) ,), dateTimeOutStr)
