'''
Created on 12.07.2018

@author: yvo
'''

from .GlamosDatabaseReader import GlamosDatabaseReader
from src.DataObjects.Glacier import Glacier
from src.DataObjects.MassBalance import MassBalanceObservation
from src.DataObjects.MassBalance import MassBalanceFixDate
from src.DataObjects.Enumerations.MassBalanceEnumerations import MassBalanceTypeEnum
from src.DataObjects.Enumerations.MassBalanceEnumerations import AnalysisMethodEnum
from src.DataObjects.Exceptions.MassBalanceError import MassBalanceTypeNotDefinedError

import uuid

class MassBalanceReader(GlamosDatabaseReader):
    '''
    Reader object to retrieve mass-balance data stored in the GLAMOS PostGIS database.
    
    Attributes:
    _TABLE_MASS_BALANCE   str   Absolute name of the table or view to retrieve the length-change data from (<schema>.<table | view>).
    '''

    # FIXME: Better view to read the data from.
    _TABLE_MASS_BALANCE = "mass_balance.vw_mass_balance"

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)
        
    def getData(self, glacier):
        '''
        Retrieves all mass-balance data of the given glacier.
        
        The measurements are stored in the massBalances dictionary of the glacier instance.
        
        @type glacier: DataObject.Glacier.Glacier
        @param glacier: Glacier of which the time series of mass-balances has to be retrieved.
        '''
        
        # FIXME: View has to be improved.        
        statement = "SELECT * FROM {0} WHERE fk_glacier = '{1}';".format(self._TABLE_MASS_BALANCE, glacier.pk)
        
        results = super().retriveData(statement)
        
        if results != None:
            for result in results:
                
                # TODO: Getting the elevation buckets from the database and adding to the mass-balance object.
                
                glacier.addMassBalance(self._recordToObject(result))
            
    def _recordToObject(self, dbRecord):
        '''
        Converts a single record of the database into a length-change object.
        
        @type dbRecord: list
        @param dbRecord: List with all values of one database record.
        
        @rtype: DataObjects.LengthChange.LengthChange
        @return: LengthChange object of the database record.
        
        @raise MassBalanceTypeNotDefinedError: Exception in case of an unknown type of mass-balance measurement.
        '''
       
        # Key attribute for mass-balance inheritance
        massBalanceType         = MassBalanceTypeEnum(int(dbRecord[2])) # fk_mass_balance_type smallint NOT NULL,
       
        # Mandatory attributes
        pk                      = uuid.UUID(dbRecord[0])                # pk                        uuid          NOT NULL
        dateFrom                = dbRecord[5]                           # date_from_annual          date          NOT NULL
        dateTo                  = dbRecord[6]                           # date_to_annual            date          NOT NULL
        dateMeasurementFall     = dbRecord[7]                           # date_from_winter          date          NOT NULL
        dateMeasurementSpring   = dbRecord[8]                           # date_to_winter            date          NOT NULL
        surface                 = float(dbRecord[9])                    # area                      numeric(9,5)  NOT NULL
        annualMassBalance       = int(dbRecord[10])                     # mass_balance_annual       integer       NOT NULL
        winterMassBalance       = int(dbRecord[11])                     # mass_balance_winter       integer       NOT NULL
        equilibriumLineAltitude = int(dbRecord[12])                     # equilibrium_line_altitude smallint      NOT NULL
        accumulationAreaRatio   = int(dbRecord[13])                     # accumulation_area_ratio   smallint      NOT NULL
        elevationMinimum        = int(dbRecord[14])                     # elevation_minimum         smallint      NOT NULL
        elevationMaximum        = int(dbRecord[15])                     # elevation_maximum         smallint      NOT NULL

        # Mandatory attributes and conversion from database integer-based lookup-values to enumeration.
        analysisMethod          = AnalysisMethodEnum(int(dbRecord[4]))  # fk_analysis_method        smallint      NOT NULL,

        #int(dbRecord[3]) # fk_embargo_type smallint NOT NULL   DEFAULT 0,

        # Optional attributes:
        remarks = None
        if dbRecord[16] != None:
            remarks = dbRecord[16] # remarks varchar(500) NULL,
        reference = None
        if dbRecord[17] != None:
            dbRecord[17] # reference varchar(500) NULL

        # Getting the appropriate data object.
        # TODO: Could be done better using a factory pattern.
        massBalance = None
        
        if massBalanceType == MassBalanceTypeEnum.Observation:
            massBalance = MassBalanceObservation(
                pk, 
                analysisMethod,
                dateFrom, dateTo,
                dateMeasurementFall, dateMeasurementSpring, 
                elevationMinimum, elevationMaximum,
                surface,
                equilibriumLineAltitude, accumulationAreaRatio,
                winterMassBalance, annualMassBalance)
        elif massBalanceType == MassBalanceTypeEnum.FixDate:
            massBalance = MassBalanceFixDate(
                pk, 
                analysisMethod,
                dateFrom.year, dateTo.year,
                elevationMinimum, elevationMaximum,
                surface,
                equilibriumLineAltitude, accumulationAreaRatio,
                winterMassBalance, annualMassBalance)
        else:
            raise MassBalanceTypeNotDefinedError("Not defined mass-balance type")

        return massBalance