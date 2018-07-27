'''
Created on 22.05.2018

@author: yvo

Description:
Example of how to retrieve glacier data of glaciers from the database
and using the information directly in Python.

Preconditions:
- Python > 3.5
- psycopg2 installed
- databaseAccessConfiguration.cfg available
'''

import os

# Import of the reader objects.
from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader

# Private configuration file for the database access.

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.private.cfg"

# Getting the database reader ready.
glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
        
def printAllGlaciers():
    '''
    Will print all glaciers stored in the database.
    '''

    allGlaciers = glacierReader.getAllGlaciers()

    for k, v in allGlaciers.items():
        print("{0} -> {1}".format(k, v))
        
        # Output:
        # ...
        # E35 /15 -> 81dcff51-4ec8-11e8-896f-985fd331b2ee, 150, agnel
        # E35 /23 -> 81e0339e-4ec8-11e8-b2fe-985fd331b2ee, 151, laviner
        # C84 /09 -> 81d473d1-4ec8-11e8-8890-985fd331b2ee, 152, cantun
        # C35 /03 -> 8109348f-4ec8-11e8-aa67-985fd331b2ee, 153, rotondo
        # C53 /03 -> 81b0981e-4ec8-11e8-8784-985fd331b2ee, 154, mucia
        # C15 /01 -> 8243b05e-4ec8-11e8-897c-985fd331b2ee, 155, sassonero
        # B53 /07 -> 80077c00-4ec8-11e8-a5bc-985fd331b2ee, 156, hohbalm
        # ...
        

def printAletschGlacier():
    '''
    Will print the Aletsch glacier stored in the database.
    '''
    
    aletsch = glacierReader.getGlacierBySgi('B36/26')
    
    print(aletsch)
    
    # Output:
    # 805d642e-4ec8-11e8-b774-985fd331b2ee, 5, aletsch


if __name__ == '__main__':

    printAllGlaciers()
    printAletschGlacier()
