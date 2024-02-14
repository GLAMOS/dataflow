'''
Created on 31.1.2024

@author: elias
'''

from .Glamos import GlamosData


class MassBalanceSwissWide(GlamosData):
    '''
    Data object describing a single swiss wide massbalanec extrapolation.

    Attributes:
        _sgi_id:
        _year:
        _area: area of glacier in km2
        _mb_evolution: annual mass balance change in m w.e.
        _vol_evolution: annual volume change in km3
    '''


    _sgi_id=None
    _fk_glacier=None
    _year=None
    _area = None
    _mb_evolution = None
    _vol_evolution = None

    @property
    def sgi_id(self):
        '''
        Gets the SGI-ID of the values.
        '''
        return self._sgi_id

    @property
    def fk_glacier(self):
        '''
        Gets the uuid of glacier of the values.
        '''
        return self._fk_glacier

    @property
    def year(self):
        '''
        Gets the year of the values.
        '''
        return self._year

    @property
    def area(self):
        '''
        Gets the area of the glacier.
        '''
        return self._area

    @property
    def mb_evolution(self):
        '''
        Gets the mass balance change.
        '''
        return self._mb_evolution

    @property
    def vol_evolution(self):
        '''
        Gets the volume change.
        '''
        return self._vol_evolution

    def __init__(self,
                 sgi_id=None,
                 fk_glacier=None,
                 year=None,
                 area=None,
                 mb_evolution = None,
                 vol_evolution = None):
        '''
        Constructor of a swiss wide mass balance object. The objects describes the swiss wide extrapolation of area,
        mass balance evolution and volume evolutionof all swiss glacier withing the corresponding year.

        @type _year: int
        @param  _year: year of extrapolation.

        @type _area: float
        @param  _area: extrapolated area of glacier in km2.

        @type _mb_evolution: float
        @param  _mb_evolution: extrapolated mass balance change in m w.e.

        @type _vol_evolution: float
        @param _vol_evolution: extrapolated volume change in km3.
        '''
        super().__init__()
        self._sgi_id = sgi_id
        self._fk_glacier = fk_glacier
        self._year = year
        self._area = area
        self._mb_evolution = mb_evolution
        self._vol_evolution = vol_evolution

    def __str__(self):
        '''
        Overrides the __str__ method. Returning a string with the key values of the measurement.

        @rtype: string
        '''

        lineToWrite = "Swiss wide extrapolation of glacier {0} in the year {1} -> area: {2} km2, massbalance change: {3} m w.e. and volume change {4} km3".format(
            self._sgi_id,
            self._year,
            self._area,
            self._mb_evolution,
            self._vol_evolution)

        return lineToWrite

    # TODO: Implementation of the __eq__ override.
    # TODO: Implementation of the __nq__ override.