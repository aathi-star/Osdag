from PyQt5 import QtWidgets, QtCore, QtGui
from importlib.resources import files


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)  
        MainWindow.setWindowTitle("Plugins")
        MainWindow.setWindowIcon(QtGui.QIcon(str(files("osdag.data.ResourceFiles.images").joinpath("Osdag.png"))))
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        #Main layout
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName("layout")

        #status label
        self.status_label = QtWidgets.QLabel("Select plugins to activate")
        self.status_label.setObjectName("status_label")
        self.layout.addWidget(self.status_label)

        #plugin list 
        self.plugin_list = QtWidgets.QListWidget(self.centralwidget)
        self.plugin_list.setObjectName("plugin_list")
        self.plugin_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.layout.addWidget(self.plugin_list)

        #activate button
        self.activate_button = QtWidgets.QPushButton("Activate Selected Plugins", self.centralwidget)
        self.activate_button.setObjectName("activate_button")
        self.layout.addWidget(self.activate_button)

        #spacing
        self.layout.addStretch()
