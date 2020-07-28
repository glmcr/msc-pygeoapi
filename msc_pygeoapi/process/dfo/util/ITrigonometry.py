#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : msc-pygeoapi DFO-CHS-ENAV-DHP process plugin
# File/Fichier    : util/ITrigonometry.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class util.Trigonometry implementation.
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
import math

#---
from msc_pygeoapi.process.dfo.util.ITimeMachine import ITimeMachine

#---
class ITrigonometry(ITimeMachine) :

    """
    Defines some constants(a.k.a. variables that
    are not allowed to vary) parameters values
    used by its sub class Trigonometry or any
    other class inheriting from it. Need to
    use unary tuples to do so.
    """

    def __init__(self) :

        ITimeMachine.__init__(self)

        self.PI_DEGREES= ( 180.0 ,)
        self.TWO_PI_DEGREES= ( 2.0*self.PI_DEGREES[0] ,)
        self.TWO_PI_DEGREES_INV= ( 1.0/self.TWO_PI_DEGREES[0] ,)

        self.TWO_PI= ( 2.0*math.pi ,)
        self.TWO_PI_INV= ( 1.0/self.TWO_PI[0], )

        self.DEGREES_2_RADIANS= ( math.pi/self.PI_DEGREES[0] ,)
        self.RADIANS_2_DEGREES= ( 1.0/self.DEGREES_2_RADIANS[0] ,)

        self.CYCLES_2_RADIANS= ( self.TWO_PI[0], )

        #: Doc Cycles per hour to radians per seconds conversion
        #  factor. (NOTE: Just used by M. Foreman's tidal method
        #  up to now)
        self.CYCLES_HOUR_2_RADIANS_SECONDS= \
           ( self.TWO_PI[0]/float(self.SECONDS_PER_HOUR[0]) ,)

        self.CLOCKWISE_ROT_ID= ( str("Clockwise") ,)
        self.COUNTER_CLOCKWISE_ROT_ID= ( str("CounterClockwise") ,)
