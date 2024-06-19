'''
Created on 1.2.2024

@author: elias
'''

from dataflow.DataWriters.DatabaseWriters.GlamosDatabaseWriter import GlamosDatabaseWriter
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataObjects.LengthChange import LengthChange


class MassBalanceSwissWideWriter(GlamosDatabaseWriter):
    '''
    Database writer for objects of the type mass balance swiss wide

    Attributes:
    _massBalanceSwissWideObservationCounter int  Counter of mass balance swiss wide observations written to the database
    '''

    _massBalanceSwissWideCounter = 0

    @property
    def massBalanceSwissWideObservationsWritten(self):
        # TODO: Description

        return self._massBalanceSwissWideCounter

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor

        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''

        super().__init__(accessConfigurationFullFileName)

    def write(self, massBalanceSwissWide):
        '''
        Writes all mass balance swiss wide observations of the given glacier into the database.

        @type glacier: dataflow.DataObjects.Glacier.Glacier
        @param glacier: Glacier object with length-change data to be written into the database
        '''

        try:

            # Check if mass balance swiss wide is already stored in the database.
            # The statement has to describe a SELECT which returns a unique record based on the definition of the record set.
            # In case the length-change data the following factors define a unique data record:
            # - The same glacier (fk_glacier)
            # - The same corresponding year (year)

            checkStatement = "SELECT * FROM {0} WHERE fk_glacier = '{1}' AND year = '{2}';".format(
                'mass_balance.swisswide',
                massBalanceSwissWide.fk_glacier,
                massBalanceSwissWide.year)

            # Record is already in database. No further inserts needed.
            if super().isRecordStored(checkStatement) == True:

                message = "The record {0} is already stored in the database. No further inserts.".format(
                    str(massBalanceSwissWide))
                #print(message)

            # The record is not yet stored in the database. Insert will be done.
            else:

                message = "The record {0} is not yet stored in the database. Insert will be done ...".format(
                    str(massBalanceSwissWide))
                print(message)

                # Preparing the INSERT of a not yet inserted record.
                insertStatement = "INSERT INTO mass_balance.swisswide (pk, fk_glacier, year, area, mb_evolution, vol_evolution) VALUES ('{0}', '{1}', {2}, {3}, {4}, {5});"

                # Getting the final INSERT-statement ready.
                insertStatement = insertStatement.format(
                    massBalanceSwissWide.pk,
                    massBalanceSwissWide.fk_glacier,
                    massBalanceSwissWide.year,
                    massBalanceSwissWide.area,
                    massBalanceSwissWide.mb_evolution,
                    massBalanceSwissWide.vol_evolution)
                #print(insertStatement)
                self._writeData(insertStatement)
                self._connection.commit()

                self._massBalanceSwissWideCounter += 1

        except Exception as exception:

            raise exception

        finally:

            self._connection.close()

        #print("\n")
        #print("-> A total of {0} mass balance swiss wide observations were inserted into the database.".format(
        #       self._massBalanceSwissWideCounter))

    def isGlacierMassBalanceSwissWideStored(self):

        pass