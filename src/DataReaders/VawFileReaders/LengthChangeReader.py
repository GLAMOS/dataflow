'''
Created on 18.05.2018

@author: yvo
'''

from .VawFileReader import VawFileReader
from DataObjects.LengthChange import LengthChange

class LengthChangeReader(VawFileReader):
    '''
    classdocs
    '''

    def __init__(self, fullFileName):
        '''
        Constructor
        '''
        
        super().__init__(fullFileName)
        
    
    def parse(self):
        
        lengthChangeList = []
        
        with open(self._fullFileName, "r") as lc:

            lineCounter = 0

            for line in lc:

                lineCounter += 1
                
                try:
                        
                    if lineCounter >= 4:
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