"""Example usage script demonstrating the healthdcat_converter package."""

from pathlib import Path
from healthdcat_converter import CSVtoRDFConverter


def main():
    """
    Example demonstrating how to use the CSV to RDF converter.

    This script shows:
    1. Auto-loading of plugins
    2. Listing available plugins
    3. Converting a CSV file to RDF format
    """

    # Path to the sample CSV file
    csv_file = Path(__file__).parent.parent / "data" / "sample.csv"

    # Initialize the converter (plugins are auto-loaded)
    converter = CSVtoRDFConverter(str(csv_file))

    # List all available plugins
    #print("Available plugins:")
    #for plugin_name in converter.list_available_plugins():
    #    print(f"  - {plugin_name}")
    #print()

    # Convert CSV to RDF format
    try:
        rdf_output = converter.convert(
            format="turtle",
            dataset_uri="http://example.org/health/dataset/sample",
            validate=True,
        )

        # print("=" * 60)
        print(rdf_output)
        # print("=" * 60)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease ensure the sample CSV file exists in the data/ directory.")
    except ValueError as e:
        print(f"Validation error: {e}")


if __name__ == "__main__":
    main()
