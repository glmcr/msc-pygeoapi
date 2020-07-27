#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/util/FilesDirs.py
# Creation        : March/Mars 2019 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.util.FilesDirs implementation.
#
# Remarks :
#
# License :
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
import inspect

#---
class FilesDirs(object) :

  """
  Provide some utility mehods for files and directories handling.
  """

  #---
  def __init__(self) :
    pass

  #---
  @staticmethod
  def createNewSubDir(MainDir, NewSubDirName) :

    """
    Create a new sub-directory in a main directory.

    MainDir (type->string): The main directory where to create the new sub-directory.

    NewSubDirName (type->string): The name of the new sub-directory to create.
    """

    methId= str(__name__)+"."+ str(inspect.stack(0)[0][3]) + " method:"

    #--- Some fool-proof checks:
    if MainDir is None :
      sys.exit("ERROR "+methId+" MainDir is None ! \n")

    if NewSubDirName is None :
      sys.exit("ERROR "+methId+" NewSubDirName is None ! \n")

    if not os.access(MainDir, os.F_OK) :
      sys.exit("ERROR "+methId+
               " main directory(MainDir method arg -> "+MainDir+" should already exists !\n")

    #: Doc Check if NewSubDirName is already defined at the end of MainDir, 
    #      do nothing if it is the case(Note the use of os.sep to get the right directory string separator)
    mainDirSplit= MainDir.split(os.sep)

    #: Doc Reverse the list to get the last directory in the path:
    mainDirSplit.reverse()

    #: Doc Set dirPathRet to MainDir by default:
    dirPathRet= MainDir

    if mainDirSplit[0] != NewSubDirName :
      dirPathRet= MainDir + os.sep + NewSubDirName

    if not os.access(dirPathRet, os.F_OK) :
      sys.stdout.write("INFO "+methId+" Need to create directory ->"+dirPathRet+"\n")
      os.mkdir(dirPathRet)

    return dirPathRet
