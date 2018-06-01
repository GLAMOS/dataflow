'''
Created on 31.05.2018

@author: yvo
'''

from .VawFileReader import VawFileReader
from DataObjects.MassBalance import MassBalance
from DataObjects.MassBalance import ElevationBand
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
    
        __FILE_COLUMN_METHOD                 # TODO: Description
        __FILE_COLUMN_DATE_FROM              # TODO: Description
        __FILE_COLUMN_DATE_TO                # TODO: Description
        __FILE_COLUMN_WINTER_BALANCE         # TODO: Description
        __FILE_COLUMN_ANNUAL_BALANCE         # TODO: Description
        
        __FILE_COLUMN_START_ELEVATION_BANDS  First column of the elevation band data.
        
        _NOT_A_NUMBER_STRING                 # TODO: Description
    '''

    __NUMBER_HEADER_LINES        = 4
    
    __NUMBER_ELEVATION_BUCKETS   = 4
    __START_ELEVATION_BUCKETS    = 5
    __END_ELEVATION_BUCKETS      = 6
    
    _numberElevationBuckets      = -1
    _startElevationBuckets       = -1
    _endElevationBuckets         = -1
    
    # Definition of the columns in the mass balance ascii files.
    __FILE_COLUMN_METHOD                    = 0
    __FILE_COLUMN_DATE_FROM                 = 1
    __FILE_COLUMN_DATE_TO                   = 4
    __FILE_COLUMN_WINTER_BALANCE            = 5
    __FILE_COLUMN_ANNUAL_BALANCE            = 6
    
    __FILE_COLUMN_MINIMUM_ELEVATION         = 10
    __FILE_COLUMN_MAXIMUM_ELEVATION         = 11
    __FILE_COLUMN_SURFACE                   = 9
    
    __FILE_COLUMN_EQUILIBRIUM_LINE_ALTITUDE = 7
    __FILE_COLUMN_ACCUMULATION_AREA_RATIO   = 8

    __FILE_COLUMN_START_ELEVATION_BANDS     = 12
    
    _NOT_A_NUMBER_STRING         = 'NaN'


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
                        
                        # Retrieving all the data of the mass balance data line (unique values and multiple values of the elevation bands).
                        data = self._getData(line)
                        
                        print(data)

                        # Creating the main object of a mass balance entry with the unique values.
                        massBalance = MassBalance(
                            None,
                            data[0][self.__FILE_COLUMN_METHOD],
                            data[0][self.__FILE_COLUMN_DATE_FROM][0],
                            data[0][self.__FILE_COLUMN_DATE_TO][0],
                            
                            data[0][self.__FILE_COLUMN_MINIMUM_ELEVATION],
                            data[0][self.__FILE_COLUMN_MAXIMUM_ELEVATION],
                            data[0][self.__FILE_COLUMN_SURFACE],

                            data[0][self.__FILE_COLUMN_EQUILIBRIUM_LINE_ALTITUDE],
                            data[0][self.__FILE_COLUMN_ACCUMULATION_AREA_RATIO],

                            data[0][self.__FILE_COLUMN_WINTER_BALANCE],
                            data[0][self.__FILE_COLUMN_ANNUAL_BALANCE])
                        
                        # Getting all elevation bands as own data objects and adding them to the mass balance.
                        for elevationBandData in data[1]:
                            
                            elevationBand = ElevationBand(
                                None,
                                elevationBandData[0],  elevationBandData[0] + self._equidistanceBuckets,
                                elevationBandData[1], elevationBandData[2],
                                elevationBandData[3])

                            massBalance.addElevationBand(elevationBand)
                        
                        # Adding the new mass balance to the collection of mass balances of the glacier.
                        self._glacier.addMassBalance(massBalance)
                        
                except Exception as e:

                    errorMessage = "{0} @ {1}: {2}".format(mb, lineCounter, e)
                    print(errorMessage)
                    
    
    def _getData(self, dataLine):
        # TODO: Description
        
        # Dictionary with the unique values per mass balance.
        data = dict()
        # List of data tripels of the mass balance elevation band data.
        dataElevationBands = list()
        
        p = re.compile(' +')
        
        dataLineParts = p.split(dataLine)
        
        data[self.__FILE_COLUMN_METHOD]                    = int(dataLineParts[self.__FILE_COLUMN_METHOD].strip())
        data[self.__FILE_COLUMN_DATE_FROM]                 = self._reformateDateYyyyMmDd(dataLineParts[self.__FILE_COLUMN_DATE_FROM].strip())
        data[self.__FILE_COLUMN_DATE_TO]                   = self._reformateDateYyyyMmDd(dataLineParts[self.__FILE_COLUMN_DATE_TO].strip())

        data[self.__FILE_COLUMN_EQUILIBRIUM_LINE_ALTITUDE] = int(dataLineParts[self.__FILE_COLUMN_EQUILIBRIUM_LINE_ALTITUDE].strip())
        data[self.__FILE_COLUMN_ACCUMULATION_AREA_RATIO]   = int(dataLineParts[self.__FILE_COLUMN_ACCUMULATION_AREA_RATIO].strip())
    
        data[self.__FILE_COLUMN_MINIMUM_ELEVATION]         = int(dataLineParts[self.__FILE_COLUMN_MINIMUM_ELEVATION].strip())
        data[self.__FILE_COLUMN_MAXIMUM_ELEVATION]         = int(dataLineParts[self.__FILE_COLUMN_MAXIMUM_ELEVATION].strip())
        data[self.__FILE_COLUMN_SURFACE]                   = float(dataLineParts[self.__FILE_COLUMN_SURFACE].strip())

        data[self.__FILE_COLUMN_WINTER_BALANCE]            = int(dataLineParts[self.__FILE_COLUMN_WINTER_BALANCE].strip())
        data[self.__FILE_COLUMN_ANNUAL_BALANCE]            = int(dataLineParts[self.__FILE_COLUMN_ANNUAL_BALANCE].strip())
        
        # Reading the elevation bands.
        
        for i in range(0, self._numberElevationBuckets):
            
            # Calculation of the current columns for the data tripel.
            columnWinterBalance = self.__FILE_COLUMN_START_ELEVATION_BANDS + i
            columnAnnualBalance = self.__FILE_COLUMN_START_ELEVATION_BANDS + i + self._numberElevationBuckets
            columnSurface       = self.__FILE_COLUMN_START_ELEVATION_BANDS + i + self._numberElevationBuckets * 2
            
            # Retrieving the data from the data line.
            winterBalanceString = dataLineParts[columnWinterBalance].strip()
            annualBalanceString = dataLineParts[columnAnnualBalance].strip()
            surfaceString       = dataLineParts[columnSurface].strip()
            
            # Preparing the possible None values for missing elevation bands.
            winterBalance = None
            annualBalance = None
            surface       = None
            
            if winterBalanceString != self._NOT_A_NUMBER_STRING:
                winterBalance = int(winterBalanceString)
            if annualBalanceString != self._NOT_A_NUMBER_STRING:
                annualBalance = int(annualBalanceString)
            if surfaceString != self._NOT_A_NUMBER_STRING:
                surface       = float(surfaceString)
            
            # Deriving the start altitude of the band.
            startElevationBucket = self._startElevationBuckets + self._equidistanceBuckets * i

            # Preparing the return value
            dataElevationBands.append([startElevationBucket, winterBalance, annualBalance, surface])
        
        return [data, dataElevationBands]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        