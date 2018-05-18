'''
Created on 18.05.2018

@author: yvo
'''

from .DataReader import DataReader

class FileDateReader(DataReader):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''


class AsciiFileDateReader(FileDateReader):
    '''
    classdocs
    '''

    _fullFileName = None

    def __init__(self, fullFileName):
        '''
        Constructor
        '''
        
        self._fullFileName = fullFileName