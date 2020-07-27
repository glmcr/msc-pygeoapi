#--- TODO: Add src file header here !!!
#

#--- NOTE: Need to be implemented as a generic package.
#          Main idea: Get a rectangular coordinates bounding box
#          and starting and ending timestamps and return a tuple
#          of tidal data(currents or water levels or both) grid
#          points to the calling method.

#---
import msc_pygeoapi.process.dfo.util

#---
_FIELDS_IDS= { _DATA_TYPES.water_levels.name : ( _UVZ_IDS.Z.name, ),
               _DATA_TYPES.currents.name     : ( _UVZ_IDS.U.name, _UVZ_IDS.V.name ) }
