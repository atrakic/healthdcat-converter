"""Plugin loader that automatically discovers and loads plugins."""

import importlib
import pkgutil
from pathlib import Path
from typing import List

from .plugin_base import PluginBase


class PluginLoader:
    """
    Loader class that discovers and loads plugins from the plugins directory.

    This class automatically imports all Python modules in the plugins directory,
    which triggers the auto-registration mechanism in PluginBase.
    """

    def __init__(self, plugins_package: str = "healthdcat_converter.plugins"):
        """
        Initialize the plugin loader.

        Args:
            plugins_package: Package path to the plugins directory
        """
        self.plugins_package = plugins_package
        self._loaded = False

    def load_plugins(self) -> List[str]:
        """
        Discover and load all plugins from the plugins directory.

        Returns:
            List of loaded plugin names
        """
        if self._loaded:
            return PluginBase.list_plugins()

        try:
            # Import the plugins package
            plugins_module = importlib.import_module(self.plugins_package)

            # Get the path to the plugins directory
            if hasattr(plugins_module, "__path__"):
                plugins_path = plugins_module.__path__
            elif plugins_module.__file__ is not None:
                plugins_path = [Path(plugins_module.__file__).parent]
            else:
                return PluginBase.list_plugins()

            # Iterate through all modules in the plugins directory
            for _, module_name, is_pkg in pkgutil.iter_modules(plugins_path):
                # Skip __pycache__ and other special directories
                if module_name.startswith("_"):
                    continue

                # Import the module to trigger plugin registration
                full_module_name = f"{self.plugins_package}.{module_name}"
                importlib.import_module(full_module_name)

            self._loaded = True

        except ImportError as e:
            print(f"Warning: Could not load plugins package: {e}")

        return PluginBase.list_plugins()

    def get_plugin(self, name: str) -> type:
        """
        Get a plugin by name.

        Args:
            name: Name of the plugin

        Returns:
            Plugin class
        """
        if not self._loaded:
            self.load_plugins()
        return PluginBase.get_plugin(name)

    def get_all_plugins(self) -> dict:
        """
        Get all loaded plugins.

        Returns:
            Dictionary of plugin name to plugin class
        """
        if not self._loaded:
            self.load_plugins()
        return PluginBase.get_all_plugins()
