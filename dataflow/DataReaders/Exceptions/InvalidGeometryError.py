'''
Created on 03.08.2018

@author: yvo
'''

class InvalidGeometryError(Exception):
    '''
    Exception which be raised in case of wrongly defined geometries (e.g. 
    WKT polygones, ...).
    '''

    def __init__(self, message):
        '''
        Constructor
        
        @type message: string
        @param message: Message of the exception
        '''
        
        self.message = message