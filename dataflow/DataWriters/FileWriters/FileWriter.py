'''
Created on 18.05.2018

@author: yvo
'''

from ..DataWriter import DataWriter

class FileWriter(DataWriter):
    '''
    Super class for all classes writing data of a glacier to the file system.
    
    Attributes:
        _fullFileName    Absolute path of the file to be written.
    '''

    _fullFileName = None

    def __init__(self, glacier, fullFileName):
        '''
        Constructor
        
        @type glacier: DataObjects.Glacier.Glacier
        @param glacier: Glacier of which the data has to be written.
        
        @type fullFileName: string
        @param fullFileName: Absolute path of the file to be written.
        '''
        
        super().__init__(glacier)
        
        self._fullFileName = fullFileName