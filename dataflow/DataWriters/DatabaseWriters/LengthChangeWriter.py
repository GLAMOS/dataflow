'''
Created on 22.05.2018

@author: yvo
'''

from dataflow.DataWriters.DatabaseWriters.GlamosDatabaseWriter import GlamosDatabaseWriter
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataObjects.LengthChange import LengthChange
import uuid


class LengthChangeWriter(GlamosDatabaseWriter):
    '''
    classdocs
    '''


    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)
    
    def write(self, glacier):
        
        # TODO: Loop over all length changes
        
            # TODO: Check if length change is already stored in the database.
            # statement = SELECT * FROM length_change.length_change_data WHERE fk_something = glacier.fk_something
            # if GlamosDatabaseWriter.isRecordStored(statement) == True:
                # TODO: Insert length change if not in database. 
                # writeData(insertStatement)
            # else:
            #     writeLoggerInformation
            
            
        
        pass
    
    def isGlacierLengthChangeStored(self):
        
        pass