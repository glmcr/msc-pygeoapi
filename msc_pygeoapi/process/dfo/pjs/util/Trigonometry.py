#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : util/Trigonometry.py
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
from msc_pygeoapi.dfo.util.Vector2D import Vector2D
from msc_pygeoapi.process.dfo.util.ITrigonometry import ITrigonometry

#--- TODO: Rename class Trigonometry as Trigo to be more "Pythonic" ?
class Trigonometry(ITrigonometry) :

    """
    Utility class implementing various generic
    trigonometric operations.
    """

    def __init__(self) :

        ITrigonometry.__init__(self)

        #--- Use a namedtuple for self._2DrotationMethods ?

        #--- Define 2D vector components rotation
        #    methods in a dictionary attribute.
        self._2DRotationMethods= {
             self.COUNTER_CLOCKWISE_ROT_ID[0] :
                 Trigonometry.rotateComponentsCounterClockWise
        }

        #--- Clock wise rotation method not implemented yet
        #self._2DRotationMethods= {
        #    self.CLOCKWISE_ROT_ID[0] :
        #        Trigonometry.rotateComponentsClockWise,
        #    self.COUNTER_CLOCKWISE_ROT_ID[0] :
        #        Trigonometry.rotateComponentsCounterClockWise
        #}

        #--- TODO: Move this static method in a TrigonometryFactory class
        #          to improve code modularization ?
        @staticmethod
        def doubleSandwich( d1: float,
                            d2: float,
                            d3: float ) -> bool:
        """
        d1 (type->float): Lower bound of the double precision
        range(a.k.a. the sandwich).

        d2 (type->float): The double precision value to check
        if it's inside the double precision range.

        d3 (type->float): Upper bound of the double
        precision range.

        returns (type->bool) : True if if we have d1 <= d2 <= d3
        i.e. d1 is clamped(sandwiched) between d2 and d3 or if
        d1 == d2 or d2 == d3 otherwise return False.
        """

        #---
        return ( ( ( d2 - d1) * ( d2 - d3 ) ) <= 0.0 )

    #---
    def getMeteoAngle( self,
                       IComponent: float,
                       JComponent: float) -> float :
        """
        Compute the meteorological angle(used also
        in physical oceanography numerical modelling)
        i.e. the 0-359.9 decimal degrees direction
        from which the currents or winds are coming
        from.

        IComponent (type->float): The I component of a vector.

        JComponent (type->float): The J component of a vector.

        return (type->float): The meteorological angle of the
        (I,J) )vector
        """

        return self.PI_DEGREES[0] + \
                   self.RADIANS_2_DEGREES[0] * \
                       math.atan2(IComponent,JComponent)
    #---
    def getNavigAngle( self,
                       IComponent: float,
                       JComponent: float ) -> float :
        """
        Compute the navigation angle used by mariners
        i.e. the 0-359.9 decimal degrees direction to
        which the currents or winds are going to.
        Just need to subtract or add 180.0 to the
        meteorological angle direction to get the
        navigation angle.

        IComponent (type->float): The I component of a vector.

        JComponent (type->float): The J component of a vector.

        return (type->float): The navigation angle of
        the (I,J) )vector
        """

        #: Doc Need to compute the meteorological angle first.
        meteoAngle= self.getMeteoAngle(IComponent,JComponent)

        #: Doc Need to check for meteo angle > 180.0
        if meteoAngle > self.PI_DEGREES[0] :

            ret= meteoAngle - self.PI_DEGREES[0]
        else :
            ret= self.PI_DEGREES[0] + meteoAngle;

        return ret

    #---
    @staticmethod
    def getUVComponentsFromVelDir( VelInMetersSec: float,
                                   NavAngleInRads: float) -> float:
        """
        Returns the U,V (West->East, South->North) current(or wind)
        components pair corresonding to a (velocity,navigation angle)
        pair.

        VelInMetersSec (type->float): A positive current(or wind)
        velocity in meters/seconds.

        NavAngleInRads (type->float): A positive navigation angle
        (i.e where the flow goes) in radians for the direction
        of the current(or wind).

        return (type->tuple of 2 type->float) U,V current(or wind)
        components pair.

        NOTE: No fool-proof check if VelInMetersSec and
        NavAngleInRads arguments values are valid(need
        to be >= 0.0).
        """

        #---
        return ( VelInMetersSec * math.sin(NavAngleInRads),  #--- U
                 VelInMetersSec * math.cos(NavAngleInRads) ) #--- V


    #---
    def getZero2PiSandwich( self,
                            AngleInRads: float) -> float:
        """
        Method which clamps a angle in radians between 0
        and 2PI.

        AngleInRads (type->float): The angle in radians
        to be clamped between 0 and 2PI.

        returns (type->float): The corresponding angle
        in radians clamped between 0 and 2PI.

        Remark: Obviously the angle in radians stays
        the same if it is already clamped between 0
        and 2PI.
        """

        newRad= AngleInRads;
        fabsRad= math.fabs(AngleInRads)

        if not Trigonometry.doubleSandwich( 0.0,
                                            AngleInRads,
                                            self.TWO_PI[0] ) :

            #--- More perf. with a multiplication than
            #    with a division.
            #intFact= int(math.floor(fabsRad/self.TWO_PI[0]))
            intFact= int(math.floor(fabsRad * self.TWO_PI_INV[0]))

            if intFact == 0 :
                newRad= self.TWO_PI[0] - fabsRad ;

            else :
                newRad= fabsRad - ( float(intFact) * self.TWO_PI[0] )

                #: Doc Check for negative AngleInRadians argument
                if AngleInRadians < 0.0 :
                    newRad= self.TWO_PI[0] - newRad
                #---

            #--- end inner if-else
        #--- end outer if.

        return newRad


    #---
    def getZero2PiSandwichWithConv( self,
                                    Angle: float,
                                    ConvCycles2Radians: bool) -> float :
        """
        Method which clamps a angle which could be expressed
        in cycles between 0 and 2PI.

        Angle (type->float): The angle in radians(or cycles)
        to be clamped between 0 and 2PI.

        ConvertCycles2Radians (type->boolean): The conversion
        flag to do the convserion from cycles to radians before
        using method self.getZero2PiSandwich.

        returns (type->float): The corresponding angle in
        radians clamped between 0 and 2PI.

        (NOTE: Just used by M. Foreman's tidal method up to now)
        """

        if ConvCycles2Radians :
            ret= self.getZero2PiSandwich(self.CYCLES_2_RADIANS[0]*Angle)
        else :
            ret= self.getZero2PiSandwich(Angle)

        return ret

    #--- TODO: Rename the following method with
    #    a slightly shorter name to comply with
    #    the "Pythonic" PEP8 standard.
    @staticmethod
    def rotateComponentsCounterClockWise( CosAngleRot: float,
                                          SinAngleRot: float,
                                          Vec2DObj: Vector2D ) -> Vector2D:
        """
        Do a counter clockwise Rotation of the cartesian components
        of a Vector2D object with a cos,sin combo.

        CosAngleRot (type->float): The cosinus of the rotation angle.

        SinAngleRot (type->float): The sinus of the rotation angle.

        Vec2DObj (type->Vector2D) : The Vector2D object to rotate.

        return (type->Vector2D) : The rotated Vector2D object.

        ASCII art depicting the matrix rotation operation :

        | rvI | = | CosAngleRot -SinAngleRot | | vI |
        | rvJ |   | SinAngleRot  CosAngleRot | | vJ |


        TODO: Add a clockwise rotation @staticmethod
        """

        tmpIComp= Vec2DObj._iComp
        tmpJComp= Vec2DObj._jComp

        Vec2DObj._iComp= CosAngleRot*tmpIComp - SinAngleRot*tmpJComp
        Vec2DObj._jComp= SinAngleRot*tmpIComp + CosAngleRot*tmpJComp

        return Vec2DObj

    #---
