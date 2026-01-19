"""RDF Generator plugin for converting data to RDF format."""

from typing import Any, Dict, List
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS
from ..plugin_base import PluginBase


class RDFGeneratorPlugin(PluginBase):
    """
    Plugin to generate RDF metadata following HealthDCAT Application Profile.

    Uses rdflib for robust RDF generation and supports multiple serialization formats.
    Implements the full HealthDCAT-AP specification: https://healthdcat-ap.github.io/
    """

    @classmethod
    def get_name(cls) -> str:
        return "rdf_generator"

    def __init__(self):
        """Initialize the RDF generator with HealthDCAT-AP namespaces."""
        self.graph = Graph()
        
        # Define namespaces
        self.DCAT = Namespace("http://www.w3.org/ns/dcat#")
        self.DCT = Namespace("http://purl.org/dc/terms/")
        self.FOAF = Namespace("http://xmlns.com/foaf/0.1/")
        self.VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
        self.SCHEMA = Namespace("http://schema.org/")
        self.CSVW = Namespace("http://www.w3.org/ns/csvw#")
        self.HEALTHDCAT = Namespace("https://health.ec.europa.eu/healthdcat-ap/")
        
        # Bind namespaces to graph
        self.graph.bind("dcat", self.DCAT)
        self.graph.bind("dct", self.DCT)
        self.graph.bind("foaf", self.FOAF)
        self.graph.bind("vcard", self.VCARD)
        self.graph.bind("schema", self.SCHEMA)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("csvw", self.CSVW)
        self.graph.bind("healthdcat", self.HEALTHDCAT)

    def execute(self, data: Any, **kwargs) -> str:
        """
        Convert data to RDF format following HealthDCAT-AP.

        Args:
            data: Data to convert (typically a list of dictionaries)
            **kwargs: Additional options:
                - format: RDF serialization format (default: 'turtle')
                - dataset_uri: Base URI for the dataset

        Returns:
            RDF data as a string in the specified format
        """
        rdf_format = kwargs.get("format", "turtle")
        dataset_uri = kwargs.get("dataset_uri", "http://example.org/dataset")

        # Create a fresh graph for this execution
        graph = Graph()
        
        # Bind namespaces
        graph.bind("dcat", self.DCAT)
        graph.bind("dct", self.DCT)
        graph.bind("foaf", self.FOAF)
        graph.bind("vcard", self.VCARD)
        graph.bind("schema", self.SCHEMA)
        graph.bind("rdfs", RDFS)
        graph.bind("csvw", self.CSVW)
        graph.bind("healthdcat", self.HEALTHDCAT)

        # Add dataset metadata
        self._add_dataset_metadata(graph, dataset_uri, data)

        # Add table schema with variables
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            self._add_table_schema(graph, dataset_uri, data)

        # Serialize to requested format
        return graph.serialize(format=rdf_format)

    def _add_dataset_metadata(self, graph: Graph, dataset_uri: str, data: List[Dict]) -> None:
        """
        Add dataset metadata to the RDF graph.

        Args:
            graph: RDF graph to add triples to
            dataset_uri: URI for the dataset
            data: Dataset content
        """
        dataset = URIRef(dataset_uri)
        
        # Add dataset type and basic properties
        graph.add((dataset, RDF.type, self.DCAT.Dataset))
        graph.add((dataset, self.DCT.title, Literal("Health Dataset")))
        graph.add((dataset, self.DCT.description, Literal("Dataset converted from CSV")))
        graph.add((dataset, self.HEALTHDCAT.hasHealthCategory, Literal("general")))

        if isinstance(data, list) and len(data) > 0:
            # Add number of records
            graph.add((dataset, self.SCHEMA.numberOfItems, Literal(len(data))))

            # Link to table schema
            if isinstance(data[0], dict):
                schema_uri = URIRef(f"{dataset_uri}/schema")
                graph.add((dataset, self.CSVW.tableSchema, schema_uri))

    def _add_table_schema(self, graph: Graph, dataset_uri: str, data: List[Dict]) -> None:
        """
        Add table schema with column/variable definitions using CSVW.

        Args:
            graph: RDF graph to add triples to
            dataset_uri: URI for the dataset
            data: Dataset content with column names
        """
        schema_uri = URIRef(f"{dataset_uri}/schema")
        
        # Add table schema type
        graph.add((schema_uri, RDF.type, self.CSVW.TableSchema))
        
        columns = list(data[0].keys())
        column_uris = [URIRef(f"{dataset_uri}/schema/column/{idx}") for idx in range(len(columns))]
        
        # Link columns to schema
        for col_uri in column_uris:
            graph.add((schema_uri, self.CSVW.column, col_uri))
        
        # Define each column
        for idx, col_name in enumerate(columns):
            col_uri = column_uris[idx]
            
            # Add column type and properties
            graph.add((col_uri, RDF.type, self.CSVW.Column))
            graph.add((col_uri, self.CSVW.name, Literal(col_name)))
            graph.add((col_uri, self.CSVW.title, Literal(col_name)))
            graph.add((col_uri, RDFS.label, Literal(col_name)))
            
            # Infer and add datatype
            datatype = self._infer_datatype(data, col_name)
            graph.add((col_uri, self.CSVW.datatype, Literal(datatype)))

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

        return "string"  # Default to string
