'''
Created on 8.2.2024

@author: elias
'''

import re
import datetime

from dataflow.DataReaders.VawFileReaders.VawFileReader import VawFileReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from dataflow.DataObjects.MassBalanceIndexSpatialSeasonal import MassBalanceIndexSpatialSeasonal
from dataflow.DataReaders.Exceptions.InvalidDataFileError import InvalidDataFileError

class MassBalanceIndexSpatialSeasonalReader(VawFileReader):
    '''
    Reader-class for parsing the VAW-ASCII-based mass balance index spatial seasonal (_pointmb) data files.

    The header of the files follows the syntax:
    ---
    # Point mass balance ; aletsch ; 5
    # Fixed-dated annual balance:  1/10 - 30/ 9; fixed-date winter balance:  1/10 - 30/ 4
    # id;Stake;date0;date_fmeas;date_fmin;date_smeas;date_smax;date1; x; y; z; b_w_meas;b_a_meas;c_w_obs;a_w_obs;c_a_obs;a_a_obs;b_w_fix;b_a_fix;c_w_fix;a_w_fix;c_a_fix;a_a_fix
    # (-);(-);(yyyymmdd);(mmdd);(mmdd);(mmdd);(mmdd);(yyyymmdd); (m); (m); (m asl.); (mm w.e.);(mm w.e.);(mm w.e.);(mm w.e.);(mm w.e.);(mm w.e.);(mm w.e.);(mm w.e.);(mm w.e.);(mm w.e.);(mm w.e.);(mm w.e.)
    ...
     ---
    '''
    # Additional header definition. --> not needed


    # Number of header lines.
    __NUMBER_HEADER_LINES = 4

    # Definition of the columns in the point mass balance ASCII files (0-based index).
    __FILE_COLUMN_EVALUATION_METHOD = 0
    __FILE_COLUMN_STAKENAME = 1
    __FILE_COLUMN_DATE_0 = 2
    __FILE_COLUMN_DATE_FMEAS = 3
    __FILE_COLUMN_DATE_FMIN = 4
    __FILE_COLUMN_DATE_SMEAS = 5
    __FILE_COLUMN_DATE_SMAX = 6
    __FILE_COLUMN_DATE_1 = 7
    __FILE_COLUMN_LATITUDE = 8
    __FILE_COLUMN_LONGITUDE = 9
    __FILE_COLUMN_ALTITUDE = 10
    __FILE_COLUMN_B_W_MEAS = 11
    __FILE_COLUMN_B_A_MEAS = 12
    __FILE_COLUMN_C_W_OBS = 13
    __FILE_COLUMN_A_W_OBS = 14
    __FILE_COLUMN_C_A_OBS = 15
    __FILE_COLUMN_A_A_OBS = 16
    __FILE_COLUMN_B_W_FIX = 17
    __FILE_COLUMN_B_A_FIX = 18
    __FILE_COLUMN_C_W_FIX = 19
    __FILE_COLUMN_A_W_FIX = 20
    __FILE_COLUMN_C_A_FIX = 21
    __FILE_COLUMN_A_A_FIX = 22

    _massBalanceIndexSpatialSeasonalCounter = 0

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

        # Check if the given file is a correct index seasonal mass balance file.
        isMassBalanceIndexSpatialSeasonalFile = False
        searchResult = re.search(config.get("MassBalanceIndexSpatialSeasonal", "indexSpatialSeasonalPatternFilename"), fullFileName)
        if searchResult != None:
            isMassBalanceIndexSpatialSeasonalFile = True

        if searchResult == None and isMassBalanceIndexSpatialSeasonalFile == False:
            message = "The file {0} is not a index spatial seasonal mass balance data file.".format(fullFileName)
            raise InvalidDataFileError(message)
        # TODO: Additional test for file check to be included. If possible, implementation in a generic way in super-class VawFileReader.



    def __str__(self):
        pass

    def parse(self):
        with open(self._fullFileName, "r") as mbis:

            lineCounter = 0
            self._numberDataLines = 0

            dataLines = []

            for line in mbis:

                lineCounter += 1

                try:

                    if lineCounter > self.__NUMBER_HEADER_LINES:
                        data = self._getData(line)

                        massBalanceIndexSpatialSeasonal = MassBalanceIndexSpatialSeasonal(
                            name=data[self.__FILE_COLUMN_STAKENAME],
                            date_0=data[self.__FILE_COLUMN_DATE_0],
                            date_fmeas=data[self.__FILE_COLUMN_DATE_FMEAS],
                            date_fmin=data[self.__FILE_COLUMN_DATE_FMIN],
                            date_smeas=data[self.__FILE_COLUMN_DATE_SMEAS],
                            date_smax=data[self.__FILE_COLUMN_DATE_SMAX],
                            date_1=data[self.__FILE_COLUMN_DATE_1],
                            analysis_method_type=data[self.__FILE_COLUMN_EVALUATION_METHOD],
                            latitude=data[self.__FILE_COLUMN_LATITUDE],
                            longitude=data[self.__FILE_COLUMN_LONGITUDE],
                            altitude=data[self.__FILE_COLUMN_ALTITUDE],
                            b_w_meas=data[self.__FILE_COLUMN_B_W_MEAS],
                            b_a_meas=data[self.__FILE_COLUMN_B_A_MEAS],
                            c_w_obs=data[self.__FILE_COLUMN_C_W_OBS],
                            c_a_obs=data[self.__FILE_COLUMN_A_W_OBS],
                            a_w_obs=data[self.__FILE_COLUMN_C_A_OBS],
                            a_a_obs=data[self.__FILE_COLUMN_A_A_OBS],
                            b_w_fix=data[self.__FILE_COLUMN_B_W_FIX],
                            b_a_fix=data[self.__FILE_COLUMN_B_A_FIX],
                            c_w_fix=data[self.__FILE_COLUMN_C_W_FIX],
                            c_a_fix=data[self.__FILE_COLUMN_A_W_FIX],
                            a_w_fix=data[self.__FILE_COLUMN_C_A_FIX],
                            a_a_fix=data[self.__FILE_COLUMN_A_A_FIX],
                            reference=None)

                        self._massBalanceIndexSpatialSeasonalCounter += 1
                        self._glacier.addMassBalanceIndexSpatialSeasonal(massBalanceIndexSpatialSeasonal)

                except Exception as e:

                    errorMessage = "{0} @ {1}: {2}".format(mbis, lineCounter, e)
                    print(errorMessage)
                    raise

    def _getData(self, dataLine):

        # Dictionary with the unique values per point mass balance data line.
        data = dict()
        p = re.compile(' +')
        dataLineParts = p.split(dataLine)

        data[self.__FILE_COLUMN_EVALUATION_METHOD] = int(dataLineParts[self.__FILE_COLUMN_EVALUATION_METHOD].strip())
        data[self.__FILE_COLUMN_STAKENAME] = str(dataLineParts[self.__FILE_COLUMN_STAKENAME].strip())
        data[self.__FILE_COLUMN_DATE_0] = self._reformateDateYyyyMmDd(dataLineParts[self.__FILE_COLUMN_DATE_0].strip())[0]
        date_0_year = int(data[self.__FILE_COLUMN_DATE_0].year)
        data[self.__FILE_COLUMN_DATE_FMEAS] = self._reformateDateMmDd(dataLineParts[self.__FILE_COLUMN_DATE_FMEAS].strip(),date_0_year)[0]
        data[self.__FILE_COLUMN_DATE_FMIN] = self._reformateDateMmDd(dataLineParts[self.__FILE_COLUMN_DATE_FMIN].strip(),date_0_year)[0]

        data[self.__FILE_COLUMN_DATE_1] = self._reformateDateYyyyMmDd(dataLineParts[self.__FILE_COLUMN_DATE_1].strip())[0]
        date_1_year = int(data[self.__FILE_COLUMN_DATE_1].year)
        data[self.__FILE_COLUMN_DATE_SMEAS] = self._reformateDateMmDd(dataLineParts[self.__FILE_COLUMN_DATE_SMEAS].strip(),date_1_year)[0]
        data[self.__FILE_COLUMN_DATE_SMAX] = self._reformateDateMmDd(dataLineParts[self.__FILE_COLUMN_DATE_SMAX].strip(),date_1_year)[0]

        data[self.__FILE_COLUMN_LATITUDE] = float(dataLineParts[self.__FILE_COLUMN_LATITUDE].strip())
        data[self.__FILE_COLUMN_LONGITUDE] = float(dataLineParts[self.__FILE_COLUMN_LONGITUDE].strip())
        data[self.__FILE_COLUMN_ALTITUDE] = float(dataLineParts[self.__FILE_COLUMN_ALTITUDE].strip())
        data[self.__FILE_COLUMN_B_W_MEAS] = int(dataLineParts[self.__FILE_COLUMN_B_W_MEAS].strip())
        data[self.__FILE_COLUMN_B_A_MEAS] = int(dataLineParts[self.__FILE_COLUMN_B_A_MEAS].strip())
        data[self.__FILE_COLUMN_C_W_OBS] = int(dataLineParts[self.__FILE_COLUMN_C_W_OBS].strip())
        data[self.__FILE_COLUMN_A_W_OBS] = int(dataLineParts[self.__FILE_COLUMN_A_W_OBS].strip())
        data[self.__FILE_COLUMN_C_A_OBS] = int(dataLineParts[self.__FILE_COLUMN_C_A_OBS].strip())
        data[self.__FILE_COLUMN_A_A_OBS] = int(dataLineParts[self.__FILE_COLUMN_A_A_OBS].strip())
        data[self.__FILE_COLUMN_B_W_FIX] = int(dataLineParts[self.__FILE_COLUMN_B_W_FIX].strip())
        data[self.__FILE_COLUMN_B_A_FIX] = int(dataLineParts[self.__FILE_COLUMN_B_A_FIX].strip())
        data[self.__FILE_COLUMN_C_W_FIX] = int(dataLineParts[self.__FILE_COLUMN_C_W_FIX].strip())
        data[self.__FILE_COLUMN_A_W_FIX] = int(dataLineParts[self.__FILE_COLUMN_A_W_FIX].strip())
        data[self.__FILE_COLUMN_C_A_FIX] = int(dataLineParts[self.__FILE_COLUMN_C_A_FIX].strip())
        data[self.__FILE_COLUMN_A_A_FIX] = int(dataLineParts[self.__FILE_COLUMN_A_A_FIX].strip())

        return(data)