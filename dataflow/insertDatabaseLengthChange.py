'''
Created on 1.2.2024

@author: elias

Main script to import all VAW length change data files into the GLAMOS database.
'''

import configparser
import os

from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataReaders.VawFileReaders.VawFileReader import VawFileReader
from dataflow.DataReaders.VawFileReaders.LengthChangeReader import LengthChangeReader
from dataflow.DataWriters.DatabaseWriters.LengthChangeWriter import LengthChangeWriter

from dataflow.DataReaders.Exceptions.InvalidDataFileError import InvalidDataFileError

config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r"./databaseAccessConfiguration.gldirw.cfg"

def insertDatabaseLengthChange(allGlaciers):
    '''
    Parsing and writing all length change data from VAW data-files into GLAMOS database.
    
    @type allGlaciers: Dictionary
    @param allGlaciers: Dictionary of all glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''    
    
    rootDirectoryPath = config.get("LengthChange", "rootDirectoryInput")
    dataDirectoryName = config.get("LengthChange", "directoryInput")
    
    dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)
    
    if os.path.exists(dataDirectoryPath):

        # Loop over all mass-balance data files in the directory.
        for inputFileName in os.listdir(dataDirectoryPath):
            
            inputFilePath = os.path.join(dataDirectoryPath, inputFileName)
            
            print("\n")
            print("----------------------------------------------------")
            print("--- Start parsing input length change data file. ---")
            print("\n")
            print("Current input data file: {0}".format(inputFilePath))
            
            # Start with parsing the data file.
            if os.path.isfile(inputFilePath):
                
                lengthChangeReader = None
                lengthChangeWriter = None
                
            try:
                # Getting the reader object and start parsing.
                lengthChangeReader = LengthChangeReader(config, inputFilePath, allGlaciers)
                
                # Important note:
                # The glacier object is still alive and could have length-change objects of a 
                # parsing process before. To have a redundancy free insert into the database,
                # possible length-change readings have to be removed.
                lengthChangeReader.glacier.lengthChanges.clear()
                
                # Start of parsing the given data file.
                lengthChangeReader.parse()

                # In case of a successful parsing process, a writer will be instantiated for immediate writing into the database.
                if lengthChangeReader != None:
                    
                    print("\n--- Start writing to the database. Will take a while ... take a break ... ---\n")
    
                    # Getting the writer object ready and start inserting into the database.
                    lengthChangeWriter = LengthChangeWriter(privateDatabaseAccessConfiguration)
                    lengthChangeWriter.write(lengthChangeReader.glacier)

                else:
                    raise Exception("LengthChangeReader is None")
                
                
            except GlacierNotFoundError as glacierNotFoundError:
                print(glacierNotFoundError.message)
            except InvalidDataFileError as invalidDataFileError:
                print(invalidDataFileError.message)
                
            finally:
                if lengthChangeReader != None:
                    lengthChangeReader = None
                    del(lengthChangeReader)
                if lengthChangeWriter != None:
                    lengthChangeWriter = None
                    del(lengthChangeWriter)
                
                
                
    else:
        raise Exception("Data directory " + dataDirectoryPath + " not existing")

if __name__ == '__main__':

    # Getting all glacier read from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    allGlaciers = glacierReader.getAllGlaciers()
    
    insertDatabaseLengthChange(allGlaciers)