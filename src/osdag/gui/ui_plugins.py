from PyQt5 import QtWidgets, QtCore, QtGui
from importlib.resources import files

class Ui_PluginsDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 500)  
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)  
        self.verticalLayout.setSpacing(2)  
        
        self.status_label = QtWidgets.QLabel("Select plugins to manage")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.status_label.setFont(font)
        self.verticalLayout.addWidget(self.status_label)
        
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        self.contentLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.contentLayout.setContentsMargins(5, 0, 5, 0)  
        self.contentLayout.setSpacing(0)  
        
        
        header_widget = QtWidgets.QWidget()
        header_widget.setFixedHeight(25)  
        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)  
        
        header_font = QtGui.QFont()
        header_font.setBold(True)
        
        plugin_header = QtWidgets.QLabel("Plugin Name")
        plugin_header.setFont(header_font)
        plugin_header.setFixedWidth(150)
        plugin_header.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        
        details_header = QtWidgets.QLabel("Plugin Details")
        details_header.setFont(header_font)
        details_header.setFixedWidth(350)
        details_header.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        
        actions_header = QtWidgets.QLabel("Actions")
        actions_header.setFont(header_font)
        actions_header.setFixedWidth(100)
        actions_header.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        
        header_layout.addWidget(plugin_header)
        header_layout.addWidget(details_header)
        header_layout.addWidget(actions_header)
        
        self.contentLayout.addWidget(header_widget)
        
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setMaximumHeight(1)  
        line.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.addWidget(line)
        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        
        try:
            Dialog.setWindowIcon(QtGui.QIcon(str(files("osdag.data.ResourceFiles.images").joinpath("Osdag.png"))))
        except Exception:
            pass
        Dialog.setWindowTitle("Osdag Plugin Manager")
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def addPlugin(self, plugin_name, plugin_metadata):
        plugin_widget = QtWidgets.QWidget()
        plugin_widget.setFixedHeight(55)  
        
        row_layout = QtWidgets.QHBoxLayout(plugin_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(0)  
        
        
        name_label = QtWidgets.QLabel(plugin_name)
        name_label.setObjectName(f"name_{plugin_name}")
        name_label.setFixedWidth(150)
        name_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        name_label.setFont(font)
        
        metadata_label = QtWidgets.QLabel(plugin_metadata)
        metadata_label.setObjectName(f"metadata_{plugin_name}")
        metadata_label.setWordWrap(True)
        metadata_label.setFixedWidth(350)
        metadata_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        
        buttons_widget = QtWidgets.QWidget()
        buttons_layout = QtWidgets.QVBoxLayout(buttons_widget)
        buttons_layout.setSpacing(2)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_widget.setFixedWidth(100)
        
        activate_button = QtWidgets.QPushButton("Activate")
        activate_button.setObjectName(f"activate_{plugin_name}")
        activate_button.setFixedSize(90, 25)  # Wider button
        
        deactivate_button = QtWidgets.QPushButton("Deactivate")
        deactivate_button.setObjectName(f"deactivate_{plugin_name}")
        deactivate_button.setFixedSize(90, 25)  # Wider button
        
        buttons_layout.addWidget(activate_button)
        buttons_layout.addWidget(deactivate_button)
        
        row_layout.addWidget(name_label)
        row_layout.addWidget(metadata_label)
        row_layout.addWidget(buttons_widget)
        
        self.contentLayout.addWidget(plugin_widget)
        
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setMaximumHeight(1)  
        line.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.addWidget(line)
        
        return activate_button, deactivate_button

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_PluginsDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
