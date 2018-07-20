'''
Created on 18.05.2018

@author: yvo
'''

from .Glamos import GlamosData
from dataflow.DataObjects.MassBalance import MassBalance
from dataflow.DataObjects.Enumerations.MassBalanceEnumerations import MassBalanceTypeEnum
#import dataflow.DataObjects.Enumerations.MassBalanceEnumerations.MassBalanceTypeEnum

class Glacier(GlamosData):
    '''
    Class representing a specific glacier of the GLAMOS dataset.
    
    Attributes:
        _pkVaw           Integer-based key used by the VAW and the Annual Glacier Report for the glacier identification.
        _pkSgi           Swiss Glacier Inventory key of the glacier.
        _pkGlims         GLIMS key of the glacier.
        _name            Common name of the glacier.
        _lengthChanges   Dictionary containing the entire time series of type DataObjects.LengthChange.LengthChange objects
        _massBalance     Dictionary containing the entire time series of type DataObjects.MassBalance.MassBalance objects
        _volumeChanges   Dictionary containing the entire time series of type DataObjects.VolumeChange.VolumeChange objects
    '''

    _pkVaw         = None
    
    _pkSgi         = None
    
    _pkGlims       = None
    
    _name          = None
    
    _lengthChanges = None
    
    _massBalances  = None
    
    _volumeChanges = None
    
    @property
    def pkVaw(self):
        '''
        Get the VAW identifier of the glacier.
        '''
        return self._pkVaw
    
    @property
    def pkSgi(self):
        '''
        Get the Swiss Glacier Inventory identifier of the glacier.
        '''
        return self._pkSgi

    
    @property
    def name(self):
        '''
        Get the name of the glacier.
        '''
        return self._name
    
    @property
    def lengthChanges(self):
        '''
        Get the entire length change time series of the glacier.
        '''
        return self._lengthChanges
    
    @property
    def massBalances(self):
        '''
        Get the entire mass balance time series of the glacier.
        '''
        return self._massBalances
    
    @property
    def massBalanceTable(self):
        '''
        Get the entire mass-balance time series of the glacier as pandas.DataFrame.
        
        #TODO: More specific description of the data frame.

        @rtype: pandas.DataFrame
        @return: Data frame (table) of the mass-balance observations.
        '''
        
        return MassBalance.createTable(self._massBalances)

    @property
    def volumeChanges(self):
        '''
        Get the entire volume change time series of the glacier.
        '''
        return self._volumeChanges

    def __init__(self, pk = None, pkVaw = None, pkSgi = None, name = None):
        '''
        Constructor of the Glacier class.
        
        @type pk: UUID
        @param pk: Unique identifier of the glacier
        
        @type pkVaw: int
        @param pkVaw: Unique identifier used by VAW.
        
        @type pkSgi: string
        @param pkSgi: Swiss Glacier Inventory identifier.
        
        @type name: string
        @param name: Common name of the glacier.
        '''
        
        super().__init__(pk)
        
        self._pkVaw   = pkVaw
        self._pkSgi   = pkSgi
        self._name    = name
        
        self._lengthChanges = dict()
        self._massBalances  = dict()
        self._volumeChanges = dict()
        
    def __str__(self):
        '''
        Overriding the __str__ method. The returned string will represent the glacier with id's and name.
        
        @rtype: string
        @return: String representation of the glacier
        '''
        
        representation = "{0}, {1}, {2}".format(self._pk, self._pkVaw, self._name)
        
        return representation
    
    def __eq__(self, other):
        '''
        Override of the default implementation of equality.
        
        Two instances of the class Glacier are identical, if both Swiss Glacier Inventory key are identical.
        
        @type other: Glacier
        @param other: Glacier to be compared.
        
        @rtype: boolean
        @return: Is the object equals with the other object.
        '''

        if isinstance(self, other.__class__):
            
            if self._pkSgi == other.pkSgi:
                return True
            else:
                return False
        else:
            return False
        
    def __ne__(self, other):
        '''
        Override of the default implementation of not equality.
        
        Two instances of the class Glacier are not identical, if the Swiss Glacier Inventory keys are not identical.
        
        @type other: Glacier
        @param other: Glacier to be compared.
        
        @rtype: boolean
        @return: Is the object not equals with the other object.
        '''
        
        return not self.__eq__(other)
    
    def addLengthChange(self, lengthChange):
        '''
        Adding an individual measurement of a length change. Containing the change between two years.
        
        @type lengthChange: DataObjects.LengthChange.LengthChange
        @param lengthChange: Length change between two specified years.
        '''
        
        #TODO: Using a different key (e.g. overriding the __eq__ and __ne__ of the LengthChange class.
        self._lengthChanges[lengthChange.dateFrom] = lengthChange
        
    def addMassBalance(self, massBalance):
        '''
        Adding an individual measurement of a mass balance. Containing the balance between two years.
        
        @type massBalance: DataObjects.MassBalance.MassBalance
        @param massBalance: Mass balance between two specified years.
        '''
        
        #TODO: Using a different key (e.g. overriding the __eq__ and __ne__ of the MassBalance class.
        self._massBalances[massBalance.dateFromAnnual] = massBalance
        
    def addVolumeChange(self, volumeChange):
        '''
        Adding an individual measurement of a volume change. Containing the change between two years.
        
        @type volumeChange: DataObjects.VolumeChange.VolumeChange
        @param volumeChange: Volume change between two specified years.
        '''
        
        #TODO: Using a different key (e.g. overriding the __eq__ and __ne__ of the VolumeChange class.
        self._volumeChanges[volumeChange.dateFrom] = volumeChange
        