# coding: utf-8

import sys
import qdarkstyle

from PySide2.QtWidgets import QApplication, QMainWindow
#from PySide2.QtCore    import QFile
#from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui     import QPixmap

from qdarkstyle.dark.palette  import DarkPalette
from qdarkstyle.light.palette import LightPalette

from library.functions import *
from ui.ui_mainwindow  import Ui_MainWindow

appname  = "KmlShpConvert"

about    = appname + " versión 3.0\n\nEste programa convierte archivos con \
\nformato KML a SHAPEFILE y vice versa"
    
authors  = ["Luis Acevedo", "<laar@pm.me>"]

credits_ = ["https://github.com/ManishSahu53", "https://github.com/tomtl"]

license_ = "Copyright 2020. All code is copyrighted by the respective authors.\n" \
+ appname + " can be redistributed and/or modified under the terms of \
the GNU GPL versions 3 or by any future license endorsed by " + authors[0] + \
".\nThis program is distributed in the hope that it will be useful, but \
WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."
    
third_party = "App logo - Icons by Orion Icon Library - https://orioniconlibrary.com"

kml_file_names = list() # File list to convert from kml to shp
shp_file_names = list() # File list to convert from shp to kml
completed = 0           # Used in progress bar

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.progressBar.setValue(0) # Progress bar
        
        pixmap = QPixmap("ui/resources/img/gdalicon.png")
        self.label_gdal2.setPixmap(pixmap)
        
        # Search files button
        pixmap = QPixmap("ui/resources/img/Start-Menu-Search-icon.png")
        self.btn_search.setIcon(pixmap)
        self.btn_search.clicked.connect(self.search)

        # Convert from kml to shp button
        pixmap = QPixmap("ui/resources/img/Accept-icon.png")
        self.btn_accept.setIcon(pixmap)
        self.btn_accept.clicked.connect(self.conversion)

        # Clear file list button
        pixmap = QPixmap("ui/resources/img/Actions-edit-clear-locationbar-rtl-icon.png")
        self.btn_clear.setIcon(pixmap)
        self.btn_clear.clicked.connect(self.clear)

        # About
        self.actionAbout.triggered.connect(self.about_)
        
        # About Qt
        self.actionAbout_Qt.triggered.connect(self.aboutQt)
        
        # Authors
        self.actionAuthors.triggered.connect(self.authors_)
        
        # License
        self.actionLicense.triggered.connect(self.license_)

        # Third party
        self.actionthird_party.triggered.connect(self.third_party_)

        # Change theme
        self.btn_change_theme.setStyleSheet(
            "QPushButton { background-color: purple; } \
                QPushButton::hover { \
                background-color: grey; \
            }"
        )
        self.btn_change_theme.setCheckable(True)
        #self.btn_change_theme.setChecked(True)
        self.btn_change_theme.clicked.connect(self.toggle_theme)

        # Exit
        self.btn_exit.clicked.connect(self.exit)

    # Search kml files in file system
    def search(self):
        aux = list()

        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        
        currentTabName = self.tabWidget.currentWidget().objectName()
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
        tmp = QtWidgets.QFileDialog.getSaveFileName(self, ("Save F:xile"), "SELECCIONE LA CARPETA DE DESTINO",)
        tmp = tmp[0].split("/")

        if len(tmp) > 1:
            save_path = ""
            for i in tmp[1:-1]:
                save_path += i + "/"
            save_path = "/" + save_path
            
            aux = list()

            global completed
            completed = completed
            completed = 0

            currentTabName = self.tabWidget.currentWidget().objectName()
            if currentTabName == "tab_kml2shp":
                convert_function = kml2shp_
                global kml_file_names
                aux = kml_file_names
            else:
                convert_function = shp2kml_
                global shp_file_names
                aux = shp_file_names

            if len(aux) == 0:
                QtWidgets.QMessageBox.critical(self, "Error", "Debe seleccionar por lo menos un archivo")
            else:
                self.label_status.setText("Convirtiendo...")
                button_reply = QtWidgets.QMessageBox.question(self, "Confirmar", "Proceder")
                if button_reply == QtWidgets.QMessageBox.Yes:
                    self.progressBar.setValue(5)
                    for i in range(len(aux)):
                        try:
                            tmp         = aux[i].split("/")
                            output_name = save_path + tmp[-1]
                            
                            convert_function(aux[i], output_name, i)
                            
                            completed = self.update_progress_bar(len(aux), completed)
                        except:
                            QtWidgets.QMessageBox.critical(self, "Error", "Ocurrió un error durante la conversión.\n" + "El archivo: " + aux2 + "\nPosiblemente esté corrupto o dañado")
                    self.label_status.setText("Ready")
                    QtWidgets.QMessageBox.about(self, "Listo", "Conversión exitosa")
                else:
                    self.label_status.setText("Ready")

    # Clear selected file list
    def clear(self):
        self.kml_file_list.setText("")
        self.shp_file_list.setText("")
        kml_file_names.clear()
        shp_file_names.clear()
        self.progressBar.setValue(0)

    def update_progress_bar(self, max_, completed):
        increment = 100 / max_

        if completed < 100:
            completed += increment
            self.progressBar.setValue(completed)
        
        return completed
    
    def about_(self):
        QtWidgets.QMessageBox.about(self, "Acerca de", about)

    def aboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self)
        
    def authors_(self):
        text = "Autores:\n" + authors[0] + " " + authors[1] + "\n\n\n" + "Cŕeditos:\n" + credits_[0] + "\n" + credits_[1]
        QtWidgets.QMessageBox.about(self, "Autores", text)
        
    def license_(self):
        QtWidgets.QMessageBox.about(self, "Licencia", license_)

    def third_party_(self):
        QtWidgets.QMessageBox.about(self, "Third party", third_party)

    def toggle_theme(self):
        if not self.btn_change_theme.isChecked():
            app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside2", palette=DarkPalette))
        else:
            app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside2", palette=LightPalette))

    def exit(self):
        sys.exit()

if __name__ == "__main__":
    
    print("\n" + appname + " Copyright (C) 2020 " + authors[0] + ".\nEste programa viene con ABSOLUTAMENTE NINGUNA GARANTÍA.\nEsto es software libre, y le invitamos a redistribuirlo\nbajo ciertas condiciones.\nPor favor, leer el archivo README.")

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside2", palette=DarkPalette))

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
