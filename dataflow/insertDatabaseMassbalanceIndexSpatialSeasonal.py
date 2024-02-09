'''
Created on 9.2.2024

@author: elias

Main script to import all VAW mass balance index spatial seasonal data files (_mb) into the GLAMOS database.
'''

import configparser
import os

from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataWriters.DatabaseWriters.MassBalanceIndexSpatialSeasonalWriter import MassBalanceIndexSpatialSeasonalWriter
from dataflow.DataReaders.VawFileReaders.MassBalanceIndexSpatialSeasonalReader import MassBalanceIndexSpatialSeasonalReader
from dataflow.DataReaders.Exceptions.InvalidDataFileError import InvalidDataFileError

config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gldirw.cfg"

def insertDatabaseMassbalanceIndexSpatialSeasonal(allGlaciers):
    '''
    Parsing and writing all mass balance index spatial seasonal data from VAW data-files into GLAMOS database.

    @type allGlaciers: Dictionary
    @param allGlaciers: Dictionary of all glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''

    rootDirectoryPath = config.get("MassBalanceIndexSpatialSeasonal", "rootDirectoryInput")
    dataDirectoryName = config.get("MassBalanceIndexSpatialSeasonal", "indexSpatialSeasonalDirectoryInput")

    dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)
    if os.path.exists(dataDirectoryPath):
        # Loop over all mass-balance index seasonal data files in the directory.
        for inputFileName in os.listdir(dataDirectoryPath):

            inputFilePath = os.path.join(dataDirectoryPath, inputFileName)

            # Start with parsing the data file.
            massBalanceIndexSpatialSeasonalReader = None
            massBalanceIndexSpatialSeasonalWriter = None

            try:
                # Getting the reader object and start parsing.
                massBalanceIndexSpatialSeasonalReader = MassBalanceIndexSpatialSeasonalReader(config, inputFilePath, allGlaciers)

                # Important note:
                # The glacier object is still alive and could have mass-balance index seasonal objects of a
                # parsing process before. To have a redundancy free insert into the database,
                # possible mass-balance index seasonal readings have to be removed.
                massBalanceIndexSpatialSeasonalReader.glacier.massBalanceIndexSpatialSeasonals.clear()

                # Start of parsing the given data file.
                massBalanceIndexSpatialSeasonalReader.parse()

                # In case of a successful parsing process, a writer will be instantiated for immediate writing into the database.
                if massBalanceIndexSpatialSeasonalReader != None:

                    print("\n" + str(inputFileName))
                    print("--- Start writing to the database. Will take a while ... take a break ... ---\n")

                    # Getting the writer object ready and start inserting into the database.
                    massBalanceIndexSpatialSeasonalWriter = MassBalanceIndexSpatialSeasonalWriter(privateDatabaseAccessConfiguration)
                    massBalanceIndexSpatialSeasonalWriter.write(massBalanceIndexSpatialSeasonalReader.glacier)
                else:
                    raise Exception("MassBalanceIndexSpatialSeasonalReader is None")

            except GlacierNotFoundError as glacierNotFoundError:
                print(glacierNotFoundError.message)
            except InvalidDataFileError as invalidDataFileError:
                print(invalidDataFileError.message)

            finally:
                if massBalanceIndexSpatialSeasonalReader != None:
                    massBalanceIndexSpatialSeasonalReader = None
                    del (massBalanceIndexSpatialSeasonalReader)
                if massBalanceIndexSpatialSeasonalWriter != None:
                    massBalanceIndexSpatialSeasonalWriter = None
                    del (massBalanceIndexSpatialSeasonalWriter)
    else:
        raise Exception("Data directory not existing")


if __name__ == '__main__':
    # Getting all glacier read from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    allGlaciers = glacierReader.getAllGlaciers()

    insertDatabaseMassbalanceIndexSpatialSeasonal(allGlaciers)