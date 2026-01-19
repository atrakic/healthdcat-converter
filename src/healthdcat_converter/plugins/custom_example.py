"""
Example custom plugin demonstrating the plugin system.

To add a new plugin:
1. Create a new Python file in the plugins/ directory
2. Import PluginBase
3. Create a class that inherits from PluginBase
4. Implement the required execute() method
5. Optionally override get_name() for a custom plugin name

The plugin will be automatically discovered and registered when the
plugin loader runs.
"""

from typing import Any, Dict
from ..plugin_base import PluginBase


class CustomTransformPlugin(PluginBase):
    """
    Example custom plugin that transforms data.

    This demonstrates how to create your own plugin.
    """

    @classmethod
    def get_name(cls) -> str:
        """Return the plugin name."""
        return "custom_transform"

    def execute(self, data: Any, **kwargs) -> Any:
        """
        Transform the data in a custom way.

        Args:
            data: Input data to transform
            **kwargs: Additional transformation options

        Returns:
            Transformed data
        """
        # Example transformation: add a custom field to each row
        if isinstance(data, list):
            transformed = []
            for row in data:
                if isinstance(row, dict):
                    row["_transformed"] = True
                    row["_plugin"] = self.get_name()
                transformed.append(row)
            return transformed

        return data
