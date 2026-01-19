"""Validator plugin for validating CSV data."""

from typing import Any, Dict, List
from ..plugin_base import PluginBase


class ValidatorPlugin(PluginBase):
    """Plugin to validate CSV data before conversion."""

    @classmethod
    def get_name(cls) -> str:
        return "validator"

    def execute(self, data: Any, **kwargs) -> Dict[str, Any]:
        """
        Validate CSV data.

        Args:
            data: Data to validate (list of dictionaries)
            **kwargs: Validation options:
                - required_fields: List of required field names
                - allow_empty: Allow empty values (default: True)

        Returns:
            Dictionary with validation results:
                - valid: Boolean indicating if data is valid
                - errors: List of validation errors
                - warnings: List of warnings
        """
        required_fields = kwargs.get("required_fields", [])
        allow_empty = kwargs.get("allow_empty", True)

        result = {"valid": True, "errors": [], "warnings": []}

        if not isinstance(data, list):
            result["valid"] = False
            result["errors"].append("Data must be a list of dictionaries")
            return result

        if len(data) == 0:
            result["warnings"].append("Dataset is empty")
            return result

        # Check required fields
        for idx, row in enumerate(data):
            if not isinstance(row, dict):
                result["valid"] = False
                result["errors"].append(f"Row {idx} is not a dictionary")
                continue

            # Check for required fields
            for field in required_fields:
                if field not in row:
                    result["valid"] = False
                    result["errors"].append(
                        f"Row {idx} missing required field: {field}"
                    )
                elif not allow_empty and not row[field]:
                    result["valid"] = False
                    result["errors"].append(
                        f"Row {idx} has empty value for required field: {field}"
                    )

        return result
