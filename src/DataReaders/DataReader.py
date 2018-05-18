'''
Created on 18.05.2018

@author: yvo
'''

class DataReader(object):
    '''
    classdocs
    '''

    _glacier = None

    @property
    def glacier(self):
        return self._glacier

    def __init__(self):
        '''
        Constructor
        '''
        