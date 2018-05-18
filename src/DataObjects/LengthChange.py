'''
Created on 18.05.2018

@author: yvo
'''

from .Glamos import GlamosData

class LengthChange(GlamosData):
    '''
    Data object describing a single length change measurement. 
    '''

    _dateFrom = None
    
    _dateFromQuality = None
    
    _dateTo = None
    
    _dateToQuality = None
    
    _measurementType = None
    
    _variationQuantitative = None
    
    _variationQuantitativeAccuracy = None
    
    _elevationMin = None
    
    _observer = None

    _remarks = None
    
    @property
    def dateFrom(self):
        return self._dateFrom
    
    @property
    def dateFromQuality(self):
        return self._dateFromQuality
    
    @property
    def dateTo(self):
        return self._dateTo
    
    @property
    def dateToQuality(self):
        return self._dateToQuality
    
    @property
    def measurementType(self):
        return self._measurementType
    
    @property
    def variationQuantitative(self):
        return self._variationQuantitative
    
    @property
    def variationQuantitativeAccuracy(self):
        return self._variationQuantitativeAccuracy
    
    @property
    def elevationMin(self):
        return self._elevationMin
    
    @property
    def observer(self):
        return self._observer

    @property
    def remarks(self):
        return self._remarks

    def __init__(self, pk = None, 
                 dateFrom = None, dateFromQuality = None, 
                 dateTo = None, dateToQuality = None, 
                 measurementType = None, 
                 variationQuantitative = None, variationQuantitativeAccuracy = None, 
                 elevationMin = None, 
                 observer = None,
                 remarks = None):
        '''
        Constructor
        '''
        
        super().__init__(pk)
        
        self._dateFrom                      = dateFrom
        self._dateFromQuality               = dateFromQuality
        self._dateTo                        = dateTo
        self._dateToQuality                 = dateToQuality
        self._measurementType               = measurementType
        self._variationQuantitative         = variationQuantitative
        self._variationQuantitativeAccuracy = variationQuantitativeAccuracy
        self._elevationMin                  = elevationMin
        self._observer                      = observer
        self._remarks                       = remarks
        
        
    def __str__(self):
        
        lineToWrite = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}".format(
            self._pk,
            self._dateFrom, self._dateFromQuality,
            self._dateTo, self._dateToQuality,
            self._measurementType, self._variationQuantitative, 
            self._variationQuantitativeAccuracy,
            self._elevationMin, self._observer,
            self._remarks)

        return lineToWrite
        