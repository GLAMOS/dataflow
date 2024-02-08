'''
Created on 19.07.2021

@author: elias
'''

from dataflow.DataReaders.DatabaseReaders.GlamosDatabaseReader import GlamosDatabaseReader
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataObjects.MassBalanceIndexTimeSeasonal import MassBalanceIndexSeasonal
from dataflow.DataObjects.Enumerations.DateEnumerations import DateQualityTypeEnum

import uuid


class MassBalanceIndexSeasonalReader(GlamosDatabaseReader):
    '''
    Reader object to retrieve mass balance index seasonal data stored in the GLAMOS PostGIS database.

    Attributes:
    _VIEW_MASS_BALANCE_INDEX_DAILY  str   Absolute name of the table or view to retrieve the mass balance seasonal data from (<schema>.<table | view>).
    '''

    _VIEW_MASS_BALANCE_INDEX_SEASONAL = "mass_balance.vw_mass_balance_index_seasonal"

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor

        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''

        super().__init__(accessConfigurationFullFileName)

    def getData(self, glacier):
        '''
        Retrieves all mass balance index seasonal data of the given glacier.

        The values are stored in the mass balance index seasonal dictionary of the glacier instance.

        @type glacier: DataObject.Glacier.Glacier
        @param glacier: Glacier of which the mass balance index seasonal data has to be retrieved.
        '''

        statement = "SELECT * FROM {0} WHERE pk_glacier = '{1}';".format(self._VIEW_MASS_BALANCE_INDEX_SEASONAL, glacier.pk)

        results = super().retriveData(statement)

        if results != None:
            for result in results:
                glacier.addMassBalanceIndexSeasonal(self._recordToObject(result))

    def _recordToObject(self, dbRecord):
        '''
        Converts a single record of the database into a mass balance index seasonal object.

        @type dbRecord: list
        @param dbRecord: List with all values of one database record.

        @rtype: DataObjects.MassBalanceIndexSeasonal
        @return: Mass balance index seasonal object of the database record.
        '''

        # Getting the individual attributes from the returned database record.
        # Mandatory attributes:
        _name = dbRecord[5]
        _date_0 = dbRecord[8]
        _date_fmeas = dbRecord[9]
        _date_fmin = dbRecord[10]
        _date_smeas = dbRecord[11]
        _date_smax = dbRecord[13]
        _date_1 = dbRecord[12]
        _analysis_method_type = dbRecord[6]
        _embargo_type = dbRecord[7]
        _latitude = dbRecord[15]
        _longitude = dbRecord[16]
        _altitude = dbRecord[17]
        _b_w_meas = dbRecord[19]
        _b_a_meas = dbRecord[19]
        _c_w_obs = dbRecord[21]
        _c_a_obs = dbRecord[20]
        _a_w_obs = dbRecord[23]
        _a_a_obs = dbRecord[22]
        _b_w_fix = dbRecord[25]
        _b_a_fix = dbRecord[24]
        _c_w_fix = dbRecord[27]
        _c_a_fix = dbRecord[26]
        _a_w_fix = dbRecord[29]
        _a_a_fix = dbRecord[28]
        _reference = dbRecord[30]

        # Optional attributes:

        # Returning the created data object.
        return MassBalanceIndexSeasonal(
            name, date_0, date_fmeas, date_fmin, date_smeas, date_smax, date_1, analysis_method_type, embargo_type,
            latitude, longitude, altitude, b_w_meas, b_a_meas, c_w_obs, c_a_obs, a_w_obs, a_a_obs, b_w_fix, b_a_fix,
            c_w_fix, c_a_fix, a_w_fix, a_a_fix, investigator, reference)