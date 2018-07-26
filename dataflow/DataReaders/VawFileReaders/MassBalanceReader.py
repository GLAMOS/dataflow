'''
Created on 31.05.2018

@author: yvo
'''

from dataflow.DataReaders.VawFileReaders import VawFileReader
from dataflow.DataObjects.MassBalance import MassBalance
from dataflow.DataObjects.MassBalance import MassBalanceObservation
from dataflow.DataObjects.MassBalance import MassBalanceFixDate
from dataflow.DataObjects.MassBalance import ElevationBand
from dataflow.DataObjects.MassBalance import MassBalanceTypeEnum
from dataflow.DataObjects.Exceptions.MassBalanceError import MassBalanceTypeNotDefinedError
from dataflow.DataObjects.Enumerations.DateEnumerations import DateQualityTypeEnum
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
import re
import copy

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
    
    # Definition of the columns in the mass balance ASCII files.
    __FILE_COLUMN_METHOD                    = 0
    __FILE_COLUMN_DATE_FROM                 = 1
    __FILE_COLUMN_DATE_TO                   = 4
    
    __FILE_COLUMN_DATE_MEASUREMENT_SPRING   = 3
    __FILE_COLUMN_DATE_MEASUREMENT_FALL     = 2
    
    __FILE_COLUMN_WINTER_BALANCE            = 5
    __FILE_COLUMN_ANNUAL_BALANCE            = 6
    
    __FILE_COLUMN_MINIMUM_ELEVATION         = 10
    __FILE_COLUMN_MAXIMUM_ELEVATION         = 11
    __FILE_COLUMN_SURFACE                   = 9
    
    __FILE_COLUMN_EQUILIBRIUM_LINE_ALTITUDE = 7
    __FILE_COLUMN_ACCUMULATION_AREA_RATIO   = 8

    __FILE_COLUMN_START_ELEVATION_BANDS     = 12
    
    _NOT_A_NUMBER_STRING                    = 'NaN'
    
    _massBalanceType                        = MassBalanceTypeEnum.NotDefinedUnknown

    _massBalanceObservationCounter = 0
    _elevationBandValidCounter     = 0
    _elevationBandInvalidCounter   = 0

    def __init__(self, config, fullFileName, glaciers):
        '''
        Constructor of the class.
        
        @type config: configparser.ConfigParser
        @param config: Configuration of the dataflow.
        @type fullFileName: string
        @param fullFileName: Absolute file path.
        @type glaciers: Dictionary
        @param glaciers: Dictionary with glaciers.
        
        @raise MassBalanceTypeNotDefinedError: Exception if mass balance type is not defined.
        @raise GlacierNotFoundError: Exception in case of not a corresponding glacier was found.
        '''
        
        # Setting the parameters of the data file.
        self._numberHeaderLines = self.__NUMBER_HEADER_LINES
        #self._headerLineContent[3] = "Method (currently not used)"
        self._headerLineContent[self.__NUMBER_ELEVATION_BUCKETS] = "Number of elevation buckets"
        self._headerLineContent[self.__START_ELEVATION_BUCKETS] = "Start elevation of elevation buckets"
        self._headerLineContent[self.__END_ELEVATION_BUCKETS] = "End elevation of elevation buckets"
        
        try:
            super().__init__(fullFileName, glaciers)
        except GlacierNotFoundError as glacierNotFoundError:
            raise glacierNotFoundError
        
        # Setting the specialised reader parameters of the header.
        self._numberElevationBuckets = int(self._headerLineContent[self.__NUMBER_ELEVATION_BUCKETS])
        self._startElevationBuckets  = int(self._headerLineContent[self.__START_ELEVATION_BUCKETS])
        self._endElevationBuckets    = int(self._headerLineContent[self.__END_ELEVATION_BUCKETS])
        
        self._equidistanceBuckets    = (self._endElevationBuckets - self._startElevationBuckets) / self._numberElevationBuckets
        
        # Definition of the based mass balance data type.
        searchResult = re.search(config.get("MassBalance", "fixDatePatternFilename"), self._fullFileName)
        if searchResult != None:
            self._massBalanceType = MassBalanceTypeEnum.FixDate
            
        searchResult = re.search(config.get("MassBalance", "observationPatternFilename"), self._fullFileName)
        if searchResult != None:
            self._massBalanceType = MassBalanceTypeEnum.Observation
            
        if self._massBalanceType == MassBalanceTypeEnum.NotDefinedUnknown:
            message = "Not defined mass balance type for file {0}".format(self._fullFileName)
            raise MassBalanceTypeNotDefinedError(message)
    
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
    
    @property
    def numberElevationBuckets(self):
        '''
        Number of elevation buckets with equal distance between start and end defined.
        '''
        
        return self._numberElevationBuckets
    
    @property
    def massBalanceObservationsParsed(self):
        '''
        Total number of parsed mass-balance observation lines.
        '''
        
        return self._massBalanceObservationCounter
    
    @property
    def elevationBandsValidParsed(self):
        # TODO: Description
        
        return self._elevationBandValidCounter
    
    @property
    def elevationBandsInvalidParsed(self):
        # TODO: Description
        
        return self._elevationBandInvalidCounter
    
    @property
    def elevationBandsParsed(self):
        '''
        Total number of parsed mass-balance elevation bands.
        '''
        
        return self._elevationBandInvalidCounter + self._elevationBandValidCounter

    def parse(self):
        '''
        Main function to start the parsing process. The function
        will run through the entire data file and creates for each data line
        a mass-balance observation and if available the individual elevation buckets.
        The mass-balance objects are added to the corresponding glacier object
        found in the dictionary given in the constructor.
        
        @raise MassBalanceTypeNotDefinedError: Exception if mass balance type is not defined.
        '''
    
        self._fullFileName
        
        massBalance = None

        with open(self._fullFileName, "r") as mb:

            lineCounter = 0
            self._numberDataLines = 0

            for line in mb:

                lineCounter += 1
                
                try:
                        
                    if lineCounter > self.__NUMBER_HEADER_LINES:
                        
                        # Retrieving all the data of the mass balance data line (unique values and multiple values of the elevation bands).
                        data = self._getData(line)
                        
                        # TODO: Including the self._numberDataLines counter.
                        
                        # Creating the main object of a mass balance entry with the unique values depending on the mass balance type.
                        if self._massBalanceType == MassBalanceTypeEnum.Observation:
                            
                            self._massBalanceObservationCounter += 1
                            
                            massBalance = MassBalanceObservation(
                                None,
                                data[0][self.__FILE_COLUMN_METHOD],
                                data[0][self.__FILE_COLUMN_DATE_FROM][0],
                                data[0][self.__FILE_COLUMN_DATE_TO][0],
                                
                                data[0][self.__FILE_COLUMN_DATE_MEASUREMENT_FALL][0],
                                data[0][self.__FILE_COLUMN_DATE_MEASUREMENT_SPRING][0],
                                
                                data[0][self.__FILE_COLUMN_MINIMUM_ELEVATION],
                                data[0][self.__FILE_COLUMN_MAXIMUM_ELEVATION],
                                data[0][self.__FILE_COLUMN_SURFACE],
    
                                data[0][self.__FILE_COLUMN_EQUILIBRIUM_LINE_ALTITUDE],
                                data[0][self.__FILE_COLUMN_ACCUMULATION_AREA_RATIO],
    
                                data[0][self.__FILE_COLUMN_WINTER_BALANCE],
                                data[0][self.__FILE_COLUMN_ANNUAL_BALANCE])
                        elif self._massBalanceType == MassBalanceTypeEnum.FixDate:
                            
                            yearFrom = data[0][self.__FILE_COLUMN_DATE_FROM][0].year
                            yearTo   = data[0][self.__FILE_COLUMN_DATE_TO][0].year
                            
                            self._massBalanceObservationCounter += 1
                            
                            massBalance = MassBalanceFixDate(
                                None,
                                data[0][self.__FILE_COLUMN_METHOD],
                                yearFrom,
                                yearTo,
                                 
                                data[0][self.__FILE_COLUMN_MINIMUM_ELEVATION],
                                data[0][self.__FILE_COLUMN_MAXIMUM_ELEVATION],
                                data[0][self.__FILE_COLUMN_SURFACE],
     
                                data[0][self.__FILE_COLUMN_EQUILIBRIUM_LINE_ALTITUDE],
                                data[0][self.__FILE_COLUMN_ACCUMULATION_AREA_RATIO],
     
                                data[0][self.__FILE_COLUMN_WINTER_BALANCE],
                                data[0][self.__FILE_COLUMN_ANNUAL_BALANCE])
                        else:
                            message = "Not defined mass balance type of file {0}".format(self._fullFileName)
                            raise MassBalanceTypeNotDefinedError(message)
                                             
                        # Getting all elevation bands as own data objects and adding them to the mass balance.
                        for elevationBandData in data[1]:
                            
                            elevationBand = ElevationBand(
                                None,
                                elevationBandData[0], elevationBandData[0] + self._equidistanceBuckets,
                                elevationBandData[1], elevationBandData[2],
                                elevationBandData[3])

                            massBalance.addElevationBand(elevationBand)
                            
                            # Counting the valid and invalid elevation bands.
                            if elevationBand.elevationFrom != None and elevationBand.elevationTo != None and elevationBand.annualMassBalance != None and elevationBand.winterMassBalance != None and elevationBand.surface:
                                self._elevationBandValidCounter += 1
                            else:
                                self._elevationBandInvalidCounter += 1
                        
                        # Setting the data source if available.
                        if self._dataSource != None:
                            massBalance.dataSource = self._dataSource
                        
                        # Adding the new mass balance to the collection of mass balances of the glacier.
                        self._glacier.addMassBalance(massBalance)

                except Exception as e:

                    errorMessage = "{0} @ {1}: {2}".format(mb, lineCounter, e)
                    print(errorMessage)
    
    def _getData(self, dataLine):
        # TODO: Description
        
        # Dictionary with the unique values per mass balance.
        data = dict()
        # List of data triples of the mass balance elevation band data.
        dataElevationBands = list()
        
        p = re.compile(' +')
        
        dataLineParts = p.split(dataLine)
        
        data[self.__FILE_COLUMN_METHOD]                    = int(dataLineParts[self.__FILE_COLUMN_METHOD].strip())  
        
        dateFrom                                           = self._reformateDateYyyyMmDd(dataLineParts[self.__FILE_COLUMN_DATE_FROM].strip())
        data[self.__FILE_COLUMN_DATE_FROM]                 = dateFrom
        dateTo                                             = self._reformateDateYyyyMmDd(dataLineParts[self.__FILE_COLUMN_DATE_TO].strip())
        data[self.__FILE_COLUMN_DATE_TO]                   = dateTo

        data[self.__FILE_COLUMN_DATE_MEASUREMENT_FALL]     = self._reformateDateMmDd(dataLineParts[self.__FILE_COLUMN_DATE_MEASUREMENT_FALL].strip(), dateFrom[0].year)
        data[self.__FILE_COLUMN_DATE_MEASUREMENT_SPRING]   = self._reformateDateMmDd(dataLineParts[self.__FILE_COLUMN_DATE_MEASUREMENT_SPRING].strip(), dateTo[0].year)

        data[self.__FILE_COLUMN_EQUILIBRIUM_LINE_ALTITUDE] = int(dataLineParts[self.__FILE_COLUMN_EQUILIBRIUM_LINE_ALTITUDE].strip())
        data[self.__FILE_COLUMN_ACCUMULATION_AREA_RATIO]   = int(dataLineParts[self.__FILE_COLUMN_ACCUMULATION_AREA_RATIO].strip())
    
        data[self.__FILE_COLUMN_MINIMUM_ELEVATION]         = int(dataLineParts[self.__FILE_COLUMN_MINIMUM_ELEVATION].strip())
        data[self.__FILE_COLUMN_MAXIMUM_ELEVATION]         = int(dataLineParts[self.__FILE_COLUMN_MAXIMUM_ELEVATION].strip())
        data[self.__FILE_COLUMN_SURFACE]                   = float(dataLineParts[self.__FILE_COLUMN_SURFACE].strip())

        data[self.__FILE_COLUMN_WINTER_BALANCE]            = int(dataLineParts[self.__FILE_COLUMN_WINTER_BALANCE].strip())
        data[self.__FILE_COLUMN_ANNUAL_BALANCE]            = int(dataLineParts[self.__FILE_COLUMN_ANNUAL_BALANCE].strip())
        
        # Reading the elevation bands.
        
        for i in range(0, self._numberElevationBuckets):
            
            # Calculation of the current columns for the data triple.
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        