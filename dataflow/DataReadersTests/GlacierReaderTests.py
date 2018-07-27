'''
Created on 27.07.2018

@author: yvo
'''
import unittest


from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataReaders.Exceptions.InvalidCoordinatesError import InvalidCoordinatesError


class GlacierReaderTests(unittest.TestCase):

    _glacierReader = None

    def setUp(self):
        
        self._glacierReader = GlacierReader(r"../databaseAccessConfiguration.private.cfg")


    def tearDown(self):
        
        del(self._glacierReader)
        
    def testRegionRhone(self):
        '''
        Test the number of glaciers found in the region of the Rhone glacier.
        '''
        
        glaciers = self._glacierReader.getGlacierByBox(2669810, 1168280, 2676200, 1158890)
        self.assertEqual(30, len(glaciers), "Number of glaciers found with LV-95 coordinates for search-box")
        
        glaciers.clear()
        
        glaciers = self._glacierReader.getGlacierByBox(669810, 168284, 676209, 158889)
        self.assertEqual(30, len(glaciers), "Number of glaciers found with LV-03 coordinates for search-box")

        glaciers.clear()
        
        glaciers = self._glacierReader.getGlacierByBox(8.35137, 46.66048, 8.43572, 46.56852)
        self.assertEqual(30, len(glaciers), "Number of glaciers found with WGS-84 coordinates for search-box")
        
        glaciers.clear()
        
        glaciers = self._glacierReader.getGlacierByBox(450329.836, 5167606.577, 456881.376, 5158204.932)
        self.assertEqual(30, len(glaciers), "Number of glaciers found with UTM-32 coordinates for search-box")
        
    def testRegionSaentis(self):
        '''
        Test the number of glaciers found in the region of peak Saentis.
        '''
        
        glaciers = self._glacierReader.getGlacierByBox(2742807.270, 1235900.138, 2745478.492, 1233720.616)
        self.assertEqual(2, len(glaciers), "Number of glaciers found with LV-95 coordinates for search-box")
        
        glaciers.clear()
        
        glaciers = self._glacierReader.getGlacierByBox(742950.247, 236060.551, 745203.001, 233912.414)
        self.assertEqual(2, len(glaciers), "Number of glaciers found with LV-03 coordinates for search-box")

        glaciers.clear()
        
        glaciers = self._glacierReader.getGlacierByBox(9.33365, 47.25849, 9.35490, 47.23969)
        self.assertEqual(2, len(glaciers), "Number of glaciers found with WGS-84 coordinates for search-box")
        
        glaciers.clear()
        
        glaciers = self._glacierReader.getGlacierByBox(525303.564, 5233637.868, 526818.839, 5232256.770)
        self.assertEqual(2, len(glaciers), "Number of glaciers found with UTM-32 coordinates for search-box")
        
    def testRegionHoenggerberg(self):
        '''
        Test if no glaciers are found in the region of Hoenggerberg.
        '''

        try:
            self._glacierReader.getGlacierByBox(2678833.942, 1252969.282, 2680277.657, 1251309.359)
        
        #TODO: Implementation and raising of own database exception.
        except Exception as e:
            if type(e) is Exception:
                self.assertTrue(True, "Correct exception raised")
            else:
                self.assertTrue(False, "Wrong exception raised")


    def testEpsgCodes(self):
        '''
        Test if the correct EPSG code of points within Switzerland are returned.
        '''
        
        self.assertEqual(21780, GlacierReader.getEpsgCode(600000, 200000), "LV03")
        self.assertEqual(2056, GlacierReader.getEpsgCode(2600000, 1200000), "LV95")
        self.assertEqual(4326, GlacierReader.getEpsgCode(8.64870, 46.88999), "WGS-84")
        self.assertEqual(32632, GlacierReader.getEpsgCode(410968.286, 5163967.012), "UTM-32")


    def testInvalidCoordinates(self):
        '''
        Test if the correct error is raised in case of wrong coordinates.
        '''
        
        # FIXME: Testing a raised exception could be done more nicely with AssertRaises.
        
        # Inverted coordinates LV03.
        try:
            GlacierReader.getEpsgCode(200000, 600000)
        
        except Exception as e:
            if type(e) is InvalidCoordinatesError:
                self.assertTrue(True, "Correct exception raised")
            else:
                self.assertTrue(False, "Wrong exception raised")

        # Inverted coordinates LV95.
        try:
            GlacierReader.getEpsgCode(1200000, 2600000)
        
        except Exception as e:
            if type(e) is InvalidCoordinatesError:
                self.assertTrue(True, "Correct exception raised")
            else:
                self.assertTrue(False, "Wrong exception raised")
                
        # Inverted coordinates WGS-84.
        try:
            GlacierReader.getEpsgCode(46.88999, 8.64870)
        
        except Exception as e:
            if type(e) is InvalidCoordinatesError:
                self.assertTrue(True, "Correct exception raised")
            else:
                self.assertTrue(False, "Wrong exception raised")
                
        # Inverted coordinates UTM-32.
        try:
            GlacierReader.getEpsgCode(5163967.012, 410968.286)
        
        except Exception as e:
            if type(e) is InvalidCoordinatesError:
                self.assertTrue(True, "Correct exception raised")
            else:
                self.assertTrue(False, "Wrong exception raised")
                
        # Nonsense.
        try:
            GlacierReader.getEpsgCode(42.2, 1973.7)
        
        except Exception as e:
            if type(e) is InvalidCoordinatesError:
                self.assertTrue(True, "Correct exception raised")
            else:
                self.assertTrue(False, "Wrong exception raised")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()