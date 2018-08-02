'''
Created on 02.08.2018

@author: yvo
'''

from enum import Enum
from enum import unique

@unique
class HeightCaptureMethodEnum(Enum):
    '''
    Enumeration of the different methods for height capturing.
     
     0 = Not defined or unknown
     1 = No height captured, only 2D data
     2 = GPS with elipsoid height correction
     3 = GPS without elipsoid height correction
     4 = Pixel maps 1:25000
     5 = Pixel maps 1:50000
     6 = Stereo digitising
     7 = DHM25
     8 = SwissAlti3D
     9 = Unknown
    10 = Miscellaneous digitised contour lines
    12 = Stereoplotter
    13 = Topographical maps 1:50000
    14 = Theodolite or Totalstation
    '''
    
    NotDefinedUnknown = 0
    NoHeightCaptured = 1
    GpsWithElipsoidHeightCorrection = 2
    GpsWithoutElipsoidHeightCorrection = 3
    PixelMaps25k = 4 
    PixelMaps50k = 5
    StereoDigitising = 6
    DHM25 = 7
    SwissAlti3D = 8
    Unknown = 9
    MiscellaneousDigitisedContourLines = 10
    Stereoplotter = 12
    TopographicalMaps50k = 13
    TheodoliteTotalstation = 14
    
