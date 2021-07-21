'''
Created on 12.07.2018

@author: yvo
'''

import matplotlib.pyplot as plt

import configparser
import os
import sys

from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataReaders.DatabaseReaders.VolumeChangeReader import VolumeChangeReader

def plotVolumeChange(glacier):
    '''
    Plotting of the volume-change data available.
    
    @type glacier: DataObjects.Glacier
    @param glacier: Glacier object which volume-change observations have to be plotted.
    '''
    
    print("Preparation of plotting {0} volume-change observations of {1}".format(len(glacier.volumeChanges), glacier.name))
    
    volumeChangesObservationsYear = []
    volumeChangesObservations     = []
    
    for volumeChange in glacier.volumeChanges.values():
        
        volumeChangesObservationsYear.append(volumeChange.dateFrom.year)
        
        if len(volumeChangesObservations) > 0:
            cumulativeVolumeChange = volumeChangesObservations[-1] + volumeChange.volumeChange
            volumeChangesObservations.append(cumulativeVolumeChange)
        else:
            volumeChangesObservations.append(volumeChange.volumeChange)
        
    if len(volumeChangesObservationsYear) > 2:
        plt.plot(volumeChangesObservationsYear, volumeChangesObservations, 'ro')
        plt.axis(
            [min(volumeChangesObservationsYear), max(volumeChangesObservationsYear),
             min(volumeChangesObservations), max(volumeChangesObservations)])
        plt.xlabel('year')
        plt.ylabel('$km^3$')
        plt.title("Mass-balance observations of {0}".format(glacier.name))
        plt.show()
        plt.gcf().clear()

if __name__ == '__main__':
    
    
    config = configparser.ConfigParser()
    config.read("dataflow.cfg")

    privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gladmin.cfg"
    
    if os.path.exists(privateDatabaseAccessConfiguration) == True:
        if os.path.isfile(privateDatabaseAccessConfiguration) == True:
            print("Private database configuration '{0}' will be used.".format(privateDatabaseAccessConfiguration)) 
        else:
            print("Private database configuration '{0}' isn't a file! Check file! Application will terminate.".format(privateDatabaseAccessConfiguration))
            sys.exit(1)
    else:
        print("Private database configuration '{0}' is not existing! Check path! Application will terminate.".format(privateDatabaseAccessConfiguration))
        sys.exit(1)
    
    focusGlaciers = ['B52-24', 'B45-04'] # Schwarzberg-Gletscher (VAW-ID = 10), Griesgletscher (VAW-ID = 3)
    
    # Getting the dataflow.DataReaders.DatabaseReaders.GlacierReader ready to retrieve glacier objects from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    # Empty directory for the found focus glaciers.
    glaciers = dict()
    
    try:
    
        # Check if the database is available. If not, get alternative glaciers for plotting.
        if glacierReader.isDatabaseAvailable == True:
            
            print("The GLAMOS database is available. Glacier objects are read from the database.")
            
            for focusGlacier in focusGlaciers:
                glacierFound = glacierReader.getGlacierBySgi(focusGlacier)
                glaciers[glacierFound.pkSgi] = glacierFound
            
            volumeChangeReader = VolumeChangeReader(privateDatabaseAccessConfiguration)
             
            for glacier in glaciers.values():
                
                volumeChangeReader.getData(glacier)
                
                print(glacier)
                for volumeChange in glacier.volumeChanges.values():
                    print("\t- " + str(volumeChange))
                    
                plotVolumeChange(glacier)
            
        else:
            
            print("Database not available! Application will terminate.")
            sys.exit(2)
            
    except Exception as e:
        
        print(e.message)
        print("Sample script aborted!")