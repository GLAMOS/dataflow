'''
Created on 31.05.2018

@author: yvo
'''

from .Glamos import GlamosData

class MassBalance(GlamosData):
    # TODO: Class documentation

    _dateFrom = None
    _dateTo = None
    
    _winterMassBalance = None
    _annualMassBalance = None
    
    # TODO: Adding the elevation bands as list or dictionary.

    def __init__(self, pk = None, 
                 dateFrom = None, dateTo = None,
                 winterMassBalance = None, annualMassBalance = None):
        '''
        Constructor
        '''
        
        super().__init__(pk)
        
        self._dateFrom = dateFrom
        self._dateTo   = dateTo
        
        self._winterMassBalance = winterMassBalance
        self._annualMassBalance = annualMassBalance
        
    @property
    def dateFrom(self):
        '''
        Gets the start date of the measurement period.
        '''
        return self._dateFrom

    @property
    def dateTo(self):
        '''
        Gets the end date of the measurement period.
        '''
        return self._dateTo
    
    @property
    def winterMassBalance(self):
        '''
        Gets the winter mass balance in mm w.e..
        '''
        return self._winterMassBalance

    @property
    def annualMassBalance(self):
        '''
        Gets the annual mass balance in mm w.e..
        '''
        return self._annualMassBalance
    

    def __str__(self):
        '''
        Overrides the __str__ method. Returning a string with the key values of the measurement. 
        
        @rtype: string
        '''
        
        lineToWrite = "{0} -> {1}\n\t{2} mm w.e. winter mass balance\n\t{3} mm w.e. annual mass balance".format(
            self._dateFrom,
            self._dateTo,
            self._winterMassBalance,
            self._annualMassBalance)

        return lineToWrite