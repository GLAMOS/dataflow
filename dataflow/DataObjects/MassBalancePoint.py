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
    _period             float
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
    _period = None
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
        pk=None,
        name = None,
        observationType = None,
        dateFrom = None, timeFrom = None,
        dateTo = None, timeTo = None,
        period = None,
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
        self._period            = period
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

    def __str__(self):
        ''' String representation of the massbalance point object.

                @rtype: str
                @return: String representation of the massbalance point object.
                '''

        stringRepresentationTemplate = "Mass balance point {0} between {1} and {2}: {3} mm w.e."

        return stringRepresentationTemplate.format(
            self.name, self.dateFrom, self.dateTo, self.massbalance_we)
    @property
    def name(self):
        '''
        Gets the name of point mass balance.
        '''
        return self._name

    @property
    def observationType(self):
        '''
        Gets the observation Type.
        '''
        return self._observationType

    @property
    def dateFrom(self):
        '''
        Gets the start date of the point massbalance.
        '''
        return self._dateFrom

    @property
    def timeFrom(self):
        '''
        Gets the start time of the point massbalance.
        '''
        return self._timeFrom

    @property
    def dateTo(self):
        '''
        Gets the end date of the point massbalance.
        '''
        return self._dateTo

    @property
    def timeTo(self):
        '''
        Gets the end time of the point massbalance.
        '''
        return self._timeTo

    @property
    def period(self):
        '''
        Gets the period of the point massbalance.
        '''
        return self._period

    @property
    def dateAccuracy(self):
        '''
        Gets the date accuracy of the point mass balance.
        '''
        return self._dateAccuracy

    @property
    def latitude(self):
        '''
        Gets the latitude of the point mass balance.
        '''
        return self._latitude

    @property
    def longitude(self):
        '''
        Gets the longitude of the point mass balance.
        '''
        return self._longitude

    @property
    def altitude(self):
        '''
        Gets the altitude of the point mass balance.
        '''
        return self._altitude

    @property
    def positionAccuracy(self):
        '''
        Gets the position accuracy of the point mass balance.
        '''
        return self._positionAccuracy

    @property
    def massbalance_raw(self):
        '''
        Gets the raw massbalance of the point mass balance.
        '''
        return self._massbalance_raw

    @property
    def density(self):
        '''
        Gets the density of the point mass balance.
        '''
        return self._density

    @property
    def densityAccuracy(self):
        '''
        Gets the density accuracy of the point mass balance.
        '''
        return self._densityAccuracy

    @property
    def massbalance_we(self):
        '''
        Gets the water equivalent mass balance of the point mass balance.
        '''
        return self._massbalance_we

    @property
    def measurement_quality(self):
        '''
        Gets the measurement quality of the point mass balance.
        '''
        return self._measurement_quality

    @property
    def measurement_type(self):
        '''
        Gets the measurement type of the point mass balance.
        '''
        return self._measurement_type

    @property
    def massbalance_error(self):
        '''
        Gets the massbalance error of the point mass balance.
        '''
        return self._massbalance_error

    @property
    def reading_error(self):
        '''
        Gets the reading error of the point mass balance.
        '''
        return self._reading_error

    @property
    def density_error(self):
        '''
        Gets the density error of the point mass balance.
        '''
        return self._density_error

    @property
    def source(self):
        '''
        Gets the source of the point mass balance.
        '''
        return self._source

