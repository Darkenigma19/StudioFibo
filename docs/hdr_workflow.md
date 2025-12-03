# HDR Workflow Guide

Complete guide to working with High Dynamic Range (HDR) assets exported from StudioFlow, including OpenEXR and 16-bit TIFF files.

## Why HDR Matters for Production

Standard 8-bit images (JPG, PNG) have limited dynamic range:

- **8-bit**: 256 levels per channel (0-255)
- **Limited latitude**: Cannot recover blown highlights or crushed shadows
- **Baked tonemap**: Color grading decisions are permanent

HDR formats preserve the full range captured by the render engine:

- **32-bit float EXR**: Unlimited dynamic range, scene-linear values
- **16-bit TIFF**: 65,536 levels per channel
- **Flexible grading**: Adjust exposure, contrast, color in post without quality loss
- **VFX integration**: Compositing, relighting, color matching

## Supported Export Formats

### OpenEXR (.exr)

**When to use**: Maximum quality, VFX pipelines, color grading, archival

- **Bit depth**: 32-bit float per channel (or 16-bit half-float)
- **Color space**: Scene-linear (no baked tone curve)
- **Metadata**: Embeds render settings, camera data, chromaticity
- **Compression**: Optional (PIZ, ZIP, DWAA)
- **File size**: Large (10-50MB for 4K), compressible

**Tools**: DaVinci Resolve, Nuke, After Effects, Blender, Photoshop (with plugin)

### 16-bit TIFF (.tif/.tiff)

**When to use**: Print workflows, Photoshop retouching, when EXR isn't supported

- **Bit depth**: 16-bit integer per channel (0-65535)
- **Color space**: sRGB or Adobe RGB (configurable)
- **Metadata**: EXIF, IPTC support
- **Compression**: LZW, ZIP (lossless)
- **File size**: Medium (5-20MB for 4K)

**Tools**: Adobe Creative Suite, Capture One, Affinity Photo, GIMP

## Exporting from StudioFlow

### Via API

```python
from backend.utils.export_exr import export_to_exr, export_to_tiff

# After rendering, you receive a float32 numpy array (H, W, 3)
image_float = render_result  # Shape: (1024, 1024, 3), dtype: float32

# Export to OpenEXR (scene-linear)
export_to_exr(
    image_float,
    output_path="output_linear.exr",
    compression="ZIP"  # Options: None, ZIP, PIZ, DWAA
)

# Export to 16-bit TIFF with tone mapping
from backend.utils.export_exr import apply_tone_mapping

image_graded = apply_tone_mapping(image_float, method="aces")
export_to_tiff(
    image_graded,
    output_path="output_display.tif",
    bit_depth=16
)
```

### Via Frontend

1. Render your scene
2. Click **Export** dropdown
3. Choose format:
   - **EXR (Linear)**: Scene-linear float, no tone mapping
   - **EXR (ACES)**: ACES tone-mapped float
   - **TIFF 16-bit**: sRGB tone-mapped integer
   - **JPG Preview**: 8-bit display copy

## Tone Mapping Methods

StudioFlow provides two tone mapping algorithms for converting scene-linear HDR to display-ready images:

### ACES (Academy Color Encoding System)

**Recommended for**: Film, advertising, photo-realistic renders

```python
display_image = apply_tone_mapping(linear_image, method="aces")
```

**Characteristics**:

- Industry-standard filmic curve
- Smooth highlight rolloff
- Preserves color saturation in highlights
- Slightly desaturated shadows (cinematic look)

**Use cases**:

- Product photography for ecommerce
- Marketing materials
- Film/TV production
- When matching live-action footage

### Reinhard

**Recommended for**: Quick previews, web displays, fast iteration

```python
display_image = apply_tone_mapping(linear_image, method="reinhard")
```

**Characteristics**:

- Simple global operator
- Fast computation
- Good for local contrast preservation
- May oversaturate in some cases

**Use cases**:

- Rapid iteration during design
- Web/social media delivery
- When speed > absolute accuracy

## Opening EXR Files

### DaVinci Resolve (Recommended for Grading)

1. **Import**: Media Pool → Right-click → Import → Select EXR
2. **Set Color Space**:
   - Project Settings → Color Management
   - Input Color Space: `Linear`
   - Timeline Color Space: `Rec.709` or `DCI-P3`
   - Output Color Space: `Rec.709-Gamma 2.4`
3. **Grade**: Use Color page tools (lift/gamma/gain, curves, LUTs)
4. **Export**: Deliver page → Format: `ProRes 422 HQ` or `H.264`

**Why Resolve**:

- Free version is powerful
- Proper ACES color pipeline
- Industry-standard grading tools
- GPU-accelerated playback

### Adobe Photoshop

1. **Install Plugin**: Download ProEXR plugin (free)
2. **Open**: File → Open → Select EXR
3. **Linear Warning**: Photoshop will warn "image is linear" → Choose `Convert to sRGB`
4. **Edit**: Use Curves, Levels, Camera Raw Filter for grading
5. **Export**: File → Export → TIFF or PSD

**Note**: Photoshop assumes sRGB workflow by default. Use 32-bit mode for full precision.

### Blender

1. **Import**: Compositor → Add → Input → Image → Load EXR
2. **View Transform**: Set to `Filmic` or `Standard`
3. **Composite**: Add color correction nodes (Color Balance, Curves, etc.)
4. **Output**: Render → Output → Choose format (EXR, PNG, TIFF)

