'''
Created on 18.05.2018

@author: yvo
'''

import uuid

class GlamosData(object):
    '''
    Main class for all GLAMOS-related data-objects sharing the common basic attributes and methods.
    '''

    _pk = None
    
    @property
    def pk(self):
        return self._pk

    def __init__(self, pk = None):
        '''
        Constructor
        '''
        
        if pk == None:
            self._pk = uuid.uuid1()
        else:
            self._pk = pk