'''
Created on 22.05.2018

@author: yvo
'''

from .DataReader import DataReader

class DatabaseReader(DataReader):
    '''
    Main class for all database readers.
    
    Attributes:
        _accessConfigurationFullFileName: Full file name of a database access configuration file.
    '''
    
    _accessConfigurationFullFileName = ""
    

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor of the super class for all database reader classes.
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Full file name of a database access configuration file.
        '''
        
        self._accessConfigurationFullFileName = accessConfigurationFullFileName
        
        
class PostgreSqlReader(DatabaseReader):
    '''
    Specialised main class for PostgreSQL and PostGIS access.
    '''

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Full file name of a database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)