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





import psycopg2
from psycopg2 import OperationalError
from .Exceptions.DatabaseConnectionError import DatabaseConnectionError
import configparser
     
class PostgreSqlReader(DatabaseReader):
    '''
    Specialised main class for PostgreSQL and PostGIS access.
    
    Attributes:
        _CONNECTION_STRING_TEMPLATE: Template of the connection to the database. host address, database name, user name and password have to be stored in a private configuration file.
        _connectionString: Entire string to access the database.
        _connection: Connection object to the database
        _cursor: Data cursor with the results of the queries.
    '''

    _CONNECTION_STRING_TEMPLATE = "host='{0}' dbname='{1}' user='{2}' password='{3} connect_timeout={4}'"
    
    _connectionString = ""
    
    _connection = None
    
    _cursor = None

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Full file name of a database access configuration file.
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
        timeout = config.getint("Access", "timeout")
        
        self._connectionString = self._CONNECTION_STRING_TEMPLATE.format(
            host, dbName, dbUser, dbPassword, timeout)
    
    @property
    def isDatabaseAvailable(self):
        '''
        Check if the defined database is available.
        
        @rtype: Boolean
        @return: True if the database is available, False if the database is not available.
        '''
        
        try:
            self._connection = psycopg2.connect(self._connectionString)
            
            return True
        
        except OperationalError:
            return False
    
    
    def retriveData(self, statement):
        '''
        Retrieving all the data records found by the query based on the given statement.
        The results are returned as list object.
        The returned results have to be interpreted by the specialised database reader classes into
        DataObjects.
        
        @type statement: string
        @param statement: SQL statement for the GLAMOS PostGIS database.
        
        @rtype: List
        @return: List of all returned records found by the statement.
        
        @raise DatabaseConnectionError: Error during connecting to database (e.g. timeout).
        '''
        
        try:
            results = list()
            
            self._connection = psycopg2.connect(self._connectionString)
            self._cursor = self._connection.cursor()

            self._cursor.execute(statement)

            for recordReturned in self._cursor:
                results.append(recordReturned)
            
            return results
        
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