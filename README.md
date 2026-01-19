# HealthDCAT-AP Converter

[![CI](https://github.com/atrakic/healthdcat-converter/actions/workflows/ci.yml/badge.svg)](https://github.com/atrakic/healthdcat-converter/actions/workflows/ci.yml)

> ⚠️ **Note:** This is an unofficial package and is not endorsed by or affiliated with the official HealthDCAT-AP project.

A Python package to read datasets and create metadata following the **HealthDCAT Application Profile** [HealthDCAT-AP](https://www.healthinformationportal.eu/healthdcat-ap).

## Installation

```bash
# Install from source
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
from healthdcat_converter import CSVtoRDFConverter

# Initialize converter (auto-loads all plugins)
converter = CSVtoRDFConverter("data/sample.csv")

# List available plugins
print(converter.list_available_plugins())

# Convert CSV to RDF (Turtle format)
rdf_output = converter.convert(
    format='turtle',
    dataset_uri='http://example.org/health/dataset/sample',
    validate=True
)

print(rdf_output)
```

See the [examples/](examples/) directory for more detailed usage examples.

## Plugin System

### Built-in Plugins

The package includes these auto-registered plugins:

1. **csv_reader** - Reads CSV files into Python dictionaries
2. **validator** - Validates data integrity and required fields
3. **rdf_generator** - Generates HealthDCAT-AP compliant RDF
4. **custom_transform** - Example custom transformation plugin

### Custom Plugins

Create a new file in `src/healthdcat_converter/plugins/` directory:

```python
from healthdcat_converter.plugin_base import PluginBase

class MyCustomPlugin(PluginBase):
    @classmethod
    def get_name(cls) -> str:
        return "my_custom_plugin"
    
    def execute(self, data, **kwargs):
        # Your plugin logic here
        return processed_data
```

The plugin will be **automatically discovered and registered** when the package loads!


## Development

```bash
# Run tests
pytest

# Run type checking
pyright

# Run linting
ruff check src/
```

