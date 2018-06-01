'''
Created on 31.05.2018

@author: yvo
'''

from .Glamos import GlamosData
from enum import Enum, unique

class MassBalance(GlamosData):
    # TODO: Class documentation

    _analysisMethod = None
    _dateFrom = None
    _dateTo = None

    _elevationMinimum  = None
    _elevationMaximum  = None
    
    _surface = None
    
    _equilibriumLineAltitude = None
    _accumulationAreaRatio = None
                 
    _winterMassBalance = None
    _annualMassBalance = None
    
    _elevationBands = dict()

    def __init__(self, pk = None, 
                 analysisMethod = 0,
                 dateFrom = None, dateTo = None,
                 elevationMinimum  = None, elevationMaximum  = None,
                 surface = None,
                 equilibriumLineAltitude = None, accumulationAreaRatio = None,
                 winterMassBalance = None, annualMassBalance = None):
        '''
        Constructor
        
        @type analysisMethod: integer
        @param analysisMethod: Method applied for the mass balance observation.
        @type dataFrom: datetime
        @param dateFrom: Start date of the mass balance observation.
        @type dateTo: datetime
        @param dateTo: End date of the mass balance observation.
        @type elevationMinimum: integer
        @param elevationMinimum: Minimum elevation of the mass balance observation.
        @type elevationMaximum: integer
        @param elevationMaximum: Maximum elevation of the mass balance observation.
        @type surface: float
        @param surface: Area of the mass balance observation in km2.
        @type equilibriumLineAltitude: integer
        @param equilibriumLineAltitude: Altitude of the equilibrium line of the observation period. # TODO: More accurate description
        @type accumulationAreaRatio: integer
        @param accumulationAreaRatio: Ratio of the accumulation area. # TODO: More accurate description
        @type winterMassBalance: integer
        @param winterMassBalance: Winter mass balance in mm w.e.
        @type annualMassBalance: integer
        @param annualMassBalance: Annual mass balance in mm w.e.
        '''
        
        super().__init__(pk)
        
        self._analysisMethod         = AnalysisMethodEnum(analysisMethod)
        
        self._dateFrom                = dateFrom
        self._dateTo                  = dateTo
        
        self._elevationMinimum        = elevationMinimum
        self._elevationMaximum        = elevationMaximum
        
        self._surface                 = surface
        
        self._equilibriumLineAltitude = equilibriumLineAltitude
        self._accumulationAreaRatio   = accumulationAreaRatio
        
        self._winterMassBalance       = winterMassBalance
        self._annualMassBalance       = annualMassBalance

    @property
    def dateFrom(self):
        '''
        Gets the start date of the measurement period.
        '''
        return self._dateFrom

    @property
    def dateTo(self):
        '''
        Gets the end date of the measurement period.
        '''
        return self._dateTo
    
    @property
    def winterMassBalance(self):
        '''
        Gets the winter mass balance in mm w.e..
        '''
        return self._winterMassBalance

    @property
    def annualMassBalance(self):
        '''
        Gets the annual mass balance in mm w.e..
        '''
        return self._annualMassBalance
    
    @property
    def elevationBands(self):
        '''
        Gets the mass balance in mm w.e. divided in elevation bands.
        
        @rtype: dict(??, ElevationBand)    # TODO: Documentation of the key value
        @return: Dictionary with all mass balances divided into the elevation bands.
        '''
        return self._elevationBands
    
    def addElevationBand(self, elevationBand):
        '''
        Adds an elevation band with the mass balance data for the band to the 
        colletion of all bands.
        
        @type elevationBand: ElevationBand
        @param elevationBand: Mass balance of a specific elevation band
        '''

        self._elevationBands[elevationBand.elevationFrom] = elevationBand
    

    def __str__(self):
        '''
        Overrides the __str__ method. Returning a string with the key values of the measurement. 
        
        @rtype: string
        '''
        
        lineToWrite = "{0} -> {1} (Method {2})\n\t{3} min masl to {4} max masl, {5} km2\n\t{6} masl ELA, {7} % AAR\n\t{8} mm w.e. winter mass balance\n\t{9} mm w.e. annual mass balance\n\t{10} elevation bands".format(
            self._dateFrom,
            self._dateTo,
            self._analysisMethod,
            self._elevationMinimum,
            self._elevationMaximum,
            self._surface,
            self._equilibriumLineAltitude,
            self._accumulationAreaRatio,
            self._winterMassBalance,
            self._annualMassBalance,
            len(self._elevationBands))
        
        # Adding the elevation bands informations.
        for elevationBand in self._elevationBands.values():
            
            elevationBandLine = "\n\t\t{0} masl - {1} masl: {2} mm w.e. winter, {3} mm w.e. annual, {4} km2 surface".format(
                elevationBand.elevationFrom, elevationBand.elevationTo,
                elevationBand.winterMassBalance, elevationBand.annualMassBalance,
                elevationBand.surface)
            
            lineToWrite += elevationBandLine
        

        return lineToWrite
    
    
    
