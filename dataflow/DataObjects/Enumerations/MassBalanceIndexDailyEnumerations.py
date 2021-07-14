'''
Created on 22.03.2021

@author: elias
'''

from enum import Enum, unique

@unique
class SurfaceTypeEnum(Enum):
    '''
    Enumeration defining the value type of mass balance index.

    0 = NotDefinedUnknown
    1 = ice
    2 = firn
    3 = snow
    4 = fresh snow
    '''
    NotDefinedUnknown = 0
    Ice = 1
    Firn = 2
    Snow = 3
    FreshSnow = 4