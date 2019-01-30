'''
Created on 22.05.2018

@author: yvo
'''

from dataflow.DataWriters.DatabaseWriters.GlamosDatabaseWriter import GlamosDatabaseWriter
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataObjects.LengthChange import LengthChange


class LengthChangeWriter(GlamosDatabaseWriter):
    '''
    Database writer for objects of the type 
    
    Attributes:
    _lengthChangeObservationCounter int  Counter of length-change observations written to the database
    '''
    
    _lengthChangeObservationCounter = 0

    @property
    def lengthChangeObservationsWritten(self):
        # TODO: Description
        
        return self._lengthChangeObservationCounter

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)
    
    def write(self, glacier):
        '''
        Writes all length-change observations of the given glacier into the database.
        
        @type glacier: dataflow.DataObjects.Glacier.Glacier
        @param glacier: Glacier object with length-change data to be written into the database
        '''

        try:
            
            for lengthChange in glacier.lengthChanges.values():
                
                # TODO: Check if length change is already stored in the database.
                # statement = SELECT * FROM length_change.length_change_data WHERE fk_something = glacier.fk_something
                # if GlamosDatabaseWriter.isRecordStored(statement) == True:
                    # TODO: Insert length change if not in database. 
                    # writeData(insertStatement)
                # else:
                #     writeLoggerInformation
                
                checkStatement = "SELECT * FROM {0} WHERE fk_glacier = '{1}' AND date_from = '{2}' AND date_to = '{3}';".format(
                    'length_change.length_change_data',
                    glacier.pkVaw,
                    lengthChange.dateFrom,
                    lengthChange.dateTo)
        
                if super().isRecordStored(checkStatement) == True:
                    
                    message = "The record {0} is already stored in the database. No further inserts.".format(str(lengthChange))
                    print(message)
                
                else:
                    
                    message = "The record {0} is not yet stored in the database. Insert will be done ...".format(str(lengthChange))
                    print(message)
                    
                    # Preparing the INSERT of a not yet inserted record.
                    insertStatement = "INSERT INTO length_change.length_change_data (pk, fk_glacier, date_from, date_from_quality, date_to, date_to_quality, fk_measurement_type, variation_quantitative, variation_quantitative_accuracy, elevation_min, observer, remarks, fk_data_embargo_type) VALUES ('{0}', {1}, '{2}', {3}, '{4}', {5}, '{6}', {7}, {8}, {9}, {10}, {11}, {12});"
                
                    # Handling possible NULL values:
                    elevationMin = 'NULL'
                    if lengthChange.elevationMin != None:
                        elevationMin = lengthChange.elevationMin
                    observer = 'NULL'
                    if lengthChange.observer != None:
                        observer = '\'{0}\''.format(lengthChange.observer)
                    remarks = 'NULL'
                    if lengthChange.remarks != None:
                        remarks = '\'{0}\''.format(lengthChange.remarks)
                        
                    # Handling not yet implemented values.
                    variationQuantitativeAccuracy = 'NULL'
                    
                    # Handling not yet implemented default values.
                    dataEmbargoType = 0
    
                    # Getting the final INSERT-statement ready.
                    insertStatement = insertStatement.format(
                        lengthChange.pk,
                        glacier.pkVaw,
                        lengthChange.dateFrom,
                        lengthChange.dateFromQuality,
                        lengthChange.dateTo,
                        lengthChange.dateToQuality,
                        lengthChange.measurementType,
                        lengthChange.variationQuantitative,
                        variationQuantitativeAccuracy,
                        elevationMin,
                        observer,
                        remarks,
                        dataEmbargoType)
                    
                    self._writeData(insertStatement)
                    self._connection.commit()
                
                    self._lengthChangeObservationCounter += 1
            
        except Exception as exception:
            
            raise exception
        
        finally:
            
            self._connection.close()
            
            print("\n")
            print("-> A total of {0} length change observations were inserted into the database.".format(self._lengthChangeObservationCounter))
    
    def isGlacierLengthChangeStored(self):
        
        pass