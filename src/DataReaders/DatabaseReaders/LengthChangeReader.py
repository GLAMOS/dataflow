'''
Created on 22.05.2018

@author: yvo
'''

from .GlamosDatabaseReader import GlamosDatabaseReader

from DataObjects.Glacier import Glacier
from DataObjects.LengthChange import LengthChange
from DataObjects.Enumerations.DateEnumerations import DateQualityTypeEnum

import uuid

class LengthChangeReader(GlamosDatabaseReader):
    '''
    Reader object to retrieve length change data stored in the GLAMOS PostGIS database.
    
    Attributes:
    _TABLE_LENGTH_CHANGE   str   Absolute name of the table or view to retrieve the length-change data from (<schema>.<table | view>).
    '''

    # FIXME: Better view to read the data from.
    _TABLE_VOLUME_CHANGE = "length_change.length_change_data"

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)

    def getData(self, glacier):
        '''
        Retrieves all length change measurement of the given glacier.
        
        The measurements are stored in the lengthChange dictionary of the glacier instance.
        
        @type glacier: DataObject.Glacier.Glacier
        @param glacier: Glacier of which the time series of length changes has to be retrieved.
        '''
        
        # FIXME: Working with glacier.pk instead of glacier.pkVaw. View has to be improved.        
        statement = "SELECT * FROM {0} WHERE fk_glacier = '{1}';".format(self._TABLE_VOLUME_CHANGE, glacier.pkVaw)
        
        results = super().retriveData(statement)
        
        if results != None:
            for result in results:
                glacier.addLengthChange(self._recordToObject(result))
            
    def _recordToObject(self, dbRecord):
        '''
        Converts a single record of the database into a length-change object.
        
        @type dbRecord: list
        @param dbRecord: List with all values of one database record.
        
        @rtype: DataObjects.LengthChange.LengthChange
        @return: LengthChange object of the database record.
        '''
       
        # Getting the individual attributes from the returned database record.
        # Mandatory attributes:
        pk                            = uuid.UUID(dbRecord[0])  # pk                       uuid           NOT NULL
        dateFrom                      = dbRecord[2]             # date_from                date           NOT NULL
        dateTo                        = dbRecord[4]             # date_to                  date           NOT NULL
        measurementType               = dbRecord[6]             # fk_measurement_type      varchar(1)     NOT NULL
        variationQuantitative         = float(dbRecord[7])      # variation_quantitative   decimal(10,2)  NOT NULL
        
        # Mandatory attributes and conversion from database integer-based lookup-values to enumeration.
        dateFromQuality               = DateQualityTypeEnum(
                                           int(dbRecord[3]))    # date_from_quality        smallint       NOT NULL
        dateToQuality                 = DateQualityTypeEnum(
                                           int(dbRecord[5]))    # date_to_quality          smallint       NOT NULL

        # Optional attributes:
        if dbRecord[8] != None:
            variationQuantitativeAccuracy = float(dbRecord[8])  # variation_quantitative_accuracy   decimal(10,2)
        else:
            variationQuantitativeAccuracy = None
        if dbRecord[9] != None:
            elevationMin                  = float(dbRecord[9])  # elevation_min            decimal(10,2)
        else:
            elevationMin = None
        if dbRecord[10] != None:
            observer                      = dbRecord[10]        # observer                 varchar(50)
        else:
            observer = None
        if dbRecord[11] != None:
            remarks                       = dbRecord[11]        # remarks                  text
        else:
            remarks = None


        # Returning the created data object.
        return LengthChange(
            pk, 
            dateFrom, dateFromQuality, 
            dateTo, dateToQuality, 
            measurementType, 
            variationQuantitative, variationQuantitativeAccuracy, 
            elevationMin, 
            observer, 
            remarks)

    