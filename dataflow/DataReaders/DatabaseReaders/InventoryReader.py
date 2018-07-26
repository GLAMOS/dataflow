'''
Created on 26.07.2018

@author: yvo
'''

from .GlamosDatabaseReader import GlamosDatabaseReader
from DataObjects.Inventory import Inventory

import uuid

class InventoryReader(GlamosDatabaseReader):
    '''
    classdocs
    '''
    
    # ---- Members of the class ---

    _TABLE_INVENTORY = "inventory.vw_inventories"

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)

    def getData(self, glacier):
        '''
        Retrieves all inventory data of the given glacier.
        
        The inventory data are stored in the inventory dictionary of the glacier instance.
        
        @type glacier: DataObject.Glacier.Glacier
        @param glacier: Glacier of which all the inventories has to be retrieved.
        '''
        
        # FIXME: Working with glacier.pk instead of glacier.pkVaw. View has to be improved.        
        statement = "SELECT * FROM {0} WHERE pk_sgi = '{1}';".format(self._TABLE_INVENTORY, glacier.pkSgi)
        
        results = super().retriveData(statement)
        
        if results != None:
            for result in results:
                glacier.addInventory(self._recordToObject(result))
            
            
    def _recordToObject(self, dbRecord):
        
        pk          = uuid.UUID(dbRecord[0])
        acquisition = int(dbRecord[2])
        sgi_release = int(dbRecord[3])
        geom_wkt    = dbRecord[4]
        
        
        return Inventory(pk, sgi_release, geom_wkt, acquisition)