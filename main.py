from PyQt5 import QtWidgets, uic
from functions.functions import *
from functions.kmz_converter import *
from functions.shp2kml import *

appname = "KmlShpConvert"
autores = ["Rosaura Rojas", "<rosaurarojas1989@gmail.com>", "Luis Acevedo", "<laar@protonmail.com>"]
licencia = "Copyright 2020. All code is copyrighted by the respective authors.\n" + appname + " can be redistributed and/or modified under the terms of the GNU GPL versions 3 or by any future license endorsed by " + autores[0] + " and " + autores[2] + "." + "\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."

ventana = "window.ui"

fileNames1 = list()
fileNames2 = list()

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi(ventana, self)
        self.show()

        self.file_list = self.findChild(QtWidgets.QTextBrowser, "file_list")
        self.file_list_2 = self.findChild(QtWidgets.QTextBrowser, "file_list_2")
        
        self.btn_buscar = self.findChild(QtWidgets.QPushButton, "btn_buscar")
        self.btn_buscar.clicked.connect(self.buscar1)
        self.btn_buscar_2 = self.findChild(QtWidgets.QPushButton, "btn_buscar_2")
        self.btn_buscar_2.clicked.connect(self.buscar2)

        self.btn_aceptar = self.findChild(QtWidgets.QPushButton, "btn_aceptar")
        self.btn_aceptar.clicked.connect(self.kml_to_shp)
        self.btn_aceptar_2 = self.findChild(QtWidgets.QPushButton, "btn_aceptar_2")
        self.btn_aceptar_2.clicked.connect(self.shp_to_kml)

        self.btn_limpiar = self.findChild(QtWidgets.QPushButton, "btn_limpiar")
        self.btn_limpiar.clicked.connect(self.limpiar)
        self.btn_limpiar_2 = self.findChild(QtWidgets.QPushButton, "btn_limpiar_2")
        self.btn_limpiar_2.clicked.connect(self.limpiar)

        self.btn_about = self.findChild(QtWidgets.QPushButton, "btn_about")
        self.btn_about.clicked.connect(self.aboutQt)

        self.btn_autores = self.findChild(QtWidgets.QPushButton, "btn_autores")
        self.btn_autores.clicked.connect(self.autores)

        self.btn_licencia = self.findChild(QtWidgets.QPushButton, "btn_licencia")
        self.btn_licencia.clicked.connect(self.licencia)

        self.btn_salir = self.findChild(QtWidgets.QPushButton, "btn_salir")
        self.btn_salir.clicked.connect(self.salir)

    def buscar1(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilter("File (*.kml *.kmz)")
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        
        global fileNames1
        if dialog.exec_():
            fileNames1.append(dialog.selectedFiles()[0])

        self.file_list.setText(list_to_string(fileNames1))

    def buscar2(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilter("File (*.shp)")
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        
        global fileNames2
        if dialog.exec_():
            fileNames2.append(dialog.selectedFiles()[0])

        self.file_list_2.setText(list_to_string(fileNames2))

    def kml_to_shp(self):
        for i in fileNames1:
            return_value = kmz_converter(i)
        if return_value == 0:
            QtWidgets.QMessageBox.about(self, "Listo", "Conversión exitosa")
        else:
            QtWidgets.QMessageBox.about(self, "Error", "Ocurrió un error durante la conversión")

    def shp_to_kml(self):
        for i in fileNames2:
            crea_archivo_kml("archivo.kml", shp2kml(i))
        QtWidgets.QMessageBox.about(self, "Listo", "Conversión exitosa")

    def limpiar(self):
        self.file_list.setText("")
        self.file_list_2.setText("")
        fileNames1.clear()
        fileNames2.clear()

    def aboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self)
    
    def autores(self):
        #autores = "Rosaura Rojas <rosaurarojas1989@gmail.com>\n\nLuis Acevedo  <laar@protonmail.com>"
        autors = autores[0] + " " + autores[1] + "\n\n" + autores[2] + "  " + autores[3]
        QtWidgets.QMessageBox.about(self, "Autores", autors)
        
    def licencia(self):
        QtWidgets.QMessageBox.about(self, "Licencia", licencia)

    def salir(self):
        sys.exit()

if __name__ == "__main__":
    
    print("KML2SHP Copyright (C) 2020 Rosaura, Luis Acevedo.\nEste programa viene con ABSOLUTAMENTE NINGUNA GARANTÍA.\nEsto es software libre, y le invitamos a redistribuirlo\nbajo ciertas condiciones.\nPor favor, leer el archivo README.")

    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    app.exec_()