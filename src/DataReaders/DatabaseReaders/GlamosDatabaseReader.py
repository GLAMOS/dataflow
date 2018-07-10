'''
Created on 22.05.2018

@author: yvo
'''

from ..DatabaseReader import PostgreSqlReader


class GlamosDatabaseReader(PostgreSqlReader):
    '''
    Main class to access the PostGIS database of GLAMOS.
    '''
    
    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor of the GlamosDatabaseReader class. The constructor
        will get the database reader objects ready to operate. After the initialising
        of the database reader, data can be retrieved directly using the retrieveData method.
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)
        