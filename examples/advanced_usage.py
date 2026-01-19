"""Advanced example showing custom plugin usage and pipeline customization."""

from pathlib import Path
from healthdcat_converter import CSVtoRDFConverter, PluginBase


def main():
    """
    Advanced example demonstrating:
    1. Accessing individual plugins
    2. Custom plugin execution
    3. Multi-step data processing pipeline
    """

    csv_file = Path(__file__).parent.parent / "data" / "sample.csv"

    # Initialize converter
    converter = CSVtoRDFConverter(str(csv_file))

    print("=== Advanced Plugin Usage ===\n")

    # Step 1: Read CSV data manually
    print("Step 1: Reading CSV data...")
    csv_data = converter.execute_plugin("csv_reader", data=str(csv_file))
    print(f"  Loaded {len(csv_data)} rows")

    # Step 2: Apply custom transformation
    print("\nStep 2: Applying custom transformation...")
    transformed_data = converter.execute_plugin("custom_transform", data=csv_data)
    print(f"  Transformed {len(transformed_data)} rows")
    if transformed_data and "_transformed" in transformed_data[0]:
        print(f"  Transform marker added: {transformed_data[0].get('_plugin')}")

    # Step 3: Validate transformed data
    print("\nStep 3: Validating data...")
    validation_result = converter.execute_plugin(
        "validator", data=transformed_data, required_fields=["_transformed"]
    )
    print(f"  Valid: {validation_result['valid']}")
    if validation_result["errors"]:
        print(f"  Errors: {validation_result['errors']}")
    if validation_result["warnings"]:
        print(f"  Warnings: {validation_result['warnings']}")

    # Step 4: Generate RDF
    print("\nStep 4: Generating RDF metadata...")
    rdf_output = converter.execute_plugin(
        "rdf_generator",
        data=transformed_data,
        dataset_uri="http://example.org/advanced/dataset",
    )
    print(f"  Generated {len(rdf_output)} characters of RDF")

    # Display sample RDF output
    print("\n=== Sample RDF Output ===")
    print(rdf_output[:500] + "..." if len(rdf_output) > 500 else rdf_output)

    # Show all registered plugins
    print("\n=== All Registered Plugins ===")
    all_plugins = PluginBase.get_all_plugins()
    for name, plugin_class in all_plugins.items():
        print(f"  - {name}: {plugin_class.__module__}.{plugin_class.__name__}")


if __name__ == "__main__":
    main()
