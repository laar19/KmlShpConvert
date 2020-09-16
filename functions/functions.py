import os
import platform
operative_system = platform.system() # Identify operative system

from PyQt5 import QtWidgets

# Convert selected file list_ to string
# in order to shown in the window
def list_to_string(list_):
    string = str()
    for i in range(len(list_)):
        string += str(i+1) + " - " + list_[i] + "\n\n"
    return string

# Specify out location on file system
def out_location():
    location = str()
    
    if operative_system == "Windows":
        location = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
        #location = os.path.join(os.path.join(os.environ["HOMEPATH"]), "Desktop")
    else:
        location = os.path.join(os.path.join(os.path.expanduser("~")))

    return location

# Select multiple files
def select_multiple_files(dialog):
    file_view = dialog.findChild(QtWidgets.QListView, "ListView")
    if file_view:
        file_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
    f_tree_view = dialog.findChild(QtWidgets.QTreeView)
    if f_tree_view:
        f_tree_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

    return f_tree_view