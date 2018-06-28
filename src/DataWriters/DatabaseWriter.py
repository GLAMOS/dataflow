'''
Created on 22.05.2018

@author: yvo
'''

from .DataWriter import DataWriter

# TODO: Simplifying the database classes. One super class for Readers and Writers.

class DatabaseWriter(DataWriter):
    '''
    classdocs
    '''

    _accessConfigurationFullFileName = ""

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        '''
        self._accessConfigurationFullFileName = accessConfigurationFullFileName
        
        super().__init__(None)
        
class PostgreSqlWriter(DatabaseWriter):
    '''
    classdocs
    '''


    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        '''
        
        super().__init__(accessConfigurationFullFileName)