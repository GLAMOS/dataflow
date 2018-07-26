'''
Created on 18.05.2018

@author: yvo
'''

import logging


class DataWriter(object):
    '''
    Generic main class of all data writer objects used for the GLAMOS data interface.
    
    An inherited data writer object can be specialised for file or database access.
    
    As main object common to all inherited objects a glacier object will has to be given to
    all constructors.
    
    Attributes:
        _glacier    Glacier of which the data has to be written.
    '''

    _glacier = None
    
    @property
    def glacier(self):
        '''
        Get the Glacier object of the data writer.
        '''
        return self._glacier


    def __init__(self, glacier):
        '''
        Main constructor for all inherited data reader objects. 
        The main constructor has to be called by super().__main__() by all constructors.
        
        @type glacier: DataObjects.Glacier.Glacier
        @param glacier: Glacier object for which the data will be read.
        '''
        
        logging.basicConfig(filename='DataWriter.log', format='%(asctime)s, %(levelname)s, %(name)s: %(message)s', level=logging.INFO)
        
        self._glacier = glacier