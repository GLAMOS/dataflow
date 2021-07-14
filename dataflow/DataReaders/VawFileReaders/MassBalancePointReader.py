'''
Created on 22.03.2021

@author: elias
'''

import re

from dataflow.DataReaders.VawFileReaders.VawFileReader import VawFileReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataObjects.Exceptions.MassBalanceError import ObservationTypeNotDefinedError
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
    __FILE_COLUMN_PERIOD = 5
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

    _massBalancePointType = ObservationTypeEnum.NotDefinedUnknown
    _massBalancePointCounter = 0

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
        isMassbalancePointFile = False
        searchResult = re.search(config.get("MassBalancePoint", "annualPatternFilename"), fullFileName)
        if searchResult != None:
            self._ObservationType = ObservationTypeEnum.Annual
            isMassbalancePointFile = True

        searchResult = re.search(config.get("MassBalancePoint", "wintersnowPatternFilename"), fullFileName)
        if searchResult != None:
            self._ObservationType = ObservationTypeEnum.Wintersnow
            isMassbalancePointFile = True

        searchResult = re.search(config.get("MassBalancePoint", "intermediatePatternFilename"), fullFileName)
        if searchResult != None:
            self._ObservationType = ObservationTypeEnum.Intermediate
            isMassbalancePointFile = True

        if searchResult == None and isMassbalancePointFile == False:
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
        with open(self._fullFileName, "r") as mbp:

            lineCounter = 0
            self._numberDataLines = 0

            dataLines = []
            if self._ObservationType == ObservationTypeEnum.Annual:
                observationType = 1
            elif self._ObservationType == ObservationTypeEnum.Wintersnow:
                observationType = 2
            elif self._ObservationType == ObservationTypeEnum.Intermediate:
                observationType = 3
            else:
                message = "Not defined point mass balance type of file {0}".format(self._fullFileName)
                raise ObservationTypeNotDefinedError(message)

            for line in mbp:

                lineCounter += 1

                try:

                    if lineCounter > self.__NUMBER_HEADER_LINES:
                        data = self._getData(line)

                        massBalancePoint = MassBalancePoint(
                            pk=None,
                            name=data[self.__FILE_COLUMN_NAME],
                            observationType=observationType,
                            dateFrom=data[self.__FILE_COLUMN_DATE_FROM], timeFrom=data[self.__FILE_COLUMN_TIME_FROM],
                            dateTo=data[self.__FILE_COLUMN_DATE_TO], timeTo=data[self.__FILE_COLUMN_TIME_TO],
                            period=data[self.__FILE_COLUMN_PERIOD],
                            dateAccuracy=data[self.__FILE_COLUMN_DATE_QUALITY],
                            latitude=data[self.__FILE_COLUMN_LATITUDE], longitude=data[self.__FILE_COLUMN_LONGITUDE], altitude=data[self.__FILE_COLUMN_ALTITUDE], positionAccuracy=data[self.__FILE_COLUMN_POSITION_ACCURACY],
                            massbalance_raw=data[self.__FILE_COLUMN_MASSBALANCE_RAW],
                            density=data[self.__FILE_COLUMN_DENSITY], densityAccuracy=data[self.__FILE_COLUMN_DENSITY_ACCURACY],
                            massbalance_we=data[self.__FILE_COLUMN_MASSBALANCE_WE], measurement_quality=data[self.__FILE_COLUMN_MASSBALANCE_QUALITY], measurement_type=data[self.__FILE_COLUMN_MASSBALANCE_TYPE],
                            massbalance_error=data[self.__FILE_COLUMN_MASSBALANCE_ERROR], reading_error=data[self.__FILE_COLUMN_READING_ERROR], density_error=data[self.__FILE_COLUMN_DENSITY_ERROR],
                            source=data[self.__FILE_COLUMN_SOURCE])

                        self._massBalancePointCounter += 1

                        self._glacier.addMassBalancePoint(massBalancePoint)


                except Exception as e:

                    errorMessage = "{0} @ {1}: {2}".format(mbp, lineCounter, e)
                    print(errorMessage)
                    raise


    def _getData(self, dataLine):

        # Dictionary with the unique values per point mass balance data line.
        data = dict()
        p = re.compile(' +')
        dataLineParts = p.split(dataLine)
        while len(dataLineParts[0]) == 0:
            dataLineParts = dataLineParts[1:]

        # Filling up of the parsed data to piped into an object.
        # ------------------------------------------------------
        if len(dataLineParts[self.__FILE_COLUMN_NAME].strip()) == 0:
            data[self.__FILE_COLUMN_NAME] = 'noname'
        else:
            data[self.__FILE_COLUMN_NAME] = dataLineParts[self.__FILE_COLUMN_NAME].strip()

        # FILE_COLUMN_DATE_FROM: if date_from in vaw-files not available write date_to (mainly within _winter.dat-files)
        if len(dataLineParts[self.__FILE_COLUMN_DATE_FROM].strip()) != 8:
            data[self.__FILE_COLUMN_DATE_FROM] = dataLineParts[self.__FILE_COLUMN_DATE_TO].strip()
        else:
            data[self.__FILE_COLUMN_DATE_FROM] = dataLineParts[self.__FILE_COLUMN_DATE_FROM].strip()

        data[self.__FILE_COLUMN_TIME_FROM] = self._reformatTime(dataLineParts[self.__FILE_COLUMN_TIME_FROM].strip())
        data[self.__FILE_COLUMN_DATE_TO] = dataLineParts[self.__FILE_COLUMN_DATE_TO].strip()
        data[self.__FILE_COLUMN_TIME_TO] = self._reformatTime(dataLineParts[self.__FILE_COLUMN_TIME_TO].strip())
        data[self.__FILE_COLUMN_PERIOD] = float(dataLineParts[self.__FILE_COLUMN_PERIOD].strip())

        # FILE_COLUMN_DATE_QUALITY: 9 was formerly used in vaw-files as unknown/undefined, in the DB undefined/unknown is 0
        data[self.__FILE_COLUMN_DATE_QUALITY] = int(self._notNine(dataLineParts[self.__FILE_COLUMN_DATE_QUALITY].strip()))

        data[self.__FILE_COLUMN_LATITUDE] = float(dataLineParts[self.__FILE_COLUMN_LATITUDE].strip())
        data[self.__FILE_COLUMN_LONGITUDE] = float(dataLineParts[self.__FILE_COLUMN_LONGITUDE].strip())
        data[self.__FILE_COLUMN_ALTITUDE] = float(dataLineParts[self.__FILE_COLUMN_ALTITUDE].strip())
        # FILE_COLUMN_DATE_QUALITY: 9 was formerly used in vaw-files as unknown/undefined, in the DB undefined/unknown is 0
        data[self.__FILE_COLUMN_POSITION_ACCURACY] = int(self._notNine(dataLineParts[self.__FILE_COLUMN_POSITION_ACCURACY].strip()))
        data[self.__FILE_COLUMN_MASSBALANCE_RAW] = int(dataLineParts[self.__FILE_COLUMN_MASSBALANCE_RAW].strip())
        data[self.__FILE_COLUMN_DENSITY] = int(dataLineParts[self.__FILE_COLUMN_DENSITY].strip())

        # FILE_COLUMN_DATE_QUALITY: 9 was formerly used in vaw-files as unknown/undefined, in the DB undefined/unknown is 0
        data[self.__FILE_COLUMN_DENSITY_ACCURACY] = int(self._notNine(dataLineParts[self.__FILE_COLUMN_DENSITY_ACCURACY].strip()))
        data[self.__FILE_COLUMN_MASSBALANCE_WE] = int(dataLineParts[self.__FILE_COLUMN_MASSBALANCE_WE].strip())
        data[self.__FILE_COLUMN_MASSBALANCE_QUALITY] = int(self._notNine(dataLineParts[self.__FILE_COLUMN_MASSBALANCE_QUALITY].strip()))

        # FILE_COLUMN_MASSBALANCE_TYPE: 9 was formerly used in vaw-files as unknown/undefined, in the DB undefined/unknown is 0
        data[self.__FILE_COLUMN_MASSBALANCE_TYPE] = int(self._notNine(dataLineParts[self.__FILE_COLUMN_MASSBALANCE_TYPE].strip()))
        data[self.__FILE_COLUMN_MASSBALANCE_ERROR] = int(dataLineParts[self.__FILE_COLUMN_MASSBALANCE_ERROR].strip())
        data[self.__FILE_COLUMN_READING_ERROR] = int(dataLineParts[self.__FILE_COLUMN_READING_ERROR].strip())
        data[self.__FILE_COLUMN_DENSITY_ERROR] = int(dataLineParts[self.__FILE_COLUMN_DENSITY_ERROR].strip())
        # TODO: FILE_COLUMN_SOURCE from abbreviations to full name conversion according to ReadMe.txt
        data[self.__FILE_COLUMN_SOURCE] = dataLineParts[self.__FILE_COLUMN_SOURCE].strip()

        return (data)


    def replace_source(self,source):
        # TODO: function not used yet
        source_replaced = []
        source_dict = {"NN": "unknown",
         "glrep": "Glaciological Reports",
         "firep": "Firnberichte",
         "vaw": "documents stored at VAW",
         "vawnf": "documents stored at VAW but could not be found",
         "kwm": "Kraftwerke Mattmark",
         "merc/plm": "Mercanton 1916, Vermessungen am Rhonegletscher",
         "pn": "Pro Natura",
         "uzh": "Universität Zürich",
         "unil": "Uni Lausanne",
         "PSI": "Paul Scherer Institute",
         "ab": "Andreas Bauder",
         "mh": "Matthias Huss",
         "mf": "Mauro Fischer",
         "mfu/fu": "Martin Funk",
         "al": "Andreas Linsbauer",
         "gka": "Giovanni Kappenberger",
         "ust": "Urs Steinegger",
         "mt": "Michael Thalmann",
         "pb": "Peter Beglinger",
         "ol": "Otto Langenegger",
         "mz": "Michael Zemp",
         "hm": "Horst Machguth",
         "ns": "Nadine Salzmann",
         "jo": "Hans Oerlemanns",
         "hz": "Harry Zekollari",
         "ph": "Philippe Huybrechts",
         "av": "Andreas Vieli",
         "bm": "Boris Mueller",
         "df": "Daniel Farinotti",
         "jl": "Johannes Landmann"}
        if source in source_dict:
            source_replaced.append(source)
        return (source_replaced)