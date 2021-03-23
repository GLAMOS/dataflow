'''
Created on 22.03.2021

@author: elias
'''

import re

from dataflow.DataReaders.VawFileReaders.VawFileReader import VawFileReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataObjects.MassBalancePoint import MassBalancePoint
from dataflow.DataReaders.Exceptions.InvalidDataFileError import InvalidDataFileError
from dataflow.DataObjects.Enumerations.MassBalancePointEnumerations import *

class MassBalancePointReader(VawFileReader):
    '''
    Reader-class for parsing the VAW-ASCII-based mass balance point data files.

    The header of the files follows the syntax:
    ---
    # Mass Balance;  Grosser Aletsch; No. 5; annual
    # name; date0; time0; date1; time1; period; date_quality; x_pos ; y_pos ; z_pos ; position_quality; mb_raw ; density ;  density_quality ; mb_we ; measurement_quality ; measurement_type ; mb_error ; reading_error ; density_error ; source
    # (-);  (yyyymmdd); (hhmm) ; (yyyymmdd); (hhmm) ; (d) ; (#) ; (m) ; (m) ; (m a.s.l.) ; (#) ; (cm) ; (kg m-3) ; (#) ; (mm w.e.) ; (#) ; (#) ; (mm w.e.) ; (mm w.e.) ; (mm w.e.) ; (-)
    # GLAMOS / VAW-ETHZ    ; production-date 20200112 ;   reference ; http://www.glamos.ch
    ...
     ---
    '''
    # Additional header definition.
    # Number of header lines.
    __NUMBER_HEADER_LINES = 4

    # Definition of the columns in the point mass balance ASCII files (0-based index).
    __FILE_COLUMN_NAME = 0
    __FILE_COLUMN_DATE_FROM = 1
    __FILE_COLUMN_TIME_FROM = 2
    __FILE_COLUMN_DATE_TO = 3
    __FILE_COLUMN_TIME_TO = 4
    __FILE_COLUMN_DATE_QUALITY = 6
    __FILE_COLUMN_LATITUDE = 7
    __FILE_COLUMN_LONGITUDE = 8
    __FILE_COLUMN_ALTITUDE = 9
    __FILE_COLUMN_POSITION_ACCURACY = 10
    __FILE_COLUMN_MASSBALANCE_RAW = 11
    __FILE_COLUMN_DENSITY = 12
    __FILE_COLUMN_DENSITY_ACCURACY = 13
    __FILE_COLUMN_MASSBALANCE_WE = 14
    __FILE_COLUMN_MASSBALANCE_QUALITY = 15
    __FILE_COLUMN_MASSBALANCE_TYPE = 16
    __FILE_COLUMN_MASSBALANCE_ERROR = 17
    __FILE_COLUMN_READING_ERROR = 18
    __FILE_COLUMN_DENSITY_ERROR = 19
    __FILE_COLUMN_SOURCE = 20

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

        # Setting the parameters of the data file.
        self._numberHeaderLines = self.__NUMBER_HEADER_LINES

        # Check if the given file is a correct point mass balance file.
        searchResult = re.search(config.get("MassbalancePoint", "annualPatternFilename"), self._fullFileName)
        if searchResult != None:
            self._ObservationType = ObservationTypeEnum.Annual

        searchResult = re.search(config.get("MassbalancePoint", "wintersnowPatternFilename"), self._fullFileName)
        if searchResult != None:
            self._ObservationType = ObservationTypeEnum.Wintersnow

        searchResult = re.search(config.get("MassbalancePoint", "intermediatePatternFilename"), self._fullFileName)
        if searchResult != None:
            self._ObservationType = ObservationTypeEnum.Intermediate

        if searchResult == None:
            message = "The file {0} is not a point mass balance data file.".format(fullFileName)
            raise InvalidDataFileError(message)
        # TODO: Additional test for file check to be included. If possible, implementation in a generic way in super-class VawFileReader.

        try:
            super().__init__(fullFileName, glaciers)
        except GlacierNotFoundError as glacierNotFoundError:
            raise glacierNotFoundError

    def __str__(self):

        pass

    def parse(self):
        # TODO: write parse method

    def _getData(self, dataLine):

        # Dictionary with the unique values per point mass balance data line.
        data = dict()
        # TODO: write getData method

        return (data)