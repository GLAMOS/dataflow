'''
Created on 18.05.2018

@author: yvo
'''

from dataflow.DataObjects.Glamos import GlamosData


class LengthChange(GlamosData):
    '''
    Data object describing a single length change measurement. 
    
    Attributes:
        _dateFrom:    Start date of the measurement.
        _dateFromQuality:    Indicator if the start date is known or estimated.
        _dateTo:    End date of the measurement.
        _dateToQuality:    Indicator if the end date is known or estimated.
        _measuremenType: Indicator if the measurement is done by field work, reconstructed or unknown.
        _variationQuantitative: Indicator if the glacier was retreating, stable or advancing.
        _variationQuantitativeAccuracy: Accuracy of the data.
        _elevationMin: Minimal elevation above sea level of the glacier tongue.
        _observer: Observer of the measurement
        _remarks: Remarks about the measurement.
    '''

    _dateFrom = None
    
    _dateFromQuality = None
    
    _dateTo = None
    
    _dateToQuality = None
    
    _measurementType = None
    
    _variationQuantitative = None #TODO: Redundant value based on VAW ASCII file. Can be eliminated.
    
    _variationQuantitativeAccuracy = None
    
    _elevationMin = None
    
    _observer = None

    _remarks = None
    
    @property
    def dateFrom(self):
        '''
        Gets the start date of the measurement period.
        '''
        return self._dateFrom
    
    @property
    def dateFromQuality(self):
        '''
        Gets the quality of the start date of the measurement period.
        '''
        return self._dateFromQuality
    
    @property
    def dateTo(self):
        '''
        Gets the end date of the measurement period.
        '''
        return self._dateTo
    
    @property
    def dateToQuality(self):
        '''
        Gets the quality of the end date of the measurement period.
        '''
        return self._dateToQuality
    
    @property
    def measurementType(self):
        '''
        Gets the type of the measurement.
        '''
        return self._measurementType
    
    @property
    def variationQuantitative(self):
        '''
        Deprecated. Gets the qualitative value of the length change (e.g. '+', '-', '0').
        '''
        #TODO: Deriving the value based on the quantitative value.
        #TODO: Clarify the need of the property.
        return self._variationQuantitative
    
    @property
    def variationQuantitativeAccuracy(self):
        '''
        Gets the accuracy of the measurement.
        '''
        return self._variationQuantitativeAccuracy
    
    @property
    def elevationMin(self):
        '''
        Gets the minimal elevation of the glacier tongue.
        '''
        return self._elevationMin
    
    @property
    def observer(self):
        '''
        Gets the observer of the measurement.
        '''
        return self._observer

    @property
    def remarks(self):
        '''
        Gets the remarks of the measurement.
        '''
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
        Constructor of a length change object. The objects describes the length change of a 
        glacier between two obeservations.
        
        @type _dateFrom: DateTime
        @param  _dateFrom: Start date of the measurement.
        
        @type _dateFromQuality: DateTime
        @param  _dateFromQuality: Indicator if the start date is known or estimated.
        
        @type _dateTo: DateTime
        @param  _dateTo: End date of the measurement.
        
        @type _dateToQuality: string
        @param _dateToQuality: Indicator if the end date is known or estimated.
        
        @type _measuremenType: string
        @param _measuremenType: Indicator if the measurement is done by field work, reconstructed or unknown.
        
        @type _variationQuantitative: string
        @param _variationQuantitative: Indicator if the glacier was retreating, stable or advancing.
        
        @type _variationQuantitativeAccuracy: float
        @param _variationQuantitativeAccuracy: Accuracy of the data.
        
        @type _elevationMin: float
        @param _elevationMin: Minimal elevation above sea level of the glacier tongue.
        
        @type _observer: string
        @param _observer: Observer of the measurement
        
        @type _remarks: string
        @param _remarks: Remarks about the measurement.
        '''
        
        super().__init__(pk)
        
        self._dateFrom                      = dateFrom
        self._dateFromQuality               = dateFromQuality #TODO: Quality based on own object or enumeration based on database lookup table.
        self._dateTo                        = dateTo
        self._dateToQuality                 = dateToQuality #TODO: Quality based on own object or enumeration based on database lookup table.
        self._measurementType               = measurementType #TODO: Type based on own object or enumeration based on database lookup table.
        self._variationQuantitative         = variationQuantitative
        self._variationQuantitativeAccuracy = variationQuantitativeAccuracy #TODO: Accuracy based on own object or enumeration based on database lookup table.
        self._elevationMin                  = elevationMin
        self._observer                      = observer
        self._remarks                       = remarks
        
        
    def __str__(self):
        '''
        Overrides the __str__ method. Returning a string with the key values of the measurement. 
        
        @rtype: string
        '''
        
        lineToWrite = "{0} -> {1}: {2} m length change".format(
            self._dateFrom,
            self._dateTo,
            self._variationQuantitative)

        return lineToWrite
        
    #TODO: Implementation of the __eq__ override.
    #TODO: Implementation of the __nq__ override.