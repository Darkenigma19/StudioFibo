"""
Tests for translator module
"""

import pytest
from backend.translator.translator import (
    translate_prompt_to_json,
    extract_focal_length,
    extract_camera_angle
)


def test_basic_translation():
    """Test basic prompt translation."""
    prompt = "Product shot of coffee grinder"
    result = translate_prompt_to_json(prompt)
    
    assert "scene" in result
    assert "camera" in result
    assert "lighting" in result
    assert result["scene"]["description"] == prompt


def test_focal_length_extraction():
    """Test focal length detection from prompt."""
    assert extract_focal_length("shot with 50mm lens") == 50
    assert extract_focal_length("85mm portrait") == 85
    assert extract_focal_length("wide angle environment") == 24
    assert extract_focal_length("product photo") == 50


def test_camera_angle_extraction():
    """Test camera angle detection."""
    assert extract_camera_angle("high angle shot") < 0
    assert extract_camera_angle("low angle dramatic") > 0
    assert extract_camera_angle("eye level portrait") == 0


def test_moody_lighting():
    """Test moody lighting detection."""
    result = translate_prompt_to_json("moody dramatic portrait")
    assert result["lighting"]["ambient"]["intensity"] < 0.3


def test_bright_lighting():
    """Test bright lighting detection."""
    result = translate_prompt_to_json("bright clean product shot")
    assert result["lighting"]["ambient"]["intensity"] > 0.5


def test_portrait_aperture():
    """Test that portraits get shallow aperture."""
    result = translate_prompt_to_json("portrait headshot")
    assert result["camera"]["lens"]["aperture"] == 2.2
