from PyQt5 import uic
from functions.functions import *
from functions.kmz_converter import *
from functions.shp_to_kml import *

appname = "KmlShpConvert"
authors = ["Rosaura Rojas", "<rrojas@abae.gob.ve>", "Luis Acevedo", "<laar@protonmail.com>"]
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
        
        self.btn_search = self.findChild(QtWidgets.QPushButton, "btn_search")        # Search files button, tab 1
        self.btn_search.clicked.connect(self.search_kml)
        self.btn_search_2 = self.findChild(QtWidgets.QPushButton, "btn_search_2")    # Search files button, tab 2
        self.btn_search_2.clicked.connect(self.search_shp)

        self.btn_accept = self.findChild(QtWidgets.QPushButton, "btn_accept")        # Convert from kml to shp button, tab 1
        self.btn_accept.clicked.connect(self.kml_to_shp)
        self.btn_accept_2 = self.findChild(QtWidgets.QPushButton, "btn_accept_2")    # Convert from kml to shp button, tab 2
        self.btn_accept_2.clicked.connect(self.shp_to_kml)

        self.btn_clear = self.findChild(QtWidgets.QPushButton, "btn_clear")          # Clear file list button, tab 1
        self.btn_clear.clicked.connect(self.clear)
        self.btn_clear_2 = self.findChild(QtWidgets.QPushButton, "btn_clear_2")      # Clear file list button, tab 2
        self.btn_clear_2.clicked.connect(self.clear)

        self.btn_about = self.findChild(QtWidgets.QPushButton, "btn_about")       # About Qt
        self.btn_about.clicked.connect(self.aboutQt)

        self.btn_authors = self.findChild(QtWidgets.QPushButton, "btn_authors")   # Authors
        self.btn_authors.clicked.connect(self.authors)

        self.btn_license = self.findChild(QtWidgets.QPushButton, "btn_license")   # license
        self.btn_license.clicked.connect(self.license_)

        self.btn_exit = self.findChild(QtWidgets.QPushButton, "btn_exit")         # Exit
        self.btn_exit.clicked.connect(self.exit)

    # Search kml files in file system
    def search_kml(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilter("File (*.kml *.kmz)")
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)

        """
        Select multiple files
        """
        select_multiple_files(dialog)

        global kml_file_names
        if dialog.exec():
            for i in dialog.selectedFiles():
                kml_file_names.append(i) # Add selected kml to files list to convert

        self.kml_file_list.setText(list_to_string(kml_file_names)) # Show selected kml files

        """
        # Select one file
        global kml_file_names
        if dialog.exec_():
            kml_file_names.append(dialog.selectedFiles()[0]) # Add selected kml to file list to convert

        self.kml_file_list.setText(list_to_string(kml_file_names)) # Show selected kml file
        """

    # Search shp files in file system
    def search_shp(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilter("File (*.shp)")
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        
        """
        Select multiple files
        """
        select_multiple_files(dialog)

        global shp_file_names
        if dialog.exec():
            for i in dialog.selectedFiles():
                shp_file_names.append(i) # Add selected shp to files list to convert

        self.shp_file_list.setText(list_to_string(shp_file_names)) # Show selected shp files

    # Convert selected kml files
    def kml_to_shp(self):
        if len(kml_file_names) == 0:
            QtWidgets.QMessageBox.critical(self, "Error", "Debe seleccionar por lo menos un archivo")
        else:
            for i in kml_file_names:
                try:
                    kmz_converter(i)
                except:
                    QtWidgets.QMessageBox.critical(self, "Error", "Ocurrió un error durante la conversión.\n" + "El archivo: " + i + "\nPosiblemente esté corrupto o dañado")
                else:
                    QtWidgets.QMessageBox.about(self, "Listo", "Conversión exitosa")

    # Convert selected shp files
    def shp_to_kml(self):
        if len(shp_file_names) == 0:
            QtWidgets.QMessageBox.critical(self, "Error", "Debe seleccionar por lo menos un archivo")
        else:
            for i in range(len(shp_file_names)):
                try:
                    shp2kml_(shp_file_names[i])
                except:
                    QtWidgets.QMessageBox.critical(self, "Error", "Ocurrió un error durante la conversión.\n" + "El archivo: " + shp_file_names[i] + "\nPosiblemente esté corrupto o dañado")
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
