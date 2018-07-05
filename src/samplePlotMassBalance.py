'''
Created on 18.05.2018

@author: yvo
'''

from src.DataWriters.FileWriters.Database.LengthChangeWriter import CopyLengthChangeData
from src.DataWriters.DatabaseWriters.MassBalanceWriter import MassBalanceWriter
from src.DataReaders.VawFileReaders.LengthChangeReader import LengthChangeReader
from src.DataReaders.VawFileReaders.MassBalanceReader import MassBalanceReader
from src.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from src.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from src.DataObjects.MassBalance import MassBalanceObservation
from src.DataObjects.MassBalance import MassBalanceFixDate

import matplotlib.pyplot as plt

import configparser
import os
from src.DataObjects.Enumerations.MassBalanceEnumerations import MassBalanceTypeEnum


config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.private.cfg"

def plotMassBalance(glacier):
    
    massBalanceObservationsYearToObservations     = []
    massBalanceObservationsCumulativeObservations = []
    
    massBalanceObservationsYearToFixDate          = []
    massBalanceObservationsCumulativeFixDate      = []

    for massBalance in glacier.massBalances.values():
        
        if isinstance(massBalance, MassBalanceObservation):
        
            massBalanceObservationsYearToObservations.append(massBalance.dateToAnnual.year)
        
            if len(massBalanceObservationsCumulativeObservations) > 0:
                cumulativeAnnualMassBalance = massBalanceObservationsCumulativeObservations[-1] + massBalance.annualMassBalance
                massBalanceObservationsCumulativeObservations.append(cumulativeAnnualMassBalance)
            else:
                massBalanceObservationsCumulativeObservations.append(massBalance.annualMassBalance)
            
        elif isinstance(massBalance, MassBalanceFixDate):
            
            massBalanceObservationsYearToFixDate.append(massBalance.dateToAnnual.year)
        
            if len(massBalanceObservationsCumulativeFixDate) > 0:
                cumulativeAnnualMassBalance = massBalanceObservationsCumulativeFixDate[-1] + massBalance.annualMassBalance
                massBalanceObservationsCumulativeFixDate.append(cumulativeAnnualMassBalance)
            else:
                massBalanceObservationsCumulativeFixDate.append(massBalance.annualMassBalance)
        

    if len(massBalanceObservationsYearToObservations) > 2:
        plt.plot(massBalanceObservationsYearToObservations, massBalanceObservationsCumulativeObservations, 'ro')
        plt.axis(
            [min(massBalanceObservationsYearToObservations), max(massBalanceObservationsYearToObservations),
             min(massBalanceObservationsCumulativeObservations), max(massBalanceObservationsCumulativeObservations)])
        plt.title("Mass-balance observations of {0}".format(glacier.name))
        plt.show()
        plt.gcf().clear()
        
    if len(massBalanceObservationsYearToFixDate) > 2:
        plt.plot(massBalanceObservationsYearToFixDate, massBalanceObservationsCumulativeFixDate, 'ro')
        plt.axis(
            [min(massBalanceObservationsYearToFixDate), max(massBalanceObservationsYearToFixDate),
             min(massBalanceObservationsCumulativeFixDate), max(massBalanceObservationsCumulativeFixDate)])
        plt.title("Mass-balance fix-date of {0}".format(glacier.name))
        plt.show()
        plt.gcf().clear()

def parseMassBalance(glaciers):
    '''
    Simple plotting of mass balance data.
    
    @type glaciers: Dictionary
    @param glaciers: Dictionary of glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''
    
    rootDirectoryPath = config.get("MassBalance", "rootDirectoryInput")
    dataDirectoryName = config.get("MassBalance", "glacierDirectoryInput")
    
    dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)
       
    if os.path.exists(dataDirectoryPath):

        for inputFileName in os.listdir(dataDirectoryPath):
            
            massBalanceReader = None
            
            inputFilePath = os.path.join(dataDirectoryPath, inputFileName)
            
            # Start with parsing the data file. Looking if the file represents the g
            if os.path.isfile(inputFilePath):

                try:
                    # Getting the reader object and start parsing.
                    massBalanceReader = MassBalanceReader(config, inputFilePath, glaciers)
                    
                    # Start of parsing the given data file.
                    massBalanceReader.parse()

                    print("-> {0}:\n\t- {1} Mass balance observations parsed\n\t- {2} Elevation bands parsed\n\t- {3} Valid elevation bands parsed\n\t- {4} Invalid elevation bands parsed".format(
                        massBalanceReader.fullFileName,
                        massBalanceReader.massBalanceObservationsParsed,
                        massBalanceReader.elevationBandsParsed,
                        massBalanceReader.elevationBandsValidParsed,
                        massBalanceReader.elevationBandsInvalidParsed))
                    
                except GlacierNotFoundError as glacierNotFoundError:
                    print(glacierNotFoundError.message)
                    
                finally:
                    if massBalanceReader != None:
                        massBalanceReader = None
                        del(massBalanceReader)


if __name__ == '__main__':
    
    #focusGlaciers = ['A50i/19', 'B36 /26']
    focusGlaciers = ['A50i/19']
    
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    
    glaciers = dict()
    
    for focusGlacier in focusGlaciers:
        
        glacier = glacierReader.getGlacierBySgi(focusGlacier)
        glaciers[glacier.pkSgi] = glacier
    
    parseMassBalance(glaciers)
    
    for glacier in glaciers.values():
        
        print(glacier.name)
        print(len(glacier.massBalances))
        
        plotMassBalance(glacier)
    