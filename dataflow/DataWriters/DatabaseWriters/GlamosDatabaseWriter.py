'''
Created on 22.05.2018

@author: yvo
'''
from dataflow.DataWriters.DatabaseWriter import PostgreSqlWriter
from dataflow.DataReaders.Exceptions.DatabaseConnectionError import DatabaseConnectionError
from dataflow.DataWriters.Exceptions.NotUniqueDataRecordError import NotUniqueDataRecordError

import psycopg2
from psycopg2 import OperationalError
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
        '''
        Check if a record is already stored in the database. The retrieving of the record is defined
        by the given statement.
        
        @type statement: string
        @param statement: Entire SQL-statement used to retrieve a single record of the database.
        
        @rtype: boolean
        @return: True if the record is already stored in the database; False if the record is not yet stored in the database.
        
        @raise DatabaseConnectionError: Exception in case of connection problems with the database.
        @raise NotUniqueDataRecordError: Exception in case of more than 1 data record found.
        '''
        
        isRecordStored = False
        
        try:
            results = list()
            
            self._connection = psycopg2.connect(self._connectionString)
            self._cursor = self._connection.cursor()

            # Getting the records from the database.
            self._cursor.execute(statement)
            
            for recordReturned in self._cursor:
                results.append(recordReturned)

            # Check the results and define the return value
            if len(results) == 0:
                isRecordStored = False
            elif len(results) == 1:
                isRecordStored = True
            else:
                message = "The statement '{0}' returns {1} records instead of 0 or 1 record.".format(
                    statement,
                    len(results))
                raise NotUniqueDataRecordError(message)
        
        except OperationalError as operationalError:
            
            errorMessage = ""
            
            if len(operationalError.args) > 0:
                errorMessage = "Error message from the database: " + operationalError.args[0]
            else:
                errorMessage = "Undefined operational error of the database"
            
            raise DatabaseConnectionError(errorMessage)
        
        except Exception as e:
            
            errorMessage = "Problem during accessing or retrieving data from the database: {0}".format(e)
            print(errorMessage)
            
            #TODO: Improving the error handling, logging etc.
        
        finally:
            if self._connection != None:
                self._connection.close()
            if self._cursor != None:
                self._cursor.close()
                
            return isRecordStored