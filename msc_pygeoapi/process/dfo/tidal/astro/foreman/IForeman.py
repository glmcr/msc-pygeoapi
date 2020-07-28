#-*-Python-*-
#
# DFO-MPO/CHS-SHC
# Institut Maurice Lamontagne Institute
#
# Project/Projet  : ENAV-DHP
# File/Fichier    : dhp/tidalprd/astro/foreman/IForeman.py
# Creation        : July/Juillet 2018 - G. Mercier - DFO-MPO/CHS-SHC
#
# Description: - Class dhp.tidalprd.astro.foreman.IForeman implementation. Used like a Java interface.
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
from msc_pygeoapi.process.dfo.tidal.ITidalPrd import ITidalPrd
from msc_pygeoapi.process.dfo.util.ITrigonometry import ITrigonometry

#---
class IForeman(ITidalPrd, ITrigonometry) :

  """
  Defines constants parameters used by this object-oriented
  Python implementation of M. Foreman's tidal prediction
  method(coded originally in the 80s in Fortran in a research
  context).
  """

  """
  JSON_LEGACY_FILE_ID: JSON static input datat string indexing id.
  JSON formatted string id for the definition of the directory path of the legacy
  static tidal astronomic data of M. Foreman's coming with its Fortran package.
  See WebTideS1**ProductsMain.json files in the cfg/Main sub-directory.

  NOTE: Using an unary tuple as it is a constant parameter.
  """
  JSON_LEGACY_FILE_ID= ( str("ForemanLegacyDataFile") ,)

  """
  FACTORY_ID:Dictionary string indexing id. for storing ForemanFactory objects:
  """
  FACTORY_ID= ( str("FACTORY") ,)

  """
  CONST_ASTRO_ID: Dictionary string indexing id. for storing ForemanConstituentAstro objects:
  """
  CONST_ASTRO_ID= ( str("CONST_ASTRO") ,)

  #---
  def __init__(self) :

    ITidalPrd.__init__(self)
    ITrigonometry.__init__(self)

    """
    NOTE: M. Foreman's method algorithm implies that we are only able to update
    astronomic informations at hh:00:00 time stamps in seconds(i.e. only
    for date-times in seconds-since-the-epoch that are multiples of 3600 seconds)
    """
    self.ASTRO_UDPATE_OFFSET_SECONDS= ( self.SECONDS_PER_HOUR[0] ,)

    """
    self.MAIN_CONST_ID: dictionary string indexing id.
    Used for main tidal constituents dictionary indexing.
    """
    self.MAIN_CONST_ID= ( str("MAIN") ,)

    """
    self.SHWT_CONST_ID: dictionary string indexing id.
    Used dor shallow water tidal constituents dictionary indexing.
    """
    self.SHWT_CONST_ID= ( str("SHALLOW_WATER") ,)

    """"
    self.JSON_STATIC_DATA_IDS : JSON static input string indexing ids.
    Used for main and shallow water tidal constituents JSON input indexing:
    """
    self.JSON_STATIC_DATA_IDS= { self.MAIN_CONST_ID[0] : str("MainConstituents"),
                                 self.SHWT_CONST_ID[0] : str("ShallowWaterConstituents") }

    #--- Define a bunch of strings indexing ids. for astro
    #    and sun-moon ephemerides JSON static input data:
    self.ASTRO_PARAMS_ID= ( str("ASTRO_PARAMS") ,)

    self.COS_IDX_ID= ( str("COS_INDEX") ,)
    self.SIN_IDX_ID= ( str("SIN_INDEX") ,)

    self.COS_ACC_INIT_ID= ( str("COS_ACC_INIT") ,)
    self.SIN_ACC_INIT_ID= ( str("SIN_ACC_INIT") ,)

    self.FV_NODAL_ADJ_FLAGS_ID= ( str("FV_NODAL_ADJ_FLAGS") ,)
    self.F_NODAL_MOD_ADJ_INIT_ID= ( str("F_NODAL_MOD_ADJ_INIT") ,)
    self.FV_NODAL_ADJ_CONSTANTS_ID=  ( str("FV_NODAL_ADJ_CONSTANTS"), )
    self.V_ASTRO_PHASE_INT_THRESHOLD_ID= ( str("V_ASTRO_PHASE_INT_THRESHOLD") ,)

    self.SME_D1_FACTOR_ID= ( str("D1_FACTOR") ,)
    self.SME_PARAMS_ID= ( str("SUN_MOON_EPHEMERIDES_PARAMS") ,)

    """
    self.SME_GREGORIAN_DAY0_SECONDS_ID: JSON static input data string indexing id.

    Seconds elapsed between December 31 1899 at 12:00 UTC and the UNIX
    epoch day0 January 1 1970 at 00:00. It is possible to get the same
    result with datetime.date.toordinal() + 366 but obviously it gives
    the same value so just define it once and for all in the JSON static
    parameters definitions file.
    """
    self.SME_GREGORIAN_DAY0_SECONDS_ID= ( str("GREGORIAN_DAY0_SECONDS") ,)

    #--- Another bunch of sun-moon ephemerides for
    #    JSON static input data strings ids. indexing:
    self.SME_MOON_EPH_POLY_COEFF_S_ID= ( str("MOON_EPH_POLY_COEFF_S") ,)
    self.SME_MOON_EPH_POLY_COEFF_P_ID= ( str("MOON_EPH_POLY_COEFF_P") ,)

    self.SME_SUN_EPH_POLY_COEFF_H_ID= ( str("SUN_EPH_POLY_COEFF_H") ,)
    self.SME_SUN_EPH_POLY_COEFF_PP_ID= ( str("SUN_EPH_POLY_COEFF_PP") ,)

    self.SME_MEAN_ASCMODE_EPH_POLY_COEFF_NP_ID= ( str("MEAN_ASCMODE_EPH_POLY_COEFF_NP") ,)

    self.SME_DEG2_DERIVATIVE_FACTOR_ID= ( str("DEG2_DERIVATIVE_FACTOR") ,)
    self.SME_DEG3_DERIVATIVE_FACTOR_ID= ( str("DEG3_DERIVATIVE_FACTOR") ,)

    #--- JSON static input data strings ids. indexing definitions
    #    for main constituents.
    self.MAIN_CONST_SATS_ID= ( str("Satellites") ,)
    self.MAIN_CONST_FREQ_ID= ( str("Frequency") ,)
    self.MAIN_CONST_DOODNUMS_ID= ( str("DoodsonNumbers") ,)
    self.MAIN_CONST_PHASECORR_ID= ( str("PhaseCorrection") ,)

    #--- JSON static input data strings ids. indexing definitions
    #    for maims constituents satellites.
    self.SAT_AMP_RATIO_ID= ( str("AmplitudeRatio") ,)
    self.SAT_PHASECORR_ID= ( str("PhaseCorrection") ,)
    self.SAT_DOODNUM_CHANGES_ID= ( str("DoodsonNbChanges") ,)
    self.SAT_AMP_RATIO_FLAG_ID= ( str("AmplitudeRatioFlag") ,)

    #--- JSON static input data strings ids. indexing definitions
    #    for shallow water constituents.
    self.SHWAT_MULT_FACT_ID= ( str("MultFactor") ,)
    self.SHWAT_MAIN_CONST_ID= ( str("MainConstituent") ,)
    self.SHWAT_MAIN_CONSTS_DERIV_ID= ( str("MainConstituentsDerivations") ,)
