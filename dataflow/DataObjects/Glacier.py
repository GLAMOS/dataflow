'''
Created on 18.05.2018

@author: yvo
'''

from dataflow.DataObjects.Glamos import GlamosData
from dataflow.DataObjects.MassBalance import MassBalance
from dataflow.DataObjects.Enumerations.MassBalanceEnumerations import MassBalanceTypeEnum
from dataflow.DataObjects.Inventory import Inventory
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
        _inventories     Dictionary containing the available inventory data of the glacier.
    '''

    _pkVaw         = None
    _pkSgi         = None
    _pkGlims       = None
    _name          = None
    _lengthChanges = None
    _massBalances  = None
    _massBalanceIndexDailys = None
    _massBalancePoints = None
    _volumeChanges = None
    _inventories   = None
    
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
    def massBalanceDataFrame(self):
        '''
        Get the entire mass-balance time series of the glacier as pandas.DataFrame.
        
        #TODO: More specific description of the data frame.

        @rtype: pandas.DataFrame
        @return: Data frame (table) of the mass-balance observations.
        '''
        
        return MassBalance.createDataFrame(self._massBalances)

    @property
    def massBalanceIndexDailys(self):
        '''
        Get the entire mass balance point time series of the glacier.
        '''
        return self._massBalanceIndexDailys

    @property
    def massBalancePoints(self):
        '''
        Get the entire mass balance point time series of the glacier.
        '''
        return self._massBalancePoints
    
    @property
    def latestInventoryGeometry(self):
        '''
        Gets the geometry from the latest inventory available of the glacier as WellKnownText.
        
        @rtype: string
        @return: Entire outline of the latest inventory available as WellKnownText.
        '''
        
        return Inventory.latestInventory(self._inventories).geometryWellKnownText

    @property
    def volumeChanges(self):
        '''
        Get the entire volume change time series of the glacier.
        '''
        return self._volumeChanges
    
    @property
    def inventories(self):
        '''
        Get all available inventories.
        '''
        
        return self._inventories

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
        self._massBalanceIndexSeasonals = dict()
        self._massBalanceIndexDailys = dict()
        self._massBalancePoints = dict()
        self._volumeChanges = dict()
        
        self._inventories   = dict()
        
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

    def addMassBalanceIndexSeasonal(self, massBalanceIndexSeasonal):
        '''
        Adding an individual massbalance index seasonal. Containing the change between two years.

        @type massbalanceIndexSeasonal: DataObjects.MassBalanceIndexSeasonal.MassBalanceIndexSeasonal
        @param massbalanceIndexSeasonal: Mass Balance on a seasonal index.
        '''

        # TODO: Using a different key (e.g. overriding the __eq__ and __ne__ of the MassBalanceIndexSeasonal class.
        self._massBalanceIndexSeasonals[massBalanceIndexSeasonal.pk] = massBalanceIndexSeasonal

    def addMassBalanceIndexDaily(self, massBalanceIndexDaily):
        '''
        Adding an individual massbalance index daily. Containing the change between two years.

        @type massbalanceIndexDaily: DataObjects.MassBalanceIndexDaily.MassBalanceIndexDaily
        @param massbalanceIndexDaily: Mass Balance on a daily index.
        '''

        # TODO: Using a different key (e.g. overriding the __eq__ and __ne__ of the MassBalanceIndexDaily class.
        self._massBalanceIndexDailys[massBalanceIndexDaily.pk] = massBalanceIndexDaily

    def addMassBalancePoint(self, massBalancePoint):
        '''
        Adding an individual measurement of a massbalance point. Containing the change between two years.

        @type massbalancePoint: DataObjects.MassBalancePoint.MassBalancePoint
        @param massbalancePoints: Mass Balance between two specified years.
        '''

        # TODO: Using a different key (e.g. overriding the __eq__ and __ne__ of the MassBalancePoint class.
        self._massBalancePoints[massBalancePoint.pk] = massBalancePoint
        
    def addVolumeChange(self, volumeChange):
        '''
        Adding an individual measurement of a volume change. Containing the change between two years.
        
        @type volumeChange: DataObjects.VolumeChange.VolumeChange
        @param volumeChange: Volume change between two specified years.
        '''
        
        #TODO: Using a different key (e.g. overriding the __eq__ and __ne__ of the VolumeChange class.
        self._volumeChanges[volumeChange.dateFrom] = volumeChange

        
    def addInventory(self, inventory):
        
        self._inventories[inventory.edition] = inventory