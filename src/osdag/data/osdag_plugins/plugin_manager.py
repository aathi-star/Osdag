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
        
        print("Checking local directory for additional plugins...")
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
            discovered_plugins = entry_points()
            osdag_plugins = [ep for ep in discovered_plugins if ep.group == 'osdag.plugins']
            print(f"Found {len(osdag_plugins)} entry points")
            
            for plugin_entry in osdag_plugins:
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

        ignore_dirs = {'__pycache__'}
        
        for dirname in os.listdir(plugin_dir):
            if dirname in ignore_dirs:
                continue
                
            plugin_path = os.path.join(plugin_dir, dirname)
            if os.path.isdir(plugin_path):
                print(f"Found potential plugin directory: {dirname}")
                try:
                    if self._try_load_plugin_from_directory(dirname, plugin_path):
                        continue
                        
                    print(f"Trying nested directories in {dirname}")
                    for nested_dir in os.listdir(plugin_path):
                        nested_path = os.path.join(plugin_path, nested_dir)
                        if os.path.isdir(nested_path) and nested_dir not in ignore_dirs:
                            print(f"Found nested plugin directory: {nested_dir}")
                            try:
                                self._try_load_plugin_from_directory(nested_dir, nested_path)
                            except Exception as e:
                                print(f"Error loading plugin from nested directory {nested_dir}: {str(e)}")
                                
                except Exception as e:
                    print(f"Error processing directory {dirname}: {str(e)}")

    def _try_load_plugin_from_directory(self, plugin_name: str, plugin_path: str) -> bool:
        """Try to load a plugin from a directory. Returns True if successful."""
        init_path = os.path.join(plugin_path, '__init__.py')
        if not os.path.exists(init_path):
            print(f"No __init__.py found in {plugin_path}")
            return False

        try:
            print(f"Attempting to load plugin from: {plugin_path}")
            spec = importlib.util.spec_from_file_location(plugin_name, init_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[plugin_name] = module
                spec.loader.exec_module(module)
                
                plugin_class = None
                if hasattr(module, 'plugin_class'):
                    plugin_class = getattr(module, 'plugin_class')
                else:
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and hasattr(attr, 'register'):
                            plugin_class = attr
                            break
                
                if plugin_class:
                    plugin_instance = plugin_class()
                    if hasattr(plugin_instance, 'register'):
                        plugin_info = PluginInfo(
                            name=getattr(plugin_instance, 'name', plugin_name),
                            version=getattr(plugin_instance, 'version', '0.1.0'),
                            description=getattr(plugin_instance, 'description', ''),
                            author=getattr(plugin_instance, 'author', 'Unknown'),
                            module=plugin_instance
                        )
                        self.plugins[plugin_name] = plugin_info
                        print(f"Successfully loaded plugin: {plugin_name} v{plugin_info.version}")
                        return True
                    else:
                        print(f"Plugin class in {plugin_name} does not have register() method")
                else:
                    print(f"No valid plugin class found in {plugin_name}")
            else:
                print(f"Could not load specification for plugin: {plugin_name}")
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {str(e)}")
            print(f"Full plugin path: {plugin_path}")
        return False

    def _load_plugin_from_entry(self, plugin_entry):
        try:
            print(f"Loading entry point: {plugin_entry.name} = {plugin_entry.value}")
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
        except Exception as e:
            print(f"Error loading entry point {plugin_entry.name}: {str(e)}")
            raise

    def get_plugin_info(self, plugin_name: str) -> PluginInfo:
        return self.plugins.get(plugin_name)
