'''
Created on 11.07.2018

@author: yvo
'''

from dataflow.DataWriters.DatabaseWriters.GlamosDatabaseWriter import GlamosDatabaseWriter
from dataflow.DataObjects.Enumerations.DataEnumerations import DataEmbargoTypeEnum
import logging

class VolumeChangeWriter(GlamosDatabaseWriter):
    '''
    # TODO: classdocs
    
    Attributes:
    _volumeChangeObservationCounter int  Counter of volume change observations written to the database
    '''

    _volumeChangeObservationCounter = 0


    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)
        
    @property
    def volumeChangeObservationCounter(self):
        '''
        Counter of volume change observations written to the database
        
        @rtype: int
        @return: Counter of volume change observations written to the database
        '''
        return self._volumeChangeObservationCounter
    
    def write(self, glacier):
        '''
        Writes all volume change observations of the given glacier into the database.
        
        @type glacier: DataObjects.Glacier.Glacier
        @param glacier: Glacier with volume change observations to be written into the database.
        '''
        
        try:
        
            for volumeChange in glacier.volumeChanges.values():
                
                # Check if volume change is already stored in the database.
                # The statement has to describe a SELECT which returns a unique record based on the definition of the record set.
                # In case the length-change data the following factors define a unique data record:
                # - The same glacier (fk_glacier)
                # - The same start date of the observation (date_from)
                # - The same end date of the observation (date_to) 
                checkStatement = "SELECT * FROM {0} WHERE fk_glacier = '{1}' AND date_from = '{2}' AND date_to = '{3}';".format(
                    'volume_change.volume_change',
                    glacier.pk,
                    volumeChange.dateFrom,
                    volumeChange.dateTo)
        
                # Record is already in database. No further inserts needed.
                if super().isRecordStored(checkStatement) == True:
                    
                    message = "The record {0} is already stored in the database. No further inserts.".format(str(volumeChange))
                    print(message)
                
                # Record is already in database. No further inserts needed.
                else:
                    
                    message = "The record {0} is not yet stored in the database. Insert will be done ...".format(str(volumeChange))
                    print(message)
                    
                    # Handling of not yet implemented values:
                    dataEmbargoType = DataEmbargoTypeEnum.Public
                               
                    statement = "INSERT INTO volume_change.volume_change (pk, fk_glacier, date_from, date_to, area_from, area_to, fk_height_capture_method_from, fk_height_capture_method_to, fk_analysis_method, elevation_maximum_from, elevation_minimum_from, elevation_maximum_to, elevation_minimum_to, volume_change, height_change_mean, fk_data_embargo_type, fk_date_from_quality, fk_date_to_quality) VALUES ('{0}', '{1}', '{2}', '{3}', {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17});".format(
                        volumeChange.pk,
                        glacier.pk,
                        volumeChange.dateFrom, volumeChange.dateTo,
                        volumeChange.areaFrom, volumeChange.areaTo,
                        volumeChange.heightCaptureMethodFrom.value, volumeChange.heightCaptureMethodTo.value,
                        volumeChange.analysisMethod.value,
                        volumeChange.elevationMaximumFrom, volumeChange.elevationMinimumFrom,
                        volumeChange.elevationMaximumTo, volumeChange.elevationMinimumTo,
                        volumeChange.volumeChange,
                        volumeChange.heightChangeMean,
                        dataEmbargoType.value,
                        volumeChange.dateFromQuality.value,
                        volumeChange.dateToQuality.value)
    
                    self._writeData(statement)
                    self._connection.commit()
                    
                    self._volumeChangeObservationCounter += 1
        
        except Exception as exception:
            
            raise exception
        
        finally:
            
            self._connection.close()

