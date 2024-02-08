'''
Created on 31.1.2024

@author: elias
'''
from dataflow.DataObjects.MassBalanceSwissWide import MassBalanceSwissWide
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError

class MassBalanceSwissWideReader():
    '''
    Specific file reader for swiss wide mass balance extrapolation files produced by Matthias Huss.

    Example of typical header line:
    ---
    #  Area in km2 for individual Swiss glaciers
    #  SGI-ID 1915  1916  1917  1918  1919  1920  1921 ...
    ---

    Attributes:
        - ___NUMBER_HEADER_LINES    Number of header lines used in the swiss wide mass balance extrapolation file.
    '''

    __NUMBER_HEADER_LINES = 2

    def __init__(self, config, fullFileNameList, glaciers):
        '''
        Constructor of the class.

        @type fullFileName: string
        @param fullFileName: Absolute file path.
        '''

        self._fullFileNameList = fullFileNameList
        self._glaciers = glaciers

        # Setting the parameters of the data file.
        self._numberHeaderLines = self.__NUMBER_HEADER_LINES


    def __str__(self):
        # TODO:
        message = "Test message for {0}".format(
            self._fullFileNameList)
        return message

    @property
    def glacier(self):
        '''
        Get the Glacier object of the data reader.
        '''
        return self._glacier

    @property
    def numberOfYears(self):
        '''
        Number of years with data
        '''
        return self._numberOfYears

    def parse(self):

        self._fullFileNameList

        massBalanceSwissWideGlacierList = []
        massBalanceSwissWideList = []

        with open(self._fullFileNameList[0], "r") as area_file:
            with open(self._fullFileNameList[1], "r") as mb_evo_file:
                with open(self._fullFileNameList[2], "r") as vol_evo_file:
                    print(area_file, mb_evo_file, vol_evo_file)

                    lineCounter = 0

                    # Combining all files line by line and loop through the combined lines
                    for line_area, line_mb_evo, line_vol_evo in zip(area_file, mb_evo_file, vol_evo_file):

                        # skip first header line contains no
                        if lineCounter == 0:
                            lineCounter += 1
                        elif lineCounter == 1:
                            years = line_area.split()[1:]
                            numberOfYears = len(years)
                            print(years,numberOfYears)
                            lineCounter += 1
                        else:
                            line_length = len(line_area.split())
                            for i in range(line_length-1):

                                sgi_id = line_area.split()[0]

                                # Looking for the corresponding glacier in the given glacier collection.
                                glacierFound = None
                                for glacier in self._glaciers.values():

                                    # Comparing the current glacier with the SGI ID of the given line.
                                    if glacier.pkSgi == sgi_id:
                                        glacierFound = glacier
                                if glacierFound != None:
                                    self._glacier = glacierFound
                                else:
                                    message = "No corresponding glacier found."
                                    raise GlacierNotFoundError(message)

                                year = years[i]
                                area = line_area.split()[i+1]
                                mb_evo = line_mb_evo.split()[i+1]
                                vol_evo = line_vol_evo.split()[i+1]
                                #print(sgi_id, year, area, mb_evo, vol_evo)

                                # Getting an object of type Mass Balance Swiss Wide with the parsed information.
                                massBalanceSwissWide = MassBalanceSwissWide(
                                    sgi_id, year, area, mb_evo ,vol_evo)

                                massBalanceSwissWideGlacierList.append(massBalanceSwissWide) # currently no use

                                self._glacier.addMassBalanceSwissWide(massBalanceSwissWide) # if calling write function only last 'glacier' will be written

                            massBalanceSwissWideList.append(massBalanceSwissWideGlacierList) # currently no use

                            lineCounter += 1

                    print(lineCounter - self._numberHeaderLines, " lines have been parsed")

        return massBalanceSwissWideList # currently no use