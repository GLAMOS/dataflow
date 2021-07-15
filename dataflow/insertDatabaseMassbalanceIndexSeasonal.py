'''
Created on 14.07.2021

@author: elias

Main script to import all VAW mass balance index seasonal data files (_mb) into the GLAMOS database.
'''

import configparser
import os

from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataWriters.DatabaseWriters.MassBalanceIndexSeasonalWriter import MassBalanceIndexSeasonalWriter
from dataflow.DataReaders.VawFileReaders.MassBalanceIndexSeasonalReader import MassBalanceIndexSeasonalReader
from dataflow.DataReaders.Exceptions.InvalidDataFileError import InvalidDataFileError

config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gldirw.cfg"

def insertDatabaseMassbalanceIndexSeasonal(allGlaciers):
    '''
    Parsing and writing all mass balance index seasonal data from VAW data-files into GLAMOS database.

    @type allGlaciers: Dictionary
    @param allGlaciers: Dictionary of all glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''

    rootDirectoryPath = config.get("MassBalanceIndexSeasonal", "rootDirectoryInput")
    dataDirectoryName = config.get("MassBalanceIndexSeasonal", "directoryInput")

    dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)
    if os.path.exists(dataDirectoryPath):
        # Loop over all mass-balance index daily data files in the directory.
        for inputFileName in os.listdir(dataDirectoryPath):

            inputFilePath = os.path.join(dataDirectoryPath, inputFileName)

            # Start with parsing the data file.
            massBalanceIndexSeasonalReader = None
            massBalanceIndexSeasonalWriter = None

            try:
                # Getting the reader object and start parsing.
                massBalanceIndexSeasonalReader = MassBalanceIndexSeasonalReader(config, inputFilePath, allGlaciers)

                # Important note:
                # The glacier object is still alive and could have mass-balance index daily objects of a
                # parsing process before. To have a redundancy free insert into the database,
                # possible mass-balance index daily readings have to be removed.
                massBalanceIndexSeasonalReader.glacier.massBalanceSeasonalDailys.clear()

                # Start of parsing the given data file.
                massBalanceIndexSeasonalReader.parse()

                # In case of a successful parsing process, a writer will be instantiated for immediate writing into the database.
                if massBalanceIndexSeasonalReader != None:

                    print("\n" + str(inputFileName))
                    print("--- Start writing to the database. Will take a while ... take a break ... ---\n")

                    # Getting the writer object ready and start inserting into the database.
                    massBalanceIndexSeasonalWriter = MassBalanceIndexSeasonalWriter(privateDatabaseAccessConfiguration)
                    massBalanceIndexSeasonalWriter.write(massBalanceIndexSeasonalReader.glacier)
                else:
                    raise Exception("MassBalanceIndexSeasonalReader is None")

            except GlacierNotFoundError as glacierNotFoundError:
                print(glacierNotFoundError.message)
            except InvalidDataFileError as invalidDataFileError:
                print(invalidDataFileError.message)

            finally:
                if massBalanceIndexSeasonalReader != None:
                    massBalanceIndexSeasonalReader = None
                    del (massBalanceIndexSeasonalReader)
                if massBalanceIndexSeasonalWriter != None:
                    massBalanceIndexSeasonalWriter = None
                    del (massBalanceIndexSeasonalWriter)
    else:
        raise Exception("Data directory not existing")


if __name__ == '__main__':
    # Getting all glacier read from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    allGlaciers = glacierReader.getAllGlaciers()

    insertDatabaseMassbalanceIndexSeasonal(allGlaciers)