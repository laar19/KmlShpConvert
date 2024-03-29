from library  import ogr2ogr
from qtpy     import QtWidgets
from datetime import datetime

# Convert selected file list_ to string
# in order to shown them in the window
def list_to_string(list_):
    string = str()
    for i in range(len(list_)):
        string += str(i+1) + " - " + list_[i] + "\n\n"
    return string

# Select multiple files
def select_multiple_files(dialog):
    file_view = dialog.findChild(QtWidgets.QListView, "ListView")
    if file_view:
        file_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
    f_tree_view = dialog.findChild(QtWidgets.QTreeView)
    if f_tree_view:
        f_tree_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

    return f_tree_view

def shp2kml_(shpfile, output_path, number):
    #shpFile = shpfile
    #kmlFile = shpFile.replace('.shp', '_CONVERTIDO_'+str(datetime.now())+'_'+str(number)+'.kml')
    output_path = output_path.replace(".shp", ".kml")
    #kmlFile.replace('-', '_')
    
    #os.system('ogr2ogr -f "KML" ' + kmlFile + ' ' + shpFile)
    #ogr2ogr.main(["", "-f", "KML", kmlFile, shpFile])
    ogr2ogr.main(["", "-f", "KML", output_path, shpfile])

def kml2shp_(kmlfile, output_path, number):
    #kmlFile = kmlfile
    #shpFile = kmlFile.replace('.kml', '_CONVERTIDO_'+str(datetime.now())+'_'+str(number)+'.shp')
    output_path = output_path.replace(".kml", ".shp")
    #shpFile.replace('-', '_')
    
    #os.system('ogr2ogr -f "ESRI Shapefile" ' + shpFile + ' ' + kmlFile)
    #ogr2ogr.main(["", "-f", "ESRI Shapefile", shpFile, kmlFile])
    ogr2ogr.main(["", "-f", "ESRI Shapefile", output_path, kmlfile])
