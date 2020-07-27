#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/util/JsonCfgIO.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.util.JsonCfgIO implementation.
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
import json
import inspect
from collections import MutableMapping

#---
from dhp.util.IDataIndexing import IDataIndexing

#---
class JsonCfgIO(IDataIndexing) :

  """
  Utility class dealing with JSON formatted HDF5 meta-data definitions.
  """

  #---
  def __init__(self) :

    IDataIndexing.__init__()

  #---
  @staticmethod
  def formatTimeStampGroupNb(TimeStampIdx) :

    """
    Return a string formatted with a minimum of 3 digits
    with the argument TimeStampIdx assumed positive integer >=1
    by prefixing one or two 0 characters to it.

    """

    #--- Default time stamp string for TimeStampIdx >= 100
    timeStampStr= str(TimeStampIdx)

    #--- Get the number suffix according to the TimeStampIdx:
    if TimeStampIdx < 10 :
      timeStampStr= "00" + str(TimeStampIdx)

    elif TimeStampIdx < 100 :
      timeStampStr= "0" + str(TimeStampIdx)

    return timeStampStr

  #---
  @staticmethod
  def getIt(JSONFile) :

    """
    Method which tries to read a JSON format file.

    JSONFile (type->string): Complete path to a Json formatted file.

    return (type->dictionary): the JSON data as a normal python dictionary.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    if not os.access(JSONFile,os.F_OK) :
      sys.exit("ERROR "+methID+" JSONFile -> "+JSONFile+ " not found !\n")

    JSONStuffFp= open(JSONFile,"r")

    JSONStuff= None

    #: Doc Using try-except block here since this method
    #    is not used in computation intensive loops:
    try :

      #--- NOTE: Are try-exception blocks compatible with ECCC Maestro way of handling
      #          errors ??

      #--- Works only with Python2 !!!
      #JSONStuff= json.load(JSONStuffFp, object_hook= JsonCfgIO.asciiEncodeDict)

      #--- Works with both Python2 and 3 but we got $#%%#*#*!&*#! unicode stuff !!!
      JSONStuff= json.load(JSONStuffFp)
      #--- UNICODE !!! JSONStuff= json.load(JSONStuffFp)

    except Exception as e :

      sys.exit("ERROR "+methID+
               " Problem with json.load(JSONFile) ! JSONFile -> "+JSONFile+", exception catched -> "+str(e)+" \n")
    #--- End try-except block.

    JSONStuffFp.close()

    return JSONStuff

  #---
  @staticmethod
  def mergeNestedDicts(SourceDict, TargetDict) :

    """
    As the method name says, it merges together two dictionaries having arbitrary nesting structures.
    Code taken from https://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge.
    (Thanx again stackoverflow !!)

    TargetDict (type->dictionary): The dictionary where the merge takes place.
    SourceDict (type->dictionary): The dictionary which contents will be merged with TargetDict.

    return (type->dictionary): TargetDict

    ex. 
    TargetDict={'ATTRIBUTES': {'productSpecification': {'DATATYPE': 'H5T_STRING', 'DATASPACE': 'SCALAR' }}}
    SourceDict= {'ATTRIBUTES': {'productSpecification': { 'DATA': 'S-111_version_1.0.0'}}}

    Use of JsonCfgIO.mergeNestedDicts(SourceDict, TargetDict) produce this :

    TargetDict= {'ATTRIBUTES': {'productSpecification': {'DATATYPE': 'H5T_STRING', 'DATASPACE': 'SCALAR', 'DATA': 'S-111_version_1.0.0'}}}

    REMARKS: 
      - Use at your own risk since it is a recursive function.
      - Could fail if the default recursion depth limit is too small.
      - Modified the original code by using tail recursion(which should improve performance).
      - Not thoroughly fool-proof tested yet.
      - Seems to be working with both Python2 and 3.
    """

    #---
    for key in tuple(SourceDict.keys()) :

      #--- Check if we have to go into recursion world.
      notRecur= not (key in TargetDict and isinstance( TargetDict[key], MutableMapping) and isinstance( SourceDict[key], MutableMapping))

      if notRecur :

        #--- Just assign SourceDict[key] to TargetDict[key]
        TargetDict[key]= SourceDict[key]

      else:

        #--- Need to go into recursion world here.
        JsonCfgIO.mergeNestedDicts( SourceDict[key], TargetDict[key])

      #--- end inner if-else block
    #--- end for loop block

    return TargetDict

#  #--- Keep for possible future usage.
#  @staticmethod
#  def asciiEncodeDict(data) :
#
#    """
#    Thanx again stackoverflow for the idea:
#
#    Get rid of the prefixed unicode 'u' char on dictionary
#    key : value pairs. but it's not working with lists of
#    unicode strings.
#
#    data (type->dictionary) : The dictionary which we want to have all its key : value pairs
#                              being straight ASCII strings.
#    Remark:
#    """
#    if sys.version_info[0] >= 3: unicode= str
#
#    ascii_encode= lambda x: x.encode('ascii') if isinstance(x, unicode) else x
#
#    return dict(map(ascii_encode, pair) for pair in data.items())

