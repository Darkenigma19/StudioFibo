# FIBO Schema Examples

## Schema Overview

The `fibo_schema.json` defines the complete structure for StudioFlow rendering manifests. This document provides explanations and examples for each field.

## Top-Level Structure

```json
{
  "scene": {},
  "camera": {},
  "lighting": {},
  "materials": {},
  "controlnet": {},
  "post_process": {}
}
```

## Field Reference

### Scene

Defines the overall scene description and rendering seed.

```json
{
  "scene": {
    "description": "Moody product shot of coffee grinder, 35mm lens, rim lighting",
    "seed": 42
  }
}
```

**Fields:**

- `description` (string): Natural language description of the shot
- `seed` (integer): Random seed for reproducible renders. Same seed + same params = identical output

**Tips:**

- Use descriptive, specific language
- Include style cues: "moody", "bright", "editorial"
- Mention key objects and desired mood
- Seeds range: 0 - 999999

### Camera

Controls camera position, lens properties, and field of view.

```json
{
  "camera": {
    "lens": {
      "focal_length_mm": 50,
      "aperture": 2.8
    },
    "position": {
      "x": 0.0,
      "y": 0.8,
      "z": 1.5
    },
    "rotation": {
      "pitch": -10,
      "yaw": 0,
      "roll": 0
    },
    "fov_degrees": 45
  }
}
```

**Lens:**

- `focal_length_mm`: 18-200 range. 35mm = product, 50mm = standard, 85mm = portrait
- `aperture`: f/1.4 - f/22. Lower = shallow DOF (blurred background)

**Position (meters):**

- `x`: Left (-) / Right (+)
- `y`: Down (-) / Up (+)
- `z`: Back (-) / Forward (+)

**Rotation (degrees):**

- `pitch`: Look up (+) / down (-)
- `yaw`: Pan left (-) / right (+)
- `roll`: Tilt counterclockwise (+) / clockwise (-)

**Common Setups:**

```json
// High angle product shot
{"position": {"x": 0, "y": 1.2, "z": 1.0}, "rotation": {"pitch": -15}}

// Eye-level portrait
{"position": {"x": 0, "y": 1.6, "z": 2.0}, "rotation": {"pitch": 0}}

// Low angle dramatic
{"position": {"x": 0, "y": 0.3, "z": 1.5}, "rotation": {"pitch": 10}}
```

### Lighting

Defines key light, rim/fill lights, and ambient illumination.

```json
{
  "lighting": {
    "key": {
      "type": "softbox",
      "intensity": 1.0,
      "direction": { "x": -0.5, "y": 0.8, "z": -0.3 },
      "color": "#ffffff"
    },
    "rim": {
      "type": "spot",
      "intensity": 0.6,
      "color": "#ffd9b3"
    },
    "ambient": {
      "intensity": 0.2
    }
  }
}
```

**Key Light:**

- `type`: `softbox`, `directional`, `point`, `spot`
- `intensity`: 0.1 - 3.0 (1.0 = normal)
- `direction`: Normalized vector pointing toward subject
- `color`: Hex color code

**Rim/Fill Lights:**

- Optional accent lights
- Same properties as key light
- Rim typically behind subject (edge lighting)

**Ambient:**

- Overall scene brightness
- 0.0 = pitch black, 1.0 = fully lit

**Lighting Recipes:**

```json
// Dramatic moody (low ambient, strong key)
{"key": {"intensity": 1.2}, "ambient": {"intensity": 0.1}}

// Bright e-commerce (high ambient)
{"key": {"intensity": 1.0}, "ambient": {"intensity": 0.5}}

// Rim-lit silhouette
{"key": {"intensity": 0.3}, "rim": {"intensity": 1.5}, "ambient": {"intensity": 0.05}}
```

### Materials (Optional)

Defines object-specific material properties.

```json
{
  "materials": {
    "grinder": {
      "color_palette": "warm_earth",
      "metalness": 0.8,
      "roughness": 0.3
    }
  }
}
```

