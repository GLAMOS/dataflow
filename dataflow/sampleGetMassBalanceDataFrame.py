'''
Created on 12.07.2018

@author: yvo

Sample script showing polymorphistic approach to retrieve attribute 
data of glaciers from the database.
'''

import configparser
import inspect
import sys

from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataReaders.DatabaseReaders.VolumeChangeReader import VolumeChangeReader
from dataflow.DataReaders.DatabaseReaders.LengthChangeReader import LengthChangeReader
from dataflow.DataReaders.DatabaseReaders.MassBalanceReader import MassBalanceReader

def printMassBalanceDataFrames(glaciers):
    
    for glacier in glaciers.values():
        print("---")
        print(glacier)
        
        # Check the availability of mass-balance object for inspection and printing the data-frame.
        if len(glacier.massBalances.values()):

        
            print("Available columns and their documentations:")
            for column in list(glacier.massBalanceDataFrame):
                
                docColumn = "Documentation not available yet"
                
                # TODO: Getting the doc string of the columns of the data frame by inspecting the members of a MassBalance object.
                
                print("- {0}: {1}".format(column, docColumn))

            print(glacier.massBalanceDataFrame)

if __name__ == '__main__':
    
    config = configparser.ConfigParser()
    config.read("dataflow.cfg")

    privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gldiro.cfg"
    print(privateDatabaseAccessConfiguration + ' will be used to access the databse')
    focusGlaciers = ['C14-10', 'B36-26', 'B83-03'] # Basodino (VAW-ID = 104), Aletsch (VAW-ID = 5), Corbassiere (VAW-ID = 38)
    
    # Getting the dataflow.DataReaders.DatabaseReaders.GlacierReader ready to retrieve glacier objects from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    # Empty directory for the found focus glaciers.
    glaciers = dict()
    
    # Getting all the data readers for the attribute values of the glaciers ready.
    dataReaders = []
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
            
            # Printing the pandas.DataFrame of the mass-balances of the glaciers.
            printMassBalanceDataFrames(glaciers)
                
        else:
            
            print("Database not available! Application will terminate.")
            sys.exit(2)
            
    except Exception as e:
        
        print(e.message)
        print("Sample script aborted!")
