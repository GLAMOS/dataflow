'''
Created on 27.07.2018

@author: yvo
'''
import unittest

from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataReaders.Exceptions.InvalidCoordinatesError import InvalidCoordinatesError

from Helper import UnitTestHelper

class GlacierReaderTests(unittest.TestCase):

    _glacierReader = None
    
    _DATABASE_ACCESS_CONFIGURATION = UnitTestHelper.getDatabaseAccessConfigurationFilePath()

    def setUp(self):
        
        self._glacierReader = GlacierReader(self._DATABASE_ACCESS_CONFIGURATION)


    def tearDown(self):
        
        del(self._glacierReader)
        
        
    def testgetGlacierByPolygon(self):
        
        # Test with a closed Polygon with WGS-84 vertices.
        epsg     = 4326
        vertices = list()
        vertices.append((8.36169, 46.71357))
        vertices.append((8.37987, 46.69586))
        vertices.append((8.38904, 46.70529))
        vertices.append((8.40233, 46.71272))
        vertices.append((8.38594, 46.71752))
        vertices.append((8.36102, 46.71748))
        vertices.append((8.36169, 46.71357))
        
        glaciers   = self._glacierReader.getGlacierByPolygon(vertices, epsg)
        self.assertEqual(8, len(glaciers), "Number of glaciers found with closed WGS-84 polygon")
        
        # Removing the closing vertex.
        vertices = vertices[:-1]
        
        glaciers   = self._glacierReader.getGlacierByPolygon(vertices, epsg)
        self.assertEqual(8, len(glaciers), "Number of glaciers found with open WGS-84 polygon")

    def testgetGlacierByWktPolygon(self):
        '''
        Test the number of glaciers found in the given polygon.
        '''
        
        wktPolygon = 'POLYGON((8.36169 46.71357,8.37987 46.69586,8.38904 46.70529,8.40233 46.71272,8.38594 46.71752,8.36102 46.71748,8.36169 46.71357))'
        epsg       = 4326
        glaciers   = self._glacierReader.getGlacierByWktPolygon(wktPolygon, epsg)
        self.assertEqual(8, len(glaciers), "Number of glaciers found with WGS-84 WKT polygon")
        
        wktPolygon = 'POLYGON((2672449.449 1172359.534,2672683.411 1173131.610,2673756.296 1173910.371,2672446.106 1174465.196,2670574.407 1174421.746,2670734.838 1171998.564,2672449.449 1172359.534))'
        epsg       = 2056
        glaciers   = self._glacierReader.getGlacierByWktPolygon(wktPolygon, epsg)
        self.assertEqual(8, len(glaciers), "Number of glaciers found with LV-95 WKT polygon")

        wktPolygon = 'POLYGON((453169.778 5171932.435,453313.692 5172597.183,454362.211 5173556.611,452888.802 5174008.914,451117.285 5173954.089,451196.095 5171463.001,453169.778 5171932.435))'
        epsg       = 32632
        glaciers   = self._glacierReader.getGlacierByWktPolygon(wktPolygon, epsg)
        self.assertEqual(8, len(glaciers), "Number of glaciers found with UTM-32N WKT polygon")
        
        wktPolygon = 'POLYGON((672572.075 172455.025,672688.090 173137.052,673721.676 174276.10,672719.730 174560.870,670649.041 174529.229,670522.480 172954.240,671373.255 172012.060,672572.075 172455.025))'
        epsg       = 21781
        #glaciers   = self._glacierReader.getGlacierByWktPolygon(wktPolygon, epsg)
        #self.assertEqual(8, len(glaciers), "Number of glaciers found with LV-03 WKT polygon")
    
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