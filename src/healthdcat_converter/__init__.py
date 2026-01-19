"""
healthdcat_converter - A package to convert CSV datasets to RDF format
following the HealthDCAT Application Profile.

This package uses a plugin architecture for extensibility and follows
Python best practices with all source code in the src directory.
"""

from .converter import CSVtoRDFConverter
from .plugin_base import PluginBase
from .plugin_loader import PluginLoader

__version__ = "0.1.0"
__all__ = ["CSVtoRDFConverter", "PluginBase", "PluginLoader"]
