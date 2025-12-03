"""
Smoke tests for orchestrator
"""

import pytest
from backend.orchestrator.render_orchestrator import RenderOrchestrator


@pytest.fixture
def orchestrator():
    return RenderOrchestrator(use_comfyui=False)


@pytest.fixture
def sample_json():
    return {
        "scene": {"description": "Test product", "seed": 42},
        "camera": {
            "lens": {"focal_length_mm": 50, "aperture": 5.6}
        },
        "lighting": {
            "key": {"type": "softbox", "intensity": 1.0},
            "ambient": {"intensity": 0.5}
        },
        "post_process": {"export": {"format": "jpg"}}
    }


def test_prepare_render_args(orchestrator, sample_json):
    """Test render args preparation."""
    args = orchestrator.prepare_render_args(sample_json)
    
    assert "prompt" in args
    assert "seed" in args
    assert args["seed"] == 42
    assert args["prompt"] == "Test product"


def test_focal_to_cfg_conversion(orchestrator):
    """Test focal length to CFG scale mapping."""
    assert orchestrator._focal_to_cfg(24) == 6.0  # Wide
    assert orchestrator._focal_to_cfg(50) == 7.5  # Standard
    assert orchestrator._focal_to_cfg(85) == 9.0  # Telephoto


def test_lighting_intensity_mapping(orchestrator):
    """Test that lighting affects prompt."""
    dark_json = {
        "scene": {"description": "Test"},
        "lighting": {"ambient": {"intensity": 0.2}}
    }
    
    args = orchestrator.prepare_render_args(dark_json)
    assert "dramatic" in args["prompt"] or "moody" in args["prompt"]


def test_controlnet_args(orchestrator):
    """Test ControlNet args are included when enabled."""
    cn_json = {
        "scene": {"description": "Test"},
        "controlnet": {
            "enabled": True,
            "type": "sketch",
            "image_ref": "/uploads/test.png",
            "strength": 0.8
        }
    }
    
    args = orchestrator.prepare_render_args(cn_json)
    
    assert "controlnet_image" in args
    assert args["controlnet_strength"] == 0.8
    assert args["controlnet_type"] == "sketch"


def test_default_seed_generation(orchestrator):
    """Test that missing seed gets generated."""
    json_no_seed = {
        "scene": {"description": "Test"}
    }
    
    args = orchestrator.prepare_render_args(json_no_seed)
    
    assert "seed" in args
    assert isinstance(args["seed"], int)
    assert args["seed"] > 0
