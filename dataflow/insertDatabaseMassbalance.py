'''
Created on 18.05.2018

@author: yvo

Main script to import all VAW mass-balance data files into the GLAMOS database.
'''

from dataflow.DataWriters.FileWriters.Database.LengthChangeWriter import CopyLengthChangeData
from dataflow.DataWriters.DatabaseWriters.MassBalanceWriter import MassBalanceWriter
from dataflow.DataReaders.VawFileReaders.LengthChangeReader import LengthChangeReader
from dataflow.DataReaders.VawFileReaders.MassBalanceReader import MassBalanceReader
from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError

import configparser
import os


config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.private.cfg"

def insertDatabaseMassbalance(allGlaciers):
    '''
    Parsing and writing all mass-balance data from VAW data-files into GLAMOS database.
    
    @type allGlaciers: Dictionary
    @param allGlaciers: Dictionary of all glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''
    
    rootDirectoryPath = config.get("MassBalance", "rootDirectoryInput")
    dataDirectoryName = config.get("MassBalance", "glacierDirectoryInput")
    
    dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)
    
    massBalanceReader = None
    
    # Getting the overall statics of the parsing and writing ready.
    # Quality assurance: Same amount of parsed data have to be written into the database.
    massBalanceObservationsParsedTotal  = 0
    elevationBandsParsedTotal           = 0
    elevationBandsValidParsedTotal      = 0
    elevationBandsInvalidParsedTotal    = 0
    
    massBalanceObservationsWrittenTotal    = 0
    elevationBandsHandledTotal             = 0
    elevationBandsValidWrittenTotal        = 0
    elevationBandsInvalidNotWrittenTotal   = 0
    
    if os.path.exists(dataDirectoryPath):

        # Loop over all mass-balance data files in the directory.
        for inputFileName in os.listdir(dataDirectoryPath):
            
            inputFilePath = os.path.join(dataDirectoryPath, inputFileName)
            
            # Start with parsing the data file.
            if os.path.isfile(inputFilePath):

                try:
                    # Getting the reader object and start parsing.
                    massBalanceReader = MassBalanceReader(config, inputFilePath, allGlaciers)
                    
                    # Important note:
                    # The glacier object is still alive and could have mass-balance objects of a 
                    # parsing process before. To have a redundancy free insert into the database,
                    # possible mass-balance readings have to be removed.
                    massBalanceReader.glacier.massBalances.clear()
                    
                    # Start of parsing the given data file.
                    massBalanceReader.parse()
                    
                    # Getting the statistics of the parsing for overall information and print to the user as control.
                    massBalanceObservationsParsedTotal += massBalanceReader.massBalanceObservationsParsed
                    elevationBandsParsedTotal          += massBalanceReader.elevationBandsParsed
                    elevationBandsValidParsedTotal     += massBalanceReader.elevationBandsValidParsed
                    elevationBandsInvalidParsedTotal   += massBalanceReader.elevationBandsInvalidParsed
                    print("-> {0}:\n\t- {1} Mass balance observations parsed\n\t- {2} Elevation bands parsed\n\t- {3} Valid elevation bands parsed\n\t- {4} Invalid elevation bands parsed".format(
                        massBalanceReader.fullFileName,
                        massBalanceReader.massBalanceObservationsParsed,
                        massBalanceReader.elevationBandsParsed,
                        massBalanceReader.elevationBandsValidParsed,
                        massBalanceReader.elevationBandsInvalidParsed))
                    
                    # In case of a successful parsing process, a writer will be instantiated for immediate writing into the database.
                    if massBalanceReader != None:
                        
                        print("\n--- Start writing to the database. Will take a while ... take a break ... ---\n")
        
                        # Getting the writer object ready and start inserting into the database.
                        massBalanceWriter = MassBalanceWriter(privateDatabaseAccessConfiguration)
                        massBalanceWriter.write(massBalanceReader.glacier)
        
                        # Getting the statistics of the inserting for overall information and print to the user as control (parsed informations == written informations)
                        massBalanceObservationsWrittenTotal  += massBalanceWriter.massBalanceObservationsWritten
                        elevationBandsValidWrittenTotal      += massBalanceWriter.elevationBandsValidWritten
                        elevationBandsInvalidNotWrittenTotal += massBalanceWriter.elevationBandsInvalidNotWritten
                        elevationBandsHandledTotal           += massBalanceWriter.elevationBandsHandled
                        print("-> {0}:\n\t- {1} Mass balance observations written\n\t- {2} Elevation bands handled\n\t- {3} Valid elevation bands written\n\t- {4} Invalid elevation bands not written".format(
                            massBalanceReader.fullFileName,
                            massBalanceWriter.massBalanceObservationsWritten,
                            massBalanceWriter.elevationBandsHandled,
                            massBalanceWriter.elevationBandsValidWritten,
                            massBalanceWriter.elevationBandsInvalidNotWritten))

                    else:
                        raise Exception("MassBalanceReader is None")
                    
                except GlacierNotFoundError as glacierNotFoundError:
                    print(glacierNotFoundError.message)
                    
                finally:
                    if massBalanceReader != None:
                        massBalanceReader = None
                        del(massBalanceReader)
                    if massBalanceWriter != None:
                        massBalanceWriter = None
                        del(massBalanceWriter)
        
    else:
        raise Exception("Data directory not existing")

    print("-------------- Summary parsing and writing --------------")
    print("-> Mass balance observations parsed vs. written: {0} vs. {1} (difference: {2})".format(
        massBalanceObservationsParsedTotal, massBalanceObservationsWrittenTotal,
        massBalanceObservationsParsedTotal - massBalanceObservationsWrittenTotal))
    print("-> Mass balance observations parsed vs. handled: {0} vs. {1} (difference: {2}".format(
        elevationBandsParsedTotal, elevationBandsHandledTotal,
        elevationBandsParsedTotal - elevationBandsHandledTotal))
    print("-> Valid elevation based parsed vs. written: {0} vs. {1} (difference: {2}".format(
        elevationBandsValidParsedTotal, elevationBandsValidWrittenTotal,
        elevationBandsValidParsedTotal - elevationBandsValidWrittenTotal))
    print("-> Invalid elevation based parsed vs. not written: {0} vs. {1} (difference: {2}".format(
        elevationBandsInvalidParsedTotal, elevationBandsInvalidNotWrittenTotal,
        elevationBandsInvalidParsedTotal - elevationBandsInvalidNotWrittenTotal))

if __name__ == '__main__':
    
    # Getting all glacier read from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    allGlaciers = glacierReader.getAllGlaciers()
    
    insertDatabaseMassbalance(allGlaciers)