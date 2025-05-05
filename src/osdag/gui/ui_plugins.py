from PyQt5 import QtWidgets, QtCore, QtGui
from importlib.resources import files

class Ui_PluginsDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        
        # Create main layout
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        
        # Add status label at the top
        self.status_label = QtWidgets.QLabel("Select plugins to activate")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.status_label)
        
        # Create scroll area to prevent layout jumping
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        
        # Create content widget for scroll area
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 780, 580))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        # Create grid layout for plugins
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSpacing(10)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        
        # Add scroll area to layout
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        
        # Add activate button at the bottom
        self.activate_button = QtWidgets.QPushButton("Activate Selected Plugin(s)", Dialog)
        self.activate_button.setObjectName("activate_button")
        self.verticalLayout.addWidget(self.activate_button)
        
        # Set window icon and title
        Dialog.setWindowIcon(QtGui.QIcon(str(files("osdag.data.ResourceFiles.images").joinpath("Osdag.png"))))
        Dialog.setWindowTitle("Osdag Plugin Manager")
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def addPlugin(self, plugin_name, plugin_metadata):
        row = self.gridLayout.rowCount()
        
        # Create checkbox
        checkbox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        checkbox.setObjectName(f"checkbox_{plugin_name}")
        checkbox.setText(plugin_name)
        checkbox.setMinimumSize(200, 40)
        
        # Create metadata label
        metadata_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        metadata_label.setObjectName(f"metadata_{plugin_name}")
        metadata_label.setText(plugin_metadata)
        metadata_label.setWordWrap(True)
        metadata_label.setMaximumWidth(500)
        metadata_label.setMinimumHeight(50)
        metadata_label.setMinimumWidth(300)
        
        # Add to grid layout
        self.gridLayout.addWidget(checkbox, row, 0)
        self.gridLayout.addWidget(metadata_label, row, 1)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_PluginsDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())