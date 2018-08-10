'''
Created on 03.08.2018

@author: yvo
'''
import unittest
import datetime
import time

from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataReaders.DatabaseReaders.MassBalanceReader import MassBalanceReader
from dataflow.DataObjects.Glacier import Glacier

class MassBalanceDatabaseReaderTests(unittest.TestCase):
    '''
    Test class of the file-based data-reader dataflow.DataReaders.DatabaseReaders.MassBalanceReader.MassBalanceReader.
    
    Attributes:
    _DATABASE_ACCESS_CONFIGURATION    string                                                                     Relative path to the database-access configuration file.
    _glacierReader                    dataflow.DataReaders.DatabaseReaders.GlacierReader.GlacierReader           Dictionary with dataflow.DataObjects.Glacier.Glacier objects.
    _massBalanceReader                dataflow.DataReaders.DatabaseReaders.MassBalanceReader.MassBalanceReader   Main reader object to be tested.
    _clariden                         dataflow.DataObjects.Glacier.Glacier                                       Glacier object with mass-balances to be tested.
    '''
    
    _DATABASE_ACCESS_CONFIGURATION = r"../databaseAccessConfiguration.private.cfg"
    
    _glacierReader                 = None
    _massBalanceReader             = None

    _clariden                      = None

    @classmethod
    def setUpClass(self):
        
        # Getting the readers ready.
        self._glacierReader = GlacierReader(self._DATABASE_ACCESS_CONFIGURATION)
        self._massBalanceReader = MassBalanceReader(self._DATABASE_ACCESS_CONFIGURATION)
        
        # Getting the mother of all mass-balance glaciers ready.
        self._clariden = self._glacierReader.getGlacierBySgi("A50i/19")
        self._massBalanceReader.getData(self._clariden)

    @classmethod
    def tearDownClass(self):
        
        del(self._glacierReader)

    def setUp(self):
        
        pass
    
    def tearDown(self):
        
        pass
    
    def testNumberElevationBands(self):
        
        testDateFrom = datetime.date(1914, 9, 28)
        
        elevationBands = self._clariden.massBalances[testDateFrom].elevationBands
        
        self.assertEqual(12, len(elevationBands), "Number of elevation bands")
        
    def testElevationBand(self):
        
        testDateFrom = datetime.date(1914, 9, 28)
        
        elevationBand = self._clariden.massBalances[testDateFrom].elevationBands[2300]
        
        self.assertEqual(   2300, elevationBand.elevationFrom,     "Start altitude of the elevation band")
        self.assertEqual(   2400, elevationBand.elevationTo,       "End altitude of the elevation band")
        self.assertEqual(    100, elevationBand.equidistant,       "Distance between start and end altitude")
        self.assertEqual(    851, elevationBand.winterMassBalance, "Winter mass-balance of the elevation band")
        self.assertEqual(   -788, elevationBand.annualMassBalance, "annual mass-balance of the elevation band")
        self.assertEqual(0.10563, elevationBand.surface,           "Surface of the elevation band")
    
    def testMassBalanceReadingsTotal(self):
        
        self.assertEqual(206, len(self._clariden.massBalances), "Total number of mass-balance readings")

    def testTimeDataAcquisition(self):
        
        start = time.time()
        time.clock() 
    
        # Reading mass-balance data and elevation bands of an expensive glacier.
        self._massBalanceReader.getData(self._glacierReader.getGlacierBySgi("A50i/19"))
        
        elapsed = time.time() - start
        
        self.assertLess(elapsed, 4.0, "Time to retrieve all mass-balance data")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()