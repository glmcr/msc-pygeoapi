#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/astro/foreman/SunMoonEphemeridesFactory.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.astro.foreman.SunMoonEphemeridesFactory implementation.
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

#---
import sys
import math
import time
import inspect

#---
from msc_pygeoapi.process.dfo.util.TimeMachine import TimeMachine
from msc_pygeoapi.process.dfo.tidal.astro.foreman.IForeman import IForeman

#---
class SunMoonEphemeridesFactory(IForeman,TimeMachine) :

   """
   Class mainly used to define the Sun&Moon astronomic ephemerides parameters
   and also to try to get a better modularization.

   TODO: Use the underscore prefix for all attributes ?
   """

   def __init__(self) :

     IForeman.__init__(self)
     TimeMachine.__init__(self)

     methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

     #--- Constants used in self.set method(see below)
     #
     #    NOTE: The original fortran code of M. Foreman uses divisions for the
     #          computations of these parameters just once which is ok if we do
     #          not have to udpate astronomic ephemerides parameters in processing
     #          loops. Here we use multiplictions since the Sun&Moon ephemerides
     #          could be updated at every 1 hour offsets by the set method of the
     #          sub class SunMoonEphemerides and consequently we need performance
     #          (i.e. divisions are way more expensive for cpu loading than multiplications)

     self.ASTRO_F1_INV= ( self.TWO_PI_DEGREES_INV[0] ,)

     self.ASTRO_F2_INV= ( self.DAYS_PER_NORMAL_YEAR[0]*self.ASTRO_F1_INV[0] ,)

     #--- Flag for checking the state of the object.
     self.ready2Use= False

     """
     self.sunH:  Mean longitude of the sun.
     """

     self.sunH= None

     """
     self.sunDH: 1st time derivative of sunH
     """

     self.sunDH= None

     """
     self.sunPP: Mean longitude of the solar perigee
     """

     self.sunPP= None

     """
     self.sunDPP: 1st time derivative of self.sunP
     """

     self.sunDPP= None

     """
     self.moonS: Mean longitude of the moon
     """

     self.moonS= None

     """
     self.moonDS: 1st time derivative of moonS
     """

     """
     self.moonDS: 1st time derivative of moonS
     """

     self.moonDS= None

     """
     self.moonP= Mean longitude of the lunar perigee
     """

     self.moonP= None

     """
     1st time derivative of moonP
     """

     self.moonDP= None

     """
     self.meanAscModeNP: Negative of the longitude of the mean ascending node(of the Moon ?)
     """

     self.meanAscModeNP= None

     """
     self.meanAscModeDNP: 1st time derivative of meanAscModeNP.
     """

     self.meanAscModeDNP= None

     """
     self.tau: Lunar time.
     """

     self.tau= None

     """
     self.dTau: Lunar time rate of change(?).
     """

     self.dTau= None
