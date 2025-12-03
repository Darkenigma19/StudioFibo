# EXR Examples

This directory contains sample EXR (OpenEXR) and TIFF renders for demonstration purposes.

## What are EXR files?

EXR (Extended Range) is a high-dynamic-range image format used in:

- VFX and compositing workflows
- Professional photography
- 3D rendering pipelines
- Color grading

## Benefits

- **32-bit float precision**: Captures full light range
- **Metadata embedding**: Stores camera, lighting, render params
- **Multi-channel**: RGB + Alpha + Depth + Normal maps
- **No clipping**: Preserves highlights and shadows

## Files

Sample files will be added after successful FIBO renders:

```
exr_examples/
├── product_shot_32bit.exr      # Full HDR product render
├── portrait_16bit.tiff         # 16-bit portrait for print
├── environment_with_depth.exr  # EXR with depth channel
└── metadata_example.json       # Embedded metadata sample
```

## Usage

### Viewing EXR files

**macOS/Windows:**

- DJV Imaging: https://dj-view.sourceforge.io/
- OpenImageIO: `oiiotool product.exr -o preview.jpg`

**Photoshop:**

- File → Open → Select .exr
- Adjust exposure in Camera Raw

**Nuke/After Effects:**

- Drag and drop for compositing

### Tone Mapping

Convert HDR → SDR for web:

```bash
python backend/utils/export_exr.py \
  --input product.exr \
  --output product.jpg \
  --tonemap aces \
  --exposure 0.5
```

## Metadata Structure

Example embedded JSON metadata:

```json
{
  "render_date": "2025-12-02T18:30:00Z",
  "fibo_version": "2.3-FAST",
  "scene_json": {
    "camera": {...},
    "lighting": {...}
  },
  "render_time_seconds": 12.4,
  "resolution": "2048x2048"
}
```

## File Naming Convention

```
{sku}_{variant}_{format}.{ext}
```

Examples:

- `SKU-001_var01_32bit.exr`
- `product_shot_16bit.tiff`
- `portrait_rgb_alpha.exr`
