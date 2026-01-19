"""Main converter class for CSV to RDF conversion using the plugin system."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from .plugin_loader import PluginLoader
from .plugin_base import PluginBase


class CSVtoRDFConverter:
    """
    Main converter class that uses plugins to convert CSV datasets to RDF format
    following the HealthDCAT Application Profile.
    """

    def __init__(self, csv_file: str, auto_load_plugins: bool = True):
        """
        Initialize the converter.

        Args:
            csv_file: Path to the CSV file to convert
            auto_load_plugins: Automatically load all plugins (default: True)
        """
        self.csv_file = Path(csv_file)
        self.plugin_loader = PluginLoader()
        self.data: Optional[List[Dict[str, Any]]] = None

        if auto_load_plugins:
            self.plugin_loader.load_plugins()

    def convert(self, **kwargs) -> str:
        """
        Convert CSV file to RDF format using the plugin pipeline.

        Args:
            **kwargs: Additional options:
                - format: RDF serialization format (default: 'turtle')
                - dataset_uri: Base URI for the dataset
                - validate: Run validation before conversion (default: True)
                - required_fields: List of required fields for validation

        Returns:
            RDF data as a string

        Raises:
            ValueError: If validation fails
            FileNotFoundError: If CSV file doesn't exist
        """
        validate = kwargs.get("validate", True)

        # Step 1: Read CSV file using the CSV reader plugin
        csv_reader = self.plugin_loader.get_plugin("csv_reader")()
        self.data = csv_reader.execute(self.csv_file)

        # Step 2: Validate data if requested
        if validate:
            validator = self.plugin_loader.get_plugin("validator")()
            validation_result = validator.execute(
                self.data,
                required_fields=kwargs.get("required_fields", []),
                allow_empty=kwargs.get("allow_empty", True),
            )

            if not validation_result["valid"]:
                error_msg = "Validation failed:\n" + "\n".join(
                    validation_result["errors"]
                )
                raise ValueError(error_msg)

            # Log warnings if any
            if validation_result["warnings"]:
                print("Validation warnings:")
                for warning in validation_result["warnings"]:
                    print(f"  - {warning}")

        # Step 3: Generate RDF using the RDF generator plugin
        rdf_generator = self.plugin_loader.get_plugin("rdf_generator")()
        rdf_output = rdf_generator.execute(
            self.data,
            format=kwargs.get("format", "turtle"),
            dataset_uri=kwargs.get(
                "dataset_uri", f"http://example.org/dataset/{self.csv_file.stem}"
            ),
        )

        return rdf_output

    def list_available_plugins(self) -> List[str]:
        """
        List all available plugins.

        Returns:
            List of plugin names
        """
        return self.plugin_loader.load_plugins()

    def get_plugin(self, name: str) -> type:
        """
        Get a specific plugin by name.

        Args:
            name: Name of the plugin

        Returns:
            Plugin class
        """
        return self.plugin_loader.get_plugin(name)

    def execute_plugin(self, plugin_name: str, data: Any = None, **kwargs) -> Any:
        """
        Execute a specific plugin with custom data.

        Args:
            plugin_name: Name of the plugin to execute
            data: Data to pass to the plugin (default: uses loaded CSV data)
            **kwargs: Additional arguments for the plugin

        Returns:
            Plugin execution result
        """
        plugin = self.get_plugin(plugin_name)()
        input_data = data if data is not None else self.data
        return plugin.execute(input_data, **kwargs)
