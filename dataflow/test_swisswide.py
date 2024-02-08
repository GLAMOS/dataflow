'''
Created on 1.2.2024

@author: elias

Main script to import all VAW mass-balance swiss wide files into the GLAMOS database.
'''

from dataflow.DataWriters.DatabaseWriters.MassBalanceWriter import MassBalanceWriter
from dataflow.DataReaders.VawFileReaders.MassBalanceReader import MassBalanceReader
from dataflow.DataObjects.Glacier import Glacier
from dataflow.DataReaders.DatabaseReaders.GlacierReader import GlacierReader
from dataflow.DataObjects.Exceptions.GlacierNotFoundError import GlacierNotFoundError

import configparser
import os

config = configparser.ConfigParser()
config.read("dataflow.cfg")

privateDatabaseAccessConfiguration = r".\databaseAccessConfiguration.gldirw.cfg"

rootDirectoryPath = config.get("MassBalanceSwissWide", "rootDirectoryInput")
dataDirectoryName = config.get("MassBalanceSwissWide", "directoryInput")

dataDirectoryPath = os.path.join(rootDirectoryPath, dataDirectoryName)

massBalanceReader = None

if os.path.exists(dataDirectoryPath):
    # Loop over all mass-balance swiss wide data files in the directory.
    __NUMBER_HEADER_LINES = 2
    lineCounter = 0
    print(os.listdir(dataDirectoryPath))
    with open(os.path.join(dataDirectoryPath, os.listdir(dataDirectoryPath)[0]), "r") as area_file:
        with open(os.path.join(dataDirectoryPath, os.listdir(dataDirectoryPath)[1]), "r") as mb_evo_file:
            with open(os.path.join(dataDirectoryPath, os.listdir(dataDirectoryPath)[2]), "r") as vol_evo_file:
                for line_area, line_mb_evo, line_vol_evo in zip(area_file, mb_evo_file, vol_evo_file):

                    lineCounter += 1

                    sgi_id = line_area.split()[0]
                    area = line_area.split()[1]
                    mb_evo = line_mb_evo.split()[1]
                    vol_evo = line_vol_evo.split()[1]
                    # print(sgi_id, area, mb_evo, vol_evo)

glacierReader = GlacierReader(privateDatabaseAccessConfiguration)
allGlaciers = glacierReader.getAllGlaciers()
for glacier in allGlaciers:
    print(glacier)



