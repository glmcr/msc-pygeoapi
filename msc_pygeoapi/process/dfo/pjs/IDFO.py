#--- TODO: Add src file header here !!!
#

import enum

#---
class IDFO(object):

   #--- Could add other specific DFO data types in _DATA_TYPES
   _DATA_TYPES= enum.Enum( str("data_types"),
                           [ str("water_levels"), str("currents") ])

   #---
   def __init__(self):
       pass
