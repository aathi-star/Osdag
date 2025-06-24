"""
Widget for Column module in Osdag UI
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class ColumnModuleWidget(QWidget):
    """Widget for Column module in Osdag UI"""
    
    def __init__(self, plugin):
        super().__init__()
        
        # Get image path from plugin
        image_path = plugin.get_image_path("column.png")
        
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Add label
        label = QLabel("Axially Loaded")
        layout.addWidget(label)
        label.setObjectName('module_name_label')
        
        # Add radio button
        self.rdbtn = QRadioButton()
        self.rdbtn.setObjectName('Column_Design')
        self.rdbtn.setIcon(QIcon(image_path))
        
        # Set icon size based on scale factor (matching Osdag's defaults)
        scale = 0.3  # Default Osdag scale
        self.rdbtn.setIconSize(QSize(int(scale*300), int(scale*300)))
        
        layout.addWidget(self.rdbtn)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))


def create_column_module_widget(plugin):
    """
    Create a widget for the Column module
    
    Args:
        plugin: The ColumnPlugin instance
        
    Returns:
        ColumnModuleWidget: The created widget
    """
    from PyQt5.QtWidgets import QWidget
    
    # Create and return the widget
    return ColumnModuleWidget(plugin)
