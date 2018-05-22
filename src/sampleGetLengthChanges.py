'''
Created on 22.05.2018

@author: yvo

Description:
Example of how to retrieve the time series of length change data of glaciers from the database
and using the information directly in Python.

Preconditions:
- Python > 3.5
- psycopg2 installed
- databaseAccessConfiguration.cfg available
'''

# Import of the reader objects.
from DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from DataReaders.DatabaseReaders.LengthChangeReader import LengthChangeReader

# Private configuration file for the database access.
privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.cfg"

# Getting the database readers ready.
glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
lengthChangeReader = LengthChangeReader(privateDatabaseAccessConfiguration)

def printGlacierLengthChangeBySgi(pkSgi):
    '''
    Will print the number of measurements and the individual measurements.
    '''
    
    # Retrieving the glacier object from the database using the SGI key.
    foundGlacier = glacierReader.getGlacierBySgi(pkSgi)
    # Retrieving of the length change time series for the given glacier.
    lengthChangeReader.getGlacierLengthChanges(foundGlacier)
    
    # Print the information.
    print("Number of measurements: {0}".format(len(foundGlacier.lengthChanges)))
    for lengthChange in foundGlacier.lengthChanges.values():
        print(lengthChange)


if __name__ == '__main__':
    
    # Print the length change data of the Aletsch glacier.
    printGlacierLengthChangeBySgi('B36 /26')
