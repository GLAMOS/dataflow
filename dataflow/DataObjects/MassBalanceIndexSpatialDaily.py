'''
Created on 8.2.2024

@author: elias
'''

from dataflow.DataObjects.Glamos import GlamosData


class MassBalanceIndexSpatialDaily(GlamosData):
    '''
    Mass Balance Index Spatial Daily
    _name               string
    _date               date
    _latitude           float
    _longitude          float
    _altitude           float
    _balance            int
    _accumulation       int
    _melt               int
    _reference          string
    _investigator       string
    _creation_date      date
    _surface_type       SurfaceTypeEnum
    _temp               float
    _precip_solid       float

    '''

    _name = None
    _date = None
    _latitude = None
    _longitude = None
    _altitude = None
    _balance = None
    _accumulation = None
    _melt = None
    _surface_type = None
    _temp = None
    _precip_solid = None
    _reference = None
    _investigator = None
    _creation_date = None

    def __init__(self,
        pk = None,
        name = None,
        date = None,
        latitude = None, longitude = None, altitude = None,
        balance = None, accumulation = None, melt = None,
        surface_type = None, temp = None, precip_solid = None,
        reference=None, investigator=None, creation_date=None):

        super().__init__(pk)

        self._name = name
        self._date = date
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._balance = balance
        self._accumulation = accumulation
        self._melt = melt
        self._surface_type = surface_type
        self._temp = temp
        self._precip_solid = precip_solid
        self._reference = reference
        self._investigator = investigator
        self._creation_date = creation_date


    def __str__(self):
        ''' String representation of the massbalance index spatial daily object.

                @rtype: str
                @return: String representation of the massbalance index spatial daily object.
                '''

        stringRepresentationTemplate = "Mass balance index spatial daily {0} from {1}: balance ({2} mm w.e.), accumulation ({3} mm w.e.), melt ({4} mm w.e.)"

        return stringRepresentationTemplate.format(
            self.name, self.date, self.balance, self.accumulation, self.melt)

    @property
    def name(self):
        '''
        Gets the name of index spatial daily mass balance.
        '''
        return self._name

    @property
    def date(self):
        '''
        Gets the date of index spatial daily mass balance.
        '''
        return self._date

    @property
    def latitude(self):
        '''
        Gets the latitude of index spatial daily mass balance.
        '''
        return self._latitude

    @property
    def longitude(self):
        '''
        Gets the longitude of index spatial daily mass balance.
        '''
        return self._longitude

    @property
    def altitude(self):
        '''
        Gets the altitude of index spatial daily mass balance.
        '''
        return self._altitude

    @property
    def balance(self):
        '''
        Gets the balance of index spatial daily mass balance.
        '''
        return self._balance

    @property
    def accumulation(self):
        '''
        Gets the accumulation of index spatial daily mass balance.
        '''
        return self._accumulation

    @property
    def melt(self):
        '''
        Gets the melt of index spatial daily mass balance.
        '''
        return self._melt

    @property
    def reference(self):
        '''
        Gets the reference of index spatial daily mass balance.
        '''
        return self._reference

    @property
    def investigator(self):
        '''
        Gets the investigator of index spatial daily mass balance.
        '''
        return self._investigator

    @property
    def creation_date(self):
        '''
        Gets the creation date of index spatial daily mass balance.
        '''
        return self._creation_date

    @property
    def surface_type(self):
        '''
        Gets the surface type of index spatial daily mass balance.
        '''
        return self._surface_type

    @property
    def temp(self):
        '''
        Gets the temperature of index spatial daily mass balance.
        '''
        return self._temp

    @property
    def precip_solid(self):
        '''
        Gets the precipitation (solid) of index spatial daily mass balance.
        '''
        return self._precip_solid