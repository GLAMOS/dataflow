'''
Created on 18.05.2018

@author: yvo
'''

import uuid

class GlamosData(object):
    '''
    Main class for all GLAMOS-related data-objects sharing the common basic attributes and methods.
    
    A GlamosData object always owns an unique object identifier:
    In case of existing (database) data objects the unique identifier will be derived by the DataReader
    object from the data source (e.g. database).
    In case of new data objects a new identifier will be created.
    
    Attributes:
        _pk          Unique object identifier of the GLAMOS data object. The identifier will be unique during the whole lifetime of the data record.
        _dataSource  Source of the data   # TODO: Improving the dealing with data source(s)
    '''

    _pk = None
    
    _dataSource = None
    
    @property
    def pk(self):
        '''
        Gets the unique identifier of the data object.
        '''
        return self._pk
    
    @property
    def dataSource(self):
        '''
        Gets the data source of the data object.
        '''
        return self._dataSource
    
    @dataSource.setter
    def dataSource(self, value):
        '''
        Sets the data source of the data object.
        '''
        
        # TODO: Correct forming of the data source given.
        self._dataSource = value

    def __init__(self, pk = None):
        '''
        Main constructor of the super class GlamosData.
        
        @type pk: UUID
        @param pk: Unique identifier of the data object. In case of None, a new identifier will be created.
        '''
        
        if pk == None:
            self._pk = uuid.uuid1()
        else:
            self._pk = pk