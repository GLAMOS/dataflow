'''
Created on 14.07.2021

@author: elias
'''

import re
import datetime

from dataflow.DataReaders.VawFileReaders.VawFileReader import VawFileReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataObjects.MassBalanceIndexDaily import MassBalanceIndexDaily
from dataflow.DataReaders.Exceptions.InvalidDataFileError import InvalidDataFileError

class MassBalanceIndexDailyReader(VawFileReader):
    '''
    Reader-class for parsing the VAW-ASCII-based mass balance index daily (_cum) data files.

    The header of the files follows the syntax:
    ---
    # Point mass balance ;  aletsch  ;  5 ; is ;   P0
    # Hyd.year ; year ; DOY ; Month ; Day ;  balance(b) ; accumulation(c) ; melt(a) ;  surface  ; T  ; Psolid
    # (yyyy) ; (yyyy) ; (ddd) ; (mm) ; (dd) ;  (mm w.e.) ; (mm w.e.) ; (mm w.e.) ;  (-) ; (degC) ; (mm)
    # VAW / ETHZ ; 2020.11.20 ; Huss and Bauder, 2008, Annals of Glaciology; www.glamos.ch
    ...
     ---
    '''
    # Additional header definition.
    __METHOD_TYPE = 3
    __STAKE_NAME = 4
    _methodType = -1
    _stakeName = -1

    # Number of header lines.
    __NUMBER_HEADER_LINES = 4

    # Definition of the columns in the point mass balance ASCII files (0-based index).
    __FILE_COLUMN_YEAR_HYD = 0
    __FILE_COLUMN_YEAR = 1
    __FILE_COLUMN_DOY = 2
    __FILE_COLUMN_MONTH = 3
    __FILE_COLUMN_DAY = 4
    __FILE_COLUMN_BALANCE = 5
    __FILE_COLUMN_ACCUMULATION = 6
    __FILE_COLUMN_MELT = 7
    __FILE_COLUMN_SURFACE_TYPE = 8
    __FILE_COLUMN_TEMP = 9
    __FILE_COLUMN_PRECIP = 10

    _massBalanceIndexDailyCounter = 0

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
        self._headerLineContent[self.__METHOD_TYPE] = "Method type"
        self._headerLineContent[self.__STAKE_NAME] = "Stake name"


        try:
            super().__init__(fullFileName, glaciers)
        except GlacierNotFoundError as glacierNotFoundError:
            raise glacierNotFoundError

        # Setting the specialised reader parameters of the header.

        self._methodType = str(self._headerLineContent[self.__METHOD_TYPE])
        self._stakeName = str(self._headerLineContent[self.__STAKE_NAME])

        # Check if the given file is a correct index daily mass balance file.
        isMassBalanceIndexDailyFile = False
        searchResult = re.search(config.get("MassBalanceIndexDaily", "indexDailyPatternFilename"), fullFileName)
        if searchResult != None:
            isMassBalanceIndexDailyFile = True

        if searchResult == None and isMassBalanceIndexDailyFile == False:
            message = "The file {0} is not a index daily mass balance data file.".format(fullFileName)
            raise InvalidDataFileError(message)
        # TODO: Additional test for file check to be included. If possible, implementation in a generic way in super-class VawFileReader.



    def __str__(self):
        pass

    def parse(self):
        with open(self._fullFileName, "r") as mbid:

            lineCounter = 0
            self._numberDataLines = 0

            dataLines = []

            for line in mbid:

                lineCounter += 1

                try:

                    if lineCounter > self.__NUMBER_HEADER_LINES:
                        data = self._getData(line)

                        massBalanceIndexDaily = MassBalanceIndexDaily(
                            name=self._stakeName,
                            date=datetime.date(data[self.__FILE_COLUMN_YEAR], data[self.__FILE_COLUMN_MONTH], data[self.__FILE_COLUMN_DAY]),
                            balance=data[self.__FILE_COLUMN_BALANCE], accumulation=data[self.__FILE_COLUMN_ACCUMULATION], melt=data[self.__FILE_COLUMN_MELT],
                            surface_type=data[self.__FILE_COLUMN_SURFACE_TYPE], temp=data[self.__FILE_COLUMN_TEMP], precip_solid=data[self.__FILE_COLUMN_PRECIP],
                            reference=self._dataSource)

                        self._massBalanceIndexDailyCounter += 1
                        self._glacier.addMassBalanceIndexDaily(massBalanceIndexDaily)

                except Exception as e:

                    errorMessage = "{0} @ {1}: {2}".format(mbid, lineCounter, e)
                    print(errorMessage)
                    raise

    def _getData(self, dataLine):

        # Dictionary with the unique values per point mass balance data line.
        data = dict()
        p = re.compile(' +')
        dataLineParts = p.split(dataLine)

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