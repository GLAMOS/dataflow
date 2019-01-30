'''
Created on 11.07.2018

@author: yvo
'''

from dataflow.DataObjects.Glamos import GlamosData
from dataflow.DataObjects.Enumerations.HeightCaptureMethodEnumeration import HeightCaptureMethodEnum
from dataflow.DataObjects.Enumerations.VolumeChangeEnumerations import AnalysisMethodEnum

class VolumeChange(GlamosData):
    '''
    Volume change observation between two dates.
    
    Attributes:
    _dateFrom                date                       Date of the reference measurement at t0
    _dateFromQuality         DateQualityTypeEnum        Indicator if the start date is known or estimated.
    _dateTo                  date                       Date of the volume change measurement at t1
    _dateToQuality           DateQualityTypeEnum        Indicator if the end date is known or estimated.
    _areaFrom                float                      Size of the area used at t0 [km2]
    _areaTo                  float                      Size of the area used at t1 [km2]
    _heightCaptureMethodFrom HeightCaptureMethodEnum    Method to derive the surface model at the from-date
    _heightCaptureMethodTo   HeightCaptureMethodEnum    Method to derive the surface model at the to-date
    _analysisMethod          AnalysisMethodEnum         Method of the analysis
    _elevationMaximumFrom    float                      Maximum elevation at date t0 [masl]
    _elevationMinimumFrom    float                      Minimum elevation at date t0 [masl]
    _elevationMaximumTo      float                      Maximum elevation at date t1 [masl]
    _elevationMinimumTo      float                      Minimum elevation at date t1 [masl]
    _volumeChange            float                      Difference of volume between t1 - t0 [km3]
    _heightChangeMean        float                      Mean difference of surface height between t1 - t0 [m]
    '''

    _dateFrom                = None
    _dateFromQuality         = None
    _dateTo                  = None
    _dateToQuality           = None
    _areaFrom                = None
    _areaTo                  = None
    _heightCaptureMethodFrom = None
    _heightCaptureMethodTo   = None
    _analysisMethod          = None
    _elevationMaximumFrom    = None
    _elevationMinimumFrom    = None
    _elevationMaximumTo      = None
    _elevationMinimumTo      = None
    _volumeChange            = None
    _heightChangeMean        = None
    

    def __init__(self, 
        pk = None,
        dateFrom = None, 
        dateFromQuality = None, 
        dateTo = None,
        dateToQuality = None,        
        areaFrom = None, areaTo = None,
        heightCaptureMethodFrom = None, heightCaptureMethodTo = None,
        analysisMethod = None,
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
        @type dateFromQuality: DateQualityTypeEnum
        @param dateFromQuality: Indicator if the start date is known or estimated.
        @type dateTo: date
        @param dateTo: Date of the volume change measurement at t1
        @type dateToQuality: DateQualityTypeEnum
        @param dateToQuality: Indicator if the end date is known or estimated.
        @type areaFrom: float
        @param areaFrom: Size of the area used at t0 [km2]
        @type areaTo: float
        @param areaTo: Size of the area used at t1 [km2]
        @type heightCaptureMethodFrom: dataflow.DataObjects.Enumerations.HeightCaptureMethodEnumeration.HeightCaptureMethodEnum
        @param heightCaptureMethodFrom: Method to derive the surface model at the from-date
        @type heightCaptureMethodTo: dataflow.DataObjects.Enumerations.HeightCaptureMethodEnumeration.HeightCaptureMethodEnum
        @param heightCaptureMethodTo: Method to derive the surface model at the to-date
        @type analysisMethod: dataflow.DataObjects.Enumerations.VolumeChangeEnumerations.AnalysisMethodEnum
        @param analysisMethod: Type of the analysis method to derive the volume change value.
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
        
        self._dateFrom                = dateFrom
        self._dateFromQuality         = dateFromQuality
        self._dateTo                  = dateTo
        self._dateToQuality           = dateToQuality
        self._areaFrom                = areaFrom
        self._areaTo                  = areaTo
        self._heightCaptureMethodFrom = heightCaptureMethodFrom
        self._heightCaptureMethodTo   = heightCaptureMethodTo
        self._analysisMethod          = analysisMethod
        self._elevationMaximumFrom    = elevationMaximumFrom
        self._elevationMinimumFrom    = elevationMinimumFrom
        self._elevationMaximumTo      = elevationMaximumTo
        self._elevationMinimumTo      = elevationMinimumTo
        self._volumeChange            = volumeChange
        self._heightChangeMean        = heightChangeMean
        
    def __str__(self):
        '''
        String representation of the volume-change object.
        
        @rtype: str
        @return: String representation of the volume-change object.
        '''
        
        stringRepresentationTemplate = "Volume change between {0} and {1}: {2} km3"
        
        return stringRepresentationTemplate.format(
            self.dateFrom, self.dateTo, self.volumeChange)
        
    @property
    def dateFrom(self):
        '''
        Date of the reference measurement at t0.
        
        @rtype: date
        @return: Date of the reference measurement at t0
        '''
        return self._dateFrom
    
    @property
    def dateFromQuality(self):
        '''
        Indicator if the start date is known or estimated.
        
        @rtype: DateQualityTypeEnum
        @return: Indicator if the start date is known or estimated.
        '''
        return self._dateFromQuality
    
    @property
    def dateTo(self):
        '''
        Date of the volume change measurement at t1.
        
        @rtype: date
        @return: Date of the volume change measurement at t1.
        '''
        return self._dateTo
        
    @property
    def dateToQuality(self):
        '''
        Indicator if the end date is known or estimated.
        
        @rtype: DateQualityTypeEnum
        @return: Indicator if the end date is known or estimated.
        '''    
        return self._dateToQuality
    
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
    def heightCaptureMethodFrom(self):
        '''
        Method to derive the surface model at the from-date
        
        @rtype: dataflow.DataObjects.Enumerations.HeightCaptureMethodEnumeration.HeightCaptureMethodEnum
        @return: Method to derive the surface model at the from-date
        '''
        return self._heightCaptureMethodFrom

    @property
    def heightCaptureMethodTo(self):
        '''
        Method to derive the surface model at the to-date
        
        @rtype: dataflow.DataObjects.Enumerations.HeightCaptureMethodEnumeration.HeightCaptureMethodEnum
        @return: Method to derive the surface model at the to-date
        '''
        return self._heightCaptureMethodTo

    @property
    def analysisMethod(self):
        '''
        Type of the analysis method to derive the volume change value.
        
        @rtype: dataflow.DataObjects.Enumerations.VolumeChangeEnumerations.AnalysisMethodEnum
        @return: Type of the analysis method to derive the volume change value.
        '''
        return self._analysisMethod

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
