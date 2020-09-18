import geoconvert as geoc

def shp2kml_(shpfile, number):
    shpFile = shpfile
    kmlFile = shpFile.replace('.shp', '_CONVERTIDO_'+str(number)+'.kml')
    kmlFile.replace('-', '_')

    # Loading data
    data = geoc.vector()
    data.path_input = shpFile
    data.config()

    # Converting data
    data.tokml(path_tokml=kmlFile)