'''
Created on 18.05.2018

@author: yvo
'''

import datetime
from ..FileDataReader import AsciiFileDateReader
from DataObjects.Glacier import Glacier

class VawFileReader(AsciiFileDateReader):
    '''
    classdocs
    '''
    
    def __init__(self, fullFileName):
        '''
        Constructor
        '''
        
        super().__init__(fullFileName)
        
        self.parseHeader()

    def parseHeader(self):
        
        with open(self._fullFileName, "r") as vaw:
            
            lineCounter = 0
            
            for line in vaw:
        
                lineCounter += 1
                
                try:
                        
                    if lineCounter == 1:
                            
                        metadata = self._getMetadata(line)
                        
                        self._glacier = Glacier(None, metadata[1], metadata[0])
                        
                        print(self._glacier)
                        
                except Exception as e:

                    errorMessage = "{0} @ {1}: {2}".format(vaw, lineCounter, e)
                    print(errorMessage)
        
        
    def _reformateDate(self, dateVaw):
    
        dateVawParts = dateVaw.split(".")
    
        day   = None
        month = None
        year  = None
    
        quality = None
    
        if dateVawParts[0] == "00" or dateVawParts[1] == "00":
            quality = 11
        else:
            quality = 1
    
        if dateVawParts[0] == "00":
            day = 1
        else:
            day = int(dateVawParts[0])
        if dateVawParts[1] == "00":
            month = 9
        else:
            month = int(dateVawParts[1])
    
        year = int(dateVawParts[2])
    
        return [datetime.date(year, month, day), quality]
    
    def _getMetadata(self, metadataLine):
    
        lineParts = metadataLine.split(";")
    
        pk_vaw = [lineParts[1].strip(), int(lineParts[2].strip())]
    
        return pk_vaw