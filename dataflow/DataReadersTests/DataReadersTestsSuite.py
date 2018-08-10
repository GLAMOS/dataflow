'''
Created on 04.08.2018

@author: yvo
'''

'''
Module to collect, and run, all UnitTests of dataflow.DataReadersTests.

The module can be started as independent Python run, or the method
createTestSuite() can be called externally to retrieve all
test to run of the given package.

Remark: Important variable is the list defined and returned in getTestModule(). The
list defines all modules to be tested. As programmer you have to maintain
this list only.
'''

import unittest

from dataflow.DataReadersTests import GlacierReaderTests
from dataflow.DataReadersTests import MassBalanceDatabaseReaderTests
from dataflow.DataReadersTests import MassBalanceReaderTests
from dataflow.DataReadersTests import VolumeChangeReaderTests

def getTestModules():
    '''
    Defines a list of all modules in the package with UnitTests which have
    to run.
    
    Remarks: In case of new test-modules, add them to the list.
    
    @rtype: list
    @return: List of modules in the package with UnitTests which have to run.
    '''
    return [
        MassBalanceDatabaseReaderTests,
        GlacierReaderTests,
        MassBalanceReaderTests,
        VolumeChangeReaderTests
        ]

def createTestSuite():
    '''
    Creates a UnitTest-Suite with all tests in the given list of modules.
    
    @rtype: list
    @return: List of UnitTestSuites to run.
    '''
    
    loader = unittest.TestLoader()
    
    testModules = getTestModules()
    
    testSuites = []
    
    for testModule in testModules:
        testSuite = loader.loadTestsFromModule(testModule)
        testSuites.append(testSuite)
    
    return testSuites

if __name__ == '__main__':
    '''
    Runs all UnitTest-Suites in the package.
    '''

    # Getting all individual UnitTest-Suites of the package.
    testSuites = createTestSuite()

    # Combining all UnitTest-Suites into one major TestSuite.
    bigSuite = unittest.TestSuite(testSuites)

    # Let's run the tests.
    runner = unittest.TextTestRunner()
    results = runner.run(bigSuite)