'''
Created on 04.06.2018

@author: yvo
'''

class MassBalanceTypeNotDefinedError(Exception):
    '''
    Exception class if undefined mass balance type.
    '''


    def __init__(self, message):
        '''
        Constructor
        
        @type message: string
        @param message: Message of the exception
        '''
        
        self.message = message