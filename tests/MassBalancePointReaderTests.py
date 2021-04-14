'''
Created on 06.04.2021

@author: elias
'''
import unittest
import configparser

from dataflow.DataReaders.VawFileReaders.MassBalancePointReader import MassBalancePointReader
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataObjects.MassBalance import MassBalanceObservation
from dataflow.DataObjects.MassBalance import MassBalanceFixDate

from Helper import UnitTestHelper


class MassBalanceReaderTests(unittest.TestCase):
    '''
    Unit-test class for the VAW-file-based data-reader for mass-balance observations.
    '''

    _glaciers = dict()

    _vawDataFiles = []

    _configuration = configparser.ConfigParser()

    _DATAFLOW_CONFIGURATION = UnitTestHelper.getDataflowConfigurationFilePath()