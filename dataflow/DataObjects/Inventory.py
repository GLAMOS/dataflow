'''
Created on 20.07.2018

@author: yvo
'''

from .Glamos import GlamosData

class Inventory(GlamosData):
    '''
    classdocs
    '''

    
    # ---- Static methods of the class ---
    @staticmethod
    def latestInventory(inventories):
        
        
        allEditions = list(inventories.keys())
        
        allEditions.sort()
        
        return inventories[allEditions[-1]]
    
    # ---- Members of the class ---
    
    _edition               = None

    _geometryWellKnownText = None
    
    _acquisition           = None

    def __init__(self, pk = None, 
                edition = None,
                geometryWellKnownText = None,
                acquisition = None):
        '''
        Constructor
        
        @type pk: uuid
        @param pk: Primary key of the inventory entry.
        @type edition: int
        @param edition: Year of the publication.
        @type geometryWellKnownText: datetime
        @param geometryWellKnownText: Start date of the mass balance observation.
        @type acquisition: int
        @param acquisition: Year of the acquisition of the geometry.
        '''
        
        super().__init__(pk)
        
        self._edition               = edition
        self._geometryWellKnownText = geometryWellKnownText
        self._acquisition           = acquisition
        
    @property
    def geometryWellKnownText(self):
        
        return self._geometryWellKnownText
    
    @property
    def edition(self):
        
        return self._edition
    
    @property
    def acquisition(self):
        
        return self._acquisition