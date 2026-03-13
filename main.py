# coding: utf-8

import sys
import qdarkstyle
import os
from qtpy.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, QFileDialog
from qtpy.QtGui import QPixmap, QIcon

from qdarkstyle.dark.palette import DarkPalette
from qdarkstyle.light.palette import LightPalette

from library.functions import *
from ui.ui_mainwindow import Ui_MainWindow

appname = "KmlShpConvert"

about = appname + " versión 4.0\n\nEste programa convierte archivos con formato KML a SHAPEFILE y viceversa"

authors = ["Luis Acevedo", "<laar@pm.me>"]

credits_ = ["https://github.com/ManishSahu53", "https://github.com/tomtl"]

license_ = "Copyright 2020. All code is copyrighted by the respective authors.\n" + appname + " can be redistributed and/or modified under the terms of the GNU GPL versions 3 or by any future license endorsed by " + authors[0] + ".\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."

third_party = "App logo - Icons by Orion Icon Library - https://orioniconlibrary.com"

# Resources path
tmp_path1 = "ui/resources/img/"
tmp_path2 = "KmlShpConvert.AppDir/usr/bin/ui/resources/img/"
path = tmp_path1 if os.path.exists(tmp_path1) else tmp_path2

kml_file_names = list()
shp_file_names = list()
completed = 0

def show_version_info():
    version_text = (
        f"Python Version: {sys.version}\n"
        f"QtPy Version: {qtpy.__version__}\n"
        f"Qt Binding: {qtpy.API_NAME}\n"
        f"Qt Binding Version: {qtpy.QtCore.__version__}"
    )
    QMessageBox.information(None, "Version Info", version_text)

def handle_fontconfig_error():
    try:
        import fontTools.ttLib
    except Exception as e:
        QMessageBox.warning(None, "Fontconfig Error", f"Fontconfig error: {e}")

def safe_field_name(field_name):
    try:
        return field_name.encode('ISO-8859-1').decode('ISO-8859-1')
    except UnicodeEncodeError:
        return field_name.encode('utf-8').decode('utf-8')

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def select_multiple_files(dialog):
    dialog.setFileMode(QFileDialog.ExistingFiles)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.progressBar.setValue(0)

        pixmap = QPixmap(resource_path("ui/resources/img/gdalicon.png"))
        self.label_gdal2.setPixmap(pixmap)

        pixmap = QIcon(resource_path("ui/resources/img/Start-Menu-Search-icon.png"))
        self.btn_search.setIcon(pixmap)
        self.btn_search.clicked.connect(self.search)

        pixmap = QIcon(resource_path("ui/resources/img/Accept-icon.png"))
        self.btn_accept.setIcon(pixmap)
        self.btn_accept.clicked.connect(self.conversion)

        pixmap = QIcon(resource_path("ui/resources/img/Actions-edit-clear-locationbar-rtl-icon.png"))
        self.btn_clear.setIcon(pixmap)
        self.btn_clear.clicked.connect(self.clear)

        self.actionAbout.triggered.connect(self.about_)
        self.actionAbout_Qt.triggered.connect(self.aboutQt)
        self.actionAuthors.triggered.connect(self.authors_)
        self.actionLicense.triggered.connect(self.license_)
        self.actionthird_party.triggered.connect(self.third_party_)

        version_action = QAction("Version Info", self)
        version_action.triggered.connect(show_version_info)
        self.menuHelp.addAction(version_action)

        self.btn_change_theme.setStyleSheet(
            "QPushButton { background-color: purple; }"
            "QPushButton::hover { background-color: grey; }"
        )
        self.btn_change_theme.setCheckable(True)
        self.btn_change_theme.clicked.connect(self.toggle_theme)

        self.btn_exit.clicked.connect(self.exit)

    def search(self):
        aux = []

        dialog = QFileDialog(self)
        select_multiple_files(dialog)

        currentTabName = self.tabWidget.currentWidget().objectName()
        if currentTabName == "tab_kml2shp":
            dialog.setNameFilter("File (*.kml *.kmz)")
            global kml_file_names
            aux = kml_file_names
        else:
            dialog.setNameFilter("File (*.shp)")
            global shp_file_names
            aux = shp_file_names

        dialog.setViewMode(QFileDialog.Detail)

        if dialog.exec():
            for file in dialog.selectedFiles():
                aux.append(file)

        if currentTabName == "tab_kml2shp":
            self.kml_file_list.setText(list_to_string(aux))
        else:
            self.shp_file_list.setText(list_to_string(aux))

    def conversion(self):
        tmp = QFileDialog.getSaveFileName(self, "Save File", "SELECCIONE LA CARPETA DE DESTINO")
        tmp = tmp[0].split("/")

        if len(tmp) > 1:
            save_path = "/"
            for i in tmp[1:-1]:
                save_path += i + "/"

            aux = []

            global completed
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
                QMessageBox.critical(self, "Error", "Debe seleccionar por lo menos un archivo")
            else:
                self.label_status.setText("Convirtiendo...")
                button_reply = QMessageBox.question(self, "Confirmar", "Proceder")
                if button_reply == QMessageBox.Yes:
                    self.progressBar.setValue(5)
                    for i in range(len(aux)):
                        try:
                            tmp = aux[i].split("/")
                            output_name = save_path + tmp[-1]

                            convert_function(aux[i], output_name, i)

                            completed = self.update_progress_bar(len(aux), completed)
                        except Exception as e:
                            QMessageBox.critical(self, "Error", f"Ocurrió un error durante la conversión.\nEl archivo: {aux[i]}\nError: {str(e)}")
                    self.label_status.setText("Ready")
                    QMessageBox.about(self, "Listo", "Conversión exitosa")
                else:
                    self.label_status.setText("Ready")

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
        QMessageBox.about(self, "Acerca de", about)

    def aboutQt(self):
        QMessageBox.aboutQt(self)

    def authors_(self):
        text = "Autores:\n" + authors[0] + " " + authors[1] + "\n\n" + "Créditos:\n" + credits_[0] + "\n" + credits_[1]
        QMessageBox.about(self, "Autores", text)

    def license_(self):
        QMessageBox.about(self, "Licencia", license_)

    def third_party_(self):
        QMessageBox.about(self, "Third party", third_party)

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