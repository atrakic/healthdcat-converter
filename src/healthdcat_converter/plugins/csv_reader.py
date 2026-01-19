"""CSV Reader plugin for reading CSV files."""

import csv
from typing import List, Dict, Any
from pathlib import Path

from ..plugin_base import PluginBase


class CSVReaderPlugin(PluginBase):
    """Plugin to read CSV files and convert them to a list of dictionaries."""

    @classmethod
    def get_name(cls) -> str:
        return "csv_reader"

    def execute(self, data: Any, **kwargs) -> List[Dict[str, Any]]:
        """
        Read a CSV file and return its contents as a list of dictionaries.

        Args:
            data: Path to the CSV file (str or Path)
            **kwargs: Additional arguments for csv.DictReader

        Returns:
            List of dictionaries representing CSV rows
        """
        file_path = Path(data)

        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, **kwargs)
            return list(reader)
