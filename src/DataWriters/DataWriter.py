'''
Created on 18.05.2018

@author: yvo
'''

class DataWriter(object):
    '''
    classdocs
    '''

    _glacier = None

    def __init__(self, glacier):
        '''
        Constructor
        '''
        
        self._glacier = glacier