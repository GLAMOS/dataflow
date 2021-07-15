'''
Created on 14.07.2021

@author: elias

Main script to import all VAW mass balance index daily data files (_cum) into the GLAMOS database.
'''

import configparser
import os

from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataWriters.DatabaseWriters.MassBalanceIndexDailyWriter import MassBalanceIndexDailyWriter
from dataflow.DataReaders.VawFileReaders.MassBalanceIndexDailyReader import MassBalanceIndexDailyReader
from dataflow.DataReaders.Exceptions.InvalidDataFileError import InvalidDataFileError

config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gldirw.cfg"

def insertDatabaseMassbalanceIndexDaily(allGlaciers):
    '''
    Parsing and writing all mass balance index daily data from VAW data-files into GLAMOS database.

    @type allGlaciers: Dictionary
    @param allGlaciers: Dictionary of all glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''

    rootDirectoryPath = config.get("MassBalanceIndexDaily", "rootDirectoryInput")
    dataDirectoryName = config.get("MassBalanceIndexDaily", "directoryInput")

    dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)

    if os.path.exists(dataDirectoryPath):
        # Loop over all mass-balance index daily data files in the directory.
        for inputFileName in os.listdir(dataDirectoryPath):

            inputFilePath = os.path.join(dataDirectoryPath, inputFileName)

            # Start with parsing the data file.
            massBalanceIndexDailyReader = None
            massBalanceIndexDailyWriter = None

            try:
                # Getting the reader object and start parsing.
                massBalanceIndexDailyReader = MassBalanceIndexDailyReader(config, inputFilePath, allGlaciers)

                # Important note:
                # The glacier object is still alive and could have mass-balance index daily objects of a
                # parsing process before. To have a redundancy free insert into the database,
                # possible mass-balance index daily readings have to be removed.
                massBalanceIndexDailyReader.glacier.massBalanceIndexDailys.clear()

                # Start of parsing the given data file.
                massBalanceIndexDailyReader.parse()

                # In case of a successful parsing process, a writer will be instantiated for immediate writing into the database.
                if massBalanceIndexDailyReader != None:

                    print("\n" + str(inputFileName))
                    print("--- Start writing to the database. Will take a while ... take a break ... ---\n")

                    # Getting the writer object ready and start inserting into the database.
                    massBalanceIndexDailyWriter = MassBalanceIndexDailyWriter(privateDatabaseAccessConfiguration)
                    massBalanceIndexDailyWriter.write(massBalanceIndexDailyReader.glacier)
                else:
                    raise Exception("MassBalancePointReader is None")

            except GlacierNotFoundError as glacierNotFoundError:
                print(glacierNotFoundError.message)
            except InvalidDataFileError as invalidDataFileError:
                print(invalidDataFileError.message)

            finally:
                if massBalanceIndexDailyReader != None:
                    massBalanceIndexDailyReader = None
                    del (massBalanceIndexDailyReader)
                if massBalanceIndexDailyWriter != None:
                    massBalanceIndexDailyWriter = None
                    del (massBalanceIndexDailyWriter)
    else:
        raise Exception("Data directory not existing")







if __name__ == '__main__':
    # Getting all glacier read from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    allGlaciers = glacierReader.getAllGlaciers()

    insertDatabaseMassbalanceIndexDaily(allGlaciers)