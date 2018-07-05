'''
Created on 31.05.2018

@author: yvo
'''

from .Glamos import GlamosData
from .Enumerations.MassBalanceEnumerations import MassBalanceTypeEnum
from .Enumerations.MassBalanceEnumerations import AnalysisMethodEnum
from datetime import date

class MassBalance(GlamosData):
    # TODO: Class documentation
    
    _massBalanceType = MassBalanceTypeEnum.NotDefinedUnknown

    _analysisMethod = AnalysisMethodEnum.NotDefinedUnknown
    
    _dateFrom = None
    _dateTo = None
    
    _dateMeasurementFall   = None
    _dateMeasurementSpring = None

    _elevationMinimum  = None
    _elevationMaximum  = None
    
    _surface = None
    
    _equilibriumLineAltitude = None
    _accumulationAreaRatio = None
                 
    _winterMassBalance = None
    _annualMassBalance = None
    
    _elevationBands = None

    def __init__(self, pk = None, 
                analysisMethod = AnalysisMethodEnum.NotDefinedUnknown,
                dateFrom = None, dateTo = None,
                dateMeasurementFall = None, dateMeasurementSpring = None, 
                elevationMinimum  = None, elevationMaximum  = None,
                surface = None,
                equilibriumLineAltitude = None, accumulationAreaRatio = None,
                winterMassBalance = None, annualMassBalance = None):
        '''
        Constructor
        
        @type analysisMethod: AnalysisMethodEnum
        @param analysisMethod: Method applied for the mass balance observation.
        @type dataFrom: datetime
        @param dateFrom: Start date of the mass balance observation.
        @type dateTo: datetime
        @param dateTo: End date of the mass balance observation.
        @type dateMeasurementFall: datetime
        @param dateMeasurementFall: Date of the fall measurement.
        @type dateMeasurementSpring: datetime
        @param dadateMeasurementSpringteTo: Date of the spring measurement.
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
        
        self._analysisMethod          = AnalysisMethodEnum(analysisMethod)
        
        self._dateFrom                = dateFrom
        self._dateTo                  = dateTo
        
        self._dateMeasurementFall     = dateMeasurementFall
        self._dateMeasurementSpring   = dateMeasurementSpring
        
        self._elevationMinimum        = elevationMinimum
        self._elevationMaximum        = elevationMaximum
        
        self._surface                 = surface
        
        self._equilibriumLineAltitude = equilibriumLineAltitude
        self._accumulationAreaRatio   = accumulationAreaRatio
        
        self._winterMassBalance       = winterMassBalance
        self._annualMassBalance       = annualMassBalance
        
        self._elevationBands          = dict()

    @property
    def dateFromAnnual(self):
        '''
        Gets the start date of the annual measurement period.
        '''
        return self._dateFrom
        
    @property
    def dateFromWinter(self):
        '''
        Gets the start date of the winter measurement period.
        '''
        return self._dateMeasurementFall

    @property
    def dateToAnnual(self):
        '''
        Gets the end date of the annual measurement period.
        '''
        return self._dateTo
    
    @property
    def dateToWinter(self):
        '''
        Gets the end date of the winter measurement period.
        '''
        return self._dateMeasurementSpring
    
    @property
    def massBalanceType(self):
        '''
        # TODO: Description
        '''    
        return self._massBalanceType

    @property
    def analysisMethodType(self):
        '''
        # TODO: Description
        '''    
        return self._analysisMethod
    
    @property
    def equilibriumLineAltitude(self):
        '''
        # TODO: Description
        '''    
        return self._equilibriumLineAltitude
    
    @property
    def accumulationAreaRatio(self):
        '''
        # TODO: Description
        '''    
        return self._accumulationAreaRatio
    
    @property
    def elevationMinimum(self):
        '''
        # TODO: Description
        '''    
        return self._elevationMinimum
    
    @property
    def elevationMaximum(self):
        '''
        # TODO: Description
        '''    
        return self._elevationMaximum
    
    @property
    def winterMassBalance(self):
        '''
        Gets the value for the winter mass balance in mm w.e..
        
        The time period of the mass balance value is between the fall and the spring measurement.
        For values based on field observations, the start and end date are the date of the field work.
        For values based on fixed dates, the start date is always October 1st and the end date is always April 30st.
                
        # TODO: Correct definition based on discussion Huss / Bauder
                
        @rtype: integer
        @return: The value for the winter mass balance.
        '''
        return self._winterMassBalance
    
    @property
    def surface(self):
        # TODO: Description
        return self._surface

    @property
    def annualMassBalance(self):
        '''
        Gets the value for the annual mass balance in mm w.e..
        
        The time period of the mass balance value is between the fall and the spring measurement.
        For values based on field observations, the start and end date are the date of the field work.
        For values based on fixed dates, the start date is always October 1st and the end date is always April 30st.
        
        # TODO: Correct definition based on discussion Huss / Bauder
        
        @rtype: integer
        @return: The annual mass balance.
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
        
        lineToWrite = "{0} -> {1} (Method: {2}; Type: {3})\n{4}: Fall date\n{5}: Spring date\n\t{6} min masl to {7} max masl, {8} km2\n\t{9} masl ELA, {10} % AAR\n\t{11} mm w.e. winter mass balance\n\t{12} mm w.e. annual mass balance\n\t{11} elevation bands".format(
            self._dateFrom,
            self._dateTo,
            self._analysisMethod,
            self._massBalanceType,
            self._dateMeasurementFall,
            self._dateMeasurementSpring,
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
        
        # Adding the data source
        if self._dataSource != None:
            lineToWrite += "\n\tData source: {0}".format(self._dataSource)

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

    def __str__(self):
        # TODO: Description
        
        lineToWrite = ""
        
        # Printing the elevation bands informations.
        elevationBandLine = "{0} masl - {1} masl: {2} mm w.e. winter, {3} mm w.e. annual, {4} km2 surface".format(
            self.elevationFrom, self.elevationTo,
            self.winterMassBalance, self.annualMassBalance,
            self.surface)
            
        lineToWrite += elevationBandLine
            
        return lineToWrite
        
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
    
    
class MassBalanceObservation(MassBalance):
    '''
    Mass balance based on observations between the from and to date.
    '''
    
    _massBalanceType = MassBalanceTypeEnum.Observation
    
    def __init__(self, pk = None, 
        analysisMethod = AnalysisMethodEnum.NotDefinedUnknown,
        dateFrom = None, dateTo = None,
        dateMeasurementFall = None, dateMeasurementSpring = None, 
        elevationMinimum  = None, elevationMaximum  = None,
        surface = None,
        equilibriumLineAltitude = None, accumulationAreaRatio = None,
        winterMassBalance = None, annualMassBalance = None):
        
        super().__init__(pk, 
            analysisMethod,
            dateFrom, dateTo,
            dateMeasurementFall, dateMeasurementSpring, 
            elevationMinimum, elevationMaximum,
            surface,
            equilibriumLineAltitude, accumulationAreaRatio,
            winterMassBalance, annualMassBalance)
      
    
class MassBalanceFixDate(MassBalance):
    '''
    Homogenised mass balance between the two fixed dates of October 1st and September 30st of the following year.
    
    Winter mass balance is always between October 1st and April 30st. 
    
    Water year:
    - https://de.wikipedia.org/wiki/Abflussjahr#Schweiz:_1._Oktober_bis_30._September
    '''
    
    _massBalanceType = MassBalanceTypeEnum.FixDate
    
    _MASSBALANCE_START_DAY          = 1
    _MASSBALANCE_START_MONTH        = 10
    
    _MASSBALANCE_END_DAY            = 30
    _MASSBALANCE_END_MONTH          = 9
    
    _WINTER_MASSBALANCE_START_DAY   = _MASSBALANCE_START_DAY
    _WINTER_MASSBALANCE_START_MONTH = _MASSBALANCE_START_MONTH
    _WINTER_MASSBALANCE_END_DAY     = 30
    _WINTER_MASSBALANCE_END_MONTH   = 4      

    def __init__(self, pk, 
                 analysisMethod,
                 yearFrom, yearTo,
                 elevationMinimum, elevationMaximum,
                 surface,
                 equilibriumLineAltitude, accumulationAreaRatio,
                 winterMassBalance, annualMassBalance):
        '''
        Constructor
        
        @type analysisMethod: AnalysisMethodEnum
        @param analysisMethod: Method applied for the mass balance observation.
        @type yearFrom: int
        @param yearFrom: Start year of the mass balance observation.
        @type yearTo: int
        @param yearTo: End year of the mass balance observation.
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
        
        # Getting the fixed dates for fall and spring measurements done.
        dateMeasurementFall   = date(yearFrom, self._WINTER_MASSBALANCE_START_MONTH, self._WINTER_MASSBALANCE_START_DAY)
        dateMeasurementSpring = date(yearTo, self._WINTER_MASSBALANCE_END_MONTH, self._WINTER_MASSBALANCE_END_DAY)

        super().__init__(pk, 
                 analysisMethod,
                 date(yearFrom, self._MASSBALANCE_START_MONTH, self._MASSBALANCE_START_DAY), 
                 date(yearTo, self._MASSBALANCE_END_MONTH, self._MASSBALANCE_END_DAY),
                 dateMeasurementFall, dateMeasurementSpring, 
                 elevationMinimum, elevationMaximum,
                 surface,
                 equilibriumLineAltitude, accumulationAreaRatio,
                 winterMassBalance, annualMassBalance)






