'''
Created on 11.07.2018

@author: yvo

Main script to import all VAW volume change data files into the GLAMOS database.
'''

import configparser
import os

from src.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from src.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from src.DataWriters.DatabaseWriters.VolumeChangeWriter import VolumeChangeWriter
from src.DataReaders.VawFileReaders.VolumeChangeReader import VolumeChangeReader

config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.private.cfg"

def insertDatabaseVolumeChange(allGlaciers):
    '''
    Parsing and writing all volume change data from VAW data-files into GLAMOS database.
    
    @type allGlaciers: Dictionary
    @param allGlaciers: Dictionary of all glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''

    rootDirectoryPath = config.get("VolumeChange", "rootDirectoryInput")
    dataDirectoryName = config.get("VolumeChange", "directoryInput")
    
    dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)
    
    volumeChangeReader = None
    
    if os.path.exists(dataDirectoryPath):

        # Loop over all mass-balance data files in the directory.
        for inputFileName in os.listdir(dataDirectoryPath):
            
            inputFilePath = os.path.join(dataDirectoryPath, inputFileName)
            
            # Start with parsing the data file.
            if os.path.isfile(inputFilePath):

                try:
                    # Getting the reader object and start parsing.
                    volumeChangeReader = VolumeChangeReader(inputFilePath, allGlaciers)
                    volumeChangeWriter = None
                    
                    # Important note:
                    # The glacier object is still alive and could have mass-balance objects of a 
                    # parsing process before. To have a redundancy free insert into the database,
                    # possible mass-balance readings have to be removed.
                    volumeChangeReader.glacier.volumeChanges.clear()
                    
                    # Start of parsing the given data file.
                    volumeChangeReader.parse()
                                      
                    # In case of a successful parsing process, a writer will be instantiated for immediate writing into the database.
                    if volumeChangeReader != None:
                        
                        print("\n--- Start writing to the database. Will take a while ... take a break ... ---\n")
        
                        # Getting the writer object ready and start inserting into the database.
                        volumeChangeWriter = VolumeChangeWriter(privateDatabaseAccessConfiguration)
                        volumeChangeWriter.write(volumeChangeReader.glacier)

                    else:
                        raise Exception("VolumeChangeReader is None")
                    
                except GlacierNotFoundError as glacierNotFoundError:
                    print(glacierNotFoundError.message)
                    
                finally:
                    if volumeChangeReader != None:
                        volumeChangeReader = None
                        del(volumeChangeReader)
                    if volumeChangeWriter != None:
                        volumeChangeWriter = None
                        del(volumeChangeWriter)
        
    else:
        raise Exception("Data directory not existing")


if __name__ == '__main__':
    
    # Getting all glacier read from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    allGlaciers = glacierReader.getAllGlaciers()
    
    insertDatabaseVolumeChange(allGlaciers)