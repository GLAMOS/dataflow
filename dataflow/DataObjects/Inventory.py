'''
Created on 20.07.2018

@author: yvo
'''

from .Glamos import GlamosData

class Inventory(GlamosData):
    '''
    classdocs
    '''

    _geometryWellKnownText = None

    def __init__(self):
        '''
        Constructor
        '''
        
    @property
    def geometryWellKnownText(self):
        
        return self._geometryWellKnownText