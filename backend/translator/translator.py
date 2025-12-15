"""
Natural Language to JSON Translator

Converts user prompts into frontend-compatible RenderParameters format.
Currently uses rule-based logic; can be upgraded to LLM.

Frontend Parameter Specifications:
- focalLength: 12-200mm (slider)
- yaw: -180 to 180 degrees (slider)
- pitch: -90 to 90 degrees (slider)
- lighting: 0-100% (slider, 0=Low Key, 100=High Key)
- colorPalette: warm | cool | neutral | cinematic | vibrant (select)
- controlNet.type: none | sketch | depth | canny (select)
- controlNet.strength: 0.0-1.0 (slider)
- colorSpace: sRGB | Adobe RGB | Display P3 (select)
"""

import re
from typing import Dict, Any


def params_to_enhanced_prompt(params: Dict[str, Any]) -> str:
    """
    Convert RenderParameters JSON back to an enhanced descriptive prompt
    that incorporates all the technical parameters for better image generation.
    
    Args:
        params: Dict containing RenderParameters (focalLength, yaw, pitch, lighting, colorPalette, etc.)
        
    Returns:
        Enhanced prompt string with technical details for image generation
    """
    base_prompt = params.get("prompt", "")
    focal_length = params.get("focalLength", 35)
    yaw = params.get("yaw", 0)
    pitch = params.get("pitch", 0)
    lighting = params.get("lighting", 50)
    color_palette = params.get("colorPalette", "neutral")
    
    # Build camera angle description
    camera_angle = ""
    if pitch < -60:
        camera_angle = "top-down aerial view"
    elif pitch < -20:
        camera_angle = "high angle view"
    elif pitch > 20:
        camera_angle = "low angle view from below"
    else:
        camera_angle = "eye-level view"
    
    # Build camera rotation description
    rotation = ""
    if yaw < -120:
        rotation = "rear view"
    elif yaw < -45:
        rotation = "from left side"
    elif yaw < -10:
        rotation = "slight left angle"
    elif yaw > 120:
        rotation = "rear view"
    elif yaw > 45:
        rotation = "from right side"
    elif yaw > 10:
        rotation = "slight right angle"
    else:
        rotation = "front facing"
    
    # Build lens description
    lens_desc = ""
    if focal_length <= 24:
        lens_desc = "ultra wide angle lens"
    elif focal_length <= 35:
        lens_desc = "wide angle 35mm lens"
    elif focal_length <= 50:
        lens_desc = "standard 50mm lens"
    elif focal_length <= 85:
        lens_desc = "portrait 85mm lens"
    else:
        lens_desc = f"telephoto {focal_length}mm lens"
    
    # Build lighting description
    lighting_desc = ""
    if lighting < 20:
        lighting_desc = "low-key dramatic lighting, dark moody atmosphere"
    elif lighting < 40:
        lighting_desc = "subtle lighting with shadows"
    elif lighting < 60:
        lighting_desc = "balanced natural lighting"
    elif lighting < 80:
        lighting_desc = "bright well-lit scene"
    else:
        lighting_desc = "high-key bright lighting, clean and airy"
    
    # Build color palette description
    palette_desc = {
        "warm": "warm golden tones, sunset colors, orange and amber hues",
        "cool": "cool blue tones, crisp cold atmosphere",
        "neutral": "balanced natural colors",
        "cinematic": "cinematic color grading, moody film look, dramatic atmosphere",
        "vibrant": "vibrant saturated colors, bold and colorful"
    }.get(color_palette, "natural colors")
    
    # Combine everything into an enhanced prompt
    enhanced_prompt = f"{base_prompt}, shot with {lens_desc}, {camera_angle}, {rotation}, {lighting_desc}, {palette_desc}, professional photography, high quality, detailed, photorealistic"
    
    return enhanced_prompt


