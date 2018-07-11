'''
Created on 15.06.2018

@author: yvo
'''

from .GlamosDatabaseWriter import GlamosDatabaseWriter
import logging

class MassBalanceWriter(GlamosDatabaseWriter):
    '''
    # TODO: classdocs
    
    Attributes:
    _massBalanceObservationCounter int  Counter of mass-balance observations written to the database
    _elevationBandValidCounter     int  Counter of valid elevation bands written to the database
    _elevationBandInvalidCounter   int  Counter of invalid elevation bands not written to the database
    '''

    _massBalanceObservationCounter = 0
    _elevationBandValidCounter     = 0
    _elevationBandInvalidCounter   = 0

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)
      
    @property
    def massBalanceObservationsWritten(self):
        # TODO: Description
        
        return self._massBalanceObservationCounter

    @property
    def elevationBandsValidWritten(self):
        # TODO: Description
        
        return self._elevationBandValidCounter

    @property
    def elevationBandsInvalidNotWritten(self):
        # TODO: Description
        
        return self._elevationBandInvalidCounter
    
    @property
    def elevationBandsHandled(self):
        # TODO: Description
        
        return self._elevationBandValidCounter + self._elevationBandInvalidCounter

    def write(self, glacier):
        # TODO: Description
        
        # TODO: Loop over all mass balances
        
            # TODO: Check if length change is already stored in the database.
            # statement = SELECT * FROM mass_balance.mass_balance WHERE fk_something = glacier.fk_something
            # if GlamosDatabaseWriter.isRecordStored(statement) == True:
                # TODO: Insert mass balance if not in database. 
                # writeData(insertStatement)
            # else:
            #     writeLoggerInformation

        try:
            
            for massBalance in glacier.massBalances.values():
                
                # TODO: Getting the hard coded column names into the header or an external lookup file.
                statement = "INSERT INTO mass_balance.mass_balance (pk, fk_glacier, fk_mass_balance_type, fk_embargo_type, fk_analysis_method, date_from_annual, date_to_annual, date_from_winter, date_to_winter, area, mass_balance_annual, mass_balance_winter, equilibrium_line_altitude, accumulation_area_ratio, elevation_minimum, elevation_maximum, remarks, reference) VALUES ('{0}', '{1}', {2}, {3}, {4}, '{5}', '{6}', '{7}', '{8}', {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, '{17}');".format(
                    massBalance.pk,
                    glacier.pk,
                    massBalance.massBalanceType.value,
                    0,
                    massBalance.analysisMethodType.value,
                    massBalance.dateFromAnnual,
                    massBalance.dateToAnnual,
                    massBalance.dateFromWinter,
                    massBalance.dateToWinter,
                    massBalance.surface,
                    massBalance.annualMassBalance,
                    massBalance.winterMassBalance,
                    massBalance.equilibriumLineAltitude,
                    massBalance.accumulationAreaRatio,
                    massBalance.elevationMinimum,
                    massBalance.elevationMaximum,
                    'NULL',
                    massBalance.dataSource
                    )
                
                self._writeData(statement)
                self._connection.commit()
                
                self._massBalanceObservationCounter += 1
                
                # Inserting all the altitude buckets into the database.
                for elevationBand in massBalance.elevationBands.values():
                    
                    # Only valid elevation buckets into the database.
                    if elevationBand.elevationFrom != None and elevationBand.elevationTo != None and elevationBand.annualMassBalance != None and elevationBand.winterMassBalance != None and elevationBand.surface:
                        
                        # TODO: Getting the hard coded column names into the header or an external lookup file.
                        elevationBandStatement = "INSERT INTO mass_balance.elevation_distribution (pk, fk_mass_balance, elevation_from, elevation_to, mass_balance_annual, mass_balance_winter, area) VALUES ('{0}', '{1}', {2}, {3}, {4}, {5}, {6})".format(
                            elevationBand.pk, massBalance.pk, 
                            elevationBand.elevationFrom, elevationBand.elevationTo, 
                            elevationBand.annualMassBalance, elevationBand.winterMassBalance, 
                            elevationBand.surface)
    
                        self._writeData(elevationBandStatement)
                        self._connection.commit()
                        self._elevationBandValidCounter += 1
                        
                    else:
                        message = "Incomplete elevation band: {0}".format(elevationBand)
                        logging.info(message)
                        
                        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
                            print(message)
                            
                        self._elevationBandInvalidCounter += 1

        except Exception as exception:
            
            raise exception
        
        finally:
            
            self._connection.close()
            
            