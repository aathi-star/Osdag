from PyQt5 import QtWidgets, QtCore, QtGui
from importlib.resources import files


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 200)
        
        # Set window title and icon
        MainWindow.setWindowTitle("Plugins")
        MainWindow.setWindowIcon(QtGui.QIcon(str(files("osdag.data.ResourceFiles.images").joinpath("Osdag.png"))))
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName("layout")

        # Add status label
        self.status_label = QtWidgets.QLabel("Select a plugin to activate")
        self.status_label.setObjectName("status_label")
        self.layout.addWidget(self.status_label)

        # Add plugin combo box
        self.plugin_combo = QtWidgets.QComboBox(self.centralwidget)
        self.plugin_combo.setObjectName("plugin_combo")
        self.plugin_combo.addItem("Select plugin")
        self.layout.addWidget(self.plugin_combo)

        # Add activate button
        self.activate_button = QtWidgets.QPushButton("Activate Plugin", self.centralwidget)
        self.activate_button.setObjectName("activate_button")
        self.layout.addWidget(self.activate_button)

        # Add spacing at the bottom
        self.layout.addStretch()
