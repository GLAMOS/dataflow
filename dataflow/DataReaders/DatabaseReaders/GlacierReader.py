'''
Created on 22.05.2018

@author: yvo
'''

from .GlamosDatabaseReader import GlamosDatabaseReader
from DataObjects.Glacier import Glacier
import uuid

class GlacierReader(GlamosDatabaseReader):
    '''
    Reader object to retrieve glacier related data stored in the GLAMOS PostGIS database.
    '''

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)
        
    def getAllGlaciers(self):
        '''
        Retrieves all individual glacier objects from the database.
        
        @rtype: dictionary
        @return: Dictionary with the SGI-ID as key and the corresponding glacier object.
        '''
        
        glaciers = dict()
        
        statement = "SELECT * FROM base_data.vw_glacier;"
        
        results = super().retriveData(statement)
        
        if results != None:
            for result in results:
                
                glacier = self._recordToObject(result)
                
                glaciers[glacier.pkSgi] = glacier
        
        return glaciers
    
    def getGlacierBySgi(self, pkSgi):
        '''
        Retrieves an individual glacier from the database based on the given Swiss Glacier Inventory key.
        
        @type pkSGI: string
        @param pkSgi: String representation of the Swiss Glacier Inventory key.
        
        @rtype: Glacier
        @return: Object representing the glacier with the given Swiss Glacier Inventory key.
        
        @raise Exception: In case of more than one glacier found.
        @raise Exception: In case of none glacier found.
        @raise OperationalError: Error during connecting to database (e.g. timeout).
        '''
        
        glaciers = dict()
        
        statement = "SELECT * FROM base_data.vw_glacier WHERE pk_sgi = '{0}';".format(pkSgi)
        
        results = super().retriveData(statement)
        
        for result in results:
            
            glacier = self._recordToObject(result)
            glaciers[glacier.pkSgi] = glacier
            
        if len(glaciers) == 1:
            return next(iter(glaciers.values()))
        elif len(glaciers) == 0:
            raise Exception("No entry found!")
            #TODO: Implementation and raising of own database exception.
        elif len(glaciers) > 1:
            raise Exception("Too many entries found!")
            #TODO: Implementation and raising of own database exception.
        
    def _recordToObject(self, dbRecord):
        '''
        Converts a single record of the database into a glacier object.
        
        @type dbRecord: list
        @param dbRecord: List with all values of one database record.
        
        @rtype: Glacier
        @return: Glacier object of the database record.
        '''
        
        pk = uuid.UUID(dbRecord[1])
        
        if dbRecord[2] != None:
            pkVaw = int(dbRecord[2])
        else:
            pkVaw = None
            
        pkSgi = dbRecord[5]
        name = dbRecord[6]
            
        return Glacier(pk, pkVaw, pkSgi, name)
        
        
        