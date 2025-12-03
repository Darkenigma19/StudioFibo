"""
Natural Language to JSON Translator

Converts user prompts into validated FIBO JSON manifests.
Currently uses rule-based logic; can be upgraded to LLM.
"""

import re
from typing import Dict, Any


def translate_prompt_to_json(prompt: str) -> Dict[str, Any]:
    """
    Convert natural language prompt to FIBO JSON structure.
    
    Args:
        prompt: Natural language description
        
    Returns:
        Dict containing FIBO-compliant JSON
    """
    prompt_lower = prompt.lower()
    
    # Extract focal length
    focal = extract_focal_length(prompt_lower)
    
    # Detect lighting mood
    ambient = 0.1 if "moody" in prompt_lower or "dramatic" in prompt_lower else 0.2
    if "bright" in prompt_lower or "clean" in prompt_lower:
        ambient = 0.7
        
    # Detect camera angle
    pitch = extract_camera_angle(prompt_lower)
    
    json_out = {
        "scene": {
            "description": prompt.strip(),
            "seed": 12345  # Default seed, can be randomized
        },
        "camera": {
            "lens": {
                "focal_length_mm": focal,
                "aperture": 2.2 if "portrait" in prompt_lower else 5.6
            },
            "position": {"x": 0.0, "y": 0.6, "z": 1.2},
            "rotation": {"pitch": pitch, "yaw": 0, "roll": 0},
            "fov_degrees": 45
        },
        "lighting": {
            "key": {
                "type": "softbox",
                "intensity": 1.0,
                "direction": {"x": -0.6, "y": 0.9, "z": -0.8}
            },
            "rim": {
                "type": "spot",
                "intensity": 0.6,
                "color": "#ffd9b3"
            },
            "ambient": {"intensity": ambient}
        },
        "controlnet": {"sketch_guidance": {"enabled": False}},
        "post_process": {"export": {"format": "jpg"}}
    }
    
    return json_out


def extract_focal_length(prompt: str) -> int:
    """Extract focal length from prompt text."""
    patterns = [
        (r'(\d+)\s*mm', 1),
        (r'(\d+)mm', 1),
    ]
    
    for pattern, group in patterns:
        match = re.search(pattern, prompt)
        if match:
            return int(match.group(group))
    
    # Defaults based on keywords
    if "wide" in prompt or "environment" in prompt:
        return 24
    elif "portrait" in prompt or "headshot" in prompt:
        return 85
    elif "product" in prompt:
        return 50
    
    return 35  # Standard default


def extract_camera_angle(prompt: str) -> int:
    """Extract camera pitch angle from prompt."""
    if "high angle" in prompt or "overhead" in prompt or "top down" in prompt:
        return -20
    elif "low angle" in prompt or "from below" in prompt:
        return 10
    elif "eye level" in prompt:
        return 0
    
    return -8  # Slight downward angle (common for product)
