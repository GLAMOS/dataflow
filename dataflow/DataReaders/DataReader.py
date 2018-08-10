'''
Created on 18.05.2018

@author: yvo
'''

class DataReader(object):
    '''
    Generic main class of all data reader objects used for the GLAMOS data interface.
    
    An inherited data reader object can be specialised for file, database or web-services ...
    
    As main object common to all inherited objects a glacier object will has to be given to
    all constructors.
    
    Attributes:
        _glacier    Glacier of which the data has to be read.
    '''

    _glacier = None
    
    #TODO: Including a logger to log all transactions done by reading files and databases.

    @property
    def glacier(self):
        '''
        Get the Glacier object of the data reader.
        '''
        return self._glacier

    def __init__(self, glacier):
        '''
        Main constructor for all inherited data reader objects. 
        The main constructor has to be called by super().__main__() by all constructors.
        
        @type glacier: DataObjects.Glacier.Glacier
        @param glacier: Glacier object for which the data will be read.
        '''
        
        self._glacier = glacier
        
    def __del__(self):
        '''
        Destructor of the DataReader and inherited classes. Deletes all main objects of the class.
        '''
        
        self._glacier = None