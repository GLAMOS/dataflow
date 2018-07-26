'''
Created on 10.07.2018

@author: yvo
'''

class DatabaseConnectionError(Exception):
    '''
    Generic error class for database-connection-related errors.
    '''


    def __init__(self, message):
        '''
        Constructor
        
        @type message: string
        @param message: Message of the exception
        '''
        
        self.message = message