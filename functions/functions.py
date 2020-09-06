import os
import platform
sistema_operativo = platform.system() # Conoce el tipo de sistema operativo

from PyQt5 import QtWidgets

# Convierte la lista de archivos seleccionados a una sóla cadena
# para ser mostrada en la ventana
def list_to_string(lista):
    cadena = str()
    for i in range(len(lista)):
        cadena += str(i+1) + " - " + lista[i] + "\n\n"
    return cadena

# Crea el archivo kml generado desde el shp en el sistema de archivos
def crea_archivo_kml(nombre_archivo, contenido):
    archivo_kml = open(nombre_archivo, "w")
    archivo_kml.write(contenido)
    archivo_kml.close()

# Especifica la ruta de salida según el sistema operativo
def ruta_salida():
    ruta = str()
    
    if sistema_operativo == "Windows":
        ruta = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        #ruta = os.path.join(os.path.join(os.environ["HOMEPATH"]), "Desktop")
    else:
        ruta = os.path.join(os.path.join(os.path.expanduser("~")))

    return ruta

# Seleccionar múltiples archivos
def select_multiple_files(dialog):
    file_view = dialog.findChild(QtWidgets.QListView, "listView")
    if file_view:
        file_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
    f_tree_view = dialog.findChild(QtWidgets.QTreeView)
    if f_tree_view:
        f_tree_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

    return f_tree_view