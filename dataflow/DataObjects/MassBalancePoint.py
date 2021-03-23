'''
Created on 22.03.2021

@author: elias
'''

from dataflow.DataObjects.Glamos import GlamosData
from dataflow.DataObjects.Enumerations.MassBalancePointEnumerations import DateAccuracyEnum
from dataflow.DataObjects.Enumerations.MassBalancePointEnumerations import DensityAccuracyEnum
from dataflow.DataObjects.Enumerations.MassBalancePointEnumerations import MeasurementQualityEnum
from dataflow.DataObjects.Enumerations.MassBalancePointEnumerations import MeasurementTypeEnum
from dataflow.DataObjects.Enumerations.MassBalancePointEnumerations import ObservationTypeEnum
from dataflow.DataObjects.Enumerations.MassBalancePointEnumerations import PositionAccuracyEnum


from datetime import date
from pandas import DataFrame

class MassBalancePoint(GlamosData):
    '''
    Point Mass Balance between two dates
    _name               string
    _observationType    ObservationTypeEnum
    _dateFrom           date
    _timeFrom           time
    _dateTo             date
    _timeTo             time
    _dateAccuracy       DateAccuracyEnum
    _latitude           float
    _longitude          float
    _altitude           float
    _positionAccuracy   PositionAccuracyEnmu
    _massbalance_raw    integer
    _density            integer
    _densityAccuracy    DensityAccuracyEnum
    _massbalance_we     integer
    _measurement_quality MeasurementQualityEnum
    _measurement_type   MeasurementTypeEnum
    _massbalance_error  integer
    _reading_error      integer
    _density_error      integer

    '''

    _name = None
    _observationType = None
    _dateFrom = None
    _timeFrom = None
    _dateTo = None
    _timeTo = None
    _dateAccuracy = None
    _latitude = None
    _longitude = None
    _altitude = None
    _positionAccuracy = None
    _massbalance_raw = None
    _density = None
    _densityAccuracy = None
    _massbalance_we = None
    _measurement_quality = None
    _measurement_type = None
    _massbalance_error = None
    _reading_error = None
    _density_error = None
    _source = None

    def __init__(self,
        name = None,
        observationType = None,
        dateFrom = None, timeFrom = None,
        dateTo = None,timeTo = None,
        dateAccuracy = None,
        latitude = None, longitude = None, altitude = None, positionAccuracy = None,
        massbalance_raw = None,
        density = None, densityAccuracy = None,
        massbalance_we = None, measurement_quality = None, measurement_type = None,
        massbalance_error = None, reading_error = None, density_error = None,
        source = None):

        '''
        Constructor: tbd
        '''

        super().__init__(pk)

        self._name              = name
        self._observationType   = observationType
        self._dateFrom          = dateFrom
        self._timeFrom          = timeFrom
        self._dateTo            = dateTo
        self._timeTo            = timeTo
        self._dateAccuracy      = dateAccuracy
        self._latitude          = latitude
        self._longitude         = longitude
        self._altitude          = altitude
        self._positionAccuracy  = positionAccuracy
        self._massbalance_raw   = massbalance_raw
        self._density           = density
        self._densityAccuracy   = densityAccuracy
        self._massbalance_we    = massbalance_we
        self._measurement_quality = measurement_quality
        self._measurement_type  = measurement_type
        self._massbalance_error = massbalance_error
        self._reading_error     = reading_error
        self._density_error     = density_error
        self._source            = source