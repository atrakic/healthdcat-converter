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


def test_converter_integration_with_sample_csv():
    """Integration test using the sample.csv file."""
    sample_csv_path = Path(__file__).parent.parent / "data" / "sample.csv"

    # Ensure the sample file exists
    assert sample_csv_path.exists(), f"Sample CSV file not found at {sample_csv_path}"

    # Initialize converter with the sample file
    converter = CSVtoRDFConverter(str(sample_csv_path))

    # Perform conversion with the sample data
    rdf_output = converter.convert(
        format="turtle",
        dataset_uri="http://example.org/health/dataset/sample",
        validate=True,
    )

    # Verify data was loaded during conversion
    assert converter.data is not None
    assert len(converter.data) > 0

    # Verify RDF output
    assert rdf_output is not None
    assert len(rdf_output) > 0
    assert "@prefix" in rdf_output
