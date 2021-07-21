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
from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataReaders.DatabaseReaders.LengthChangeReader import LengthChangeReader

# Private configuration file for the database access.
privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gldiro.cfg"

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
    lengthChangeReader.getData(foundGlacier)
    
    # Print the information.
    print("Number of measurements: {0}".format(len(foundGlacier.lengthChanges)))
    
    # Output:
    # Number of measurements: 126
    
    for lengthChange in foundGlacier.lengthChanges.values():
        print(lengthChange)

    # Output:
    # ...
    # 1995-09-01 -> 1996-09-01: -30.0 m length change
    # 1996-09-01 -> 1997-09-01: -43.0 m length change
    # 1997-09-01 -> 1999-09-01: -46.0 m length change
    # 1999-10-27 -> 2000-08-23: -18.5 m length change
    # 2000-08-23 -> 2001-08-23: -47.8 m length change
    # 2001-08-23 -> 2002-09-16: -57.0 m length change
    # ...

if __name__ == '__main__':
    
    # Print the length change data of the Aletsch glacier.
    printGlacierLengthChangeBySgi('B36-26')
