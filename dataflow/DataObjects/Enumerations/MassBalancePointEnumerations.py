'''
Created on 22.03.2021

@author: elias
'''

from enum import Enum, unique

@unique
class DateAccuracyEnum(Enum):
    '''
    Enumeration defining the type of data accuracy.

    0 = NotDefinedUnknown
    1 = start and end dates exactly known
    2 = start date exactly known and end date estimated/unknown
    3 = start date estimated/unknown and end date exactly known
    '''
    NotDefinedUnknown = 0
    ExactlyKnown = 1
    StartKnownEndUnknown = 2
    StartUnknownEndKnown = 3

@unique
class DensityAccuracyEnum(Enum):
    '''
    Enumeration defining the type of density accuracy
    0 = Not defined or unknown
    1 = Ice density
    2 = Measured snow/firn/ice density
    3 = Density of snow/firn estimated from nearby measurements)
    4 = Density of snow/firn estimated without nearby measurements
    5 = Water equivalent based on combination of fresh snow density and ice density
    6 = Estimated based on linear regression with DOY and elevation in post-processing
        (24 + 0.038 * dayofyear + 0.009 * z-pos)
    '''
    NotDefinedUnknown = 0
    IceDensity = 1
    MeasuredDensity = 2
    EstimatedDensityFromMeasurementsNearby = 3
    EstimatedDensityWithoutMeasurement = 4
    WaterEquivalent = 5
    EstimatedLinearRegression = 6

@unique
class MeasurementQualityEnum(Enum):
    '''
    Enumeration defining the type of measurement quality

    0 = Not defined or unknown: no information available to assess the quality of the measurement point
    1 = Typical reading uncertainty of mass balance at a stake in the case of good conditions, assumed as about pm 5cm
    2 = High reading uncertainty in case of difficult conditions (e.g. stake is bent or broken, melt-in of the stake is
        suspected, etc.), assumed as bigger than about pm 15cm
    3 = No actual measurement was possible as the stake completely melted out, value inferred from indirect evidence
        (minimal melt, nearby stakes, etc.)
    4 = No actual measurement was possible as the stake was buried by snow, value inferred from indirect evidence
        (maximal melt, minimal accumulation, nearby stakes, etc.)
    5 = No actual measurement was possible for alternative reasons, value inferred from indirect evidence
    '''

    NotDefinedUnknown = 0
    TypicalReadingUncertainty = 1
    HighReadingUncertainty = 2
    ReconstructedValue_StakeCompletelyMeltedOut = 3
    ReconstructedValue_StakeBuriedBySnow = 4
    ReconstructedValue_OtherReason = 5

@unique
class MeasurementTypeEnum(Enum):
    '''
    Enumeration defining the type of measurement type

    0 = Not defined or unknown
    1 = observation at a mass balance stake
    2 = observation based on snow probing, a snow pit or a snow core
    3 = marked horizon (eg. snowpit, coring)
    4 = observation based on ground-penetrating radar
    5 = indirect mass balance observation based on the location of the snowline (b=0)
    6 = painted marks on rock face
    9 = other observation types
    '''
    NotDefinedUnknown = 0
    Stake = 1
    ProbingSnowpitCoring = 2
    MarkedHorizon = 3
    GroundPenetratingRadar = 4
    Snowline = 5
    Nivometer = 6
    Other = 9

@unique
class ObservationTypeEnum(Enum):
    '''
    Enumeration defining the type of observation type

    0 = Not defined or unknown
    1 = annual mass balance point observations
    2 = winter mass balance point observation (snow accumulation)
    3 = intermediate mass balance point observation (arbitrary time periods between principal annual surveys
    '''
    NotDefinedUnknown = 0
    Annual = 1
    Wintersnow = 2
    Intermediate = 3

@unique
class PositionAccuracyEnum(Enum):
    '''
    Enumeration defining the type of position accuracy

    0 = Not defined or unknown
    1 = measured by differential GPS, accuracy ~0.1m
    2 = measured by handheld GPS, accuracy ~3-5m
    3 = measured using an alternative method (e.g. theodolite, triangulation)
    4 = estimated from previous measurements
    5 = estimated based on altitude information
    '''
    NotDefinedUnknown = 0
    DifferentialGPS = 1
    HandheldGPS = 2
    AlternativeMethod = 3
    EstimatedFromPrevious = 4
    EstimatedFromAltitude = 5