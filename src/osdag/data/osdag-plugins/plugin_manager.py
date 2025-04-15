import os
import importlib.util
import sys
from typing import Dict, Any
from importlib.metadata import entry_points
from dataclasses import dataclass

@dataclass
class PluginInfo:
    #storing plugin metadata
    name: str
    version: str
    description: str
    author: str
    module: Any

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, PluginInfo] = {}

    def load_plugins(self):
        print("Starting plugin loading process...")
        self._load_from_entry_points()
        
        if not self.plugins:
            print("No plugins found from entry points, trying local directory...")
            self._load_from_directory()
        
        
        if self.plugins:
            print("Loaded plugins:")
            for name, info in self.plugins.items():
                print(f"- {name} (v{info.version})")
        else:
            print("No plugins were loaded.")

    def _load_from_entry_points(self):
        try:
            print("Searching for entry points in group 'osdag.plugins'...")
            discovered_plugins = entry_points(group='osdag.plugins')
            
            # Convert to list to see if we found any
            plugin_list = list(discovered_plugins)
            print(f"Found {len(plugin_list)} entry points")
            
            for plugin_entry in plugin_list:
                print(f"Attempting to load plugin from entry point: {plugin_entry.name}")
                try:
                    self._load_plugin_from_entry(plugin_entry)
                except Exception as e:
                    print(f"Error loading plugin {plugin_entry.name}: {str(e)}")
        except Exception as e:
            print(f"Error discovering plugins via entry points: {str(e)}")

    def _load_from_directory(self):
        plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
        print(f"Searching for plugins in directory: {plugin_dir}")
        
        if not os.path.exists(plugin_dir):
            print(f"Plugin directory not found: {plugin_dir}")
            return

        # Files to ignore
        ignore_files = {'__init__.py', 'setup.py', 'README.md'}
        
        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py') and filename not in ignore_files:
                print(f"Found potential plugin file: {filename}")
                try:
                    self._load_plugin_from_file(filename, plugin_dir)
                except Exception as e:
                    print(f"Error loading plugin {filename}: {str(e)}")

    def _load_plugin_from_entry(self, plugin_entry):
        plugin_class = plugin_entry.load()
        print(f"Loaded class {plugin_class.__name__} from entry point")
        plugin_instance = plugin_class()
        
        if hasattr(plugin_instance, 'register'):
            plugin_info = PluginInfo(
                name=getattr(plugin_instance, 'name', plugin_entry.name),
                version=getattr(plugin_instance, 'version', '0.1.0'),
                description=getattr(plugin_instance, 'description', ''),
                author=getattr(plugin_instance, 'author', 'Unknown'),
                module=plugin_instance
            )
            self.plugins[plugin_entry.name] = plugin_info
            print(f"Successfully loaded plugin from entry point: {plugin_entry.name} v{plugin_info.version}")
        else:
            print(f"Plugin {plugin_entry.name} does not have register() function.")

    def _load_plugin_from_file(self, filename: str, plugin_dir: str):
        plugin_name = os.path.splitext(filename)[0]
        plugin_path = os.path.join(plugin_dir, filename)
        print(f"Attempting to load plugin from file: {plugin_path}")
        
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[plugin_name] = module
                spec.loader.exec_module(module)
                
                # Look for any class that has a register method
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and hasattr(attr, 'register'):
                        print(f"Found plugin class: {attr_name}")
                        try:
                            plugin_instance = attr()
                            plugin_info = PluginInfo(
                                name=getattr(plugin_instance, 'name', plugin_name),
                                version=getattr(plugin_instance, 'version', '0.1.0'),
                                description=getattr(plugin_instance, 'description', ''),
                                author=getattr(plugin_instance, 'author', 'Unknown'),
                                module=plugin_instance
                            )
                            self.plugins[plugin_name] = plugin_info
                            print(f"Successfully loaded plugin from file: {plugin_name} v{plugin_info.version}")
                            return
                        except Exception as e:
                            print(f"Error instantiating plugin class {attr_name}: {str(e)}")
                            continue
                            
                print(f"No valid plugin class found in {filename}")
            else:
                print(f"Could not load specification for plugin: {plugin_name}")
        except Exception as e:
            print(f"Error loading plugin file {filename}: {str(e)}")
            raise

    def get_plugin_info(self, plugin_name: str) -> PluginInfo:
        return self.plugins.get(plugin_name) #to get info on plugin
