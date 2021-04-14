# coding: utf-8

import sys

from PySide2.QtWidgets import QApplication, QDialog
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap

import qdarkstyle
from qdarkstyle.dark.palette import DarkPalette
from qdarkstyle.light.palette import LightPalette

from functions.functions import *

appname  = "KmlShpConvert"
authors  = ["Luis Acevedo", "<laar@protonmail.com>", "Rosaura Rojas", "<rrojas@abae.gob.ve>"]
credits_ = ["https://github.com/ManishSahu53", "https://github.com/tomtl"]
license_ = "Copyright 2020. All code is copyrighted by the respective authors.\n" + appname + " can be redistributed and/or modified under the terms of the GNU GPL versions 3 or by any future license_ endorsed by " + authors[0] + " and " + authors[2] + "." + "\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."

# Spcify user interface location
if (len(sys.argv) < 2):
    ui_file = "ui/window.ui"        # Default
elif (len(sys.argv) == 2):
    ui_file = sys.argv[1]           # Custom, in order to make and exeutable with pyinstaller
else:
    print("Argumento/s inválido/s") # Any other option, error
    sys.exit()

kml_file_names = list() # File list to convert from kml to shp
shp_file_names = list() # File list to convert from shp to kml
completed = 0           # Used in progress bar

class MyApp(QDialog):
    def __init__(self, ui_file):
        super().__init__()
        self.ui_file = QFile(ui_file)
        self.ui_file.open(QFile.ReadOnly)

        self.loader = QUiLoader()
        self.window = self.loader.load(self.ui_file)
        self.window.show()

        self.tab = self.window.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.kml_file_list = self.window.findChild(QtWidgets.QTextBrowser, "kml_file_list") # Show file list to convert, from kml to shp, tab 1
        self.shp_file_list = self.window.findChild(QtWidgets.QTextBrowser, "shp_file_list") # Show file list to convert, from shp to kml, tab 2

        self.progress = self.window.findChild(QtWidgets.QProgressBar, "progressBar")        # Progress bar
        print(self.progress)
        self.progress.setValue(0)

        self.label_status = self.window.findChild(QtWidgets.QLabel, "label_status")

        self.label_gdal = self.window.findChild(QtWidgets.QLabel, "label_4")
        pixmap = QPixmap("ui/img/gdalicon.png")
        self.label_gdal.setPixmap(pixmap)
        
        
        self.btn_search = self.window.findChild(QtWidgets.QPushButton, "btn_search")        # Search files button
        pixmap = QPixmap("ui/icons/Start-Menu-Search-icon.png")
        self.btn_search.setIcon(pixmap)
        self.btn_search.clicked.connect(self.search)

        self.btn_accept = self.window.findChild(QtWidgets.QPushButton, "btn_accept")        # Convert from kml to shp button
        pixmap = QPixmap("ui/icons/Accept-icon.png")
        self.btn_accept.setIcon(pixmap)
        self.btn_accept.clicked.connect(self.conversion)

        self.btn_clear = self.window.findChild(QtWidgets.QPushButton, "btn_clear")          # Clear file list button
        pixmap = QPixmap("ui/icons/Actions-edit-clear-locationbar-rtl-icon.png")
        self.btn_clear.setIcon(pixmap)
        self.btn_clear.clicked.connect(self.clear)

        self.btn_about = self.window.findChild(QtWidgets.QPushButton, "btn_about")       # About Qt
        self.btn_about.clicked.connect(self.aboutQt)

        self.btn_authors = self.window.findChild(QtWidgets.QPushButton, "btn_authors")   # Authors
        self.btn_authors.clicked.connect(self.authors)

        self.btn_license = self.window.findChild(QtWidgets.QPushButton, "btn_license")   # License
        self.btn_license.clicked.connect(self.license_)

        self.btn_change_theme = self.window.findChild(QtWidgets.QPushButton, "btn_change_theme") # License
        self.btn_change_theme.setStyleSheet("background-color: purple")
        self.btn_change_theme.setCheckable(True)
        #self.btn_change_theme.setChecked(True)
        self.btn_change_theme.clicked.connect(self.toggle_theme)

        self.btn_exit = self.window.findChild(QtWidgets.QPushButton, "btn_exit") # Exit
        self.btn_exit.clicked.connect(self.exit)

    # Search kml files in file system
    def search(self):
        aux = list()

        dialog = QtWidgets.QFileDialog(self.window)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        
        currentTabName = self.tab.currentWidget().objectName()
        if currentTabName == "tab_kml2shp":
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

        if currentTabName == "tab_kml2shp":
            self.kml_file_list.setText(list_to_string(aux)) # Show selected kml files
        else:
            self.shp_file_list.setText(list_to_string(aux)) # Show selected shp files

    # Convert selected kml files
    def conversion(self):
        aux = list()

        global completed
        completed = completed
        completed = 0

        currentTabName = self.tab.currentWidget().objectName()
        if currentTabName == "tab_kml2shp":
            convert_function = kml2shp_
            global kml_file_names
            aux = kml_file_names
        else:
            convert_function = shp2kml_
            global shp_file_names
            aux = shp_file_names

        if len(aux) == 0:
            QtWidgets.QMessageBox.critical(self.window, "Error", "Debe seleccionar por lo menos un archivo")
        else:
            self.label_status.setText("Convirtiendo...")
            button_reply = QtWidgets.QMessageBox.question(self.window, "Confirmar", "Proceder")
            if button_reply == QtWidgets.QMessageBox.Yes:
                self.progress.setValue(5)
                for i in range(len(aux)):
                    try:
                        #aux2 = '"' + aux[i] + '"' # Fix folder location with namespaces
                        aux2 = aux[i]
                        convert_function(aux2, i)
                        completed = self.update_progress_bar(len(aux), completed)
                    except:
                        QtWidgets.QMessageBox.critical(self.window, "Error", "Ocurrió un error durante la conversión.\n" + "El archivo: " + aux2 + "\nPosiblemente esté corrupto o dañado")
                self.label_status.setText("Ready")
                QtWidgets.QMessageBox.about(self.window, "Listo", "Conversión exitosa")
            else:
                self.label_status.setText("Ready")

    # Clear selected file list
    def clear(self):
        self.kml_file_list.setText("")
        self.shp_file_list.setText("")
        kml_file_names.clear()
        shp_file_names.clear()
        self.progress.setValue(0)

    def update_progress_bar(self, max_, completed):
        increment = 100 / max_

        if completed < 100:
            completed += increment
            self.progress.setValue(completed)
        
        return completed

    def aboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self.window)
    
    def authors(self):
        mensaje = "Autores:\n" + authors[0] + " " + authors[1] + "\n" + authors[2] + "  " + authors[3] + "\n\n\n" + "Cŕeditos:\n" + credits_[0] + "\n" + credits_[1]
        QtWidgets.QMessageBox.about(self.window, "Autores", mensaje)
        
    def license_(self):
        QtWidgets.QMessageBox.about(self.window, "Licencia", license_)

    def toggle_theme(self):
        if not self.btn_change_theme.isChecked():
            app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside2', palette=DarkPalette))
        else:
            app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside2', palette=LightPalette))

    def exit(self):
        sys.exit()

if __name__ == "__main__":
    
    print("\n" + appname + " Copyright (C) 2020 " + authors[0] + ", " + authors[2] + ".\nEste programa viene con ABSOLUTAMENTE NINGUNA GARANTÍA.\nEsto es software libre, y le invitamos a redistribuirlo\nbajo ciertas condiciones.\nPor favor, leer el archivo README.")

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside2', palette=DarkPalette))
    w = MyApp(ui_file)
    sys.exit(app.exec_())
