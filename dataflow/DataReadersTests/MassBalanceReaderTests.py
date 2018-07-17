'''
Created on 06.07.2018

@author: yvo
'''
import unittest
import configparser

from DataReaders.VawFileReaders.MassBalanceReader import MassBalanceReader
from DataObjects.Glacier import Glacier
from DataObjects.MassBalance import MassBalanceObservation
from DataObjects.MassBalance import MassBalanceFixDate

class MassBalanceReaderTests(unittest.TestCase):
    '''
    Unit-test class for the VAW-file-based data-reader for mass-balance observations.
    '''

    _glaciers      = dict()
    
    _vawDataFiles  = []
    
    _configuration = configparser.ConfigParser()

    def setUp(self):
        '''
        Setup of the test environment with a list of parser objects.
        Purpose of having a list of parsers doing the job in the setUp function
        is to simulate similar tasks during database import jobs (first parsing
        all available data files and following insert into the database.
        '''

        # Getting the test glaciers.
        clariden = Glacier(None, 141, "A50i/19", "Clariden")
        adler    = Glacier(None, 16,  "B56/03",  "Adler")
        self._glaciers[clariden.pkSgi] = clariden
        self._glaciers[adler.pkSgi]    = adler
        
        # Reading the configuration file.
        self._configuration.read("../dataflow.cfg")
        
        # Setup of the input files.
        self._vawDataFiles.append("./VawDataFiles/adler_fix.dat")
        self._vawDataFiles.append("./VawDataFiles/adler_obs.dat")
        self._vawDataFiles.append("./VawDataFiles/clariden_fix.dat")
        self._vawDataFiles.append("./VawDataFiles/clariden_obs.dat")
        
        # Setup of class-wide parser objects.
        self._massBalanceParsers = []
        self._massBalanceParsers.append(MassBalanceReader(self._configuration, self._vawDataFiles[3], self._glaciers)) # Clariden observations
        self._massBalanceParsers.append(MassBalanceReader(self._configuration, self._vawDataFiles[0], self._glaciers)) # Adler fix date readings
        # Running the parsing processes.
        for massBalanceParser in self._massBalanceParsers:
            massBalanceParser.parse()

    def tearDown(self):
        
        for massBalanceParser in self._massBalanceParsers:
            del(massBalanceParser)


    def testBasicParsingObservations(self):
        '''
        Test method for the basic parsing attributes of mass-balance observations.
        '''

        self.assertTrue(self._massBalanceParsers[0].massBalanceObservationsParsed == 103, "Number of parsed mass-balance observations")
        self.assertTrue(self._massBalanceParsers[0].numberElevationBuckets == 12,         "Number of elevation bands")
        self.assertTrue(
            self._massBalanceParsers[0].massBalanceObservationsParsed * self._massBalanceParsers[0].numberElevationBuckets == 1236,         
                                                                                          "Number of parsed mass-balance elevation bands")
        for massbalance in self._massBalanceParsers[0].glacier.massBalances.values():
            self.assertTrue(isinstance(massbalance, MassBalanceObservation),              "Test of mass-balance type")
            
    def testBasicParsingFixDate(self):
        '''
        Test method for the basic parsing attributes of mass-balance fix-date readings.
        '''
               
        self.assertTrue(self._massBalanceParsers[1].massBalanceObservationsParsed == 12, "Number of parsed mass-balance observations")
        self.assertTrue(self._massBalanceParsers[1].numberElevationBuckets == 13,        "Number of elevation bands")
        self.assertTrue(
            self._massBalanceParsers[1].massBalanceObservationsParsed * self._massBalanceParsers[1].numberElevationBuckets == 156,         
                                                                                         "Number of parsed mass-balance elevation bands")
        for massbalance in self._massBalanceParsers[1].glacier.massBalances.values():
            self.assertTrue(isinstance(massbalance, MassBalanceFixDate),                 "Test of mass-balance type")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()