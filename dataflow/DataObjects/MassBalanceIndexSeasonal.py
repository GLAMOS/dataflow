'''
Created on 22.07.2021

@author: elias
'''

from dataflow.DataObjects.Glamos import GlamosData
from dataflow.DataObjects.Enumerations.MassBalanceEnumerations import AnalysisMethodEnum

from datetime import date
from pandas import DataFrame

class MassBalanceIndexSeasonal(GlamosData):
    '''
    Data object describing a single Index Seasonal Mass Balance

    Attributes:
        _name           string  name of stake
        _date0       	date	date of begin of period  [yyyymmdd]
        _date_fmeas  	date	reference start date of measured winter balance / [yyyymmdd]
        _date_fmin   	date	date of minimum in fall = begin of stratigraphic winter period  [mmdd] / [yyyymmdd]
        _date_smeas  	date	date of end of winter period (spring measurements, maximum in spring)  [mmdd] / [yyyymmdd]
        _date_smax   	date	[yyyymmdd]; date of maximum in spring = begin of stratigraphic summer period  [mmdd]
        _date1       	date	date of end of period  [yyyymmdd]
        _latitude		float	lat-coordinate (x) of stake in LV03/LN02
        _longitude		float	long-coordinate (y) of stake in LV03/LN02
        _altitude		float	altitude (z) of stake in LV03/LN02
        _b_w_meas    	int		measured winter balance of period date_fmeas - date_smeas  [mm w.e.]
        _b_a_meas    	int		measured annual balance of period date_fmeas - date1  [mm w.e.]
        _c_w_obs     	int		total winter accumulation of period date0 - date_smeas  [mm w.e.]
        _c_a_obs     	int		total annual accumulation of period date0 - date1  [mm w.e.]
        _a_w_obs     	int		total winter ablation of period date0 - date_smeas  [mm w.e.]
        _a_a_obs     	int		total annual ablation of period date0 - date1  [mm w.e.]
        _b_w_fix     	int		winter balance of fixed date period 1.Oct - 30.Apr  [mm w.e.]
        _b_a_fix     	int		annual balance of fixed date period 1.Oct - 30.Sep  [mm w.e.]
        _c_w_fix     	int		total winter accumulation of fixed date period 1.Oct - 30.Apr  [mm w.e.]
        _c_a_fix     	int		total annual accumulation of fixed date period 1.Oct - 30.Sep  [mm w.e.]
        _a_w_fix     	int		total winter ablation of fixed date period 1.Oct - 30.Apr  [mm w.e.]
        _a_a_fix     	int		total annual ablation of fixed date period 1.Oct - 30.Sep  [mm w.e.]
        _reference      string  reference of data
        '''

    _name = None
    _date_0 = None
    _date_fmeas = None
    _date_fmin = None
    _date_smeas = None
    _date_smax = None
    _date_1 = None
    _analysis_method_type = None
    _latitude = None
    _longitude = None
    _altitude = None
    _b_w_meas = None
    _b_a_meas = None
    _c_w_obs = None
    _c_a_obs = None
    _a_w_obs = None
    _a_a_obs = None
    _b_w_fix = None
    _b_a_fix = None
    _c_w_fix = None
    _c_a_fix = None
    _a_w_fix = None
    _a_a_fix = None
    _investigator =None
    _reference = None


    def __init__(self,
        pk=None,
        name = None, date_0 = None, date_fmeas = None, date_fmin = None,
        date_smeas = None, date_smax = None, date_1 = None,
        analysis_method_type = None,
        latitude = None, longitude = None, altitude = None,
        b_w_meas = None, b_a_meas = None,
        c_w_obs = None, c_a_obs = None, a_w_obs = None, a_a_obs = None,
        b_w_fix = None, b_a_fix = None ,c_w_fix = None, c_a_fix = None, a_w_fix = None, a_a_fix = None,
        investigator = None, reference=None):
        '''
        Constructor of a mass balance indexz seasonal object. The object describes the modelledannual and winter mass balance,
        accumulation and ablation at a specific stake

        @type
        @param

        ... TODO integrate descriptions
        '''
        super().__init__(pk)

        self._name = name
        self._date_0 = date_0
        self._date_fmeas = date_fmeas
        self._date_fmin = date_fmin
        self._date_smeas = date_smeas
        self._date_smax = date_smax
        self._date_1 = date_1
        self._analysis_method_type = analysis_method_type
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._b_w_meas = b_w_meas
        self._b_a_meas = b_a_meas
        self._c_w_obs = c_w_obs
        self._c_a_obs = c_a_obs
        self._a_w_obs = a_w_obs
        self._a_a_obs = a_a_obs
        self._b_w_fix = b_w_fix
        self._b_a_fix = b_a_fix
        self._c_w_fix = c_w_fix
        self._c_a_fix = c_a_fix
        self._a_w_fix = a_w_fix
        self._a_a_fix = a_a_fix
        self._investigator = investigator
        self._reference = reference

    def __str__(self):
        ''' String representation of the massbalance index seasonal object.

                @rtype: str
                @return: String representation of the massbalance index seasonal object.
                '''
        stringRepresentationTemplate = "Mass balance index seasonal {0} from {1} to {2}: b_w_meas ({3} mm w.e.), b_a_meas ({4} mm w.e.)"

        return stringRepresentationTemplate.format(
            self._name, self._date_0, self._date_1, self._b_w_meas, self._b_a_meas)


    @property
    def name(self):
        '''
        Gets the name of index seasonal.
        '''
        return self._name

    @property
    def date_0(self):
        '''
        Gets the date_0 of index seasonal.
        '''
        return self._date_0

    @property
    def date_fmeas(self):
        '''
        Gets the date_fmeas of index seasonal.
        '''
        return self._date_fmeas

    @property
    def date_fmin(self):
        '''
        Gets the date_fmin of index seasonal.
        '''
        return self._date_fmin

    @property
    def date_smeas(self):
        '''
        Gets the date_smeas of index seasonal.
        '''
        return self._date_smeas

    @property
    def date_smax(self):
        '''
        Gets the date_smax of index seasonal.
        '''
        return self._date_smax

    @property
    def date_1(self):
        '''
        Gets the date_1 of index seasonal.
        '''
        return self._date_1

    @property
    def analysis_method_type(self):
        '''
        Gets the analysis method type of index seasonal.
        '''
        return self._analysis_method_type

    @property
    def latitude(self):
        '''
        Gets the latitude of index seasonal.
        '''
        return self._latitude

    @property
    def longitude(self):
        '''
        Gets the longitude of index seasonal.
        '''
        return self._longitude

    @property
    def altitude(self):
        '''
        Gets the altitude of index seasonal.
        '''
        return self._altitude

    @property
    def b_w_meas(self):
        '''
        Gets the total winter balance of measured period (date_fmeas to date_smeas) index seasonal.
        '''
        return self._b_w_meas

    @property
    def b_a_meas(self):
        '''
        Gets the total annual balance of measured period (date_fmeas to date_1) of index seasonal.
        '''
        return self._b_a_meas

    @property
    def c_w_obs(self):
        '''
        Gets the total winter accumulation of observed period (date_0 to date_smeas) of index seasonal.
        '''
        return self._c_w_obs

    @property
    def c_a_obs(self):
        '''
        Gets the total annual accumulation of observed period (date_0 to date_1) of index seasonal.
        '''
        return self._c_a_obs

    @property
    def a_w_obs(self):
        '''
        Gets the total winter ablation of observed period (date_0 to date_smeas) of index seasonal.
        '''
        return self._a_w_obs

    @property
    def a_a_obs(self):
        '''
        Gets the total annual ablation of observed period (date_0 to date_1) of index seasonal.
        '''
        return self._a_a_obs

    @property
    def b_w_fix(self):
        '''
        Gets the total winter balance of fixed date period seasonal.
        '''
        return self._b_w_fix

    @property
    def b_a_fix(self):
        '''
        Gets the total annual balance of fixed date period of index seasonal.
        '''
        return self._b_a_fix

    @property
    def c_w_fix(self):
        '''
        Gets the total winter accumulation of fixed date period of index seasonal.
        '''
        return self._c_w_fix

    @property
    def c_a_fix(self):
        '''
        Gets the total annual accumulation of fixed date period of index seasonal.
        '''
        return self._c_a_fix

    @property
    def a_w_fix(self):
        '''
        Gets the total winter ablation of fixed date period of index seasonal.
        '''
        return self._a_w_fix

    @property
    def a_a_fix(self):
        '''
        Gets the total annual ablation of fixed date period of index seasonal.
        '''
        return self._a_a_fix

    @property
    def investigator(self):
        '''
        Gets the investigator of index seasonal.
        '''
        return self._investigator
    @property
    def reference(self):
        '''
        Gets the reference of index seasonal.
        '''
        return self._reference