'''
Created on 12.07.2018

@author: yvo
'''

from dataflow.DataReaders.DatabaseReaders.GlamosDatabaseReader import GlamosDatabaseReader
from dataflow.DataObjects.VolumeChange import VolumeChange
from dataflow.DataObjects.Enumerations.HeightCaptureMethodEnumeration import HeightCaptureMethodEnum
from dataflow.DataObjects.Enumerations.VolumeChangeEnumerations import AnalysisMethodEnum


import uuid

class VolumeChangeReader(GlamosDatabaseReader):
    '''
    Reader object to retrieve volume change data stored in the GLAMOS PostGIS database.
    
    Attributes:
    _TABLE_VOLUME_CHANGE   str   Absolute name of the table or view to retrieve the volume-change data from (<schema>.<table | view>).
    '''

    _TABLE_VOLUME_CHANGE = "volume_change.vw_volume_change"

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)
        
        
    def getData(self, glacier):
        '''
        Retrieves all volume change measurement of the given glacier. As identification
        of the glacier, the uuid-based primary key of the glacier will be used.
        
        The measurements are stored in the volumeChange dictionary of the glacier instance.
        
        @type glacier: DataObject.Glacier.Glacier
        @param glacier: Glacier of which the time series of volume changes has to be retrieved.
        '''
        
        statement = "SELECT * FROM {0} WHERE fk_glacier = '{1}';".format(self._TABLE_VOLUME_CHANGE, glacier.pk)
        
        results = super().retriveData(statement)
        
        for result in results:
            
            glacier.addVolumeChange(self._recordToObject(result))
            
    def _recordToObject(self, dbRecord):
        '''
        Converts a single record of the database into a glacier object.
        
        @type dbRecord: list
        @param dbRecord: List with all values of one database record.
        
        @rtype: DataObjects.VolumeChange.VolumeChange
        @return: VolumeChange object of the database record.
        '''
        
        # Converting the PostgreSQL data types into Python data types.
        pk                      = uuid.UUID(dbRecord[0])
        dateFrom                = dbRecord[2]
        dateTo                  = dbRecord[3]
        areaFrom                = float(dbRecord[4])
        areaTo                  = float(dbRecord[5])
        heightCaptureMethodFrom = HeightCaptureMethodEnum(int(dbRecord[6]))
        heightCaptureMethodTo   = HeightCaptureMethodEnum(int(dbRecord[7]))
        analysisMethod          = AnalysisMethodEnum(int(dbRecord[8]))
        elevationMaximumFrom    = float(dbRecord[9])
        elevationMinimumFrom    = float(dbRecord[10])
        elevationMaximumTo      = float(dbRecord[11])
        elevationMinimumTo      = float(dbRecord[12])
        volumeChange            = float(dbRecord[13])
        heightChangeMean        = float(dbRecord[14])

        return VolumeChange(
            pk, 
            dateFrom, dateTo, 
            areaFrom, areaTo, 
            heightCaptureMethodFrom, heightCaptureMethodTo,
            analysisMethod,
            elevationMaximumFrom, elevationMinimumFrom, 
            elevationMaximumTo, elevationMinimumTo,
            volumeChange, 
            heightChangeMean)
    