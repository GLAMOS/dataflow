'''
Created on 14.07.2021

@author: elias

Main script to import all VAW mass balance index seasonal data files (_mb) into the GLAMOS database.
'''

import configparser
import os

from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataWriters.DatabaseWriters.MassBalanceIndexTimeSeasonalWriter import MassBalanceIndexTimeSeasonalWriter
from dataflow.DataReaders.VawFileReaders.MassBalanceIndexTimeSeasonalReader import MassBalanceIndexTimeSeasonalReader
from dataflow.DataReaders.Exceptions.InvalidDataFileError import InvalidDataFileError

config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gldirw.cfg"

def insertDatabaseMassbalanceIndexTimeSeasonal(allGlaciers):
    '''
    Parsing and writing all mass balance index seasonal data from VAW data-files into GLAMOS database.

    @type allGlaciers: Dictionary
    @param allGlaciers: Dictionary of all glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''

    rootDirectoryPath = config.get("MassBalanceIndexTimeSeasonal", "rootDirectoryInput")
    dataDirectoryName = config.get("MassBalanceIndexTimeSeasonal", "indexTimeSeasonalDirectoryInput")

    dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)
    if os.path.exists(dataDirectoryPath):
        # Loop over all mass-balance index seasonal data files in the directory.
        for inputFileName in os.listdir(dataDirectoryPath):

            inputFilePath = os.path.join(dataDirectoryPath, inputFileName)

            # Start with parsing the data file.
            massBalanceIndexTimeSeasonalReader = None
            massBalanceIndexTimeSeasonalWriter = None

            try:
                # Getting the reader object and start parsing.
                massBalanceIndexTimeSeasonalReader = MassBalanceIndexTimeSeasonalReader(config, inputFilePath, allGlaciers)

                # Important note:
                # The glacier object is still alive and could have mass-balance index seasonal objects of a
                # parsing process before. To have a redundancy free insert into the database,
                # possible mass-balance index seasonal readings have to be removed.
                massBalanceIndexTimeSeasonalReader.glacier.massBalanceIndexTimeSeasonals.clear()

                # Start of parsing the given data file.
                massBalanceIndexTimeSeasonalReader.parse()

                # In case of a successful parsing process, a writer will be instantiated for immediate writing into the database.
                if massBalanceIndexTimeSeasonalReader != None:

                    print("\n" + str(inputFileName))
                    print("--- Start writing to the database. Will take a while ... take a break ... ---\n")

                    # Getting the writer object ready and start inserting into the database.
                    massBalanceIndexTimeSeasonalWriter = MassBalanceIndexTimeSeasonalWriter(privateDatabaseAccessConfiguration)
                    massBalanceIndexTimeSeasonalWriter.write(massBalanceIndexTimeSeasonalReader.glacier)
                else:
                    raise Exception("MassBalanceIndexSeasonalReader is None")

            except GlacierNotFoundError as glacierNotFoundError:
                print(glacierNotFoundError.message)
            except InvalidDataFileError as invalidDataFileError:
                print(invalidDataFileError.message)

            finally:
                if massBalanceIndexTimeSeasonalReader != None:
                    massBalanceIndexTimeSeasonalReader = None
                    del (massBalanceIndexTimeSeasonalReader)
                if massBalanceIndexTimeSeasonalWriter != None:
                    massBalanceIndexTimeSeasonalWriter = None
                    del (massBalanceIndexTimeSeasonalWriter)
    else:
        raise Exception("Data directory not existing")


if __name__ == '__main__':
    # Getting all glacier read from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    allGlaciers = glacierReader.getAllGlaciers()

    insertDatabaseMassbalanceIndexTimeSeasonal(allGlaciers)