def translate_prompt_to_json(prompt: str) -> Dict[str, Any]:
    """
    Convert natural language prompt to frontend RenderParameters format.
    
    Args:
        prompt: Natural language description
        
    Returns:
        Dict matching frontend RenderParameters interface with proper ranges and options
    """
    prompt_lower = prompt.lower()
    
    # Extract focal length
    focal = extract_focal_length(prompt_lower)
    
    # Detect lighting mood
    ambient = 0.1 if "moody" in prompt_lower or "dramatic" in prompt_lower else 0.2
    if "bright" in prompt_lower or "clean" in prompt_lower:
        ambient = 0.7
        
    # Detect camera angle (pitch: -90 to 90)
    pitch = extract_camera_angle(prompt_lower)
    
    # Detect yaw (camera rotation: -180 to 180)
    yaw = extract_yaw(prompt_lower)
    
    # Detect color palette (must match frontend options)
    color_palette = extract_color_palette(prompt_lower)
    
    # Extract lighting (0-100 scale for frontend slider)
    lighting_value = extract_lighting_value(prompt_lower)
    
    # Frontend-compatible JSON format matching RenderParameters interface
    json_out = {
        "prompt": prompt.strip(),
        "focalLength": focal,  # 12-200 range
        "yaw": yaw,  # -180 to 180
        "pitch": pitch,  # -90 to 90
        "lighting": lighting_value,  # 0-100
        "colorPalette": color_palette,  # warm/cool/neutral/cinematic/vibrant
        "controlNet": {
            "type": "none",  # none/sketch/depth/canny
            "strength": 0.75,  # 0.0-1.0
            "image": None
        },
        "seed": 12345,
        "resolution": {"width": 1920, "height": 1080},
        "colorSpace": "sRGB"  # sRGB/Adobe RGB/Display P3
    }
    
    return json_out


def extract_focal_length(prompt: str) -> int:
    """Extract focal length from prompt text. Range: 12-200mm (frontend slider)."""
    patterns = [
        (r'(\d+)\s*mm', 1),
        (r'(\d+)mm', 1),
    ]
    
    for pattern, group in patterns:
        match = re.search(pattern, prompt)
        if match:
            focal = int(match.group(group))
            # Clamp to frontend range (12-200)
            return max(12, min(200, focal))
    
    # Defaults based on keywords (within 12-200 range)
    if "wide" in prompt or "environment" in prompt or "landscape" in prompt:
        return 24
    elif "portrait" in prompt or "headshot" in prompt or "closeup" in prompt:
        return 85
    elif "product" in prompt:
        return 50
    elif "telephoto" in prompt or "zoom" in prompt:
        return 135
    
    return 35  # Standard default


def extract_camera_angle(prompt: str) -> int:
    """Extract camera pitch angle from prompt. Range: -90 to 90 (frontend slider)."""
    if "high angle" in prompt or "overhead" in prompt or "bird's eye" in prompt:
        return -45
    elif "top down" in prompt or "directly above" in prompt:
        return -90
    elif "low angle" in prompt or "from below" in prompt or "worm's eye" in prompt:
        return 30
    elif "eye level" in prompt or "straight on" in prompt:
        return 0
    elif "slight tilt down" in prompt:
        return -15
    elif "slight tilt up" in prompt:
        return 15
    
    return 0  # Default (eye level)


def extract_yaw(prompt: str) -> int:
    """Extract camera yaw (rotation) from prompt. Range: -180 to 180 (frontend slider)."""
    if "from left" in prompt or "left side" in prompt:
        return -45
    elif "from right" in prompt or "right side" in prompt:
        return 45
    elif "front" in prompt or "straight ahead" in prompt:
        return 0
    elif "behind" in prompt or "rear" in prompt:
        return 180
    elif "quarter left" in prompt or "3/4 left" in prompt:
        return -30
    elif "quarter right" in prompt or "3/4 right" in prompt:
        return 30
    
    return 0  # Default (front view)


def extract_color_palette(prompt: str) -> str:
    """Extract color palette preference from prompt. 
    Options: warm, cool, neutral, cinematic, vibrant (frontend select).
    """
    if "warm" in prompt or "golden" in prompt or "sunset" in prompt or "orange" in prompt:
        return "warm"
    elif "cool" in prompt or "blue" in prompt or "cold" in prompt or "icy" in prompt:
        return "cool"
    elif "cinematic" in prompt or "moody" in prompt or "dramatic" in prompt or "film" in prompt:
        return "cinematic"
    elif "vibrant" in prompt or "bright" in prompt or "saturated" in prompt or "colorful" in prompt:
        return "vibrant"
    elif "neutral" in prompt or "balanced" in prompt or "natural" in prompt:
        return "neutral"
    
    return "neutral"  # Default


def extract_lighting_value(prompt: str) -> int:
    """Extract lighting intensity from prompt. Range: 0-100 (frontend slider).
    0 = Low Key (dark/moody), 100 = High Key (bright).
    """
    if "very dark" in prompt or "extremely dark" in prompt:
        return 5
    elif "dark" in prompt or "low key" in prompt or "moody" in prompt or "dramatic" in prompt:
        return 20
    elif "dim" in prompt or "subtle" in prompt:
        return 35
    elif "bright" in prompt or "high key" in prompt or "well lit" in prompt:
        return 85
    elif "very bright" in prompt or "extremely bright" in prompt:
        return 95
    elif "normal" in prompt or "standard" in prompt:
        return 50
    
    return 50  # Default (middle value)
