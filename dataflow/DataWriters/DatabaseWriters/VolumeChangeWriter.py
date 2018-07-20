'''
Created on 11.07.2018

@author: yvo
'''

from .GlamosDatabaseWriter import GlamosDatabaseWriter
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
                
                statement = "INSERT INTO volume_change.volume_change (pk, fk_glacier, date_from, date_to, area_from, area_to, elevation_maximum_from, elevation_minimum_from, elevation_maximum_to, elevation_minimum_to, volume_change, height_change_mean) VALUES ('{0}', '{1}', '{2}', '{3}', {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11});".format(
                    volumeChange.pk,
                    glacier.pk,
                    volumeChange.dateFrom, volumeChange.dateTo,
                    volumeChange.areaFrom, volumeChange.areaTo,
                    volumeChange.elevationMaximumFrom, volumeChange.elevationMinimumFrom,
                    volumeChange.elevationMaximumTo, volumeChange.elevationMinimumTo,
                    volumeChange.volumeChange,
                    volumeChange.heightChangeMean)

                self._writeData(statement)
                self._connection.commit()
                
                self._volumeChangeObservationCounter += 1
        
        except Exception as exception:
            
            raise exception
        
        finally:
            
            self._connection.close()
