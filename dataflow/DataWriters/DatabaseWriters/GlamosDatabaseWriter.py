'''
Created on 22.05.2018

@author: yvo
'''
from dataflow.DataWriters.FileWriters import PostgreSqlWriter
import psycopg2
import configparser
import logging


class GlamosDatabaseWriter(PostgreSqlWriter):
    '''
    classdocs
    '''
    
    # Getting the common members into a super class for database readers and writers.
    
    _CONNECTION_STRING_TEMPLATE = "host='{0}' dbname='{1}' user='{2}' password='{3}'"
    
    _connectionString = ""
    
    _connection = None
    
    _cursor = None


    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        '''
        
        super().__init__(accessConfigurationFullFileName)
        
        self._connection = None
        self._cursor = None
        
        config = configparser.ConfigParser()
        config.read(self._accessConfigurationFullFileName)
        
        host = config.get("Access", "host")
        dbName = config.get("Access", "dbname")
        dbUser = config.get("Access", "user")
        dbPassword = config.get("Access", "password")
        
        self._connectionString = self._CONNECTION_STRING_TEMPLATE.format(
            host, dbName, dbUser, dbPassword)
        
    def _writeData(self, statement):
        # TODO: Description
        
        try:
            
            self._connection = psycopg2.connect(self._connectionString)
            self._cursor = self._connection.cursor()
            
            self._cursor.execute(statement)
            
            logging.debug(statement)
            
            if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
                print(statement)
            
        except Exception as e:
            
            errorMessage = "Problem during accessing or writing data to the database: {0}".format(e)
            print(errorMessage)
            logging.error('Exception during inserting data into database %s', errorMessage)
        
    
    def isRecordStored(self, statement):
        
        # TODO: Returns True if statement returns exactly one record.
        
        # TODO: Returns False if statement returns exactly no record.
        
        # TODO: Raises an exception if statement returns 2 or more records.
        
        pass 