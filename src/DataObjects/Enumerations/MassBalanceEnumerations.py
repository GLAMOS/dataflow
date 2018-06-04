'''
Created on 04.06.2018

@author: yvo
'''

from enum import Enum, unique

@unique
class MassBalanceTypeEnum(Enum):
    '''
    Enumeration defining the type of mass balance observation.
    
    0 = Not defined / unknown
    1 = Observation
    2 = FixDate
    '''
    
    NotDefinedUnknown = 0
    Observation = 1
    FixDate = 2

@unique
class AnalysisMethodEnum(Enum):
    '''
    Enumeration of the analysis methods for mass balance observations.
    
    0 = Not defined / unknown
    1 = Analysis of seasonal stake observations (b_w & b_a)
    2 = Analysis of annual stake observations but not close to the end of the period (b_w)
    3 = Analysis of annual stake observations (b_a)
    4 = Combined analysis of seasonal stake observations with volume change (b_w & b_a & dV)
    5 = Combined analysis of annual stake observations within the period with volume change (b_w & dV)
    6 = Combined analysis of annual stake observations with volume change (b_a & dV)
    7 = Reconstruction from volume change analysis (dV)
    8 = Reconstruction from volume change with help of stake data (dV & b_a/b_w)
    '''
    
    NotDefinedUnknown = 0
    SeasonalStakeObservations = 1
    AnnualStakeObservationsNotCloseEndPeriod = 2
    AnnualStakeObservations = 3
    CombinedSeasonalStakeObservationsVolumeChange = 4
    CombinedAnnualStakeObservationsVolumeChangeWithinPeriod = 5
    CombinedAnnualStakeObservationsVolumeChange = 6
    ReconstructionVolumeChange = 7
    ReconstructionVolumeChangeHelpStake = 8
