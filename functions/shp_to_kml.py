#import geoconvert as geoc # using pip
from geoconvert import *

def shp2kml_(shpfile, number):
    shpFile = shpfile
    kmlFile = shpFile.replace('.shp', '_CONVERTIDO_'+str(number)+'.kml')
    kmlFile.replace('-', '_')

    # Loading data
    #data = geoc.vector() # using pip
    data = vector()
    data.path_input = shpFile
    data.config()

    # Converting data
    data.tokml(path_tokml=kmlFile)