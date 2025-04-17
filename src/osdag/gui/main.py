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

        print("Initializing plugin manager...")
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()

        #list with plugins
        self.ui.plugin_list.clear()
        plugins = list(self.plugin_manager.plugins.keys())
        print(f"Found {len(plugins)} plugins: {plugins}")
        
        for plugin_name in plugins:
            print(f"Adding plugin to list: {plugin_name}")
            item = QtWidgets.QListWidgetItem(plugin_name)
            self.ui.plugin_list.addItem(item)
        
        if not plugins:
            self.ui.status_label.setText("No plugins found. Please check the plugins directory.")
        else:
            self.ui.status_label.setText("Select plugins to activate")
        
        self.ui.activate_button.clicked.connect(self.activate_plugins)
        self.ui.plugin_list.itemSelectionChanged.connect(self.update_plugin_info)

    def update_plugin_info(self):
        selected_items = self.ui.plugin_list.selectedItems()
        if not selected_items:
            self.ui.status_label.setText("Select plugins to activate")
            return

        info_text = "Selected plugins:\n"
        for item in selected_items:
            plugin_name = item.text()
            plugin_info = self.plugin_manager.get_plugin_info(plugin_name)
            if plugin_info:
                info_text += f"\n{plugin_info.name} v{plugin_info.version}\n"
                info_text += f"Author: {plugin_info.author}\n"
                info_text += f"Description: {plugin_info.description}\n"
        
        self.ui.status_label.setText(info_text)

    def activate_plugins(self):
        selected_items = self.ui.plugin_list.selectedItems()
        if not selected_items:
            self.ui.status_label.setText("Please select at least one plugin first")
            return
            
        activation_results = []
        for item in selected_items:
            plugin_name = item.text()
            plugin_info = self.plugin_manager.get_plugin_info(plugin_name)
            if plugin_info:
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
    
