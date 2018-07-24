'''
Created on 18.05.2018

@author: yvo
'''

from dataflow.DataWriters.FileWriters.FileWriter import FileWriter


class CopyLengthChangeData(FileWriter):
    '''
    classdocs
    '''

    _HEADER_LINE = "pk;fk_glacier;date_from;date_from_quality;date_to;date_to_quality;fk_measurement_type;variation_quantitative;variation_quantitative_accuracy;elevation_min;observer;remarks"
    
    _LINE_TEMPLATE = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11}"

    def __init__(self, glacier, fullFileName):
        '''
        Constructor
        '''
        
        super().__init__(glacier, fullFileName)
        
    def writeAllData(self):
        
        with open(self._fullFileName, "w") as outputFile:
            
            outputFile.write(self._HEADER_LINE + "\n")
            
            for value in self._glacier.lengthChanges.values():
                
                lineToWrite = self._LINE_TEMPLATE.format(
                    value.pk, self._glacier.pkVaw,
                    value.dateFrom, value.dateFromQuality,
                    value.dateTo, value.dateToQuality,
                    value.measurementType,
                    value.variationQuantitative, value.variationQuantitativeAccuracy,
                    value.elevationMin,
                    value.observer,
                    value.remarks)
                
                outputFile.write(lineToWrite + "\n")
        
class ImportLengthChangeData(FileWriter):
    '''
    classdocs
    '''


    def __init__(self, fullFileName):
        '''
        Constructor
        '''
        
        super().__init__(fullFileName)