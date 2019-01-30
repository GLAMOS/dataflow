from enum import Enum, unique

@unique
class DataEmbargoTypeEnum(Enum):
    '''
    Enumeration defining the quality of dates.
    
    0  = Not defined / unknown
    1  = Precisely  known
    11 = Estimated such as September 1st
    '''
    
    Public    = 0
    Protected = 11
    Private   = 21
