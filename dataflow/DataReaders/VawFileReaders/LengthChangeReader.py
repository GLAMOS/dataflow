'''
Created on 18.05.2018

@author: yvo
'''

from .VawFileReader import VawFileReader
from DataObjects.LengthChange import LengthChange

class LengthChangeReader(VawFileReader):
    '''
    Specific file reader for length change measurement files used by Andreas Bauder.
    
    Example of typical header line:
    ---
    #  Length Change; Allalin; 11; 6.50
    #  surv.date; m-code; ref.date; lc; clc; h_min; observer
    #  dt:ddmmyyyy; ; dt:ddmmyyyy; (m); (m); (m asl);
    ---
    
    Attributes:
        - ___NUMBER_HEADER_LINES    Number of header lines used in the length change file.
    '''

    ___NUMBER_HEADER_LINES = 3

    def __init__(self, fullFileName):
        '''
        Constructor of the class.
        
        @type fullFileName: string
        @param fullFileName: Absolute file path.
        '''
        
        super().__init__(fullFileName)
        
        # Setting the parameters of the data file.
        self._numberHeaderLines = self.___NUMBER_HEADER_LINES
        #self._headerLineContent[3] = "Length change (can be ignored)"
    
    def parse(self):
        '''
        Starts the parsing of the given file. The parser runs through the entire file
        and collects the individual length change measurements.
        Each line of a length change measurement will be converted into a 
        DataObjects.LengthChange.LengthChange object.
        
        Only measurements which are measured, reconstructed or observed are included.
        
        The individual measurements are included into a list containing the entire 
        time series of the length change measurement of the glacier as given in the file.
        
        @rtype: List of DataObjects.LengthChange.LengthChange objects
        @return: Entire time series of the length changes of the glacier.
        '''
        
        lengthChangeList = []
        
        with open(self._fullFileName, "r") as lc:

            lineCounter = 0

            for line in lc:

                lineCounter += 1
                
                try:
                        
                    if lineCounter > self._NUMBER_HEADER_LINES:
                        data = self._getData(line)

                        if data[4] == "m" or data[4] == "r" or data[4] == "o":

                            lengthChange = LengthChange(None, 
                                         data[0], data[1], 
                                         data[2], data[3],
                                         data[4], 
                                         data[5], "",
                                         data[6], 
                                         data[7],
                                         "")
                            
                            lengthChangeList.append(lengthChange)
                            
                            self._glacier.addLengthChange(lengthChange)
                   
                        
                except Exception as e:

                    errorMessage = "{0} @ {1}: {2}".format(lc, lineCounter, e)
                    print(errorMessage)
                    
        return lengthChangeList
        
    def _getData(self, dataLine):
        '''
        Helper function to retrieve all information of a single length change measurement line.
        
        Each parameter stored in the text file will be parsed and converted into an appropriate type.
        
        @type dataLine: string
        @param dataLine: Entire line with a measurement of the text file.
        
        @rtype: Array
        @return: Converted data of one length change measurement.
        '''
    
        dateToReformated   = self._reformateDate(dataLine[:10])
        dateFromReformated = self._reformateDate(dataLine[16:26])
        dateTo             = dateToReformated[0]
        dateToQuality      = dateToReformated[1]
        dateFrom           = dateFromReformated[0]
        dateFromQuality    = dateFromReformated[1]
    
        measurementType = dataLine[12:13]
    
        variationQuantitative = float(dataLine[26:37].strip())
    
        elevationMin     = ""
        elevationMinTemp = dataLine[42:54].strip()
        if elevationMinTemp != "NaN":
            try:
                elevationMin = float(elevationMinTemp)
            except:
                elevationMin = ""
    
        observer = ""
        observerTemp = dataLine[54:].strip()
        if observerTemp != "-":
            observer = observerTemp
    
        return [dateFrom, dateFromQuality, dateTo, dateToQuality, measurementType, variationQuantitative, elevationMin, observer]