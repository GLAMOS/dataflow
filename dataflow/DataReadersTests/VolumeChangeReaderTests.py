
'''
Created on 11.07.2018

@author: yvo
'''
import unittest
import datetime
import configparser

from dataflow.DataReaders.VawFileReaders.VolumeChangeReader import VolumeChangeReader
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError


class VolumeChangeReaderTest(unittest.TestCase):
    '''
    Test class of the file-based data-reader dataflow.DataReaders.VawFileReaders.VolumeChangeReader.VolumeChangeReader.
    
    Attributes:
    _glaciers                 dict                          Dictionary with dataflow.DataObjects.Glacier.Glacier objects.
    _vawDataFiles             list                          List of VAW-ASCII files for testing the reader object.
    _DATAFLOW_CONFIGURATION   string                        Path to configuration file of the dataflow application.
    _config                   configparser.ConfigParser     Configuration parser for the dataflow application.
    '''

    _glaciers               = dict()
    
    _vawDataFiles           = []
    
    _DATAFLOW_CONFIGURATION = r"../dataflow.cfg"
    
    _config                 = None

    def setUp(self):
        '''
        Setup of the test environment with a list of parser objects.
        Purpose of having a list of parsers doing the job in the setUp function
        is to simulate similar tasks during database import jobs (first parsing
        all available data files and following insert into the database.
        '''

        # Getting the test glaciers.
        corbassiere = Glacier(None, 38, "B83/03", "Corbassière")
        findelen    = Glacier(None, 16, "B56/03", "Findelen")
        self._glaciers[corbassiere.pkSgi] = corbassiere
        self._glaciers[findelen.pkSgi]    = findelen
        
        # Setup of the input files.
        self._vawDataFiles.append("./VawDataFiles/corbassiere_glev.dat")
        self._vawDataFiles.append("./VawDataFiles/findelen_glev.dat")
        self._vawDataFiles.append("./VawDataFiles/gietro_glev.dat")
        self._vawDataFiles.append("./VawDataFiles/gorner_glev.dat")
        
        # Setup of the configuration parser for the application.
        self._config = configparser.ConfigParser()
        self._config.read(self._DATAFLOW_CONFIGURATION)
        
        # Setup of class-wide parser objects.
        self._volumeChangeParsers = []
        self._volumeChangeParsers.append(VolumeChangeReader(self._config, self._vawDataFiles[0], self._glaciers)) # Corbassière
        self._volumeChangeParsers.append(VolumeChangeReader(self._config, self._vawDataFiles[1], self._glaciers)) # Findelen
        # Running the parsing processes.
        for volumeChangeParser in self._volumeChangeParsers:
            volumeChangeParser.parse()

    def tearDown(self):
        pass


    def testName(self):
        
        self.assertTrue(True, "Hello World")
        
        
    def testHeaderInformation(self):
        '''
        Test if the corresponding glacier to the data file is found.
        '''
        
        volumeChangeReader = VolumeChangeReader(self._config, self._vawDataFiles[0], self._glaciers)
        
        self.assertTrue(volumeChangeReader.glacier.pkVaw == 38, "Corresponding glacier found")

        
    def testMissingGlacierException(self):
        '''
        Test if the correct exception is raised if not a corresponding glacier to the data file is found.
        '''

        try:
            VolumeChangeReader(self._config, self._vawDataFiles[3], self._glaciers)
        
        except Exception as e:
            if type(e) is GlacierNotFoundError:
                self.assertTrue(True, "Correct exception raised")
            else:
                self.assertTrue(False, "Wrong exception raised")
                
        # FIXME: Testing a raised exception could be done more nicely with AssertRaises
        
        
    def testCountDataLineCounter(self):
        '''
        Test if the correct number of data lines in the file was found.
        '''
        
        volumeChangeReader = VolumeChangeReader(self._config, self._vawDataFiles[0], self._glaciers)
        volumeChangeReader.parse()
        
        self.assertTrue(volumeChangeReader.numberDataLines == 6, "Correct number of data lines parsed")
        
    def testCountVolumeChanges(self):
        '''
        Test if the correct number of volume change data in the file was found.
        '''
        
        volumeChangeReader = VolumeChangeReader(self._config, self._vawDataFiles[0], self._glaciers)
        volumeChangeReader.parse()
        
        self.assertTrue(
            len(volumeChangeReader.glacier.volumeChanges) == volumeChangeReader.numberDataLines - 1, 
            "Correct number of volume changes parsed")
        
    def testFromToDates(self):
        '''
        Test if the from- and to-date of the volume changes are correctly parsed and set.
        '''
        
        volumeChangeReader = VolumeChangeReader(self._config, self._vawDataFiles[0], self._glaciers)
        volumeChangeReader.parse()
        
        # Setting the correct from-date. 
        # TODO: Getting it dynamically done with the test data files.
        
        fromDates = []
        fromDates.append(datetime.date(1934, 9,  1))
        fromDates.append(datetime.date(1983, 9,  7))
        fromDates.append(datetime.date(1998, 8, 31))
        fromDates.append(datetime.date(2003, 8,  2))
        fromDates.append(datetime.date(2008, 8, 29))
        fromDates.append(datetime.date(2013, 8, 21))
        
        for i in range(0, len(fromDates) - 1):
            
            dateFrom = fromDates[i]
            dateTo   = fromDates[i + 1]
 
            volumeChange = volumeChangeReader.glacier.volumeChanges[dateFrom]
            
            self.assertTrue(
                volumeChange.dateFrom == dateFrom and volumeChange.dateTo == dateTo,
                "From- and to-date")
        
    def testVolumeChangeAttributes(self):
        '''
        Test if the volume changes attributes are correctly parsed and set.
        '''
        # TODO: Getting the reading of reference data dynamically from the test data files.
        
        # Getting test volume change observations.
        volumeChangeReader = VolumeChangeReader(self._config, self._vawDataFiles[0], self._glaciers)
        volumeChangeReader.parse()
        
        # Choosing randomly an observation from the dictionary.
        dateFrom = datetime.date(2003, 8,  2)
        volumeChange = volumeChangeReader.glacier.volumeChanges[dateFrom]
        # Getting all attributes tested. Testing of exactly the values given in the text file (instead of using assertAlmostEquals for float).
        self.assertTrue(volumeChange.areaFrom == 18.514583, "Area from")
        self.assertTrue(volumeChange.areaTo == 18.202454, "Area to")
        self.assertTrue(volumeChange.elevationMaximumFrom == 4310.0, "Elevation maximum from")
        self.assertTrue(volumeChange.elevationMinimumFrom == 2204.4, "Elevation minimum from")
        self.assertTrue(volumeChange.elevationMaximumTo == 4312.6, "Elevation maximum to")
        self.assertTrue(volumeChange.elevationMinimumTo == 2234.9, "Elevation minimum to")
        self.assertTrue(volumeChange.volumeChange == -0.093029, "Volume change")
        self.assertTrue(volumeChange.heightChangeMean == -4.97, "Height change mean")
        
        # Choosing the first observation from the data file.
        dateFrom = datetime.date(1934, 9,  1)
        volumeChange = volumeChangeReader.glacier.volumeChanges[dateFrom]
        # Getting all attributes tested. Testing of exactly the values given in the text file (instead of using assertAlmostEquals for float).
        self.assertTrue(volumeChange.areaFrom == 19.388145, "Area from")
        self.assertTrue(volumeChange.areaTo == 19.498960, "Area to")
        self.assertTrue(volumeChange.elevationMaximumFrom == 4317.3, "Elevation maximum from")
        self.assertTrue(volumeChange.elevationMinimumFrom == 2005.4, "Elevation minimum from")
        self.assertTrue(volumeChange.elevationMaximumTo == 4312.1, "Elevation maximum to")
        self.assertTrue(volumeChange.elevationMinimumTo == 2180.7, "Elevation minimum to")
        self.assertTrue(volumeChange.volumeChange == -0.086011, "Volume change")
        self.assertTrue(volumeChange.heightChangeMean == -4.26, "Height change mean")
        
        # Choosing the last observation from the data file.
        dateFrom = datetime.date(2008, 8, 29)
        volumeChange = volumeChangeReader.glacier.volumeChanges[dateFrom]
        # Getting all attributes tested. Testing of exactly the values given in the text file (instead of using assertAlmostEquals for float).
        self.assertTrue(volumeChange.areaFrom == 18.202454, "Area from")
        self.assertTrue(volumeChange.areaTo == 17.517860, "Area to")
        self.assertTrue(volumeChange.elevationMaximumFrom == 4312.6, "Elevation maximum from")
        self.assertTrue(volumeChange.elevationMinimumFrom == 2234.9, "Elevation minimum from")
        self.assertTrue(volumeChange.elevationMaximumTo == 4319.5, "Elevation maximum to")
        self.assertTrue(volumeChange.elevationMinimumTo == 2309.0, "Elevation minimum to")
        self.assertTrue(volumeChange.volumeChange == -0.078336, "Volume change")
        self.assertTrue(volumeChange.heightChangeMean == -4.26, "Height change mean")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()