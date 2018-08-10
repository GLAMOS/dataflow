'''
Created on 10.08.2018

@author: yvo
'''

class UnitTestHelper(object):
    '''
    Helper class for the UnitTest. The class supports the UnitTests of the 
    application by providing general settings and functionalities such as
    path to configuration files.
    
    Attributes:
    _databaseAccessConfigurationFilePath      string    Path to the configuration file for accessing the GLAMOS database
    _dataflowConfigurationFilePath            string    Path to the configuration file of dataflow
    '''

    _databaseAccessConfigurationFilePath = r"../dataflow/databaseAccessConfiguration.private.cfg"
    _dataflowConfigurationFilePath = r"../dataflow/dataflow.cfg"

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    @staticmethod
    def getDatabaseAccessConfigurationFilePath():
        '''
        Gets the path to the configuration file for accessing the GLAMOS database.
        
        @rtype: string
        @return: Path to the configuration file for accessing the GLAMOS database
        '''
        
        return UnitTestHelper._databaseAccessConfigurationFilePath
    
    @staticmethod
    def getDataflowConfigurationFilePath():
        '''
        Gets the path to the configuration file of dataflow
        
        @rtype: string
        @return: Path to the configuration file of dataflow
        '''
        
        return UnitTestHelper._dataflowConfigurationFilePath