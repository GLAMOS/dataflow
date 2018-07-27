'''
Created on 27.07.2018

@author: yvo
'''

class InvalidCoordinatesError(Exception):
    '''
    Generic error class for unclear coordinate definitions or projections.
    '''


    def __init__(self, message):
        '''
        Constructor
        
        @type message: string
        @param message: Message of the exception
        '''
        
        self.message = message