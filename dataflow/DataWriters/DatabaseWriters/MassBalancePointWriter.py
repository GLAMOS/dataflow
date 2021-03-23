'''
Created on 22.03.2021

@author: elias
'''

from dataflow.DataWriters.DatabaseWriters.GlamosDatabaseWriter import GlamosDatabaseWriter
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataObjects.MassBalancePoint import MassBalancePoint


class MassBalancePointWriter(GlamosDatabaseWriter):
    '''
    Database writer for objects of the type point mass balance

    Attributes:
    _MassBalancePointObservationCounter int  Counter of length-change observations written to the database
    '''

    _MassBalancePointObservationCounter = 0

    @property
    def MassBalancePointObservationsWritten(self):
        # TODO: Description

        return self._MassBalancePointObservationCounter

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor

        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''

        super().__init__(accessConfigurationFullFileName)

    def isGlacierLengthChangeStored(self):
        pass