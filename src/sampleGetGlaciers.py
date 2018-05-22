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

# Import of the reader objects.
from DataReaders.DatabaseReaders.GlacierReader import GlacierReader

# Private configuration file for the database access.
privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.cfg"

# Getting the database reader ready.
glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
        
def printAllGlaciers():
    '''
    Will print all glaciers stored in the database.
    '''

    allGlaciers = glacierReader.getAllGlaciers()

    for k, v in allGlaciers.items():
        print("{0} -> {1}".format(k, v))
        

def printAletschGlacier():
    '''
    Will print the Aletsch glacier stored in the database.
    '''
    
    aletsch = glacierReader.getGlacierBySgi('B36 /26')
    
    print(aletsch)


if __name__ == '__main__':
    
    printAllGlaciers()
    printAletschGlacier()