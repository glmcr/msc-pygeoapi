#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/util/MultiProcFactory.py
# Creation        : Octobre/Octobre 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.util.MultiProcFactory implementation.
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
#==============================================================================

#--- Do not allow relative imports.
from __future__ import absolute_import

#--- Built-in modules.
import os
import sys
import inspect
import multiprocessing

#---
class MultiProcFactory(object) :

  """
  Parallelization (with multiprocessing module) utility class for providing
  methods used in the context of the SFMT DHP data files creation.
  """

  #---
  def __init__(self) :
    pass

  #---
  @staticmethod
  def joinAndCheckForErrors(MultiProcObjects) :

    """
    Tell the main process to wait for a bunch of multiprocessing objects to finish their jobs
    before resuming sequential execution.

    MultiProcObjects (type->tuple) : A tuple holding a variable number of multiprocessing objects.

    return (type->boolean) : False when success(i.e. no errors to report), True otherwise.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #: Doc Tell the main process to wait for all other processes to
    #      finish before doing something else serially.
    for mpObj in MultiProcObjects :
      mpObj.join()
    #---

    #; Doc We are back to serial exec. at this point.

    errors2Report= False

    #: Doc Now check if a multiprocessing object reports an exec. error.
    for mpObj in MultiProcObjects :

      #: Doc Errors are signaled with mpObj.exitcode != 0
      if mpObj.exitcode != 0 :

        #: Doc One of the multiprocessing objects had a SNAFU.
        errors2Report= True

        #sys.stderr.write("ERROR "+methID+" multiprocessing object -> "+
        #                 str(mpObj.pid)+" failed with exitcode -> "+str(mpObj.exitcode)+" !\n")
        break
     #--- end inner if block

    #--- end for loop block.

    return errors2Report

  #---
  @staticmethod
  def getKeysSubsets(NbCoresPerNode, NbMultiProcesses, DictKeysTuple) :

    """
    Build and return a tuple holding subsets of string keys ids. that will be used to
    parallelize the SFMT DHP data files creation with the multiprocessing module process method.

    NbCoresPerNode (type->int): The number of cores-cpus on a single machine node.

    NbMultiProcesses (type->int): The number of multiprocessing objects to use
    for the parallelization.

    DictKeysTuple (type->dictionary): A tuple holding the keys of the dictionary that will be
    splitted between the multi processes.

    return (type->tuple): A tuple holding the dictionary keys subsets as lists.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    if NbCoresPerNode is None :
      sys.exit("ERROR "+methID+" NbCoresPerNode is None !\n")

    #--- Seems odd but we never know.
    if NbCoresPerNode <= 0 :
      sys.exit("ERROR "+methID+" NbCoresPerNode <= 0 !\n")

    if NbMultiProcesses is None :
      sys.exit("ERROR "+methID+" NbMultiProcesses is None !\n")

    #--- It's an error when NbMultiProcesses <= 1 :
    if NbMultiProcesses <= 1 :
      sys.exit("ERROR "+methID+" NbMultiProcesses <= 1 !\n")

    if DictKeysTuple is None :
      sys.exit("ERROR "+methID+" DictKeysTuple is None !\n")

    #: Doc Verify if the NbMultiProcesses is compatible with NbCoresPerNode
    #: If not then just put issue WARNING on stdout and set the NbMultiProcesses to NbCoresPerNode.

    #--- NOTE: We can have more NbMultiProcesses than NbCoresPerNode but it could(most of the time)
    #          degrade the performance.
    if NbMultiProcesses > NbCoresPerNode :
      sys.stdout.write("WARNING "+methID+
                       " NbMultiProcesses > NbCoresPerNode, setting NbMultiProcesses to NbCoresPerNode \n")

      NbMultiProcesses= NbCoresPerNode
    #---

    sys.stdout.write("INFO "+methID+" Using "+ str(NbMultiProcesses) +" multi-process(es)\n")

    #: Doc Prepare the keys ids lists subsets for the multi processes:
    dictKeysSubsets= []

    #: Doc Loop on the NbMultiProcesses to create the dictionary keys subsets.
    for process in tuple( range(0, NbMultiProcesses) ) :

      #: Doc Create an empty list for each process for now:
      dictKeysSubsets.append( [] )

    #: Doc process number counter to set processes ids.:
    process= 0

    #: Doc Populate keys ids lists subsets for each parallel multiprocess
    #      object. The key ids are successively added to one of the multiprocess
    #      objects ids list to get equi-partitions lists of key ids.(except
    #      for the last multiprocess object in case we have an odd number of
    #      keys) between all the available multiprocess objects used.
    for key in DictKeysTuple :

      #: Doc assign the dictionary key to a multiprocessing object.
      dictKeysSubsets[process].append(key)

      #: Doc Update the multiprocess object number according to its current value.
      if process == NbMultiProcesses-1 : process= 0
      else : process += 1

    #: Doc Return the dictionary keys subsets(as a tuple) to the caller:
    return tuple(dictKeysSubsets)

  #---
  @staticmethod
  def getTupleSubsets(NbCoresPerNode, NbMultiProcesses, ATuple) : #NbTupleItems)

    """
    Split items of a tuple in tuples subsets that will be used with the multiprocessing module.

    NbCoresPerNode (type->int): The number of cores-cpus on a single machine node.

    NbMultiProcesses (type->int): The number of multiprocessing objects to use
    for the parallelization.

    ATuple (type->tuple): The tuple which we want to split.

    return (type->dictionary): A dictionary holding the tuples subsets and using
    multiprocessing integer ids. as keys.
    """

    methID= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    if NbCoresPerNode is None :
      sys.exit("ERROR "+methID+" NbCoresPerNode is None !\n")

    #--- Seems odd but we never know.
    if NbCoresPerNode <= 0 :
      sys.exit("ERROR "+methID+" NbCoresPerNode <= 0 !\n")

    if NbMultiProcesses is None :
      sys.exit("ERROR "+methID+" NbMultiProcesses is None !\n")

    #--- It's an error when NbMultiProcesses <= 1 :
    if NbMultiProcesses <= 1 :
      sys.exit("ERROR "+methID+" NbMultiProcesses <= 1 !\n")

    if ATuple is None :
      sys.exit("ERROR "+methID+" ATuple is None !\n")

    if len(ATuple) <= 2*NbMultiProcesses :
      sys.exit("ERROR "+methID+" len(ATuple) <= 2*NbMultiProcesses !\n")

    #: Doc Verify if the NbMultiProcesses is compatible with NbCoresPerNode.
    #: If not then just put issue WARNING on stdout and set the NbMultiProcesses to NbCoresPerNode.

    #--- NOTE: We can have more NbMultiProcesses than NbCoresPerNode but it could(most of the time) 
    #          degrade the performance.
    if NbMultiProcesses > NbCoresPerNode :
      sys.stdout.write("WARNING "+methID+
                       " NbMultiProcesses > NbCoresPerNode, setting NbMultiProcesses to NbCoresPerNode \n")

      NbMultiProcesses= NbCoresNode

    #--- End block if NbMultiProcesses > NbCoresPerNode

    sys.stdout.write("INFO "+methID+" start, using "+ str(NbMultiProcesses) +" multi-processes\n")

    tupleSubsetsDict= {}

    nbTupleItems= len(ATuple)

    #: Doc Compute the nb. of tuple items ranges relative to the nb of
    #      multiprocessing objects.
    nbIndicesRanges= int(nbTupleItems/NbMultiProcesses)

    #: Doc Keep track of the previous upper bound index for sub-tuples indices ranges.
    prevUpperBnd= 0

    #: Doc Loop on the NbMultiProcesses wanted(need to subtract 1 from 
    #      NbMultiProcesses for the loop range to get the right indices mappings)
    for proc in tuple(range(0, NbMultiProcesses-1)) :

      upperBnd= nbIndicesRanges*(proc+1)

      #: Doc Extract(tuple slicing) the tuple subset between prevUppedBnd and upperBnd and assign
      #      (indexed by the multiprocessing objects integer keys)its contents to the returned dictionay
      tupleSubsetsDict[proc]= ATuple[prevUpperBnd : upperBnd]

      #: Doc Update the previous upper bound index for the next loop iteration.
      prevUpperBnd= upperBnd

    #--- end for loop block.

    #: Doc Need to assign the last tuple subset at NbMultiProcesses-1 index outside the loop.
    tupleSubsetsDict[NbMultiProcesses-1]= ATuple[prevUpperBnd : nbTupleItems]

    sys.stdout.write("INFO "+methID+" end\n")

    return tupleSubsetsDict
