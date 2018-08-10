'''
Created on 10.08.2018

@author: yvo
'''

import unittest

from dataflow.DataReadersTests import DataReadersTestsSuite

if __name__ == '__main__':
    
    testSuites = []

    testSuites.extend(DataReadersTestsSuite.createTestSuite())
    
    # Combining all UnitTest-Suites into one major TestSuite.
    bigSuite = unittest.TestSuite(testSuites)

    # Let's run the tests.
    runner = unittest.TextTestRunner()
    results = runner.run(bigSuite)