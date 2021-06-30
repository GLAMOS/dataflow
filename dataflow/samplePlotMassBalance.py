'''
Created on 18.05.2018

@author: yvo
'''

from dataflow.DataWriters.FileWriters.Database.LengthChangeWriter import CopyLengthChangeData
from dataflow.DataWriters.DatabaseWriters.MassBalanceWriter import MassBalanceWriter
from dataflow.DataReaders.VawFileReaders.LengthChangeReader import LengthChangeReader
from dataflow.DataReaders.VawFileReaders.MassBalanceReader import MassBalanceReader
from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataObjects.MassBalance import MassBalanceObservation
from dataflow.DataObjects.MassBalance import MassBalanceFixDate
from dataflow.DataObjects.Enumerations.MassBalanceEnumerations import MassBalanceTypeEnum
from dataflow.DataObjects.Glacier import Glacier

import matplotlib.pyplot as plt

import configparser
import os
import sys

def plotMassBalance(glacier):
    '''
    Plotting of the mass-balance data available. Fix-date observations and field observations are plotted individually.
    
    @type glacier: DataObjects.Glacier
    @param glacier: Glacier object which mass-balance readings have to be plotted.
    '''
    
    print("Preparation of plotting {0} mass-balance readings of {1}".format(len(glacier.massBalances), glacier.name))
    
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

def parseMassBalance(configuration, glaciers):
    '''
    Parsing of mass balance data files.
    
    @type configuration: File handler
    @type configuration: File handler to main configuration file
    @type glaciers: Dictionary
    @param glaciers: Dictionary of glaciers stored in the database. Key: SGI-ID; Value: Glacier
    '''
    
    rootDirectoryPath = configuration.get("MassBalance", "rootDirectoryInput")
    dataDirectoryName = configuration.get("MassBalance", "glacierDirectoryInput")
    
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
                        
            else:
                print("Given input file '{0}' is not a file".format(inputFilePath))


if __name__ == '__main__':
    
    
    config = configparser.ConfigParser()
    config.read("dataflow.cfg")

    privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gladmin.cfg"
    
    if os.path.exists(privateDatabaseAccessConfiguration) == True:
        if os.path.isfile(privateDatabaseAccessConfiguration) == True:
            print("Private database configuration '{0}' will be used.".format(privateDatabaseAccessConfiguration)) 
        else:
            print("Private database configuration '{0}' isn't a file! Check file! Application will terminate.".format(privateDatabaseAccessConfiguration))
            sys.exit(1)
    else:
        print("Private database configuration '{0}' is not existing! Check path! Application will terminate.".format(privateDatabaseAccessConfiguration))
        sys.exit(1)
    
    focusGlaciers = ['A50i-19', 'B36-26', 'B56-03', 'B43-03']

    # Getting the dataflow.DataReaders.DatabaseReaders.GlacierReader ready to retrieve glacier objects from the database.
    glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
    # Empty directory for the found focus glaciers.
    glaciers = dict()
    
    try:
    
        # Check if the database is available. If not, get alternative glaciers for plotting.
        if glacierReader.isDatabaseAvailable == True:
            print("The GLAMOS database is available. Glacier objects are read from the database.")
            for focusGlacier in focusGlaciers:
                
                glacier = glacierReader.getGlacierBySgi(focusGlacier)
                glaciers[glacier.pkSgi] = glacier
        else:
            print("The GLAMOS database is not available. Glacier objects are improvised.")
            
            # Getting some improvised glaciers.
            clariden = Glacier(None, 141, "A50i-19", "Clariden")
            adler    = Glacier(None, 16,  "B56-03",  "Adler")
            rhone    = Glacier(None, 1,   "B43-03",  "Rhone")
            aletsch  = Glacier(None, 5,   "B36-26",  "Aletsch")
            glaciers[clariden.pkSgi] = clariden
            glaciers[adler.pkSgi]    = adler
            glaciers[rhone.pkSgi]    = rhone
            glaciers[aletsch.pkSgi]  = aletsch
        
        parseMassBalance(config, glaciers)
        
        for glacier in glaciers.values():
                   
            plotMassBalance(glacier)
    
    except Exception as e:
        
        print(e.message)
        print("Sample script aborted!")
