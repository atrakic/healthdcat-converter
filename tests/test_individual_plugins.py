"""Unit tests for individual plugins."""

import pytest
from healthdcat_converter.plugins.validator import ValidatorPlugin
from healthdcat_converter.plugins.rdf_generator import RDFGeneratorPlugin


def test_validator_with_valid_data():
    """Test validator with valid data."""
    validator = ValidatorPlugin()

    data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]

    result = validator.execute(data, required_fields=["name"])

    assert result["valid"] is True
    assert len(result["errors"]) == 0


def test_validator_with_missing_field():
    """Test validator detects missing required fields."""
    validator = ValidatorPlugin()

    data = [
        {"name": "Alice"},
        {"age": 25},  # Missing 'name'
    ]

    result = validator.execute(data, required_fields=["name"])

    assert result["valid"] is False
    assert len(result["errors"]) > 0


def test_validator_with_empty_data():
    """Test validator handles empty dataset."""
    validator = ValidatorPlugin()

    result = validator.execute([])

    assert result["valid"] is True
    assert len(result["warnings"]) > 0


def test_rdf_generator_basic():
    """Test RDF generator produces output."""
    generator = RDFGeneratorPlugin()

    data = [{"name": "Test", "value": "123"}]

    rdf_output = generator.execute(data, dataset_uri="http://example.org/test")

    assert "dcat:Dataset" in rdf_output
    assert "http://example.org/test" in rdf_output
    assert "@prefix" in rdf_output


def test_rdf_generator_namespaces():
    """Test that RDF generator includes proper namespaces."""
    generator = RDFGeneratorPlugin()

    rdf_output = generator.execute([], dataset_uri="http://example.org/test")

    # Check for HealthDCAT-AP namespace
    assert "healthdcat:" in rdf_output
    assert "dcat:" in rdf_output
    assert "dct:" in rdf_output
