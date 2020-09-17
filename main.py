from PyQt5 import uic
from functions.functions import *
from functions.kmz_converter import *
from functions.shp_to_kml import *

appname  = "KmlShpConvert"
authors  = ["Rosaura Rojas", "<rrojas@abae.gob.ve>", "Luis Acevedo", "<laar@protonmail.com>"]
credits_ = ["https://github.com/DavidDarlingKhepryOrg", "https://github.com/tomtl"]
license_ = "Copyright 2020. All code is copyrighted by the respective authors.\n" + appname + " can be redistributed and/or modified under the terms of the GNU GPL versions 3 or by any future license_ endorsed by " + authors[0] + " and " + authors[2] + "." + "\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."

window = "ui/window.ui"

kml_file_names = list() # File list to convert from kml to shp
shp_file_names = list() # File list to convert from shp to kml

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi(window, self)
        self.show()

        self.kml_file_list = self.findChild(QtWidgets.QTextBrowser, "kml_file_list") # Show file list to convert, from kml to shp, tab 1
        self.shp_file_list = self.findChild(QtWidgets.QTextBrowser, "shp_file_list") # Show file list to convert, from shp to kml, tab 2
        
        self.btn_search = self.findChild(QtWidgets.QPushButton, "btn_search")        # Search files button
        self.btn_search.clicked.connect(self.search)

        self.btn_accept = self.findChild(QtWidgets.QPushButton, "btn_accept")        # Convert from kml to shp button
        self.btn_accept.clicked.connect(self.conversion)

        self.btn_clear = self.findChild(QtWidgets.QPushButton, "btn_clear")          # Clear file list button
        self.btn_clear.clicked.connect(self.clear)

        self.btn_about = self.findChild(QtWidgets.QPushButton, "btn_about")       # About Qt
        self.btn_about.clicked.connect(self.aboutQt)

        self.btn_authors = self.findChild(QtWidgets.QPushButton, "btn_authors")   # Authors
        self.btn_authors.clicked.connect(self.authors)

        self.btn_license = self.findChild(QtWidgets.QPushButton, "btn_license")   # License
        self.btn_license.clicked.connect(self.license_)

        self.btn_exit = self.findChild(QtWidgets.QPushButton, "btn_exit")         # Exit
        self.btn_exit.clicked.connect(self.exit)

    # Search kml files in file system
    def search(self):
        aux = list()

        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        
        currentTabName = self.tabWidget.currentWidget().objectName()
        if currentTabName == "tab":
            dialog.setNameFilter("File (*.kml *.kmz)")
            global kml_file_names
            aux = kml_file_names
        else:
            dialog.setNameFilter("File (*.shp)")
            global shp_file_names
            aux = shp_file_names

        dialog.setViewMode(QtWidgets.QFileDialog.Detail)

        """
        # Select one file
        if dialog.exec_():
            aux.append(dialog.selectedFiles()[0]) # Add selected kml to file list to convert

        self.kml_file_list.setText(list_to_string(kml_file_names)) # Show selected kml file
        """

        #Select multiple files
        select_multiple_files(dialog)
        if dialog.exec():
            for i in dialog.selectedFiles():
                aux.append(i) # Add selected kml to files list to convert

        if currentTabName == "tab":
            self.kml_file_list.setText(list_to_string(aux)) # Show selected kml files
        else:
            self.shp_file_list.setText(list_to_string(aux)) # Show selected shp files

    # Convert selected kml files
    def conversion(self):
        aux = list()

        currentTabName = self.tabWidget.currentWidget().objectName()
        if currentTabName == "tab":
            convert_function = kmz_converter
            aux = kml_file_names
        else:
            convert_function = shp2kml_
            aux = shp_file_names

        if len(aux) == 0:
            QtWidgets.QMessageBox.critical(self, "Error", "Debe seleccionar por lo menos un archivo")
        else:
            for i in range(len(aux)):
                try:
                    convert_function(aux[i], i)
                except:
                    QtWidgets.QMessageBox.critical(self, "Error", "Ocurrió un error durante la conversión.\n" + "El archivo: " + aux[i] + "\nPosiblemente esté corrupto o dañado")
                else:
                    QtWidgets.QMessageBox.about(self, "Listo", "Conversión exitosa")

    # Clear selected file list
    def clear(self):
        self.kml_file_list.setText("")
        self.shp_file_list.setText("")
        kml_file_names.clear()
        shp_file_names.clear()

    def aboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self)
    
    def authors(self):
        mensaje = "Autores:\n" + authors[0] + " " + authors[1] + "\n" + authors[2] + "  " + authors[3] + "\n\n\n" + "Cŕeditos:\n" + credits_[0] + "\n" + credits_[1]
        QtWidgets.QMessageBox.about(self, "Autores", mensaje)
        
    def license_(self):
        QtWidgets.QMessageBox.about(self, "Licencia", license_)

    def exit(self):
        sys.exit()

if __name__ == "__main__":
    
    print(appname + " Copyright (C) 2020 " + authors[0] + ", " + authors[2] + ".\nEste programa viene con ABSOLUTAMENTE NINGUNA GARANTÍA.\nEsto es software libre, y le invitamos a redistribuirlo\nbajo ciertas condiciones.\nPor favor, leer el archivo README.")

    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    app.exec_()
