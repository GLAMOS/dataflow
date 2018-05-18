'''
Created on 18.05.2018

@author: yvo
'''

from .Glamos import GlamosData

class Glacier(GlamosData):
    '''
    classdocs
    '''

    _pkVaw = None
    
    _name  = None
    
    _lengthChanges = dict()
    
    @property
    def pkVaw(self):
        return self._pkVaw
    
    @property
    def name(self):
        return self._name
    
    @property
    def lengthChanges(self):
        return self._lengthChanges

    def __init__(self, pk = None, pkVaw = None, name = None):
        '''
        Constructor
        '''
        
        super().__init__(pk)
        
        self._pkVaw = pkVaw
        self._name  = name
        
    def __str__(self):
        
        representation = "{0}, {1}, {2}".format(self._pk, self._pkVaw, self._name)
        
        return representation
    
    def addLengthChange(self, lengthChange):
        
        self._lengthChanges[lengthChange.dateFrom] = lengthChange