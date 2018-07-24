'''
Created on 18.05.2018

@author: yvo
'''

from dataflow.DataReaders.DataReader import DataReader


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
    Generic class for reading and parsing of ASCII-based files.
    
    Attributes:
        _fullFileName    Absolute path of the file in the file system
    '''

    _fullFileName = None

    def __init__(self, fullFileName):
        '''
        Constructor
        
        @type fullFileName: string
        @param fullFileName: Absolute path of the file in the file system
        '''
        
        self._fullFileName = fullFileName
        
        # TODO: Throw exception in case of not existing file.
        
    @property
    def fullFileName(self):
        '''
        Get the full name of the referenced file.
        
        @rtype: string
        @return: Absolute path of the file in the file system
        '''
        return self._fullFileName