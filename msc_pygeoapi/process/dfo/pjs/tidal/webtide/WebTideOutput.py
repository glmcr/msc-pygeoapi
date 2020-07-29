#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidaprd/webtide/WebTideOutput.py
# Creation        : October/Octobre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidaprd.webtide.WebTideOutput.py implementation.
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
import multiprocessing

#---
from msc_pygeoapi.process.dfo.pjs.tidal.TidalPrd import TidalPrd
from msc_pygeoapi.process.dfo.pjs.tidal.ITidalPrd import ITidalPrd
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.ISFMT import ISFMT
from msc_pygeoapi.process.dfo.pjs.tidal.webtide.WebTide import WebTide
from msc_pygeoapi.process.dfo.pjs.tidal.webtide.IWebTide import IWebTide
from msc_pygeoapi.process.dfo.pjs.util.MultiProcFactory import MultiProcFactory
from msc_pygeoapi.process.dfo.pjs.tidal.webtide.WebTideTiles import WebTideTiles
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.SFMTModelFactory import SFMTModelFactory
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s111.S111DataCodingFmt3 import S111DataCodingFmt3
from msc_pygeoapi.process.dfo.chs.enav.pjs.sfmt.s104.S104DataCodingFmt3 import S104DataCodingFmt3

#---
class WebTideOutput(SFMTModelFactory, WebTideTiles) :

  """
  Class used mainly for WebTide source code modularization.
  Defines some methods for the WebTide tiles input data processing.
  This class is sub-classed by class WebTideFactory
  (i.e. otherwise said, it is a super class of class WebTideFactory).
  """

  #---
  def __init__( self,
                SFMTObjInst,
                SFMTFactoryObj ) :
    """
    Constructor for class WebTideOutput.

    SFMTObjInst (type->SFMTObj) : A SFMTObj class instance object.

    SFMTFactoryObj (type->SFMTFactory): A SFMTFactory class object instance.
    """

    WebTideTiles.__init__(self)

    methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + str(" method:")

    #---
    if SFMTObjInst is None :
      sys.exit("ERROR "+methID+" SFMTObjInst is None !\n")
    #---

    SFMTModelFactory.__init__(self, SFMTObjInst)

    methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + str(" method:")

    #---
    if SFMTFactoryObj is None :
      sys.exit("ERROR "+methID+" SFMTFactoryObj is None !\n")
    #---

    if SFMTFactoryObj._s102TilesObj is None :
      sys.exit("ERROR "+methID+": SFMTProductsObj._s102TilesObj is None ! !\n")

    #--- Need to keep a reference to the SFMTFactoryObj in this object for later usage:
    self._sFMTFactoryObj= SFMTFactoryObj

  #---
  def produceDataSetOutputs( self,
                             TidalPrdFactoryObj: TidalPrd,
                             DataSetId: str,
                             WebTideObj: WebTide,
                             NbMultiProcesses: int = 1,
                             WarningsLog: bool = False) :
    """
    TidalPrdFactoryObj : The TidalPrd object going with the WebTide dataset object WebTideObj.

    DataSetId : The string id. of the regional dataset from which the WebTideObj was created.

    WebTideObj : The WebTide object holding the tiled input data of a regional dataset.

    NbMultiProcesses <DEFAULT==1> : The number of multiprocessing objects(a.k.a. "threads") to use
    to speed up the exec.

    WarningsLog <OPTIONAL,default==False> To put(or not to) log WARNING messages on the stdout file
    stream.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + str(" method:")

    #--- Can do the usual fool-proof checks here, this method
    #    is not used in number crunching intensive loops.
    if self._sFMTFactoryObj is None :
      sys.exit("ERROR "+methID+" self._sFMTFactoryObj is None !\n")

    if TidalPrdFactoryObj is None :
      sys.exit("ERROR "+methID+" TidalPrdFactoryObj is None !\n")

    if WebTideObj is None :
      sys.exit("ERROR "+methID+" WebTideObj is None !\n")

    if WebTideObj._fieldsVarsType is None :
      sys.exit("ERROR "+methID+" WebTideObj._fieldsVarsType is None !\n")

    if DataSetId is None :
      sys.exit("ERROR "+methID+" DataSetId is None !\n")

    if self._dateTimeStringsIdxDict is None :
      sys.exit("ERROR "+methID+" self._dateTimeStringsIdxDict is None !\n")

    if len(self._dateTimeStringsIdxDict.keys()) == 0 :
      sys.exit("ERROR "+methID+" len(self._dateTimeStringsIdxDict.keys()) == 0 !\n")

    if WebTideObj._tilesWithData is None :
      sys.exit("ERROR "+methID+" WebTideObj._tilesWithData is None !\n")

    if len(WebTideObj._tilesWithData.keys()) == 0 :
      sys.exit("ERROR "+methID+" len(WebTideObj._tilesWithData.keys()) == 0 !\n")

    sys.stdout.write("INFO "+methID+" Start: DataSetId="+DataSetId+
                     " WebTideObj._fieldsVarsType -> "+WebTideObj._fieldsVarsType+"\n")

    #--- Avoid awkward behavior if NbMultiProcesses is passed as a string:
    NbMultiProcesses= int(NbMultiProcesses)

    #--- Get a sorted(increasing ASCII mode) tuple with the string keys ids.
    #    of the WebTideObj._tilesWithData dictionary:
    tilesKeysIdsTuple= tuple( sorted( list( WebTideObj._tilesWithData.keys() ) ) )

    #print str(tilesKeysIdsList)

    #--- Check if the number of parallel multiprocess objects wanted is
    #    compatible with the number of cpus-cores of the machine.
    nbCpusCores= multiprocessing.cpu_count()

    #--- Create the threads handles control list for subsequent usage:
    multiProcsInstances= []

    sys.stdout.write("INFO "+methID+" nb. cpus-cores available="
                     +str(nbCpusCores)+", NbMultiProcesses="+ str(NbMultiProcesses) +"\n")

    #--- First check for nbCpusCores and NbMultiProcesses values :
    if nbCpusCores > 1 and NbMultiProcesses > 1:

      #--- Split the tiles bundle in subsets for parallelization:
      #    NOTE: tilesKeysIdsSubsets is tuple:
      tilesKeysIdsSubsets= MultiProcFactory.getKeysSubsets(nbCpusCores, NbMultiProcesses, tilesKeysIdsTuple)

      nbTilesSubsets= len(tilesKeysIdsSubsets)

      ##--- It could happen that nbTilesSubsets < NbMultiProcesses
      #if nbTilesSubsets < NbMultiProcesses :
      #
      #  sys.stdout.write("WARNING "+methID+" Got less tiles subsets -> "+str(nbTilesSubsets)+
      #                   " than NbMultiProcesses, must set NbMultiProcesses to nbTilesSubsets.\n")
      #  #--- No point to have more NbMultiProcesses than number of tiles subsets:
      #  NbMultiProcesses= nbTilesSubsets

      #--- *** TODO***: Add protection code here in case we have less tiles than cpus available ??.
      for tilesProcId in range(nbTilesSubsets) :

        #--- Need to pass a tuple containing self.produceTilesOutputs method arguments to multiprocessing.Process method
        methodArgs= ( TidalPrdFactoryObj, DataSetId, WebTideObj, tilesKeysIdsSubsets[tilesProcId] )

        #--- Create a new multiprocessing object (thread):
        newMultiProc= multiprocessing.Process(target= self.produceTilesOutputs, args= methodArgs )

        #--- Keep track of the newly created thread:
        multiProcsInstances.append(newMultiProc)

        #--- And launch the multiprocessing exec. for this newMultiProc:
        #    (unfortunately, we can't do method chaining here
        #    i.e. using something like multiProcsInstances.append(newMultiProc).start()
        newMultiProc.start()

      #--- end loop for tilesProcId in range(nbTilesSubsets)

      #--- Tell the main process to wait for all other processes to
      #    finish before doing something else serially.
      for mpInstance in multiProcsInstances :
        mpInstance.join()
      #---

      sys.stdout.write("INFO "+methID+
                       " parallelized SFMT DHP data files output are done for dataset -> "+DataSetId+"\n")

    else :

      #--- Serial exec. here.
      #    NOTE: It will took a while to crunch data whitout thread parallelization
      #          especially if all the WebTide dataset are used.
      sys.stdout.write("INFO "+methID+" Using serial exec.\n")

      self.produceTilesOutputs(TidalPrdFactoryObj, DataSetId, WebTideObj, tilesKeysIdsTuple)

      sys.stdout.write("INFO "+methID+" end for serial exec.\n")

    #---
    #sys.stdout.write("INFO "+methID+" end\n")

    #--- Return(?) the calling method to control the exec. of all the started threads.
    #return tuple(multiProcsInstances)

  #---
  def produceTilesOutputs( self,
                           TidalPrdFactoryObj: TidalPrd,
                           DataSetId: str,
                           WebTideObj: WebTide,
                           TilesKeysIdsTuple: tuple,
                           InfoLog: bool = False,
                           WarningsLog: bool = False) :
    """
    Method dealing both with the computation of the WebTide tidal predictions and with
    the S111 & S104 tiled output data files production with those tidal predictions after
    they have been computed.

    TidalPrdFactoryObj : The TidalPrd object going with the WebTide dataset object WebTideObj.

    DataSetId : The string id. of the regional dataset from which the WebTideObj was created.

    WebTideObj : The WebTide object holding the tiled input data of a regional dataset.

    TilesKeysIdsTuple : A tuple holding the string keys ids. of the WebTide data tiles
    to use for the tidal predictions.

    InfoLog <OPTIONAL,default==False> : To put(or not to) log INFO messages on the stdout file stream.

    WarningsLog <OPTIONAL,default==False> To put(or not to) log WARNING messages on the stdout file
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + str(" method:")

    #--- Get the thread string id. as an uanry tuple for (possible) messages log.
    thPrId= ( str(multiprocessing.current_process()) ,)

    if InfoLog :
      sys.stdout.write("INFO "+methID+" Start, thread process id="+thPrId[0]+"\n")

    ##--- Uncomment for debugging:
    #if TidalPrdFactoryObj is None :
    #  sys.exit("ERROR "+methID+
    #           " TidalPrdFactoryObj is None !, thread process id="+thPrId[0]+"\n")
    ##---

    ##--- Uncomment for debugging
    #if DataSetId is None :
    #  sys.exit("ERROR "+methID+" DataSetId is None !, thread process id="+thPrId[0]+"\n")

    ##--- Uncomment for debugging
    #if WebTideObj is None :
    #  sys.exit("ERROR "+methID+" WebTideObj is None !, thread process id="+thPrId[0]+"\n")

    ##--- Uncomment for debugging
    #if TilesKeysIdsTuple is None :
    #  sys.exit("ERROR "+methID+" TilesKeysIdsTuple is None !, thread process id="+thPrId[0]+"\n")

    ##--- Uncomment for debugging
    #if self._sFMTFactoryObj is None :
    #  sys.exit("ERROR "+methID+" self._sFMTFactoryObj is None !, thread process id="+thPrId[0]+"\n")

    ##--- Uncomment for debugging
    #if self._sFMTFactoryObj._minNbPointsPerTile is None :
    #  sys,exit("ERROR "+methID+
    #           " self._sFMTFactoryObj._minNbPointsPerTile is None !, thread process id="+thPrId[0]+"\n")
    ##---

    ##--- Uncomment for debugging
    #if WebTideObj._tilesWithData is None :
    #  sys.exit("ERROR "+methID+" WebTideObj._tilesWithData is None !\n")

    #--- Local shortcut tp the SFMTFactory object:
    sFMTFactoryObj= self._sFMTFactoryObj

    if InfoLog :
      sys.stdout.write("INFO "+methID+" Got -> "+
                       str(len(TilesKeysIdsTuple))+
                       " tiles to process for dataset -> "+
                       DataSetId+", thread process id="+thPrId[0]+"\n")
    #---

    #--- Loop on all tiles string keys ids. in TilesKeysIdsTuple
    for tileId in TilesKeysIdsTuple :

      #--- Get the tile dictionary from WebTideObj._tilesWithData:
      tileDict= WebTideObj._tilesWithData[tileId]

      #--- Unlikely to happen but checked anyways:
      if self.POINTS_DATAIN_ID[0] not in tileDict :

        if WarningsLog :
          sys.stdout.write("WARNING "+methId+
                           " No points data dictionary found for the tile -> "+
                           tileId+" with the dataset -> "+
                           DataSetId+"  skipping this tile  tile !\n")
        #---

        continue
      #--- end outer if block.

      #--- Check if tile have the minimum number of points for output:
      nbPoints= len( tileDict[ self.POINTS_DATAIN_ID[0] ])

      #--- Skip tile if not enough points in it:
      #    NOTE: self._sFMTFactoryObj._minNbPointsPerTile is an unary tuple.
      if nbPoints < sFMTFactoryObj._minNbPointsPerTile[0] :

        if WarningsLog :
          sys.stdout.write("WARNING "+methId+" No enough data points -> "+
                           str(nbPoints)+" for tile -> "+tileId+" need at least -> "+
                           str(sFMTFactoryObj._minNbPointsPerTile[0]) +" points, skipping this tile  !\n")
        continue
      #--- end if block.

      #if tileDict[ S102.LEVEL_ID[0] ] == TILES_LEVEL2_ID[0] \
      #   and WebTideObj._self._fieldsVarsType ==
      #   and tileDict[ self.TILES_NEXT_LEVEL_ID[0] ] == None :
      #
      # #if WarningsLog :
      #    sys.stdout.write("WARNING "+methId+" No enclosed level 5 tile inside level 2 tile -> "+
      #                     tileId+" No need to produce water levels for this tile  !\n")
      #
      #  continue

      if InfoLog :
        sys.stdout.write("INFO "+methID+
                          " Doing tidal predictions computations for tile -> "+
                          tileId+" with dataset -> "+
                          DataSetId+", thread process id="+thPrId[0]+"\n")
      #---

      #--- Compute all time stamped tiled predictions for the tile being processed:
      checkRet= self.getPredictionsForTile( TidalPrdFactoryObj,
                                            WebTideObj,
                                            tileId,
                                            tileDict,
                                            self._dateTimeStringsIdxDict )
      #--- Check checkRet:
      if checkRet is not None :

        if InfoLog :
          sys.stdout.write("INFO "+methID+
                           " Done with tidal predictions computations for tile -> "+
                           tileId+" with dataset -> "+DataSetId+
                           ", thread process id="+thPrId[0]+"\n")

          sys.stdout.write("INFO "+methID+
                           " Now writing tidal predictions for tile -> "+
                           tileId+" with dataset -> "+DataSetId+
                           ", thread process id="+thPrId[0]+"\n")
         #--- end inner if

        #--- Write the new tidal predictions S111 and-or S104 products:
        sFMTFactoryObj.writeTileDHProduct( tileId,
                                           tileDict,
                                           self._dateTimeStringsOutDict,
                                           DataSetId,
                                           True,
                                           False,
                                           InfoLog )

        if InfoLog :
          sys.stdout.write("INFO "+methID+
                           " Done with tidal predictions output for for tile -> "+
                           tileId+" with dataset -> "+DataSetId+
                           ", thread process id="+thPrId[0]+"\n")
        #---

      else :

        if WarningsLog :
          sys.stdout.write("WARNING "+methID+
                           " Nothing to write for tile -> "+tileId+
                           " with dataset -> "+DataSetId+
                           ", thread process id="+thPrId[0]+"\n")
        #---
      #--- end inner if-else block.

      #--- Allow the garbage collector to assign the now useless memory of
      #    tileDict to something else.
      tileDict= None

      #--- end outer if block.
    #--- end for loop block.

    if InfoLog :
      sys.stdout.write("INFO "+methID+" end, thread process id="+thPrId[0]+"\n")
    #---

  #---
  def setupOutputObjects(self,
                         ProductType: str) :

    """
    Do the setup of S111 and-or S104 output objects. Method which overrides
    super-class SFMTModelFactory setupOutputObjects method.

    ProductType : Currents or Water levels string id.

    TODO: It seems to be possible to move all that method to the super-class
    with adding an argument to this method to pass as the 5th argument
    to the S111DataCodingFmt3 and S104DataCodingFmt3 methods
    """

    methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + str(" method:")

    sys.stdout.write("INFO "+methID+" start, ProductType -> "+ProductType+"\n")

    #--- Shortcut to the SFMTFactory object:
    sFMTFactoryObj= self._sFMTFactoryObj

    superShortCut= super(WebTideOutput,self)

    #--- Invoke super-class setupOutputObjects method for some generic processing.
    superShortCut.setupOutputObjects(ProductType)

    #--- Invoke super-class generic setupDCFmt3OutputObjects with the proper arguments.
    superShortCut.setupDCFmt3OutputObjects( ProductType,
                                            sFMTFactoryObj.TYPES_OF_DATA[ self.ASTRO_PRED_ID[0] ],
                                            ISFMT.WEBTIDE_STR_ID[0] )

    sys.stdout.write("INFO "+methID+" end\n")

  #---
