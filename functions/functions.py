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