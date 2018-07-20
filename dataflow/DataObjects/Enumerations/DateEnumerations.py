'''
Created on 04.06.2018

@author: yvo
'''

from enum import Enum, unique

@unique
class DateQualityTypeEnum(Enum):
    '''
    Enumeration defining the quality of dates.
    
    0  = Not defined / unknown
    1  = Precisely  known
    11 = Estimated such as September 1st
    '''
    
    NotDefinedUnknown = 0
    Precisely = 1
    Estimated = 11
