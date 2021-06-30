'''
Created on 23.03.2021

@author: elias

Main script to import all VAW mass balance point data files into the GLAMOS database.
'''

import configparser
import os

from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataWriters.DatabaseWriters.MassBalancePointWriter import MassBalancePointWriter
from dataflow.DataReaders.VawFileReaders.MassBalancePointReader import MassBalancePointReader
from dataflow.DataReaders.Exceptions.InvalidDataFileError import InvalidDataFileError

config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gldirw.cfg"


def insertDatabaseMassbalancePoint(allGlaciers):
    '''
    Parsing and writing all mass balance point data from VAW data-files into GLAMOS database.

    @type allGlaciers: Dictionary
    @param allGlaciers: Dictionary of all glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''

    rootDirectoryPath = config.get("MassbalancePoint", "rootDirectoryInput")
    dataDirectoryName = config.get("MassbalancePoint", "directoryInput")

    dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)

    if os.path.exists(dataDirectoryPath):
        # Loop over all mass-balance data files in the directory.
        for inputFileName in os.listdir(dataDirectoryPath):

            inputFilePath = os.path.join(dataDirectoryPath, inputFileName)

            # Start with parsing the data file.
            if os.path.isfile(inputFilePath):
                massBalancePointReader = None
                massBalancePointWriter = None

            try:
                # Getting the reader object and start parsing.
                massBalancePointReader = MassBalancePointReader(config, inputFilePath, allGlaciers)

                # Important note:
                # The glacier object is still alive and could have mass-balance point objects of a
                # parsing process before. To have a redundancy free insert into the database,
                # possible mass-balance point readings have to be removed.
                massBalancePointReader.glacier.massBalancePoints.clear()

                # Start of parsing the given data file.
                massBalancePointReader.parse()

                # In case of a successful parsing process, a writer will be instantiated for immediate writing into the database.
                if massBalancePointReader != None:

                    print("\n" + str(inputFileName))
                    print("--- Start writing to the database. Will take a while ... take a break ... ---\n")

                    # Getting the writer object ready and start inserting into the database.
                    massBalancePointWriter = MassBalancePointWriter(privateDatabaseAccessConfiguration)
                    massBalancePointWriter.write(massBalancePointReader.glacier)

                else:
                    raise Exception("MassBalancePointReader is None")

            except GlacierNotFoundError as glacierNotFoundError:
                print(glacierNotFoundError.message)
            except InvalidDataFileError as invalidDataFileError:
                print(invalidDataFileError.message)

            finally:
                if massBalancePointReader != None:
                    massBalancePointReader = None
                    del (massBalancePointReader)
                if massBalancePointWriter != None:
                    massBalancePointWriter = None
                    del (massBalancePointWriter)
    else:
        raise Exception("Data directory not existing")


if __name__ == '__main__':
    # Getting all glacier read from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    allGlaciers = glacierReader.getAllGlaciers()

    insertDatabaseMassbalancePoint(allGlaciers)