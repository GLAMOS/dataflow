'''
Created on 18.05.2018

@author: yvo
'''

from ..DataWriter import DataWriter

class FileWriter(DataWriter):
    '''
    classdocs
    '''

    _fullFileName = None

    def __init__(self, glacier, fullFileName):
        '''
        Constructor
        '''
        
        super().__init__(glacier)
        
        self._fullFileName = fullFileName