class ElevationBand(GlamosData):
    '''
    Data container storing the mass balance of specific elevation range. The range starts and ends
    at the given elevation in masl.
    Additionally to the elevation the winter and annual mass balance of the range is stored.
    
    An object of the type ElevationBand is always part of an object of type MassBalance.
    
    Attributes:
        _elevationFrom      Minimum elevation in masl of the band.
        _elevationEnd       Maximum elevation in masl of the band.
        _winterMassBalance  Winter mass balance in mm w.e. of the band.
        _annualMassBalance  Annual mass balance in mm w.e. of the band.
        _surface            Total glacier surface of the band in km2.
    '''
    
    _elevationFrom = None
    _elevationTo = None
    _winterMassBalance = None
    _annualMassBalance = None
    _surface = None
    
    def __init__(self, pk = None, 
             elevationFrom = None, elevationTo = None,
             winterMassBalance = None, annualMassBalance = None,
             surface = None):
        '''
        Constructor
        
        @type pk: uuid
        @param uuid: Unique identifier of the elevation band.
        @type elevationFrom: integer
        @param elevationFrom: Minimum elevation in masl of the band.
        @type elevationFrom: integer
        @param elevationEnd: Maximum elevation in masl of the band.
        @type winterMassBalance: integer
        @param winterMassBalance:  Winter mass balance in mm w.e. of the band.
        @type annualMassBalance: integer
        @param annualMassBalance: Annual mass balance in mm w.e. of the band.
        @type surface: float
        @param surface: Total glacier surface of the band in km2.
        '''
                
        super().__init__(pk)
        
        self._elevationFrom = elevationFrom
        self._elevationTo = elevationTo
        self._winterMassBalance = winterMassBalance
        self._annualMassBalance = annualMassBalance
        self._surface = surface
        
    @property
    def elevationFrom(self):
        '''
        Gets the start elevation in masl of the band.
        
        @rtype: integer
        @return: Start elevation in masl of the band.
        '''
        return self._elevationFrom
    
    
    @property
    def elevationTo(self):
        '''
        Gets the end elevation in masl of the band.
        
        @rtype: integer
        @return: End elevation in masl of the band.
        '''
        return self._elevationTo
    
    @property
    def surface(self):
        '''
        Gets the surface in km2 of the band.
        
        @rtype: float
        @return: Suraface in km2 of the band.
        '''
        return self._surface

    @property
    def winterMassBalance(self):
        '''
        Gets the winter mass balance in mm w.e..
        '''
        return self._winterMassBalance

    @property
    def equidistant(self):
        '''
        Gets the elevation range of the band in meters.
        
        @rtype: integer
        @return: Elevation range in meters of the band.
        '''
        return self._elevationTo - self._elevationFrom
 
    @property
    def annualMassBalance(self):
        '''
        Gets the annual mass balance in mm w.e..
        '''
        return self._annualMassBalance
    
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














