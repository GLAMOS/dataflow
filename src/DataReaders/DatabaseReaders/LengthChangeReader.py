'''
Created on 22.05.2018

@author: yvo
'''

from .GlamosDatabaseReader import GlamosDatabaseReader
from DataObjects.Glacier import Glacier
from DataObjects.LengthChange import LengthChange
import uuid

class LengthChangeReader(GlamosDatabaseReader):
    '''
    Reader object to retrieve length change data stored in the GLAMOS PostGIS database.
    '''

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)
        
    def getGlacierLengthChanges(self, glacier):
        '''
        Retrieves all length change measurement of the given glacier.
        
        The measurements are stored in the lengthChange dictionary of the glacier instance.
        
        @type glacier: DataObject.Glacier.Glacier
        @param glacier: Glacier of which the time series of length changes has to be retrieved.
        '''
        
        statement = "SELECT * FROM length_change.vw_length_change WHERE pk_sgi = '{0}';".format(glacier.pkSgi)
        
        results = super().retriveData(statement)
        
        for result in results:
            
            glacier.addLengthChange(self._recordToObject(result))
            
            
            
    def _recordToObject(self, dbRecord):
        '''
        Converts a single record of the database into a glacier object.
        
        @type dbRecord: list
        @param dbRecord: List with all values of one database record.
        
        @rtype: DataObjects.LengthChange.LengthChange
        @return: LengthChange object of the database record.
        '''

        #TODO: Include the additional members as well (e.g. pk, ...)

        dateFrom = dbRecord[5]
        dateTo   = dbRecord[6]
        variationQuantitative   = float(dbRecord[7])
        
        return LengthChange(None, dateFrom, None, dateTo, None, None, variationQuantitative, None, None, None, None)