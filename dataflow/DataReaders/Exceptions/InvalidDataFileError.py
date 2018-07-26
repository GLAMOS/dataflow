'''
Created on 12.07.2018

@author: yvo
'''


class InvalidDataFileError(Exception):
    '''
    Generic error class for invalid data files.
    '''

    def __init__(self, message):
        '''
        Constructor
        
        @type message: string
        @param message: Message of the exception
        '''
        
        self.message = message