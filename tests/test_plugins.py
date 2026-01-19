"""Unit tests for the plugin system."""

import pytest
from healthdcat_converter import PluginBase, PluginLoader


def test_plugin_auto_registration():
    """Test that plugins are automatically registered."""
    loader = PluginLoader()
    plugins = loader.load_plugins()

    # Check that our core plugins are registered
    assert "csv_reader" in plugins
    assert "rdf_generator" in plugins
    assert "validator" in plugins
    assert "custom_transform" in plugins


def test_get_plugin():
    """Test retrieving a specific plugin."""
    loader = PluginLoader()
    loader.load_plugins()

    csv_reader_class = loader.get_plugin("csv_reader")
    assert csv_reader_class is not None
    assert issubclass(csv_reader_class, PluginBase)


def test_custom_plugin_name():
    """Test that plugins can have custom names."""
    loader = PluginLoader()
    loader.load_plugins()

    # CSVReaderPlugin should be registered as 'csv_reader'
    plugin = loader.get_plugin("csv_reader")
    assert plugin.get_name() == "csv_reader"


def test_plugin_execution():
    """Test basic plugin execution."""
    loader = PluginLoader()
    loader.load_plugins()

    # Test the custom transform plugin
    transform_plugin_class = loader.get_plugin("custom_transform")
    transform_plugin = transform_plugin_class()

    test_data = [{"name": "test", "value": 123}]
    result = transform_plugin.execute(test_data)

    assert len(result) == 1
    assert result[0]["_transformed"] is True
    assert result[0]["_plugin"] == "custom_transform"


def test_plugin_not_found():
    """Test that getting a non-existent plugin raises an error."""
    loader = PluginLoader()
    loader.load_plugins()

    with pytest.raises(KeyError):
        loader.get_plugin("non_existent_plugin")


def test_list_all_plugins():
    """Test listing all available plugins."""
    loader = PluginLoader()
    plugins = loader.load_plugins()

    assert isinstance(plugins, list)
    assert len(plugins) >= 4  # At least our 4 default plugins
