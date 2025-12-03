# ComfyUI Integration

## Overview

StudioFlow can integrate with ComfyUI for advanced workflow customization. ComfyUI provides a node-based interface for complex rendering pipelines.

## Architecture

```
StudioFlow JSON → Recipe Mapper → ComfyUI API → Rendered Output
```

## Recipe System

Recipes are JSON files that map StudioFlow schema fields to ComfyUI node configurations.

### Recipe Structure

```json
{
  "name": "product_with_sketch",
  "description": "Product render with ControlNet sketch guidance",
  "nodes": {
    "checkpoint": {
      "class_type": "CheckpointLoaderSimple",
      "inputs": {
        "ckpt_name": "bria_fibo_v2.safetensors"
      }
    },
    "controlnet": {
      "class_type": "ControlNetLoader",
      "inputs": {
        "control_net_name": "control_v11p_sd15_lineart.pth"
      }
    }
  }
}
```

## Field Mapping

### Camera Parameters

| StudioFlow JSON               | ComfyUI Node | Parameter    |
| ----------------------------- | ------------ | ------------ |
| `camera.lens.focal_length_mm` | KSampler     | CFG Scale    |
| `camera.rotation.yaw`         | LatentRotate | angle        |
| `camera.fov_degrees`          | -            | (calculated) |

### Lighting

| StudioFlow JSON              | ComfyUI Node | Parameter     |
| ---------------------------- | ------------ | ------------- |
| `lighting.key.intensity`     | -            | prompt weight |
| `lighting.ambient.intensity` | KSampler     | denoise       |

### ControlNet

| StudioFlow JSON        | ComfyUI Node     | Parameter        |
| ---------------------- | ---------------- | ---------------- |
| `controlnet.type`      | ControlNetLoader | control_net_name |
| `controlnet.image_ref` | LoadImage        | image path       |
| `controlnet.strength`  | ControlNetApply  | strength         |

## API Integration

### 1. Start ComfyUI Server

```bash
python main.py --port 8188
```

### 2. Configure StudioFlow

In `.env`:

```
COMFYUI_URL=http://localhost:8188
COMFYUI_ENABLED=true
```

### 3. Submit Workflow

```python
import requests

workflow = load_recipe("product_with_sketch.json")
mapped_workflow = map_json_to_workflow(scene_json, workflow)

response = requests.post(
    "http://localhost:8188/prompt",
    json={"prompt": mapped_workflow}
)
```

## Recipe Development

### Creating a New Recipe

1. **Design in ComfyUI UI**: Create workflow visually
2. **Export as JSON**: File → Export
3. **Add to `comfyui-recipes/`**
4. **Create mapper function** in `orchestrator/comfyui_adapter.py`

### Testing

```bash
cd scripts
./test_comfyui_recipe.sh product_with_sketch
```

## Available Recipes

### `product_with_sketch.json`

- Product photography with sketch guidance
- ControlNet: Lineart
- Best for: Product mockups with specific poses

### `portrait_controlnet.json`

- Portrait rendering with depth guidance
- ControlNet: Depth
- Best for: Character renders, face-focused shots

## Advanced Features

### Multi-ControlNet

```json
{
  "controlnet": [
    {
      "type": "sketch",
      "image_ref": "/uploads/sketch.png",
      "strength": 0.8
    },
    {
      "type": "depth",
      "image_ref": "/uploads/depth.png",
      "strength": 0.6
    }
  ]
}
```

### Custom Nodes

Add third-party ComfyUI nodes:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager
```

## Limitations

- ComfyUI must be running separately
- Recipe version compatibility
- Not all JSON fields map directly to nodes

## Future Enhancements

- [ ] Auto-generate recipes from JSON schema
- [ ] Visual recipe editor in StudioFlow UI
- [ ] Recipe marketplace/sharing
- [ ] Embedded ComfyUI server mode
