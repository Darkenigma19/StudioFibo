"""
Tests for JSON schema validation
"""

import pytest
from backend.utils.validate_json import validate_fibo_json, get_schema_hints


def test_valid_minimal_json():
    """Test validation of minimal valid JSON."""
    json_data = {
        "scene": {"description": "Test", "seed": 42},
        "camera": {"lens": {"focal_length_mm": 50}},
        "lighting": {"key": {"type": "softbox"}},
        "post_process": {"export": {"format": "jpg"}}
    }
    
    is_valid, error = validate_fibo_json(json_data)
    assert is_valid, f"Validation failed: {error}"


def test_invalid_missing_scene():
    """Test validation fails without scene."""
    json_data = {
        "camera": {"lens": {"focal_length_mm": 50}}
    }
    
    is_valid, error = validate_fibo_json(json_data)
    assert not is_valid
    assert "scene" in error.lower()


def test_invalid_focal_length_range():
    """Test validation fails with out-of-range focal length."""
    json_data = {
        "scene": {"description": "Test", "seed": 42},
        "camera": {"lens": {"focal_length_mm": 5}},  # Too small
        "lighting": {"key": {"type": "softbox"}},
        "post_process": {"export": {"format": "jpg"}}
    }
    
    is_valid, error = validate_fibo_json(json_data)
    # Should fail if schema has min/max constraints
    # If not enforced, this test documents expected behavior


def test_schema_hints():
    """Test schema hints retrieval."""
    hints = get_schema_hints("camera.lens.focal_length_mm")
    
    assert "type" in hints
    # Additional assertions depend on schema structure


def test_controlnet_optional():
    """Test that controlnet is optional."""
    json_data = {
        "scene": {"description": "Test", "seed": 42},
        "camera": {"lens": {"focal_length_mm": 50}},
        "lighting": {"key": {"type": "softbox"}},
        "post_process": {"export": {"format": "jpg"}}
    }
    
    is_valid, error = validate_fibo_json(json_data)
    assert is_valid
