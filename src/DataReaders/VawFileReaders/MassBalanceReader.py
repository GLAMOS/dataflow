'''
Created on 31.05.2018

@author: yvo
'''

from .VawFileReader import VawFileReader
from DataObjects.MassBalance import MassBalance
import re

class MassBalanceReader(VawFileReader):
    '''
    Specific file reader for mass balance files used by VAW.
    
    Example of typical header line:
    ---
    # Mass Balance; Allalin; 11; gl; 20; 2200; 4200;
    # id; date0; date_f; date_s; date1; Winter Balance; Annual Balance; ELA; AAR; Area; Minimum Elevation; Maximum Elevation; Elevation Bands
    # (#); (yyyymmdd); (mmdd); (mmdd); (yyyymmdd); (mm w.e.); (mm w.e.); (m asl.); (%); (km2); (m asl.); (m asl.); (mm w.e.); (mm w.e.); (km2)
    # © VAW / ETH Zürich; 2017; Huss et al. 2015, Journal of Glaciology; http://www.glamos.ch
    ---
    
    Attributes:
        - ___NUMBER_HEADER_LINES      Number of header lines used in the mass balance file.
        - __NUMBER_ELEVATION_BUCKETS  Position in the header line of number of elevation buckets
        - __START_ELEVATION_BUCKETS   Position in the header line of start elevation of elevation buckets
        - __END_ELEVATION_BUCKETS     Position in the header line of end elevation of elevation buckets
        - _numberElevationBuckets     Number of elevation buckets as defined in the header line
        - _startElevationBuckets      Start elevation of elevation buckets as defined in the header line
        - _endElevationBuckets        End elevation of elevation buckets as defined in the header line
    
        __FILE_COLUMN_METHOD          # TODO: Description
        __FILE_COLUMN_DATE_FROM       # TODO: Description
        __FILE_COLUMN_DATE_TO         # TODO: Description
        __FILE_COLUMN_WINTER_BALANCE  # TODO: Description
        __FILE_COLUMN_ANNUAL_BALANCE  # TODO: Description
        
        _NOT_A_NUMBER_STRING           # TODO: Description
    '''

    __NUMBER_HEADER_LINES        = 4
    
    __NUMBER_ELEVATION_BUCKETS   = 4
    __START_ELEVATION_BUCKETS    = 5
    __END_ELEVATION_BUCKETS      = 6
    
    _numberElevationBuckets      = -1
    _startElevationBuckets       = -1
    _endElevationBuckets         = -1
    
    __FILE_COLUMN_METHOD         = 0
    __FILE_COLUMN_DATE_FROM      = 1
    __FILE_COLUMN_DATE_TO        = 4
    __FILE_COLUMN_WINTER_BALANCE = 5
    __FILE_COLUMN_ANNUAL_BALANCE = 6
    
    _NOT_A_NUMBER_STRING         = "NaN"


    def __init__(self, fullFileName):
        '''
        Constructor of the class.
        
        @type fullFileName: string
        @param fullFileName: Absolute file path.
        '''
        
        # Setting the parameters of the data file.
        self._numberHeaderLines = self.__NUMBER_HEADER_LINES
        #self._headerLineContent[3] = "Method (currently not used)"
        self._headerLineContent[self.__NUMBER_ELEVATION_BUCKETS] = "Number of elevation buckets"
        self._headerLineContent[self.__START_ELEVATION_BUCKETS] = "Start elevation of elevation buckets"
        self._headerLineContent[self.__END_ELEVATION_BUCKETS] = "End elevation of elevation buckets"
        
        super().__init__(fullFileName)
        
        # Setting the specialised reader parameters of the header.
        self._numberElevationBuckets = int(self._headerLineContent[self.__NUMBER_ELEVATION_BUCKETS])
        self._startElevationBuckets  = int(self._headerLineContent[self.__START_ELEVATION_BUCKETS])
        self._endElevationBuckets    = int(self._headerLineContent[self.__END_ELEVATION_BUCKETS])
        
        self._equidistanceBuckets    = (self._endElevationBuckets - self._startElevationBuckets) / self._numberElevationBuckets
    
    def __str__(self):
        
        message = "{0}\n\t{1} ({2})\n\tmin = {3}, max = {4}, n = {5}, equidistance = {6}".format(
            self._fullFileName,
            self._glacier.name,
            self._glacier.pkVaw,
            self._startElevationBuckets,
            self._endElevationBuckets,
            self._numberElevationBuckets,
            self._equidistanceBuckets)

        return message
    
    def parse(self):
        # TODO: Description
        
        with open(self._fullFileName, "r") as mb:

            lineCounter = 0

            for line in mb:

                lineCounter += 1
                
                try:
                        
                    if lineCounter > self.__NUMBER_HEADER_LINES:
                        
                        data = self._getData(line)

                        massBalance = MassBalance(
                            None,
                            data[self.__FILE_COLUMN_DATE_FROM][0],
                            data[self.__FILE_COLUMN_DATE_TO][0],
                            data[self.__FILE_COLUMN_WINTER_BALANCE],
                            data[self.__FILE_COLUMN_ANNUAL_BALANCE])
                        
                        self._glacier.addMassBalance(massBalance)
                        
                        # TODO: Adding the elevation bands to the individual mass balance informations.
                        
                except Exception as e:

                    errorMessage = "{0} @ {1}: {2}".format(mb, lineCounter, e)
                    print(errorMessage)
                    
    
    def _getData(self, dataLine):
        # TODO: Description
        
        data = dict()
        
        p = re.compile(' +')
        
        dataLineParts = p.split(dataLine)
        
        data[self.__FILE_COLUMN_METHOD]         = int(dataLineParts[self.__FILE_COLUMN_METHOD])
        data[self.__FILE_COLUMN_DATE_FROM]      = self._reformateDateYyyyMmDd(dataLineParts[self.__FILE_COLUMN_DATE_FROM])
        data[self.__FILE_COLUMN_DATE_TO]        = self._reformateDateYyyyMmDd(dataLineParts[self.__FILE_COLUMN_DATE_TO])
        data[self.__FILE_COLUMN_WINTER_BALANCE] = int(dataLineParts[self.__FILE_COLUMN_WINTER_BALANCE])
        data[self.__FILE_COLUMN_ANNUAL_BALANCE] = int(dataLineParts[self.__FILE_COLUMN_ANNUAL_BALANCE])
        
        # TODO: Reading the elevation bands.
        
        return data
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        