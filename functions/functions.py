def list_to_string(lista):
    cadena = str()
    for i in range(len(lista)):
        cadena += str(i+1) + " - " + lista[i] + "\n\n"
    return cadena

def crea_archivo_kml(nombre_archivo, contenido):
    archivo_kml = open(nombre_archivo, "w")
    archivo_kml.write(contenido)
    archivo_kml.close()