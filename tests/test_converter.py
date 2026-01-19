"""Unit tests for the CSV to RDF converter."""

import pytest
from pathlib import Path
from healthdcat_converter import CSVtoRDFConverter


def test_converter_initialization():
    """Test that the converter initializes correctly."""
    # Use a dummy path for testing
    converter = CSVtoRDFConverter("dummy.csv", auto_load_plugins=False)

    assert converter.csv_file == Path("dummy.csv")
    assert converter.data is None


def test_converter_lists_plugins():
    """Test that the converter can list available plugins."""
    converter = CSVtoRDFConverter("dummy.csv")
    plugins = converter.list_available_plugins()

    assert "csv_reader" in plugins
    assert "rdf_generator" in plugins
    assert "validator" in plugins


def test_converter_get_plugin():
    """Test that the converter can retrieve plugins."""
    converter = CSVtoRDFConverter("dummy.csv")

    csv_reader_class = converter.get_plugin("csv_reader")
    assert csv_reader_class is not None


def test_converter_with_missing_file():
    """Test that conversion fails gracefully with missing file."""
    converter = CSVtoRDFConverter("non_existent.csv")

    with pytest.raises(FileNotFoundError):
        converter.convert()


# Integration test would require an actual CSV file
# This is just a structure - you can expand with real test data
