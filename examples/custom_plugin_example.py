"""Example showing how to create and use a custom plugin."""

from pathlib import Path
from typing import Any, Dict, List
from healthdcat_converter import CSVtoRDFConverter, PluginBase


# Define a custom plugin inline (normally this would be in the plugins/ directory)
class CustomFilterPlugin(PluginBase):
    """Example plugin that filters rows based on criteria."""

    @classmethod
    def get_name(cls) -> str:
        return "custom_filter"

    def execute(self, data: Any, **kwargs) -> List[Dict[str, Any]]:
        """
        Filter rows based on a key-value criteria.

        Args:
            data: List of dictionaries to filter
            **kwargs:
                - filter_key: Key to check
                - filter_value: Value to match

        Returns:
            Filtered list of dictionaries
        """
        if not isinstance(data, list):
            return data

        filter_key = kwargs.get("filter_key")
        filter_value = kwargs.get("filter_value")

        if not filter_key:
            return data

        filtered = [
            row
            for row in data
            if isinstance(row, dict) and row.get(filter_key) == filter_value
        ]

        print(f"Filtered {len(data)} rows down to {len(filtered)} rows")
        return filtered


def main():
    """
    Example demonstrating custom plugin creation and usage.
    """

    csv_file = Path(__file__).parent.parent / "data" / "sample.csv"

    # The custom plugin is automatically registered when the class is defined
    converter = CSVtoRDFConverter(str(csv_file))

    print("=== Custom Plugin Example ===\n")

    # List all plugins (should include our custom_filter)
    print("Available plugins:")
    for plugin_name in converter.list_available_plugins():
        marker = " (custom)" if plugin_name == "custom_filter" else ""
        print(f"  - {plugin_name}{marker}")

    print("\n=== Using Custom Filter Plugin ===\n")

    # Read CSV data
    csv_data = converter.execute_plugin("csv_reader", data=str(csv_file))
    print(f"Original data: {len(csv_data)} rows")

    # Example: Filter data (adjust filter_key and filter_value based on your CSV)
    # This is just a demonstration - you'd use actual column names from your data
    filtered_data = converter.execute_plugin(
        "custom_filter",
        data=csv_data,
        filter_key="status",  # Change to match your CSV columns
        filter_value="active",  # Change to match your desired value
    )

    if filtered_data:
        print("\nFiltered data sample (first row):")
        print(f"  {filtered_data[0]}")

    # Generate RDF from filtered data
    if filtered_data:
        rdf_output = converter.execute_plugin(
            "rdf_generator",
            data=filtered_data,
            dataset_uri="http://example.org/filtered/dataset",
        )

        print("\n=== Filtered RDF Output (sample) ===")
        print(rdf_output[:500] + "..." if len(rdf_output) > 500 else rdf_output)
    else:
        print("\nNo data matched the filter criteria")


if __name__ == "__main__":
    main()
