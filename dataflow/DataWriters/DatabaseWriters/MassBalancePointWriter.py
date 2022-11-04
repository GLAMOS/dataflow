'''
Created on 22.03.2021

@author: elias
'''

from dataflow.DataWriters.DatabaseWriters.GlamosDatabaseWriter import GlamosDatabaseWriter
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataObjects.MassBalancePoint import MassBalancePoint


class MassBalancePointWriter(GlamosDatabaseWriter):
    '''
    Database writer for objects of the type mass balance point

    Attributes:
    _MassBalancePointObservationCounter int  Counter of mass balance points written to the database
    '''

    _MassBalancePointObservationCounter = 0

    @property
    def massBalancePointObservationsWritten(self):
        # TODO: Description

        return self._MassBalancePointObservationCounter

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor

        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''

        super().__init__(accessConfigurationFullFileName)

    def isMassBalancePointStored(self):
        pass

    def write(self, glacier):
        '''
        Writes all mass balance point observation of the given glacier into the database.

        @type glacier: dataflow.DataObjects.Glacier.Glacier
        @param glacier: Glacier object with length-change data to be written into the database
        '''

        try:
            for massbalancePoint in glacier.massBalancePoints.values():
                # Check if mass balance point observation is already stored in the database.
                # The statement has to describe a SELECT which returns a unique record based on the definition of the record set.
                # In case the mass balance data the following factors define a unique data record:
                # - The same glacier (fk_glacier)
                # - The same name (name)
                # - The same start date of the observation (date_from)
                # - The same end date of the observation (date_to)

                checkStatement = "SELECT * FROM {0} WHERE fk_glacier = '{1}' AND name = '{2}' AND " \
                                 "fk_observation_type ='{3}' AND date_from = '{4}' AND time_from = '{5}' AND " \
                                 "date_to = '{6}' AND time_to = '{7}' AND " \
                                 "latitude = '{8}' AND longitude = '{9}';".format(
                    'mass_balance.point',
                    glacier.pk,
                    massbalancePoint.name,
                    massbalancePoint.observationType,
                    massbalancePoint.dateFrom, massbalancePoint.timeFrom,
                    massbalancePoint.dateTo, massbalancePoint.timeTo,
                    massbalancePoint.latitude,
                    massbalancePoint.longitude)
                # Record is already in database. No further inserts needed.
                if super().isRecordStored(checkStatement) == True:
                    message = "The record {0} is already stored in the database. No further inserts.".format(
                        str(massbalancePoint))
                    print(message)

                # The record is not yet stored in the database. Insert will be done.
                else:
                    message = "The record {0} is not yet stored in the database. Insert will be done ...".format(
                        str(massbalancePoint))
                    print(message)

                    # Preparing the INSERT of a not yet inserted record.
                    insertStatement = "INSERT INTO mass_balance.point (pk, fk_glacier, name, fk_observation_type, date_from, time_from, date_to, time_to, fk_date_quality, period, latitude, longitude, altitude, fk_position_quality, massbalance_raw, density, fk_density_quality, massbalance_we, fk_measurement_quality, fk_measurement_type, massbalance_error, reading_error, density_error, source) VALUES ('{0}', '{1}', '{2}', {3}, '{4}', '{5}', '{6}', '{7}', {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}, {22}, '{23}');"

                    # Handling possible NULL values:
                    # TODO: if Null values possible
                    # Handling not yet implemented values.
                    # TODO: if values are not yet implemented
                    # Handling not yet implemented default values.
                    # TODO: if default values not yet implemented

                    # Getting the final INSERT-statement ready.
                    insertStatement = insertStatement.format(
                        massbalancePoint.pk,
                        glacier.pk,
                        massbalancePoint.name,
                        massbalancePoint.observationType,
                        massbalancePoint.dateFrom, massbalancePoint.timeFrom,
                        massbalancePoint.dateTo, massbalancePoint.timeTo,
                        massbalancePoint.dateAccuracy,
                        massbalancePoint.period,
                        massbalancePoint.latitude, massbalancePoint.longitude, massbalancePoint.altitude,
                        massbalancePoint.positionAccuracy,
                        massbalancePoint.massbalance_raw,
                        massbalancePoint.density, massbalancePoint.densityAccuracy,
                        massbalancePoint.massbalance_we,
                        massbalancePoint.measurement_quality, massbalancePoint.measurement_type,
                        massbalancePoint.massbalance_error, massbalancePoint.reading_error, massbalancePoint.density_error,
                        massbalancePoint.source)

                    self._writeData(insertStatement)
                    self._connection.commit()

                    self._MassBalancePointObservationCounter += 1
        except Exception as exception:

            raise exception

        finally:

            self._connection.close()

            print("\n")
            print("-> A total of {0} mass balance point observations were inserted into the database.".format(
                self._MassBalancePointObservationCounter))