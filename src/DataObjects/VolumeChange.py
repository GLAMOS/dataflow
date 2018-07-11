'''
Created on 11.07.2018

@author: yvo
'''

from .Glamos import GlamosData

class VolumeChange(GlamosData):
    '''
    Volume change observation between two dates.
    
    Attributes:
    _dateFrom              date     Date of the reference measurement at t0
    _dateTo                date     Date of the volume change measurement at t1
    _areaFrom              float    Size of the area used at t0 [km2]
    _areaTo                float    Size of the area used at t1 [km2]
    _elevationMaximumFrom  float    Maximum elevation at date t0 [masl]
    _elevationMinimumFrom  float    Minimum elevation at date t0 [masl]
    _elevationMaximumTo    float    Maximum elevation at date t1 [masl]
    _elevationMinimumTo    float    Minimum elevation at date t1 [masl]
    _volumeChange          float    Difference of volume between t1 - t0 [km3]
    _heightChangeMean      float    Mean difference of surface height between t1 - t0 [m]
    '''

    _dateFrom             = None
    _dateTo               = None
    _areaFrom             = None
    _areaTo               = None
    _elevationMaximumFrom = None
    _elevationMinimumFrom = None
    _elevationMaximumTo   = None
    _elevationMinimumTo   = None
    _volumeChange         = None
    _heightChangeMean     = None
    

    def __init__(self, 
        pk = None,
        dateFrom = None, dateTo = None,
        areaFrom = None, areaTo = None,
        elevationMaximumFrom = None, elevationMinimumFrom = None,
        elevationMaximumTo = None, elevationMinimumTo = None,
        volumeChange = None,
        heightChangeMean = None):
        '''
        Constructor
    
        @type pk: uuid
        @param pk: Unique identifier
        @type dateFrom: date
        @param dateFrom: Date of the reference measurement at t0
        @type dateTo: date
        @param dateTo: Date of the volume change measurement at t1
        @type areaFrom: float
        @param areaFrom: Size of the area used at t0 [km2]
        @type areaTo: float
        @param areaTo: Size of the area used at t1 [km2]
        @type elevationMaximumFrom: float
        @param elevationMaximumFrom: Maximum elevation at date t0 [masl]
        @type elevationMinimumFrom: float
        @param elevationMinimumFrom: Minimum elevation at date t0 [masl]
        @type elevationMaximumTo: float
        @param elevationMaximumTo: Maximum elevation at date t1 [masl]
        @type elevationMinimumTo: float
        @param elevationMinimumTo: Minimum elevation at date t1 [masl]
        @type volumeChange: float
        @param volumeChange: Difference of volume between t1 - t0 [km3]
        @type heightChangeMean: float
        @param heightChangeMean: Mean difference of surface height between t1 - t0 [m]
        '''
        
        super().__init__(pk)
        
        self._dateFrom             = dateFrom
        self._dateTo               = dateTo
        self._areaFrom             = areaFrom
        self._areaTo               = areaTo
        self._elevationMaximumFrom = elevationMaximumFrom
        self._elevationMinimumFrom = elevationMinimumFrom
        self._elevationMaximumTo   = elevationMaximumTo
        self._elevationMinimumTo   = elevationMinimumTo
        self._volumeChange         = volumeChange
        self._heightChangeMean     = heightChangeMean
        
        
    @property
    def dateFrom(self):
        '''
        Date of the reference measurement at t0.
        
        @rtype: date
        @return: Date of the reference measurement at t0
        '''
        return self._dateFrom
    
    @property
    def dateTo(self):
        '''
        Date of the volume change measurement at t1.
        
        @rtype: date
        @return: Date of the volume change measurement at t1.
        '''
        return self._dateTo
    
    @property
    def areaFrom(self):
        '''
        Size of the area used at t0 [km2]
        
        @rtype: float
        @return: Size of the area used at t0 [km2]
        '''
        return self._areaFrom
    
    @property
    def areaTo(self):
        '''
        Size of the area used at t1 [km2]
        
        @rtype: float
        @return: Size of the area used at t1 [km2]
        '''
        return self._areaTo
    
    @property
    def elevationMaximumFrom(self):
        '''
        Maximum elevation at date t0 [masl]
        
        @rtype: float
        @return: Maximum elevation at date t0 [masl]
        '''
        return self._elevationMaximumFrom
    
    @property
    def elevationMinimumFrom(self):
        '''
        Minimum elevation at date t0 [masl]
        
        @rtype: float
        @return: Minimum elevation at date t0 [masl]
        '''
        return self._elevationMinimumFrom
    
    @property
    def elevationMaximumTo(self):
        '''
        Maximum elevation at date t1 [masl]
        
        @rtype: float
        @return: Maximum elevation at date t1 [masl]
        '''
        return self._elevationMaximumTo
    
    @property
    def elevationMinimumTo(self):
        '''
        Minimum elevation at date t1 [masl]
        
        @rtype: float
        @return: Minimum elevation at date t1 [masl]
        '''
        return self._elevationMinimumTo
    
    @property
    def volumeChange(self):
        '''
        Difference of volume between t1 - t0 [km3]
        
        @rtype: float
        @return: Difference of volume between t1 - t0 [km3]
        '''
        return self._volumeChange
    
    @property
    def heightChangeMean(self):
        '''
        Mean difference of surface height between t1 - t0 [m]
        
        @rtype: float
        @return: Mean difference of surface height between t1 - t0 [m]
        '''
        return self._heightChangeMean
