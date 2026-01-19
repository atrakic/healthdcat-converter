"""RDF Generator plugin for converting data to RDF format."""

from typing import Any, Dict, List
from ..plugin_base import PluginBase


class RDFGeneratorPlugin(PluginBase):
    """
    Plugin to generate RDF metadata following HealthDCAT Application Profile.

    This is a basic implementation that can be extended to follow the full
    HealthDCAT-AP specification.
    """

    @classmethod
    def get_name(cls) -> str:
        return "rdf_generator"

    def __init__(self):
        """Initialize the RDF generator with HealthDCAT-AP namespaces."""
        self.namespaces = {
            "dcat": "http://www.w3.org/ns/dcat#",
            "dct": "http://purl.org/dc/terms/",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "vcard": "http://www.w3.org/2006/vcard/ns#",
            "schema": "http://schema.org/",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "csvw": "http://www.w3.org/ns/csvw#",
            "healthdcat": "https://health.ec.europa.eu/healthdcat-ap/",
        }

    def execute(self, data: Any, **kwargs) -> str:
        """
        Convert data to RDF format following HealthDCAT-AP.

        Args:
            data: Data to convert (typically a list of dictionaries)
            **kwargs: Additional options:
                - format: RDF serialization format (default: 'turtle')
                - dataset_uri: Base URI for the dataset

        Returns:
            RDF data as a string
        """
        rdf_format = kwargs.get("format", "turtle")
        dataset_uri = kwargs.get("dataset_uri", "http://example.org/dataset")

        # Basic RDF generation (simplified)
        # In production, use rdflib or similar library
        rdf_output = self._generate_turtle_header()
        rdf_output += self._generate_dataset_metadata(dataset_uri, data)

        # Add table schema with variables
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            rdf_output += self._generate_table_schema(dataset_uri, data)

        return rdf_output

    def _generate_turtle_header(self) -> str:
        """Generate Turtle format header with namespace prefixes."""
        header = ""
        for prefix, uri in self.namespaces.items():
            header += f"@prefix {prefix}: <{uri}> .\n"
        header += "\n"
        return header

    def _generate_dataset_metadata(self, dataset_uri: str, data: List[Dict]) -> str:
        """
        Generate basic dataset metadata in Turtle format.

        Args:
            dataset_uri: URI for the dataset
            data: Dataset content

        Returns:
            RDF metadata as Turtle string
        """
        metadata = f"<{dataset_uri}> a dcat:Dataset ;\n"
        metadata += f'    dct:title "Health Dataset" ;\n'
        metadata += f'    dct:description "Dataset converted from CSV" ;\n'

        if isinstance(data, list) and len(data) > 0:
            # Add number of records
            metadata += f"    schema:numberOfItems {len(data)} ;\n"

            # Link to table schema
            if isinstance(data[0], dict):
                metadata += f"    csvw:tableSchema <{dataset_uri}/schema> ;\n"

        metadata += f'    healthdcat:hasHealthCategory "general" .\n'

        return metadata

    def _generate_table_schema(self, dataset_uri: str, data: List[Dict]) -> str:
        """
        Generate table schema with column/variable definitions using CSVW.

        Args:
            dataset_uri: URI for the dataset
            data: Dataset content with column names

        Returns:
            RDF for table schema including columns
        """
        schema_uri = f"{dataset_uri}/schema"
        schema = f"\n<{schema_uri}> a csvw:TableSchema ;\n"
        schema += f"    csvw:column "

        columns = list(data[0].keys())
        column_uris = []

        for idx, col_name in enumerate(columns):
            col_uri = f"{dataset_uri}/schema/column/{idx}"
            column_uris.append(f"<{col_uri}>")

        schema += ", ".join(column_uris) + " .\n"

        # Define each column
        for idx, col_name in enumerate(columns):
            col_uri = f"{dataset_uri}/schema/column/{idx}"
            schema += f"\n<{col_uri}> a csvw:Column ;\n"
            schema += f'    csvw:name "{col_name}" ;\n'
            schema += f'    csvw:title "{col_name}" ;\n'
            schema += f'    rdfs:label "{col_name}" ;\n'

            # Infer datatype from first non-empty value
            datatype = self._infer_datatype(data, col_name)
            schema += f'    csvw:datatype "{datatype}" .\n'

        return schema

    def _infer_datatype(self, data: List[Dict], column_name: str) -> str:
        """
        Infer datatype for a column based on its values.

        Args:
            data: Dataset content
            column_name: Name of the column

        Returns:
            Datatype string (xsd types)
        """
        for row in data:
            value = row.get(column_name)
            if value is not None and value != "":
                # Try to infer type
                if isinstance(value, bool):
                    return "boolean"
                elif isinstance(value, int):
                    return "integer"
                elif isinstance(value, float):
                    return "decimal"
                else:
                    # Try to parse string as number
                    str_value = str(value).strip()
                    try:
                        int(str_value)
                        return "integer"
                    except ValueError:
                        try:
                            float(str_value)
                            return "decimal"
                        except ValueError:
                            return "string"

        return "string"  # Default to stringa += f"    dcat:keyword {', '.join([f'\"{k}\"' for k in keys])} ;\n"

        metadata += f'    healthdcat:hasHealthCategory "general" .\n'

        return metadata
