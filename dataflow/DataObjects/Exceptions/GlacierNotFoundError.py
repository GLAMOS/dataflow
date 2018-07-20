'''
Created on 04.06.2018

@author: yvo
'''

class GlacierNotFoundError(Exception):
    '''
    Exception class if a glacier object was not found.
    '''


    def __init__(self, message):
        '''
        Constructor
        
        @type message: string
        @param message: Message of the exception
        '''
        
        self.message = message