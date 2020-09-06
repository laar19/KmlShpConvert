from PyQt5 import uic
from functions.functions import *
from functions.kmz_converter import *
from functions.shp2kml import *

appname = "KmlShpConvert"
autores = ["Rosaura Rojas", "<rosaurarojas1989@gmail.com>", "Luis Acevedo", "<laar@protonmail.com>"]
creditos = ["https://github.com/cthrall", "https://github.com/tomtl"]
licencia = "Copyright 2020. All code is copyrighted by the respective authors.\n" + appname + " can be redistributed and/or modified under the terms of the GNU GPL versions 3 or by any future license endorsed by " + autores[0] + " and " + autores[2] + "." + "\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."

ventana = "window.ui"

fileNames1 = list() # Lista de archivos a convertir de km la shp
fileNames2 = list() # Lista de archivos a convertir de shp a kml

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi(ventana, self)
        self.show()

        self.file_list = self.findChild(QtWidgets.QTextBrowser, "file_list")     # Muestra los archivos a convertir de kml a shp, pestaña 1
        self.file_list_2 = self.findChild(QtWidgets.QTextBrowser, "file_list_2") # Muestra los archivos a convertir de shp a kml, pestaña 2
        
        self.btn_buscar = self.findChild(QtWidgets.QPushButton, "btn_buscar")     # Botón de buscar archivos, pestaña 1
        self.btn_buscar.clicked.connect(self.buscar1)
        self.btn_buscar_2 = self.findChild(QtWidgets.QPushButton, "btn_buscar_2") # Botón de buscar archivos, pestaña 2
        self.btn_buscar_2.clicked.connect(self.buscar2)

        self.btn_aceptar = self.findChild(QtWidgets.QPushButton, "btn_aceptar")     # Botón para convertir archivos de kml a shp, pestaña 1
        self.btn_aceptar.clicked.connect(self.kml_to_shp)
        self.btn_aceptar_2 = self.findChild(QtWidgets.QPushButton, "btn_aceptar_2") # Botón para convertir archivos de shp a kml, pestaña 2
        self.btn_aceptar_2.clicked.connect(self.shp_to_kml)

        self.btn_limpiar = self.findChild(QtWidgets.QPushButton, "btn_limpiar")     # Botón para limpiar la lista de archivos, pestaña 1
        self.btn_limpiar.clicked.connect(self.limpiar)
        self.btn_limpiar_2 = self.findChild(QtWidgets.QPushButton, "btn_limpiar_2") # Botón para limpiar la lista de archivos, pestaña 2
        self.btn_limpiar_2.clicked.connect(self.limpiar)

        self.btn_about = self.findChild(QtWidgets.QPushButton, "btn_about") # About Qt
        self.btn_about.clicked.connect(self.aboutQt)

        self.btn_autores = self.findChild(QtWidgets.QPushButton, "btn_autores") # Autores
        self.btn_autores.clicked.connect(self.autores)

        self.btn_licencia = self.findChild(QtWidgets.QPushButton, "btn_licencia") # Licencia
        self.btn_licencia.clicked.connect(self.licencia)

        self.btn_salir = self.findChild(QtWidgets.QPushButton, "btn_salir") # Salir
        self.btn_salir.clicked.connect(self.salir)

    # Función para buscar los archivos kml en el sistema de archivos
    def buscar1(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilter("File (*.kml *.kmz)")
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)

        """
        Seleccionar múltiples archivos
        """
        select_multiple_files(dialog)

        global fileNames1
        if dialog.exec():
            for i in dialog.selectedFiles():
                fileNames1.append(i) # Añade los kml seleccionados a la lista de archivos a convertir

        self.file_list.setText(list_to_string(fileNames1)) # Muestra todos los kml seleccionados

        """
        # Seleccionar un sólo archivo
        global fileNames1
        if dialog.exec_():
            fileNames1.append(dialog.selectedFiles()[0]) # Añade el kml seleccionado a la lista de archivos a convertir

        self.file_list.setText(list_to_string(fileNames1)) # Muestra todos los kml seleccionados
        """

    # Función para buscar los archivos shp en el sistema de archivos
    def buscar2(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilter("File (*.shp)")
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        
        """
        Seleccionar múltiples archivos
        """
        select_multiple_files(dialog)

        global fileNames2
        if dialog.exec():
            for i in dialog.selectedFiles():
                fileNames2.append(i) # Añade los kml seleccionados a la lista de archivos a convertir

        self.file_list_2.setText(list_to_string(fileNames2)) # Muestra todos los kml seleccionados

    # Convierte los kml seleccionados
    def kml_to_shp(self):
        if len(fileNames1) == 0:
            QtWidgets.QMessageBox.critical(self, "Error", "Debe seleccionar por lo menos un archivo")
        else:
            for i in fileNames1:
                try:
                    kmz_converter(i)
                except:
                    QtWidgets.QMessageBox.critical(self, "Error", "Ocurrió un error durante la conversión.\n" + "El archivo: " + i + "\nPosiblemente esté corrupto o dañado")
                else:
                    QtWidgets.QMessageBox.about(self, "Listo", "Conversión exitosa")

    # Convierte los shp seleccionados
    def shp_to_kml(self):
        if len(fileNames2) == 0:
            QtWidgets.QMessageBox.critical(self, "Error", "Debe seleccionar por lo menos un archivo")
        else:
            for i in range(len(fileNames2)):
                try:
                    ruta = ruta_salida() + "/" + str(i) + "_archivo.kml"
                    crea_archivo_kml(ruta, shp2kml(fileNames2[i]))
                except:
                    QtWidgets.QMessageBox.critical(self, "Error", "Ocurrió un error durante la conversión.\n" + "El archivo: " + fileNames2[i] + "\nPosiblemente esté corrupto o dañado")
                else:
                    QtWidgets.QMessageBox.about(self, "Listo", "Conversión exitosa")

    # Limpia la lista de archivos seleccionados
    def limpiar(self):
        self.file_list.setText("")
        self.file_list_2.setText("")
        fileNames1.clear()
        fileNames2.clear()

    def aboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self)
    
    def autores(self):
        mensaje = "Autores:\n" + autores[0] + " " + autores[1] + "\n" + autores[2] + "  " + autores[3] + "\n\n\n" + "Cŕeditos:\n" + creditos[0] + "\n" + creditos[1]
        QtWidgets.QMessageBox.about(self, "Autores", mensaje)
        
    def licencia(self):
        QtWidgets.QMessageBox.about(self, "Licencia", licencia)

    def salir(self):
        sys.exit()

if __name__ == "__main__":
    
    print(appname + " Copyright (C) 2020 " + autores[0] + ", " + autores[2] + ".\nEste programa viene con ABSOLUTAMENTE NINGUNA GARANTÍA.\nEsto es software libre, y le invitamos a redistribuirlo\nbajo ciertas condiciones.\nPor favor, leer el archivo README.")

    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    app.exec_()