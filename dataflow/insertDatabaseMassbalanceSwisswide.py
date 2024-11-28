'''
Created on 1.2.2024

@author: elias

Main script to import all VAW mass-balance swiss wide files into the GLAMOS database.
'''

from dataflow.DataWriters.DatabaseWriters.MassBalanceSwissWideWriter import MassBalanceSwissWideWriter
from dataflow.DataReaders.VawFileReaders.MassBalanceSwissWideReader import MassBalanceSwissWideReader
from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError

import configparser
import os

config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gldirw.cfg"


def insertDatabaseMassbalanceSwissWide(allGlaciers):
    '''
    Parsing and writing all mass-balance data from VAW data-files into GLAMOS database.

    @type allGlaciers: Dictionary
    @param allGlaciers: Dictionary of all glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''

    rootDirectoryPath = config.get("MassBalanceSwissWide", "rootDirectoryInput")
    dataDirectoryName = config.get("MassBalanceSwissWide", "directoryInput")

    dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)

    massBalanceSwissWideReader = None
    massBalanceSwissWideWriter = None

    if os.path.exists(dataDirectoryPath):
        # Get  all mass-balance swiss wide data files in the directory.
        inputFilePathList = []
        for inputFileName in os.listdir(dataDirectoryPath):
            inputFilePath = os.path.join(dataDirectoryPath, inputFileName)
            inputFilePathList.append(inputFilePath)
        print(inputFilePathList)

        # Get the first file of the list, because handing over a list of file paths to the reader does not work
        inputFilePath = inputFilePathList[0]

        try:
            massBalanceSwissWideReader = MassBalanceSwissWideReader(config, inputFilePathList, allGlaciers)

            # Important note:
            # The glacier object is still alive and could have mass-balance objects of a
            # parsing process before. To have a redundancy free insert into the database,
            # possible mass-balance readings have to be removed.
            # MassBalanceReaderSwissWide.glacier.massBalancesSwissWide.clear()

            # Start of parsing the given data file.
            parsedMassBalanceSwissWideList = massBalanceSwissWideReader.parse()
            print(len(parsedMassBalanceSwissWideList), 'are ready to be compared with entries in the Database')

            counter = 0
            print("\n--- Start writing to the database. Will take a while ... take a break ... ---\n")

            for parsedMassBalanceSwissWideObject in parsedMassBalanceSwissWideList:

                # Getting the writer object ready and start inserting into the database.
                massBalanceSwissWideWriter = MassBalanceSwissWideWriter(privateDatabaseAccessConfiguration)
                massBalanceSwissWideWriter.write(parsedMassBalanceSwissWideObject)
                counter +=1
                #print(counter, 'have been checked')



        except GlacierNotFoundError as glacierNotFoundError:
            print(glacierNotFoundError.message)

        finally:
            if massBalanceSwissWideReader != None:
                massBalanceSwissWideReader = None
                del (massBalanceSwissWideReader)
            if massBalanceSwissWideWriter != None:
                massBalanceSwissWideWriter = None
                del (massBalanceSwissWideWriter)
            else:
                raise Exception("Data directory not existing")

    print("-------------- Summary parsing and writing --------------")



if __name__ == '__main__':
    # Getting all glacier read from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    allGlaciers = glacierReader.getAllGlaciers()

    insertDatabaseMassbalanceSwissWide(allGlaciers)