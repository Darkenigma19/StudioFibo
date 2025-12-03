"""
JSON Schema Validation Utilities
"""

from jsonschema import validate, ValidationError, Draft7Validator
from typing import Dict, Any, Tuple
import json
from pathlib import Path


def load_schema() -> Dict[str, Any]:
    """Load the FIBO JSON schema."""
    schema_path = Path(__file__).parent.parent.parent / "schemas" / "fibo_schema.json"
    with open(schema_path, 'r') as f:
        return json.load(f)


def validate_fibo_json(instance: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate JSON instance against FIBO schema.
    
    Args:
        instance: JSON object to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        schema = load_schema()
        validate(instance=instance, schema=schema)
        return (True, "")
    except ValidationError as e:
        return (False, e.message)
    except Exception as e:
        return (False, str(e))


def get_schema_hints(field_path: str) -> Dict[str, Any]:
    """
    Get schema hints for autocomplete/validation.
    
    Args:
        field_path: Dot-notation path (e.g., "camera.lens.focal_length_mm")
        
    Returns:
        Dict with type, range, and description
    """
    schema = load_schema()
    
    # Navigate schema by path
    parts = field_path.split('.')
    current = schema.get("properties", {})
    
    for part in parts:
        if "properties" in current:
            current = current["properties"].get(part, {})
        else:
            return {}
    
    return {
        "type": current.get("type"),
        "minimum": current.get("minimum"),
        "maximum": current.get("maximum"),
        "enum": current.get("enum"),
        "description": current.get("description", "")
    }
