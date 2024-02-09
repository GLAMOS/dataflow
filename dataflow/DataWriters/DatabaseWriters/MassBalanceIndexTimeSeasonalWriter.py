'''
Created on 14.07.2021

@author: elias
'''

from dataflow.DataWriters.DatabaseWriters.GlamosDatabaseWriter import GlamosDatabaseWriter
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataObjects.MassBalanceIndexTimeSeasonal import MassBalanceIndexTimeSeasonal
import datetime

class MassBalanceIndexTimeSeasonalWriter(GlamosDatabaseWriter):
    '''
    Database writer for objects of the type mass balance index seasonal

    Attributes:
    _MassBalanceIndexSeasonalCounter int  Counter of mass balance index seasonal written to the database
    '''

    _MassBalanceIndexTimeSeasonalCounter = 0

    @property
    def massBalanceIndexTimeSeasonalWritten(self):
        # TODO: Description

        return self._MassBalanceIndexTimeSeasonalCounter

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor

        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''

        super().__init__(accessConfigurationFullFileName)

    def isMassBalanceIndexTimeSeasonalStored(self):
        pass

    def write(self, glacier):
        '''
        Writes all mass balance index seasonal data of the given glacier into the database.

        @type glacier: dataflow.DataObjects.Glacier.Glacier
        @param glacier: Glacier object with massbalance index seasonal data to be written into the database
        '''

        try:
            for massbalanceIndexTimeSeasonal in glacier.massBalanceIndexTimeSeasonals.values():
                # Check if mass balance index daily is already stored in the database.
                # The statement has to describe a SELECT which returns a unique record based on the definition of the record set.
                # In case the mass balance data the following factors define a unique data record:
                # - The same glacier (fk_glacier)
                # - The same name (name)
                # - The start and end date of annual period (date_0, date_1)
                # - The balance values of entry (b_w_meas, b_a_meas)

                checkStatement = "SELECT * FROM {0} WHERE fk_glacier = '{1}' AND name = '{2}' AND " \
                                 "date_from_annual ='{3}' AND date_to_annual = '{4}' AND b_w_meas = '{5}' AND b_a_meas = '{6}';".format(
                    'mass_balance.index_time_seasonal',
                    glacier.pk,
                    massbalanceIndexTimeSeasonal.name,
                    massbalanceIndexTimeSeasonal.date_0,
                    massbalanceIndexTimeSeasonal.date_1,
                    massbalanceIndexTimeSeasonal.b_w_meas,
                    massbalanceIndexTimeSeasonal.b_a_meas,)

                # Record is already in database. No further inserts needed.
                if super().isRecordStored(checkStatement) == True:
                    message = "The record {0} is already stored in the database. No further inserts.".format(
                        str(massbalanceIndexTimeSeasonal))
                    print(message)

                # The record is not yet stored in the database. Insert will be done.
                else:
                    message = "The record {0} is not yet stored in the database. Insert will be done ...".format(
                        str(massbalanceIndexTimeSeasonal))
                    print(message)

                    # Preparing the INSERT of a not yet inserted record.
                    insertStatement = "INSERT INTO mass_balance.index_time_seasonal (pk, fk_glacier, fk_embargo_type, fk_analysis_method_type, name, date_from_annual, date_to_annual, date_from_winter, date_to_winter, date_fall_min, date_spring_max, latitude, longitude, altitude, b_w_meas, b_a_meas, c_w_obs, c_a_obs, a_w_obs, a_a_obs, b_w_fix, b_a_fix, c_w_fix, c_a_fix, a_w_fix, a_a_fix, investigator, reference) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', {11}, {12}, {13}, '{14}', '{15}', '{16}', '{17}', '{18}', '{19}', '{20}', '{21}', '{22}', '{23}', '{24}', '{25}', '{26}', '{27}');"

                    # Handling possible NULL values:
                    # TODO: if Null values possible
                    # Handling not yet implemented values.
                    # TODO: if values are not yet implemented
                    # Handling not yet implemented default values.
                    # TODO: if default values not yet implemented

                    # Getting the final INSERT-statement ready.
                    insertStatement = insertStatement.format(
                        massbalanceIndexTimeSeasonal.pk,
                        glacier.pk,
                        massbalanceIndexTimeSeasonal.embargo_type,
                        massbalanceIndexTimeSeasonal.analysis_method_type,
                        massbalanceIndexTimeSeasonal.name,
                        massbalanceIndexTimeSeasonal.date_0,
                        massbalanceIndexTimeSeasonal.date_1,
                        massbalanceIndexTimeSeasonal.date_fmeas,
                        massbalanceIndexTimeSeasonal.date_smeas,
                        massbalanceIndexTimeSeasonal.date_fmin,
                        massbalanceIndexTimeSeasonal.date_smax,
                        massbalanceIndexTimeSeasonal.latitude,
                        massbalanceIndexTimeSeasonal.longitude,
                        massbalanceIndexTimeSeasonal.altitude,
                        massbalanceIndexTimeSeasonal.b_w_meas,
                        massbalanceIndexTimeSeasonal.b_a_meas,
                        massbalanceIndexTimeSeasonal.c_w_obs,
                        massbalanceIndexTimeSeasonal.c_a_obs,
                        massbalanceIndexTimeSeasonal.a_w_obs,
                        massbalanceIndexTimeSeasonal.a_a_obs,
                        massbalanceIndexTimeSeasonal.b_w_fix,
                        massbalanceIndexTimeSeasonal.b_a_fix,
                        massbalanceIndexTimeSeasonal.c_w_fix,
                        massbalanceIndexTimeSeasonal.c_a_fix,
                        massbalanceIndexTimeSeasonal.a_w_fix,
                        massbalanceIndexTimeSeasonal.a_a_fix,

                        massbalanceIndexTimeSeasonal.investigator,
                        massbalanceIndexTimeSeasonal.reference)

                    self._writeData(insertStatement)
                    self._connection.commit()

                    self._MassBalanceIndexTimeSeasonalCounter += 1
        except Exception as exception:

            raise exception

        finally:

            self._connection.close()

            print("\n")
            print("-> A total of {0} mass balance index time seasonal were inserted into the database.".format(
                self._MassBalanceIndexTimeSeasonalCounter))