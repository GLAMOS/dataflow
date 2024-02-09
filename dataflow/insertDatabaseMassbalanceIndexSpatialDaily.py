'''
Created on 14.07.2021

@author: elias

Main script to import all VAW mass balance index daily data files (_cum) into the GLAMOS database.
'''

import configparser
import os

from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataWriters.DatabaseWriters.MassBalanceIndexSpatialDailyWriter import MassBalanceIndexSpatialDailyWriter
from dataflow.DataReaders.VawFileReaders.MassBalanceIndexSpatialDailyReader import MassBalanceIndexSpatialDailyReader
from dataflow.DataReaders.Exceptions.InvalidDataFileError import InvalidDataFileError

config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gldirw.cfg"

def insertDatabaseMassbalanceIndexSpatialDaily(allGlaciers):
    '''
    Parsing and writing all mass balance index spatial daily data from VAW data-files into GLAMOS database.

    @type allGlaciers: Dictionary
    @param allGlaciers: Dictionary of all glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''

    rootDirectoryPath = config.get("MassBalanceIndexSpatialDaily", "rootDirectoryInput")
    dataDirectoryName = config.get("MassBalanceIndexSpatialDaily", "indexSpatialDailyDirectoryInput")

    dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)

    if os.path.exists(dataDirectoryPath):
        # Loop over all mass-balance index spatial daily data files in the directory.
        for inputFileName in os.listdir(dataDirectoryPath):

            inputFilePath = os.path.join(dataDirectoryPath, inputFileName)

            # Start with parsing the data file.
            massBalanceIndexSpatialDailyReader = None
            massBalanceIndexSpatialDailyWriter = None

            try:
                # Getting the reader object and start parsing.
                massBalanceIndexSpatialDailyReader = MassBalanceIndexSpatialDailyReader(config, inputFilePath, allGlaciers)

                # Important note:
                # The glacier object is still alive and could have mass-balance index spatial daily objects of a
                # parsing process before. To have a redundancy free insert into the database,
                # possible mass-balance index spatial daily readings have to be removed.
                massBalanceIndexSpatialDailyReader.glacier.massBalanceIndexSpatialDailys.clear()

                # Start of parsing the given data file.
                massBalanceIndexSpatialDailyReader.parse()

                # In case of a successful parsing process, a writer will be instantiated for immediate writing into the database.
                if massBalanceIndexSpatialDailyReader != None:

                    print("\n" + str(inputFileName))
                    print("--- Start writing to the database. Will take a while ... take a break ... ---\n")

                    # Getting the writer object ready and start inserting into the database.
                    massBalanceIndexSpatialDailyWriter = MassBalanceIndexSpatialDailyWriter(privateDatabaseAccessConfiguration)
                    massBalanceIndexSpatialDailyWriter.write(massBalanceIndexSpatialDailyReader.glacier)
                else:
                    raise Exception("MassBalanceIndexDailyReader is None")

            except GlacierNotFoundError as glacierNotFoundError:
                print(glacierNotFoundError.message)
            except InvalidDataFileError as invalidDataFileError:
                print(invalidDataFileError.message)

            finally:
                if massBalanceIndexSpatialDailyReader != None:
                    massBalanceIndexSpatialDailyReader = None
                    del (massBalanceIndexSpatialDailyReader)
                if massBalanceIndexSpatialDailyWriter != None:
                    massBalanceIndexSpatialDailyWriter = None
                    del (massBalanceIndexSpatialDailyWriter)
    else:
        raise Exception("Data directory not existing")







if __name__ == '__main__':
    # Getting all glacier read from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    allGlaciers = glacierReader.getAllGlaciers()

    insertDatabaseMassbalanceIndexSpatialDaily(allGlaciers)