**Properties:**

- `color_palette`: Preset or hex colors
- `metalness`: 0.0 (dielectric) - 1.0 (pure metal)
- `roughness`: 0.0 (mirror) - 1.0 (matte)

### ControlNet

Enables sketch/depth/pose-guided rendering.

```json
{
  "controlnet": {
    "type": "sketch",
    "image_ref": "/uploads/sketch_abc123.png",
    "strength": 0.8,
    "enabled": true
  }
}
```

**Types:**

- `sketch`: Line art/edge detection
- `depth`: Depth map
- `pose`: Human pose skeleton
- `seg`: Semantic segmentation

**Strength:**

- 0.0 = ignore guidance
- 1.0 = strict adherence
- 0.6-0.8 recommended for most cases

### Post-Process

Output format and post-processing options.

```json
{
  "post_process": {
    "export": {
      "format": "jpg",
      "quality": 95
    },
    "tone_mapping": {
      "enabled": true,
      "exposure": 0.0
    }
  }
}
```

**Formats:**

- `jpg`: Standard web/preview
- `png`: Lossless with transparency
- `exr`: 32-bit HDR for compositing
- `tiff`: 16-bit for print

**Tone Mapping:**

- `exposure`: -2.0 to +2.0 (stops)
- `contrast`: 0.8 to 1.2

## Complete Examples

### Example 1: E-Commerce Product

```json
{
  "scene": {
    "description": "Clean product photo of wireless headphones on white background",
    "seed": 12345
  },
  "camera": {
    "lens": { "focal_length_mm": 85, "aperture": 5.6 },
    "position": { "x": 0, "y": 0.5, "z": 1.0 },
    "rotation": { "pitch": -5, "yaw": 0, "roll": 0 }
  },
  "lighting": {
    "key": { "type": "softbox", "intensity": 1.0 },
    "ambient": { "intensity": 0.8 }
  },
  "post_process": {
    "export": { "format": "png" }
  }
}
```

### Example 2: Editorial Portrait

```json
{
  "scene": {
    "description": "Dramatic portrait with Rembrandt lighting",
    "seed": 99887
  },
  "camera": {
    "lens": { "focal_length_mm": 85, "aperture": 1.8 },
    "position": { "x": 0, "y": 1.6, "z": 2.0 }
  },
  "lighting": {
    "key": {
      "type": "point",
      "intensity": 1.2,
      "direction": { "x": -0.7, "y": 0.5, "z": -0.5 }
    },
    "ambient": { "intensity": 0.1 }
  },
  "post_process": {
    "export": { "format": "tiff" },
    "tone_mapping": { "exposure": -0.3 }
  }
}
```

### Example 3: ControlNet Sketch

```json
{
  "scene": {
    "description": "Coffee grinder based on sketch reference",
    "seed": 42
  },
  "camera": {
    "lens": { "focal_length_mm": 35, "aperture": 2.2 }
  },
  "lighting": {
    "key": { "type": "softbox", "intensity": 1.0 }
  },
  "controlnet": {
    "type": "sketch",
    "image_ref": "/uploads/grinder_sketch.png",
    "strength": 0.75,
    "enabled": true
  },
  "post_process": {
    "export": { "format": "jpg" }
  }
}
```

## Validation

All JSON must validate against `fibo_schema.json`. Use the `/validate` endpoint:

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d @my_scene.json
```

## Tips & Best Practices

1. **Start Simple**: Begin with scene + camera + basic lighting
2. **Iterate**: Make small changes, re-render, compare
3. **Use Seeds**: Lock seed when fine-tuning other parameters
4. **Save Variants**: Store each iteration with descriptive names
5. **Study Samples**: Check `/samples` directory for working examples

## Schema Evolution

The schema will expand over time. Future additions:

- Animation keyframes
- Multi-object scenes
- Advanced materials (subsurface scattering)
- Environment maps (HDRI)

Always check `fibo_schema.json` for the latest authoritative structure.
