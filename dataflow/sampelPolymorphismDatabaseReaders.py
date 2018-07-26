'''
Created on 12.07.2018

@author: yvo

Sample script showing polymorphistic approach to retrieve attribute 
data of glaciers from the database.
'''

import configparser
import os
import sys

from DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from DataReaders.DatabaseReaders.VolumeChangeReader import VolumeChangeReader
from DataReaders.DatabaseReaders.LengthChangeReader import LengthChangeReader
from DataReaders.DatabaseReaders.MassBalanceReader import MassBalanceReader


def listData(glaciers):
    '''
    Simple listing of the attribute data of the given glaciers.
    
    @type glaciers: dict
    @param glaciers: Dictionary with DataObjects.Glacier.Glacier objects.
    '''
    
    for glacier in glaciers.values():
        print("---")
        print(glacier)
        
        # Printing all volume change data if available.
        if len(glacier.volumeChanges) > 0:
            print("Volume changes:")
            for volumeChange in glacier.volumeChanges.values():
                print("\t-> " + str(volumeChange))

        # Printing all length change data if available.
        if len(glacier.lengthChanges) > 0:
            print("Length changes:")
            for lengthChange in glacier.lengthChanges.values():
                print("\t-> " + str(lengthChange))
                
        # Printing all mass balance data if available.
        if len(glacier.massBalances) > 0:
            print("Mass balances:")
            for massBalance in glacier.massBalances.values():
                print("\t-> " + str(massBalance))

if __name__ == '__main__':
    
    config = configparser.ConfigParser()
    config.read("dataflow.cfg")

    privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.private.cfg"
    
    if os.path.exists(privateDatabaseAccessConfiguration) == True:
        if os.path.isfile(privateDatabaseAccessConfiguration) == True:
            print("Private database configuration '{0}' will be used.".format(privateDatabaseAccessConfiguration)) 
        else:
            print("Private database configuration '{0}' isn't a file! Check file! Application will terminate.".format(privateDatabaseAccessConfiguration))
            sys.exit(1)
    else:
        print("Private database configuration '{0}' is not existing! Check path! Application will terminate.".format(privateDatabaseAccessConfiguration))
        sys.exit(1)
    
    focusGlaciers = ['C14 /10', 'B36 /26', 'B83 /03'] # Basodino (VAW-ID = 104), Aletsch (VAW-ID = 5), Corbassiere (VAW-ID = 38)
    
    # Getting the dataflow.DataReaders.DatabaseReaders.GlacierReader ready to retrieve glacier objects from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    # Empty directory for the found focus glaciers.
    glaciers = dict()
    
    # Getting all the data readers for the attribute values of the glaciers ready.
    dataReaders = []
    dataReaders.append(VolumeChangeReader(privateDatabaseAccessConfiguration))
    dataReaders.append(LengthChangeReader(privateDatabaseAccessConfiguration))
    dataReaders.append(MassBalanceReader(privateDatabaseAccessConfiguration))
    
    try:
    
        # Check if the database is available. If not, get alternative glaciers for plotting.
        if glacierReader.isDatabaseAvailable == True:
            
            print("The GLAMOS database is available. Glacier objects are read from the database.")
            
            for focusGlacier in focusGlaciers:
                glacierFound = glacierReader.getGlacierBySgi(focusGlacier)
                glaciers[glacierFound.pkSgi] = glacierFound

            # Getting the attributes from the database.
            for glacier in glaciers.values():
                
                # Polymorphistic approach to read attribute data by a list of readers.
                for dataReader in dataReaders:
                    dataReader.getData(glacier)
            
            # Printing the glaciers and their attributes to the console.  
            listData(glaciers)
                
        else:
            
            print("Database not available! Application will terminate.")
            sys.exit(2)
            
    except Exception as e:
        
        print(e.message)
        print("Sample script aborted!")
