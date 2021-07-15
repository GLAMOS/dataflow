'''
Created on 14.07.2021

@author: elias
'''

from dataflow.DataWriters.DatabaseWriters.GlamosDatabaseWriter import GlamosDatabaseWriter
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataObjects.MassBalanceIndexSeasonal import MassBalanceIndexSeasonal
import datetime

class MassBalanceIndexSeasonalWriter(GlamosDatabaseWriter):
    '''
    Database writer for objects of the type mass balance index seasonal

    Attributes:
    _MassBalanceIndexSeasonalCounter int  Counter of mass balance index seasonal written to the database
    '''

    _MassBalanceIndexSeasonalCounter = 0

    @property
    def massBalanceIndexSeasonalWritten(self):
        # TODO: Description

        return self._MassBalanceIndexSeasonalCounter

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor

        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''

        super().__init__(accessConfigurationFullFileName)

    def isMassBalanceIndexSeasonalStored(self):
        pass

    def write(self, glacier):
        '''
        Writes all mass balance index seasonal data of the given glacier into the database.

        @type glacier: dataflow.DataObjects.Glacier.Glacier
        @param glacier: Glacier object with massbalance index seasonal data to be written into the database
        '''

        try:
            for massbalanceIndexSeasonal in glacier.massBalanceIndexSeasonals.values():
                # Check if mass balance index daily is already stored in the database.
                # The statement has to describe a SELECT which returns a unique record based on the definition of the record set.
                # In case the mass balance data the following factors define a unique data record:
                # - The same glacier (fk_glacier)
                # - The same name (name)
                # - The date of daily value (date)
                # - The values of entry (balance, accumulation, melt)

                checkStatement = "SELECT * FROM {0} WHERE fk_glacier = '{1}' AND name = '{2}' AND " \
                                 "date ='{3}' AND balance = '{4}' AND accumulation = '{5}' AND " \
                                 "melt = '{6}';".format(
                    'mass_balance.index_seasonal',
                    glacier.pk,
                    massbalanceIndexSeasonal.name,
                    massbalanceIndexSeasonal.date,
                    massbalanceIndexSeasonal.balance,
                    massbalanceIndexSeasonal.accumulation,
                    massbalanceIndexSeasonal.melt)

                # Record is already in database. No further inserts needed.
                if super().isRecordStored(checkStatement) == True:
                    message = "The record {0} is already stored in the database. No further inserts.".format(
                        str(massbalanceIndexSeasonal))
                    print(message)

                # The record is not yet stored in the database. Insert will be done.
                else:
                    message = "The record {0} is not yet stored in the database. Insert will be done ...".format(
                        str(massbalanceIndexSeasonal))
                    print(message)

                    # Preparing the INSERT of a not yet inserted record.
                    insertStatement = "INSERT INTO mass_balance.index_seasonal (pk, fk_glacier, name, date, balance, accumulation, melt, fk_surface_type, temperature, precipitation,reference) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', {8}, {9}, '{10}');"

                    # Handling possible NULL values:
                    # TODO: if Null values possible
                    # Handling not yet implemented values.
                    # TODO: if values are not yet implemented
                    # Handling not yet implemented default values.
                    # TODO: if default values not yet implemented

                    # Getting the final INSERT-statement ready.
                    insertStatement = insertStatement.format(
                        massbalanceIndexSeasonal.pk,
                        glacier.pk,
                        massbalanceIndexSeasonal.name,
                        massbalanceIndexSeasonal.date,
                        massbalanceIndexSeasonal.balance,
                        massbalanceIndexSeasonal.accumulation,
                        massbalanceIndexSeasonal.melt,
                        massbalanceIndexSeasonal.surface_type,
                        massbalanceIndexSeasonal.temp,
                        massbalanceIndexSeasonal.precip_solid,
                        massbalanceIndexSeasonal.reference)

                    self._writeData(insertStatement)
                    self._connection.commit()

                    self._MassBalanceIndexSeasonalCounter += 1
        except Exception as exception:

            raise exception

        finally:

            self._connection.close()

            print("\n")
            print("-> A total of {0} mass balance index seasonal were inserted into the database.".format(
                self._MassBalanceIndexSeasonalCounter))