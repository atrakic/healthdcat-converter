"""Base class for all plugins in the healthdcat_converter package."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class PluginBase(ABC):
    """
    Abstract base class for all plugins.

    All plugins must inherit from this class and implement the required methods.
    Plugins are automatically registered when they are imported.
    """

    # Class variable to store all registered plugins
    _registry: Dict[str, type] = {}

    def __init_subclass__(cls, **kwargs):
        """
        Automatically register plugin subclasses.

        This method is called when a class inherits from PluginBase,
        enabling automatic plugin registration.
        """
        super().__init_subclass__(**kwargs)
        if not cls.__name__.startswith("_"):  # Skip private/abstract classes
            cls._registry[cls.get_name()] = cls

    @classmethod
    def get_name(cls) -> str:
        """
        Get the name of the plugin.

        By default, uses the class name. Override for custom names.
        """
        return cls.__name__

    @abstractmethod
    def execute(self, data: Any, **kwargs) -> Any:
        """
        Execute the plugin's main functionality.

        Args:
            data: Input data to process
            **kwargs: Additional keyword arguments

        Returns:
            Processed data
        """
        raise NotImplementedError("Plugin must implement execute method")

    @classmethod
    def get_plugin(cls, name: str) -> type:
        """
        Get a registered plugin by name.

        Args:
            name: Name of the plugin

        Returns:
            Plugin class

        Raises:
            KeyError: If plugin is not found
        """
        return cls._registry[name]

    @classmethod
    def get_all_plugins(cls) -> Dict[str, type]:
        """
        Get all registered plugins.

        Returns:
            Dictionary of plugin name to plugin class
        """
        return cls._registry.copy()

    @classmethod
    def list_plugins(cls) -> list:
        """
        List names of all registered plugins.

        Returns:
            List of plugin names
        """
        return list(cls._registry.keys())
