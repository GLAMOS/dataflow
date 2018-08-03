'''
Created on 22.05.2018

@author: yvo
'''

from dataflow.DataReaders.DatabaseReaders.GlamosDatabaseReader import GlamosDatabaseReader
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataReaders.Exceptions.InvalidCoordinatesError import InvalidCoordinatesError
from dataflow.DataReaders.Exceptions.InvalidGeometryError import InvalidGeometryError

import uuid

class GlacierReader(GlamosDatabaseReader):
    '''
    Reader object to retrieve glacier related data stored in the GLAMOS PostGIS database.
    '''
    
    _TABLE_GLACIER      = "base_data.vw_glacier"
    _TABLE_GLACIER_EPSG = 2056
    
    @staticmethod
    def getEpsgCode(eastingToCheck, nortingToCheck):
        '''
        Based on the given coordinate pair the corresponding EPSG code will be returned. Currently supported
        are the following coordinate systems:
        - LV03
        - LV95
        - WGS-84
        - UTM-32
        
        The method works with the bounding
        box of Switzerland and the following restrictions / parameters:
        
        Name:     EPSG:    Upper left:           Lower right:
        LV03      21780     504000   280000       886000     60000
        LV95       2056    2504000  1280000      2886000   1031600
        WGS-84     4326    6.18080  48.0019     11.19506  45.40207
        UTM-32    32632     298700  5290800       658400   5046000
        
        @type eastingToCheck: float
        @param eastingToCheck: Easting coordinate
        @type northingToCheck: float
        @param eastingToCheck: Easting coordinate
        
        @rtype: int
        @return: EPSG code of the given coordinate pair.
        
        @raise InvalidCoordinatesError: Error will be raised in case of not supported coordinate system or wrong assignment of Easting and Northing.
        '''
        
        if eastingToCheck > 504000.0 and eastingToCheck < 886000.0 and nortingToCheck < 280000.0 and nortingToCheck > 60000.0:
            return 21780
        elif eastingToCheck > 2504000.0 and eastingToCheck < 2886000.0 and nortingToCheck < 1280000.0 and nortingToCheck > 1031600.0:
            return 2056
        elif eastingToCheck > 6.18080 and eastingToCheck < 11.19506 and nortingToCheck < 48.0019 and nortingToCheck > 45.40207:
            return 4326
        elif eastingToCheck > 298700.0 and eastingToCheck < 658400.0 and nortingToCheck < 5290800.0 and nortingToCheck > 5046000.0:
            return 32632
        else:
            message = "The coordinate pair {0} / {1} does not fit with the supported coordinate systems. Check the values and order (Easting and Northing).".format(eastingToCheck, nortingToCheck)
            raise InvalidCoordinatesError(message)

    def __init__(self, accessConfigurationFullFileName):
        '''
        Constructor
        
        @type accessConfigurationFullFileName: string
        @param accessConfigurationFullFileName: Path to the private database access configuration file.
        '''
        
        super().__init__(accessConfigurationFullFileName)
        
    def getAllGlaciers(self):
        '''
        Retrieves all individual glacier objects from the database.
        
        @rtype: dictionary
        @return: Dictionary with the SGI-ID as key and the corresponding glacier object.
        '''
        
        glaciers = dict()
        
        statement = "SELECT * FROM {0};".format(self._TABLE_GLACIER)
        
        results = super().retriveData(statement)
        
        if results != None:
            for result in results:
                
                glacier = self._recordToObject(result)
                
                glaciers[glacier.pkSgi] = glacier
        
        return glaciers
    
    def getGlacierBySgi(self, pkSgi):
        '''
        Retrieves an individual glacier from the database based on the given Swiss Glacier Inventory key.
        
        @type pkSGI: string
        @param pkSgi: String representation of the Swiss Glacier Inventory key.
        
        @rtype: Glacier
        @return: Object representing the glacier with the given Swiss Glacier Inventory key.
        
        @raise Exception: In case of more than one glacier found.
        @raise Exception: In case of none glacier found.
        @raise OperationalError: Error during connecting to database (e.g. timeout).
        '''
        
        glaciers = dict()
        
        statement = "SELECT * FROM {0} WHERE pk_sgi = '{1}';".format(self._TABLE_GLACIER, pkSgi)
        
        results = super().retriveData(statement)
        
        for result in results:
            
            glacier = self._recordToObject(result)
            glaciers[glacier.pkSgi] = glacier
            
        if len(glaciers) == 1:
            return next(iter(glaciers.values()))
        elif len(glaciers) == 0:
            raise Exception("No entry found!")
            #TODO: Implementation and raising of own database exception.
        elif len(glaciers) > 1:
            raise Exception("Too many entries found!")
            #TODO: Implementation and raising of own database exception.

    def getGlacierByPolygon(self, polygonVertices, epsg):
        '''
        Retrieves all glaciers from the database based on the given polygon defined as an array of 2D- or 3D-vertices. 
        All glaciers within the polygon are returned as dictionary.
        
        Important: The method is only tested with 2D-geometries yet:
        
        Most of the EPSG projections are supported. Code tested with the following projections:
        - LV03:    EPSG = 21781
        - LV95:    EPSG = 2056 
        - UTM-32:  EPSG = 32632
        - WGS-84:  EPSG = 4326
        
        @type polygonVertices: list of tuples
        @param wktPolygon: List of vertices of a polygon
        @type epsg: int
        @param epsg: EPSG id of the projection of the given polygon
        
        @rtype: dictionary
        @return: Dictionary with the SGI-ID as key and the corresponding glacier object.

        @raise Exception: In case of none glacier found.
        @raise OperationalError: Error during connecting to database (e.g. timeout).
        @raise dataflow.DataReaders.Exceptions.InvalidGeometryError import InvalidGeometryError: Error in case of wrongly defined polygon
        '''
        
        # Converting the vertices into a WKT polygon.
        wktPolygon = self._verticesToWktPolygon(polygonVertices)
        
        # Retrieving and returning the glaciers within the polygon.
        return self.getGlacierByWktPolygon(wktPolygon, epsg)
        
    
    def getGlacierByWktPolygon(self, wktPolygon, epsg):
        '''
        Retrieves all glaciers from the database based on the given polygon defined as WellKnownText. 
        All glaciers within the polygon are returned as dictionary.
        
        Important: The method is only tested with 2D-geometries yet:
        
        Most of the EPSG projections are supported. Code tested with the following projections:
        - LV03:    EPSG = 21781
        - LV95:    EPSG = 2056 
        - UTM-32:  EPSG = 32632
        - WGS-84:  EPSG = 4326

        @type wktPolygon: string
        @param wktPolygon: Polygon as WellKnownText with a defined projection.
        @type epsg: int
        @param epsg: EPSG id of the projection of the given polygon
        
        @rtype: dictionary
        @return: Dictionary with the SGI-ID as key and the corresponding glacier object.

        @raise Exception: In case of none glacier found.
        @raise OperationalError: Error during connecting to database (e.g. timeout).
        '''
        
        glaciers = dict()
        statement = ""
        
        if epsg == 21780:

            statement = "SELECT * FROM {0} WHERE ST_Within({0}.geom, st_setsrid(st_transform(ST_GeomFromText('{1}'), '+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs', '+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs'), {2}));".format(
                    self._TABLE_GLACIER,
                    wktPolygon,
                    self._TABLE_GLACIER_EPSG)
        
        else:

            statement = "SELECT * FROM {0} WHERE ST_Within({0}.geom, st_transform(st_setsrid(ST_GeomFromText('{1}'), {2}), {3}));".format(
                self._TABLE_GLACIER,
                wktPolygon, epsg,
                self._TABLE_GLACIER_EPSG)
            
        results = super().retriveData(statement)
        
        for result in results:
            
            glacier = self._recordToObject(result)
            glaciers[glacier.pkSgi] = glacier
            
        if len(glaciers) == 0:
            raise Exception("No entry found!")
            #TODO: Implementation and raising of own database exception.
        elif len(glaciers) > 0:
            return glaciers
            #TODO: Implementation and raising of own database exception.
            
            
    def getGlacierByBox(self, upperLeftEasting, upperLeftNorthing, lowerRightEasting, lowerRightNorthing):
        '''
        Retrieves glaciers from the database based on a geographical box. All glaciers
        within the box are returned as dictionary.
        
        Following coordinate systems are supported (EPSG code will be derived automatically):
        - LV03
        - LV95
        - UTM-32
        - WGS-84
        
        @type upperLeftEasting: float
        @param upperLeftEasting: Easting coordinates of upper left corner of the search-box.
        @type upperLeftNorthing: float
        @param upperLeftNorthing: Northing coordinates of upper left corner of the search-box.
        @type lowerRightEasting: float
        @param lowerRightEasting: Easting coordinates of lower right corner of the search-box.
        @type lowerRightNorthing: float
        @param lowerRightNorthing: Northing coordinates of lower right corner of the search-box.
        
        @rtype: dictionary
        @return: Dictionary with the SGI-ID as key and the corresponding glacier object.

        @raise Exception: In case of none glacier found.
        @raise OperationalError: Error during connecting to database (e.g. timeout).
        '''
        
        epsgUpperLeft = GlacierReader.getEpsgCode(upperLeftEasting, upperLeftNorthing)
        epsgLowerRight = GlacierReader.getEpsgCode(lowerRightEasting, lowerRightNorthing)
        
        if epsgUpperLeft != epsgLowerRight:
            
            message = "The bounding box coordinate pairs are not within the same coordinate system."
            raise InvalidCoordinatesError(message)
        
        glaciers = dict()
        
        # Statements: 
        # LV95:   SELECT * FROM base_data.vw_glacier WHERE ST_Within(base_data.vw_glacier.geom, st_transform(st_setsrid(ST_MakeEnvelope(2669957.513,1168228.193,2676059.549,1158937.028), 2056), 2056));
        # WGS-84: SELECT * FROM base_data.vw_glacier WHERE ST_Within(base_data.vw_glacier.geom, st_transform(st_setsrid(ST_MakeEnvelope(8.35111,46.66279,8.43558,46.57434), 4326), 2056));
        # UTM-32: SELECT * FROM base_data.vw_glacier WHERE ST_Within(base_data.vw_glacier.geom, st_transform(st_setsrid(ST_MakeEnvelope(450412.107,5167764.985,456519.738,5158114.929), 32632), 2056));
        # LV03:   SELECT * FROM base_data.vw_glacier WHERE ST_Within(base_data.vw_glacier.geom, st_setsrid(st_transform(ST_MakeEnvelope(669957.513,168228.193,676059.549,158937.028), '+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs', '+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs'), 2056));
        
        statement = ""
        
        if epsgUpperLeft == 21780:
            
            statement = "SELECT * FROM {0} WHERE ST_Within({0}.geom, st_setsrid(st_transform(ST_MakeEnvelope({1}, {2}, {3}, {4}), '+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs', '+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs'), 2056));".format(
                self._TABLE_GLACIER,
                upperLeftEasting, upperLeftNorthing,
                lowerRightEasting, lowerRightNorthing,
                self._TABLE_GLACIER_EPSG)
            
        else:
            statement = "SELECT * FROM {0} WHERE ST_Within({0}.geom, st_transform(st_setsrid(ST_MakeEnvelope({1}, {2}, {3}, {4}), {5}), {6}));".format(
                self._TABLE_GLACIER,
                upperLeftEasting, upperLeftNorthing,
                lowerRightEasting, lowerRightNorthing,
                epsgUpperLeft,
                self._TABLE_GLACIER_EPSG)

        results = super().retriveData(statement)
        
        for result in results:
            
            glacier = self._recordToObject(result)
            glaciers[glacier.pkSgi] = glacier
            
        if len(glaciers) == 0:
            raise Exception("No entry found!")
            #TODO: Implementation and raising of own database exception.
        elif len(glaciers) > 0:
            return glaciers
            #TODO: Implementation and raising of own database exception.

    def _recordToObject(self, dbRecord):
        '''
        Converts a single record of the database into a glacier object.
        
        @type dbRecord: list
        @param dbRecord: List with all values of one database record.
        
        @rtype: Glacier
        @return: Glacier object of the database record.
        '''
        
        pk = uuid.UUID(dbRecord[1])
        
        if dbRecord[2] != None:
            pkVaw = int(dbRecord[2])
        else:
            pkVaw = None
            
        pkSgi = dbRecord[5]
        name = dbRecord[6]
            
        return Glacier(pk, pkVaw, pkSgi, name)
        
    def _verticesToWktPolygon(self, polygonVertices):
        '''
        Converts the given list of 2D- or 3D-coordinate tuples into a regular polygon defined as WellKnownText.
        Important: Holes or multi-polygons are not supported yet.
        
        Precondition:
        1) The given list of vertices must contain at least three vertices.
        2) In case of three vertices, the first and last vertex has to be different (in Easting and Northing)
        If only one precondition is not fulfilled, an InvalidGeometryError will be raised.
        
        The given polygon will be auto-closed:
        In case of different first and last vertex (Easting and Northing), 
        an additional vertex will be added at the end with the values of the first vertex.
        
        @type polygonVertices: list of tuples
        @param polygonVertices: List of individual tuples containing the Easting and Northing 2D-coordinates of an individual vertex.
        
        @rtype: string
        @return: Polygon as WellKnownText
        
        @raise dataflow.DataReaders.Exceptions.InvalidGeometryError import InvalidGeometryError: Error in case of wrongly defined polygon
        '''
        
        # Do some consistency checks.
        # Minimal length of vertex list.
        if len(polygonVertices) < 3:
            raise InvalidGeometryError("To few vertices. Check your geometry.")
        # Check 2D- or 3D-coordinates for each vertex.
        # The definition if 2D or 3D has to be consequent for all vertices.
        dimensions = len(polygonVertices[0])
        if dimensions < 2 and dimensions > 3:
            raise InvalidGeometryError("Invalid dimension of the first vertex. Check your geometry.")
        
        for vertex in polygonVertices:
            if len(vertex) != dimensions:
                raise InvalidGeometryError("To few or to many coordinates for at least one vertex. Check your geometry.")
        
        # Closing the polygon
        firstVertex = polygonVertices[0]
        lastVertex = polygonVertices[len(polygonVertices) - 1]
        
        if dimensions == 2:
            if firstVertex[0] != lastVertex[0] and firstVertex[1] != lastVertex[1]:
                # Closing the 2D polygon with the first vertex.
                polygonVertices.append((firstVertex[0], firstVertex[1]))
        else:
            if firstVertex[0] != lastVertex[0] and firstVertex[1] != lastVertex[1] and firstVertex[2] != lastVertex[2]:
                # Closing the 2D polygon with the first vertex.
                polygonVertices.append((firstVertex[0], firstVertex[1], firstVertex[2]))
                
        # Getting the individual vertices into one string.
        vertexTemplate2D = '{0} {1}'
        vertexTemplate3D = '{0} {1} {2}'
        verticesText     = ''
        
        counterVertices = 0
        for vertex in polygonVertices:
            
            counterVertices += 1
            
            vertexText = ''
            
            if dimensions == 2:
                vertexText = vertexTemplate2D.format(vertex[0], vertex[1])
            else:
                vertexText = vertexTemplate3D.format(vertex[0], vertex[1], vertex[2])
        
            # Getting all individual vertices into one string.
            verticesText += vertexText
            # Except of the last vertex, all vertices are comma separated.
            if counterVertices != len(polygonVertices):
                verticesText += ","
                
        # Getting the entire WKT string done.
        polygonTemplate  = 'POLYGON(({0}))'
        polygoneText = polygonTemplate.format(verticesText)
        
        return polygoneText