import sys
import os
from PyQt5 import QtWidgets
from osdag.gui.ui_plugins import Ui_PluginsDialog
from osdag.data.osdag_plugins.plugin_manager import PluginManager

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PluginsDialog()
        self.ui.setupUi(self)

        print("Initializing plugin manager...")
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()

        self.load_plugins()

    def load_plugins(self):
        plugins = self.plugin_manager.plugins
        if not plugins:
            self.ui.status_label.setText("No plugins found. Please check the plugins directory.")
            return

        self.ui.status_label.setText("Plugin Manager")
        for plugin_name, plugin_info in plugins.items():
            metadata = f"Version: {plugin_info.version}\nDescription: {plugin_info.description}\nAuthor: {plugin_info.author}"
            activate_btn, deactivate_btn = self.ui.addPlugin(plugin_name, metadata)
            
            activate_btn.clicked.connect(lambda checked, name=plugin_name: self.activate_plugin(name))
            deactivate_btn.clicked.connect(lambda checked, name=plugin_name: self.deactivate_plugin(name))
    
    def activate_plugin(self, plugin_name):
        try:
            plugin_info = self.plugin_manager.get_plugin_info(plugin_name)
            if plugin_info:
                plugin_info.module.register()
                self.ui.status_label.setText(f"Plugin '{plugin_info.name}' v{plugin_info.version} activated successfully!")
            else:
                self.ui.status_label.setText(f"Plugin '{plugin_name}' not found")
        except Exception as e:
            self.ui.status_label.setText(f"Error activating {plugin_name}: {str(e)}")
    
    def deactivate_plugin(self, plugin_name):
        try:
            plugin_info = self.plugin_manager.get_plugin_info(plugin_name)
            if plugin_info:
                if hasattr(plugin_info.module, 'deactivate'):
                    plugin_info.module.deactivate()
                    self.ui.status_label.setText(f"Plugin '{plugin_info.name}' v{plugin_info.version} deactivated successfully!")
                else:
                    self.ui.status_label.setText(f"Plugin '{plugin_info.name}' does not support deactivation")
            else:
                self.ui.status_label.setText(f"Plugin '{plugin_name}' not found")
        except Exception as e:
            self.ui.status_label.setText(f"Error deactivating {plugin_name}: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
