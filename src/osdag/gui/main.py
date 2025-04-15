import sys
import os
from PyQt5 import QtWidgets
from osdag.gui.ui_plugins import Ui_MainWindow
from osdag.data.osdag_plugins.plugin_manager import PluginManager

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()

        self.ui.plugin_combo.clear()
        self.ui.plugin_combo.addItem("Select plugin")
        self.ui.plugin_combo.addItems(self.plugin_manager.plugins.keys())
        
        self.ui.activate_button.clicked.connect(self.activate_plugin)
        self.ui.plugin_combo.currentTextChanged.connect(self.update_plugin_info)
        
        self.ui.status_label.setText("Select a plugin to activate")

    def update_plugin_info(self, plugin_name: str):
        if plugin_name == "Select plugin":
            self.ui.status_label.setText("Select a plugin to activate")
            return

        plugin_info = self.plugin_manager.get_plugin_info(plugin_name)
        if plugin_info:
            info_text = (f"Name: {plugin_info.name}\n"
                        f"Version: {plugin_info.version}\n"
                        f"Author: {plugin_info.author}\n"
                        f"Description: {plugin_info.description}")
            self.ui.status_label.setText(info_text)
        else:
            self.ui.status_label.setText("Plugin information not available")

    def activate_plugin(self):
        plugin_name = self.ui.plugin_combo.currentText()
        if plugin_name == "Select plugin":
            self.ui.status_label.setText("Please select a plugin first")
            return
            
        plugin_info = self.plugin_manager.get_plugin_info(plugin_name)
        if plugin_info:
            try:
                plugin_info.module.register()
                self.ui.status_label.setText(f"Plugin '{plugin_info.name}' v{plugin_info.version} activated successfully!")
            except Exception as e:
                self.ui.status_label.setText(f"Error activating plugin: {str(e)}")
        else:
            self.ui.status_label.setText("Selected plugin not found")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
