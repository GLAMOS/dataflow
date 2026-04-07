'''
Created on 17.12.2025

@author: elias

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
import pandas as pd
import matplotlib.pyplot as plt

# Private configuration file for the database access.
privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gldiro.cfg"

# Getting the database readers ready.
glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
lengthChangeReader = LengthChangeReader(privateDatabaseAccessConfiguration)


def getGlacierLengthChangeBySgi(pkSgi):
    '''
    Will print the number of measurements and the individual measurements.
    '''

    # Retrieving the glacier object from the database using the SGI key.
    foundGlacier = glacierReader.getGlacierBySgi(pkSgi)
    # Retrieving of the length change time series for the given glacier.
    lengthChangeReader.getData(foundGlacier)

    # Print the information.
    print(foundGlacier.name + '(' + foundGlacier.pkSgi + ')')
    print("Number of measurements: {0}".format(len(foundGlacier.lengthChanges)))

    df = pd.DataFrame(columns=['date_from','date_to','variation'])

    for lengthChange in foundGlacier.lengthChanges.values():
        date_from = lengthChange.dateFrom
        date_to = lengthChange.dateTo
        variation = lengthChange.variationQuantitative

        # Create a new row
        new_data = {'date_from': date_from, 'date_to': date_to, 'variation': variation}

        # Add it to the dataframe
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)


    print(df)
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
    getGlacierLengthChangeBySgi('B36-26')