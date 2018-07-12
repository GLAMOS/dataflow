'''
Created on 11.07.2018

@author: yvo
'''

from .VawFileReader import VawFileReader
import re
from src.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError
from src.DataObjects.VolumeChange import VolumeChange
from ..Exceptions.InvalidDataFileError import InvalidDataFileError

class VolumeChangeReader(VawFileReader):
    '''
    classdocs
    '''
    
    # Additional header definition.
    __NUMBER_HEADER_LINES        = 3

    # Definition of the columns in the mass balance ASCII files.
    __FILE_COLUMN_DATE               = 1
    __FILE_COLUMN_AREA               = 3
    __FILE_COLUMN_ELEVATION_MAXIMUM  = 5
    __FILE_COLUMN_ELEVATION_MINIMUM  = 6
    __FILE_COLUMN_VOLUME_CHANGE      = 7
    __FILE_COLUMN_HEIGHT_CHANGE_MEAN = 8
    
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

        # Check if the given file is a correct volume change file.
        searchResult = re.search(config.get("VolumeChange", "volumeChangePatternFilename"), fullFileName)
        if searchResult == None:
            message = "The file {0} is not a volume change data file.".format(fullFileName)
            raise InvalidDataFileError(message)
        # TODO: Additional test for file check to be included. If possible, implementation in a generic way in super-class VawFileReader.

        try:
            super().__init__(fullFileName, glaciers)
        except GlacierNotFoundError as glacierNotFoundError:
            raise glacierNotFoundError
        
    def __str__(self):
        
        pass

    def parse(self):
        
        with open(self._fullFileName, "r") as vc:
            
            lineCounter = 0
            self._numberDataLines = 0
            
            dataLines = []
            
            for line in vc:
                
                lineCounter += 1
                
                try:
                    
                    if lineCounter > self.__NUMBER_HEADER_LINES:
                        
                        data = self._getData(line)
                    
                        if len(data) > 0:
                            self._numberDataLines += 1
                            # Intermediate storage of the parsed data for the later instances of volume changes.
                            dataLines.append(data)
                    
                except Exception as e:

                    errorMessage = "{0} @ {1}: {2}".format(vc, lineCounter, e)
                    print(errorMessage)
                    
            # Getting the individual volume change readings ready.
            # An individual volume change reading consists of two data lines: i = reference, i + 1 = observation.
            referenceReadingIndex = 0
            changeReadingIndex    = 1
            
            for i in range(referenceReadingIndex, len(dataLines) - 1):
                
                referenceReadingData    = dataLines[referenceReadingIndex]
                volumeChangeReadingData = dataLines[changeReadingIndex]
                
                # Creating a new volume change object based on the reference and the observation data.
                volumeChange = VolumeChange(
                    None,
                    referenceReadingData[self.__FILE_COLUMN_DATE], volumeChangeReadingData[self.__FILE_COLUMN_DATE],
                    referenceReadingData[self.__FILE_COLUMN_AREA], volumeChangeReadingData[self.__FILE_COLUMN_AREA],
                    referenceReadingData[self.__FILE_COLUMN_ELEVATION_MAXIMUM], referenceReadingData[self.__FILE_COLUMN_ELEVATION_MINIMUM],
                    volumeChangeReadingData[self.__FILE_COLUMN_ELEVATION_MAXIMUM], volumeChangeReadingData[self.__FILE_COLUMN_ELEVATION_MINIMUM],
                    volumeChangeReadingData[self.__FILE_COLUMN_VOLUME_CHANGE],
                    volumeChangeReadingData[self.__FILE_COLUMN_HEIGHT_CHANGE_MEAN])
                
                self._glacier.addVolumeChange(volumeChange)
            
                referenceReadingIndex += 1
                changeReadingIndex    += 1

    def _getData(self, dataLine):
        # TODO: Description
        
        # Dictionary with the unique values per volume change data line.
        data = dict()
        
        p = re.compile(' +')
        
        dataLineParts = p.split(dataLine)
        
        # Getting the data columns into the dictionary.
        # Getting the date out of the data. Because every fucking file of VAW has it own format for date, an additional hack is needed (replace the - sign)
        referenceDate = self._reformateDateYyyyMmDd(dataLineParts[self.__FILE_COLUMN_DATE].strip().replace("-", ""))[0]
        data[self.__FILE_COLUMN_DATE]               = referenceDate
        data[self.__FILE_COLUMN_AREA]               = float(dataLineParts[self.__FILE_COLUMN_AREA].strip())
        data[self.__FILE_COLUMN_ELEVATION_MAXIMUM]  = float(dataLineParts[self.__FILE_COLUMN_ELEVATION_MAXIMUM].strip())
        data[self.__FILE_COLUMN_ELEVATION_MINIMUM]  = float(dataLineParts[self.__FILE_COLUMN_ELEVATION_MINIMUM].strip())
        data[self.__FILE_COLUMN_VOLUME_CHANGE]      = float(dataLineParts[self.__FILE_COLUMN_VOLUME_CHANGE].strip())
        data[self.__FILE_COLUMN_HEIGHT_CHANGE_MEAN] = float(dataLineParts[self.__FILE_COLUMN_HEIGHT_CHANGE_MEAN].strip())

        return data