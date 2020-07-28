#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/astro/foreman/SunMoonEphemerides.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.astro.foreman.SunMoonEphemerides implementation.
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
import math
import time
import inspect

#---
from msc_pygeoapi.process.dfo.tidal.astro.foreman.SunMoonEphemeridesFactory import SunMoonEphemeridesFactory

#---
class SunMoonEphemerides(SunMoonEphemeridesFactory) :

   """
   Compute the astronomic ephemerides parameters for the Foreman tidal prediction method.

   TODO: Use namedtuple objects for the SME constants instead of plain tuple objects.
   """

   #---
   def __init__(self, StaticData, SecondsSinceEpoch= None) :

     SunMoonEphemeridesFactory.__init__(self)

     methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"

     if StaticData is None :
       sys.exit("ERROR "+methID+" StaticData is None !\n")

     #--- Init. all the static data used in the dynamic computations
     #    (see the set method below) for the astronomic ephemerides parameters.

     #--- Set the static data shortcut reference for static data access.
     self.__static= StaticData[ self.SME_PARAMS_ID[0] ]

     #--- static data shortcuts:
     self.D1_FACTOR= ( self.__static[self.SME_D1_FACTOR_ID[0] ] ,)

     #--- See IForeman class for self.GREGORIAN_DAY0_SECONDS definition:
     self.GREGORIAN_DAY0_SECONDS= ( self.__static[ self.SME_GREGORIAN_DAY0_SECONDS_ID[0] ] ,)

     """
     self.MOON_EPH_POLY_COEFF_S:
     Coefficients of the polynomial expression used for the computation the mean longitude of the moon.
     """

     self.MOON_EPH_POLY_COEFF_S= tuple(self.__static[ self.SME_MOON_EPH_POLY_COEFF_S_ID[0] ])

     """
     self.MOON_EPH_POLY_COEFF_P:
     Coefficients of the polynomial expression used for the computation the mean longitude of the lunar perigee.
     """

     self.MOON_EPH_POLY_COEFF_P= tuple(self.__static[ self.SME_MOON_EPH_POLY_COEFF_P_ID[0] ])

     """
     self.SUN_EPH_POLY_COEFF_H:
     Coefficients of the polynomial expression used for the computation the mean longitude of the sun.
     """

     self.SUN_EPH_POLY_COEFF_H= tuple(self.__static[ self.SME_SUN_EPH_POLY_COEFF_H_ID[0] ])

     #print str(self.SUN_EPH_POLY_COEFF_H[2])

     """
     self.SUN_EPH_POLY_COEFF_PP:
     Coefficients of the polynomial expression used for the computation the Mean longitude of the solar perigee.
     """

     self.SUN_EPH_POLY_COEFF_PP= tuple(self.__static[ self.SME_SUN_EPH_POLY_COEFF_PP_ID[0] ])

     """
     self.MEAN_ASCMODE_EPH_POLY_COEFF_NP:
     Coefficients of the polynomial expression used for the computation the mean longitude of the negative
     of the longitude of the mean ascending node.
     """

     self.MEAN_ASCMODE_EPH_POLY_COEFF_NP= tuple(self.__static[self.SME_MEAN_ASCMODE_EPH_POLY_COEFF_NP_ID[0]])

     #--- Set the derivatives of the respectives polynomial Coefficients:

     DEG2_DERIVATIVE_FACTOR= self.__static[ self.SME_DEG2_DERIVATIVE_FACTOR_ID[0] ]
     DEG3_DERIVATIVE_FACTOR= self.__static [self.SME_DEG3_DERIVATIVE_FACTOR_ID[0] ]

     """
     self.MOON_EPH_POLY_COEFF_DS:
     1st time derivative of the polynomial expression used for the computation the mean longitude of the moon.
     """

     self.MOON_EPH_POLY_COEFF_DS= tuple( [ self.MOON_EPH_POLY_COEFF_S[1],
                                           DEG2_DERIVATIVE_FACTOR*self.MOON_EPH_POLY_COEFF_S[2],
                                           DEG3_DERIVATIVE_FACTOR*self.MOON_EPH_POLY_COEFF_S[3] ] )
     """
     self.MOON_EPH_POLY_COEFF_DP:
     1st time derivative of the polynomial expression used for the computation the mean longitude of the lunar perigee.
     """

     self.MOON_EPH_POLY_COEFF_DP= tuple( [ self.MOON_EPH_POLY_COEFF_P[1],
                                           DEG2_DERIVATIVE_FACTOR*self.MOON_EPH_POLY_COEFF_P[2],
                                           DEG3_DERIVATIVE_FACTOR*self.MOON_EPH_POLY_COEFF_P[3] ] )

     """
     self.SUN_EPH_POLY_COEFF_DH:
     1st time derivative of the polynomial expression used for the computation the mean longitude of the sun.
     """

     self.SUN_EPH_POLY_COEFF_DH= tuple( [ self.SUN_EPH_POLY_COEFF_H[1],
                                          DEG2_DERIVATIVE_FACTOR* self.SUN_EPH_POLY_COEFF_H[2] ] )

     """
     self.SUN_EPH_POLY_COEFF_DPP:
     1st time derivative of the polynomial expression used for the computation the Mean longitude of the solar perigee.
     """

     self.SUN_EPH_POLY_COEFF_DPP= tuple( [ self.SUN_EPH_POLY_COEFF_PP[1],
                                           DEG2_DERIVATIVE_FACTOR*self.SUN_EPH_POLY_COEFF_PP[2],
                                           DEG3_DERIVATIVE_FACTOR*self.SUN_EPH_POLY_COEFF_PP[3] ] )
     """
     self.MEAN_ASCMODE_EPH_POLY_COEFF_DNP:
     1st time derivative of the polynomial expression used for the computation the mean longitude of the negative
     of the longitude of the mean ascending node(of the Moon???).
     """

     self.MEAN_ASCMODE_EPH_POLY_COEFF_DNP= tuple( [ self.MEAN_ASCMODE_EPH_POLY_COEFF_NP[1],
                                                    DEG2_DERIVATIVE_FACTOR*self.MEAN_ASCMODE_EPH_POLY_COEFF_NP[2],
                                                    DEG3_DERIVATIVE_FACTOR*self.MEAN_ASCMODE_EPH_POLY_COEFF_NP[3] ])
     #--- Could set self attributes here.
     if SecondsSinceEpoch is not None :
       self.set(SecondsSinceEpoch)

   #---
   def clear(self) :

     self.ready2Use= False

     self.tau= self.dTau= self.sunH= self.sunDH= 0.0
     self.sunPP= self.sunDPP= self.moonS= self.moonDS= 0.0
     self.moonP= self.moonDP= self.meanAscModeNP= self.meanAscModeDNP= 0.0

   #---
   def set(self, SecondsSinceEpoch) :

     """
     Compute the dynamic data of the astronomic ephemerides parameters according to the SecondsSinceEpoch argument.

     SecondsSinceEpoch (type->long int): Seconds since the epoch used to set dynamic data of the astronomic ephemerides parameters.
     """

     #--- Uncomment for debugging
     #methID= str(__name__)+"."+ str(inspect.stack()[0][3]) + " method:"
     #if SecondsSinceEpoch is None :
     # sys.exit("ERROR "+thisMethod+" method: SecondsSinceEpoch is None !\n")

     #if SecondsSinceEpoch <= 0 :
     # sys.exit("ERROR "+thisMethod+" method: Invalid SecondsSinceEpoch ->"+str(SecondsSinceEpoch) +" !\n")

     self.clear()

     #--- Local constants(i.e. do not modify it after defining it!)

     """
     ASTRO_D1: The number of days elapsed since December 31 1899 at 12:00:00UTC
     """

     #ASTRO_D1= ForemanFactory.getAstroD1(SecondsSinceEpoch)
     ASTRO_D1= ( self.SECONDS_PER_DAY_INV[0] * (SecondsSinceEpoch + self.GREGORIAN_DAY0_SECONDS[0]) ,)

     #print "ASTRO_D1="+str(ASTRO_D1)
     #print "self.ASTRO_F2_INV[0]="+str(self.ASTRO_F2_INV[0])
     #print "self.SUN_EPH_POLY_COEFF_DPP[0]="+str(self.SUN_EPH_POLY_COEFF_DPP[0])
     #print "self.SUN_EPH_POLY_COEFF_DPP[1]="+str(self.SUN_EPH_POLY_COEFF_DPP[1])
     #print "self.SUN_EPH_POLY_COEFF_DPP[2]="+str(self.SUN_EPH_POLY_COEFF_DPP[2])

     ASTRO_D1_SQUR= ( ASTRO_D1[0] * ASTRO_D1[0] ,)

     #---
     ASTRO_D2= ( self.D1_FACTOR[0] * ASTRO_D1[0] ,)
     ASTRO_D2_SQUR= ( ASTRO_D2[0] * ASTRO_D2[0] ,)
     ASTRO_D2_CUBE= ( ASTRO_D2[0] * ASTRO_D2_SQUR[0] ,)

     #sys.stdout.write("SecondsSinceEpoch="+str(SecondsSinceEpoch)+"\n")
     #sys.stdout.write("ASTRO_D1="+str(ASTRO_D1)+"\n")
     #sys.stdout.write("ASTRO_D2="+str(ASTRO_D2)+"\n")

     self.sunH= self.ASTRO_F1_INV[0]*(self.SUN_EPH_POLY_COEFF_H[0] +
                                      ASTRO_D1[0]*self.SUN_EPH_POLY_COEFF_H[1] +
                                      ASTRO_D2_SQUR[0]*self.SUN_EPH_POLY_COEFF_H[2])

     #--- Need the fractional part only:
     self.sunH -= math.floor(self.sunH)

     self.sunPP= self.ASTRO_F1_INV[0] * (self.SUN_EPH_POLY_COEFF_PP[0] +
                                         ASTRO_D1[0]*self.SUN_EPH_POLY_COEFF_PP[1] +
                                         ASTRO_D2_SQUR[0]*self.SUN_EPH_POLY_COEFF_PP[2] +
                                         ASTRO_D2_CUBE[0]*self.SUN_EPH_POLY_COEFF_PP[3])

     #--- Need the fractional part only:
     self.sunPP -= math.floor(self.sunPP)

     self.sunDH= self.ASTRO_F2_INV[0] * (self.SUN_EPH_POLY_COEFF_DH[0] +
                                         ASTRO_D1[0]*self.SUN_EPH_POLY_COEFF_DH[1] )

     self.sunDPP= self.ASTRO_F2_INV[0] * (self.SUN_EPH_POLY_COEFF_DPP[0] +
                                          ASTRO_D1[0]*self.SUN_EPH_POLY_COEFF_DPP[1] +
                                          ASTRO_D1_SQUR[0]*self.SUN_EPH_POLY_COEFF_DPP[2])

     self.moonS= self.ASTRO_F1_INV[0] * ( self.MOON_EPH_POLY_COEFF_S[0] +
                                          ASTRO_D1[0]*self.MOON_EPH_POLY_COEFF_S[1] +
                                          ASTRO_D2_SQUR[0]*self.MOON_EPH_POLY_COEFF_S[2] +
                                          ASTRO_D2_CUBE[0]*self.MOON_EPH_POLY_COEFF_S[3] )

     #--- Need the fractional part only:
     self.moonS -= math.floor(self.moonS)

     self.moonP= self.ASTRO_F1_INV[0] * (self.MOON_EPH_POLY_COEFF_P[0] +
                                         ASTRO_D1[0]*self.MOON_EPH_POLY_COEFF_P[1] +
                                         ASTRO_D2_SQUR[0]*self.MOON_EPH_POLY_COEFF_P[2] +
                                         ASTRO_D2_CUBE[0]*self.MOON_EPH_POLY_COEFF_P[3] )

     #--- Need the fractional part only:
     self.moonP -= math.floor(self.moonP)

     self.moonDS= self.ASTRO_F2_INV[0] * (self.MOON_EPH_POLY_COEFF_DS[0] +
                                          ASTRO_D1[0]*self.MOON_EPH_POLY_COEFF_DS[1] +
                                          ASTRO_D1_SQUR[0]*self.MOON_EPH_POLY_COEFF_DS[2] )

     self.moonDP= self.ASTRO_F2_INV[0] * (self.MOON_EPH_POLY_COEFF_DP[0] +
                                          ASTRO_D1[0]*self.MOON_EPH_POLY_COEFF_DP[1] +
                                          ASTRO_D1_SQUR[0]*self.MOON_EPH_POLY_COEFF_DP[2] )

     self.meanAscModeNP= self.ASTRO_F1_INV[0] * (self.MEAN_ASCMODE_EPH_POLY_COEFF_NP[0] +
                                                 ASTRO_D1[0]*self.MEAN_ASCMODE_EPH_POLY_COEFF_NP[1] +
                                                 ASTRO_D2_SQUR[0]*self.MEAN_ASCMODE_EPH_POLY_COEFF_NP[2] +
                                                 ASTRO_D2_CUBE[0]*self.MEAN_ASCMODE_EPH_POLY_COEFF_NP[3] )
     #--- Need the fractional part only:
     self.meanAscModeNP -= math.floor(self.meanAscModeNP)

     self.meanAscModeDNP= self.ASTRO_F2_INV[0] * (self.MEAN_ASCMODE_EPH_POLY_COEFF_DNP[0] +
                                                  ASTRO_D1[0]*self.MEAN_ASCMODE_EPH_POLY_COEFF_DNP[1] +
                                                  ASTRO_D1_SQUR[0]*self.MEAN_ASCMODE_EPH_POLY_COEFF_DNP[2] )

     #--- Extract the day hour from SecondsSinceEpoch.
     #    NOTE: self.DATE_TIME_ARRAY_INDICES is a namedtuple(see dhp.util.ITimeMachine class src file).
     dayHour= time.gmtime(SecondsSinceEpoch)[ self.DATE_TIME_ARRAY_INDICES.HOUR ]

     #--- Only the fractional part of a solar day need be retained for computing the lunar time TAU.
     self.tau= self.HOURS_PER_DAY_INV[0]*dayHour + (self.sunH - self.moonS)

     self.dTau= (self.DAYS_PER_NORMAL_YEAR[0] + (self.sunDH - self.moonDS))

     self.ready2Use= True

     #--- Keep track of the time-stamp used to set each SunMoonEphemerides object
     self.SecondsSinceEpoch= SecondsSinceEpoch

     #---- Uncomment for debugging
     #sys.stdout.write("INFO "+methID+" self.sunH="+str(self.sunH)+"\n")
     #sys.stdout.write("INFO "+methID+" self.sunPP="+str(self.sunPP)+"\n")
     #sys.stdout.write("INFO "+methID+" self.sunDH="+str(self.sunDH)+"\n")
     #sys.stdout.write("INFO "+methID+" self.sunDPP="+str(self.sunDPP)+"\n")
     #sys.stdout.write("INFO "+methID+" self.moonS="+str(self.moonS)+"\n")
     #sys.stdout.write("INFO "+methID+" self.moonP="+str(self.moonP)+"\n")
     #sys.stdout.write("INFO "+methID+" self.moonDS="+str(self.moonDS)+"\n")
     #sys.stdout.write("INFO "+methID+" self.moonDP="+str(self.moonDP)+"\n")
     #sys.stdout.write("INFO "+methID+" self.meanAscModeNP="+str(self.meanAscModeNP)+"\n")
     #sys.stdout.write("INFO "+methID+" self.meanAscModeDNP="+str(self.meanAscModeDNP)+"\n")
     #sys.stdout.write("INFO "+methID+" self.tau="+str(self.tau)+"\n")
     #sys.stdout.write("INFO "+methID+" self.dTau="+str(self.dTau)+"\n")
     #sys.stdout.write("INFO "+methID+" exit 0 \n")
     #sys.exit(0)
