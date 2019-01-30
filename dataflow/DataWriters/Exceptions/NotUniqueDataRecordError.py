'''
Created on 30.01.2019

@author: yvo
'''

class NotUniqueDataRecordError(Exception):
    '''
    Exception in case of multiple data records found in the database.
    
    The exception can be thrown in cases a unique record was requested from the database
    but multiple sets were returned. 
    '''

    def __init__(self, message):
        '''
        Constructor
        
        @type message: string
        @param message: Message of the exception
        '''
        
        self.message = message