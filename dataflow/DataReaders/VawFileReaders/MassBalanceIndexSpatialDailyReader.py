'''
Created on 14.07.2021

@author: elias
'''

import re
import datetime

from dataflow.DataReaders.VawFileReaders.VawFileReader import VawFileReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataObjects.MassBalanceIndexSpatialDaily import MassBalanceIndexSpatialDaily
from dataflow.DataReaders.Exceptions.InvalidDataFileError import InvalidDataFileError

class MassBalanceIndexSpatialDailyReader(VawFileReader):
    '''
    Reader-class for parsing the VAW-ASCII-based mass balance index spaital daily (_cumulative) data files.

    The header of the files follows the syntax:
    ---
    # Point mass balance ; aletsch ; 5
    # Surface type code: 0: ice, 1: snow, 2: firn, 3: summer fresh snow
    # Stake ; Hyd.year ; year ; DOY ; Month ; Day ;  balance(b) ; accumulation(c) ; melt(a) ;  surface  ; T  ; Psolid
    # (-) ; (yyyy) ; (yyyy) ; (ddd) ; (mm) ; (dd) ;  (mm w.e.) ; (mm w.e.) ; (mm w.e.) ;  (-) ; (degC) ; (mm)
    ...
     ---
    '''
    # Additional header definition. -> no additional needed

    # Number of header lines.
    __NUMBER_HEADER_LINES = 4

    # Definition of the columns in the point mass balance ASCII files (0-based index).
    # __FILE_COLUMN_EMPTY = 0 -> first entry is a space
    __FILE_COLUMN_STAKENAME = 1
    __FILE_COLUMN_YEAR_HYD = 2
    __FILE_COLUMN_YEAR = 3
    __FILE_COLUMN_DOY = 4
    __FILE_COLUMN_MONTH = 5
    __FILE_COLUMN_DAY = 6
    __FILE_COLUMN_BALANCE = 7
    __FILE_COLUMN_ACCUMULATION = 8
    __FILE_COLUMN_MELT = 9
    __FILE_COLUMN_SURFACE_TYPE = 10
    __FILE_COLUMN_TEMP = 11
    __FILE_COLUMN_PRECIP = 12

    _massBalanceIndexSpatialDailyCounter = 0

    def __init__(self, config, fullFileName, glaciers):
        '''
        Constructor

        @type config: configparser.ConfigParser
        @param config: Configuration of the dataflow.
        @type fullFileName: string
        @param fullFileName: Absolute file path.
        @type glaciers: Dictionary
        @param glaciers: Dictionary with glaciers.


        @raise GlacierNotFoundError: Exception in case of not a corresponding glacier was found.
        @raise InvalidDataFileError: Exception in case of an invalid data file.
        '''


        # Setting up a new dictionary for the header lines.
        if self._headerLineContent == None:
            self._headerLineContent = dict()

        # Setting the parameters of the data file.
        self._numberHeaderLines = self.__NUMBER_HEADER_LINES

        try:
            super().__init__(fullFileName, glaciers)
        except GlacierNotFoundError as glacierNotFoundError:
            raise glacierNotFoundError

        # Setting the specialised reader parameters of the header. -> not needed


        # Check if the given file is a correct index spatial daily mass balance file.
        isMassBalanceIndexSpatialDailyFile = False
        searchResult = re.search(config.get("MassBalanceIndexSpatialDaily", "indexSpatialDailyPatternFilename"), fullFileName)
        if searchResult != None:
            isMassBalanceIndexSpatialDailyFile = True

        if searchResult == None and isMassBalanceIndexSpatialDailyFile == False:
            message = "The file {0} is not a index spatial daily mass balance data file.".format(fullFileName)
            raise InvalidDataFileError(message)
        # TODO: Additional test for file check to be included. If possible, implementation in a generic way in super-class VawFileReader.


    def __str__(self):
        pass

    def parse(self):
        with open(self._fullFileName, "r") as mbisd:

            lineCounter = 0
            self._numberDataLines = 0

            dataLines = []

            for line in mbisd:

                lineCounter += 1

                try:

                    if lineCounter > self.__NUMBER_HEADER_LINES:
                        data = self._getData(line)

                        massBalanceIndexSpatialDaily = MassBalanceIndexSpatialDaily(
                            name=data[self.__FILE_COLUMN_STAKENAME],
                            date=datetime.date(data[self.__FILE_COLUMN_YEAR], data[self.__FILE_COLUMN_MONTH], data[self.__FILE_COLUMN_DAY]),
                            balance=data[self.__FILE_COLUMN_BALANCE], accumulation=data[self.__FILE_COLUMN_ACCUMULATION], melt=data[self.__FILE_COLUMN_MELT],
                            surface_type=data[self.__FILE_COLUMN_SURFACE_TYPE], temp=data[self.__FILE_COLUMN_TEMP], precip_solid=data[self.__FILE_COLUMN_PRECIP],
                            reference=None)

                        self._massBalanceIndexSpatialDailyCounter += 1
                        self._glacier.addMassBalanceIndexSpatialDaily(massBalanceIndexSpatialDaily)

                except Exception as e:

                    errorMessage = "{0} @ {1}: {2}".format(mbisd, lineCounter, e)
                    print(errorMessage)
                    raise

    def _getData(self, dataLine):

        # Dictionary with the unique values per point mass balance data line.
        data = dict()
        p = re.compile(' +')
        dataLineParts = p.split(dataLine)

        data[self.__FILE_COLUMN_STAKENAME] = str(dataLineParts[self.__FILE_COLUMN_STAKENAME].strip())
        data[self.__FILE_COLUMN_YEAR_HYD] = int(dataLineParts[self.__FILE_COLUMN_YEAR_HYD].strip())
        data[self.__FILE_COLUMN_YEAR] = int(dataLineParts[self.__FILE_COLUMN_YEAR].strip())
        data[self.__FILE_COLUMN_DOY] = int(dataLineParts[self.__FILE_COLUMN_DOY].strip())
        data[self.__FILE_COLUMN_MONTH] = int(dataLineParts[self.__FILE_COLUMN_MONTH].strip())
        data[self.__FILE_COLUMN_DAY] = int(dataLineParts[self.__FILE_COLUMN_DAY].strip())
        data[self.__FILE_COLUMN_BALANCE] = int(dataLineParts[self.__FILE_COLUMN_BALANCE].strip())
        data[self.__FILE_COLUMN_ACCUMULATION] = int(dataLineParts[self.__FILE_COLUMN_ACCUMULATION].strip())
        data[self.__FILE_COLUMN_MELT] = int(dataLineParts[self.__FILE_COLUMN_MELT].strip())
        data[self.__FILE_COLUMN_SURFACE_TYPE] = int(dataLineParts[self.__FILE_COLUMN_SURFACE_TYPE].strip())
        data[self.__FILE_COLUMN_TEMP] = float(dataLineParts[self.__FILE_COLUMN_TEMP].strip())
        data[self.__FILE_COLUMN_PRECIP] = float(dataLineParts[self.__FILE_COLUMN_PRECIP].strip())

        return (data)