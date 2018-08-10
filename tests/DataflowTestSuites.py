'''
Created on 10.08.2018

@author: yvo
'''

'''
Main UnitTest module of the GLAMOS dataflow application.

The module runs automatically all UnitTest defined for the different packages.
'''

import unittest

import DataReadersTestSuites
import DataObjectsTestSuites
import DataWritersTestSuites

if __name__ == '__main__':
    
    # List to contain all UnitTestSuits to run.
    testSuites = []

    # Getting all TestSuits of the defined packages of dataflow.
    testSuites.extend(DataReadersTestSuites.createTestSuite())
    testSuites.extend(DataObjectsTestSuites.createTestSuite())
    testSuites.extend(DataWritersTestSuites.createTestSuite())
    
    # Combining all UnitTest-Suites into one major TestSuite.
    bigSuite = unittest.TestSuite(testSuites)

    # Let's run the tests.
    runner = unittest.TextTestRunner()
    results = runner.run(bigSuite)