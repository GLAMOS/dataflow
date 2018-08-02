'''
Created on 02.08.2018

@author: yvo
'''

from enum import Enum
from enum import unique

@unique
class AnalysisMethodEnum(Enum):
    '''
    Enumeration of the different methods for the volume change analysis.
     
    0 = Not defined or unknown
    1 = DSM difference with outlines
    2 = DSM difference without outlines
    '''
    
    NotDefinedUnknown = 0
    DsmDifferenceWithOutlines = 1 
    DsmDifferenceWithoutOutlines = 2