**Advantage**: Full scene-linear compositing pipeline, free and open-source.

### Nuke (VFX Production)

1. **Read Node**: Create → Image → Read → Select EXR
2. **Colorspace**: Set to `linear` (usually auto-detected)
3. **Grade**: Add Grade, ColorCorrect, or LUT nodes
4. **Write Node**: Output to delivery format

**Use case**: Professional VFX pipelines, multi-layer compositing.

## Working with 16-bit TIFF

### Capture One

1. **Import**: File → Import Images → Select TIFF
2. **Profile**: Choose `Adobe RGB` or `ProPhoto RGB` for wide gamut
3. **Edit**: Exposure, contrast, color grading tools
4. **Export**: High-quality JPG or TIFF for delivery

**Best for**: Commercial photography retouching.

### Affinity Photo

1. **Open**: File → Open → TIFF (auto-detects 16-bit)
2. **Adjustments**: Use Adjustment Layers (Curves, HSL, etc.)
3. **Export**: File → Export → Choose format

**Advantage**: One-time purchase, no subscription.

## Color Space Considerations

### Scene-Linear (EXR default)

- **Values**: No gamma correction, direct light intensity
- **Range**: Can exceed 1.0 (super-whites)
- **Appearance**: Looks dark when viewed directly
- **Workflow**: Must apply view transform/LUT for display

### sRGB (TIFF default)

- **Values**: Gamma 2.2 baked in
- **Range**: Clamped to 0.0-1.0
- **Appearance**: Correct for web/monitors
- **Workflow**: Edit directly, what you see is what you get

### Recommendation

- **Archive/Master**: Always keep scene-linear EXR
- **Delivery**: Convert to sRGB TIFF or JPG with tone mapping
- **Grading**: Work in linear, apply LUT/transform at the end

## Metadata Embedded in Exports

StudioFlow embeds the following metadata in EXR/TIFF exports:

```python
{
  "StudioFlow:Version": "1.0.0",
  "StudioFlow:Seed": 12345,
  "StudioFlow:RenderTime": "2025-12-02T10:30:00Z",
  "StudioFlow:FIBO_JSON": "{ full JSON manifest }",
  "Camera:FocalLength": 50,
  "Camera:Aperture": 2.8,
  "Lighting:KeyIntensity": 1.0
}
```

**Use cases**:

- Reproduce exact render from metadata
- Batch processing based on camera settings
- Asset management and search

**Access metadata**:

```python
import OpenEXR
import Imath

exr = OpenEXR.InputFile("output.exr")
header = exr.header()
print(header["StudioFlow:Seed"])
```

## Production Workflow Example

### Step 1: Render Scene

```bash
curl -X POST http://localhost:8000/render \
  -H "Content-Type: application/json" \
  -d @samples/product_shot.json
```

### Step 2: Export HDR Master

```python
# Export scene-linear EXR for archival
export_to_exr(render_output, "masters/product_v001.exr")
```

### Step 3: Create Display Versions

```python
# ACES tone-mapped TIFF for retouching
aces_graded = apply_tone_mapping(render_output, method="aces")
export_to_tiff(aces_graded, "delivery/product_v001_aces.tif", bit_depth=16)

# 8-bit JPG for web
from PIL import Image
import numpy as np

jpg_preview = (np.clip(aces_graded, 0, 1) * 255).astype(np.uint8)
Image.fromarray(jpg_preview).save("web/product_v001.jpg", quality=95)
```

### Step 4: Grade in DaVinci Resolve

1. Import `product_v001_aces.tif`
2. Apply client LUT or custom grade
3. Export ProRes for video or TIFF for print

### Step 5: Retouch in Photoshop (if needed)

1. Open TIFF in Photoshop
2. Clean up, add overlays, text
3. Export final JPG/PNG

## Troubleshooting

### "EXR looks too dark"

**Cause**: Viewing scene-linear image without display transform
**Solution**: Apply ACES or Reinhard tone mapping, or set viewer to `Linear → sRGB` transform

### "Colors look washed out"

**Cause**: Incorrect color space interpretation
**Solution**: Ensure input is tagged as `linear` and output is `sRGB` or `Rec.709`

### "File size too large"

**Cause**: Uncompressed EXR
**Solution**: Enable ZIP or DWAA compression (10-30% of original size)

### "Photoshop won't open EXR"

**Cause**: Missing plugin
**Solution**: Install ProEXR from fnordware.com

## Best Practices

1. **Always keep the linear EXR master**: You can recreate any delivery format from it
2. **Use ACES for client-facing work**: Industry standard, predictable results
3. **Tag color spaces correctly**: Prevents "double gamma" errors
4. **Embed metadata**: Saves hours when recreating renders months later
5. **Use 16-bit TIFF as intermediate**: Good balance of quality and compatibility
6. **Version your exports**: `product_v001.exr`, `product_v002.exr`, etc.

## Further Reading

- [ACES Documentation](https://www.oscars.org/science-technology/aces)
- [OpenEXR Technical Introduction](https://www.openexr.com)
- [Color Management in VFX](https://chrisbrejon.com/cg-cinematography/chapter-1-5-academy-color-encoding-system-aces/)

---

For questions or issues with HDR workflow, see [docs/next_steps.md](next_steps.md) or open a GitHub issue.
