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

        # Load plugins into the grid layout
        self.load_plugins()

        # Connect signals
        self.ui.activate_button.clicked.connect(self.activate_plugins)

    def load_plugins(self):
        plugins = self.plugin_manager.plugins
        if not plugins:
            self.ui.status_label.setText("No plugins found. Please check the plugins directory.")
            return

        self.ui.status_label.setText("Select plugins to activate")
        for plugin_name, plugin_info in plugins.items():
            metadata = f"Version: {plugin_info.version}\nDescription: {plugin_info.description}"
            self.ui.addPlugin(plugin_name, metadata)

    def activate_plugins(self):
        selected_plugins = []
        # Get all items in the grid layout
        for row in range(self.ui.gridLayout.rowCount()):
            # Get the checkbox from column 0
            checkbox_item = self.ui.gridLayout.itemAtPosition(row, 0)
            if checkbox_item:
                checkbox = checkbox_item.widget()
                if isinstance(checkbox, QtWidgets.QCheckBox) and checkbox.isChecked():
                    selected_plugins.append(checkbox.text())

        if not selected_plugins:
            self.ui.status_label.setText("Please select at least one plugin first")
            return
            
        activation_results = []
        for plugin_name in selected_plugins:
            plugin_info = self.plugin_manager.plugins.get(plugin_name)
            if plugin_info and hasattr(plugin_info.module, 'register'):
                try:
                    plugin_info.module.register()
                    activation_results.append(f"Plugin '{plugin_info.name}' v{plugin_info.version} activated successfully!")
                except Exception as e:
                    activation_results.append(f"Error activating {plugin_info.name}: {str(e)}")
        
        self.ui.status_label.setText("\n".join(activation_results))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())