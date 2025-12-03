#!/bin/bash
# Export sample renders to EXR/TIFF format

set -e

echo "📤 Exporting renders to professional formats..."

source ../venv/bin/activate 2>/dev/null || . ../venv/Scripts/activate

SAMPLES_DIR="../backend/samples/output"
EXR_DIR="../samples/exr_examples"

mkdir -p "$EXR_DIR"

# Find all rendered JPEGs
for jpg in "$SAMPLES_DIR"/*.jpg; do
    if [ -f "$jpg" ]; then
        filename=$(basename "$jpg" .jpg)
        
        echo "Processing $filename..."
        
        # Export to 32-bit EXR
        python3 -c "
from backend.utils.export_exr import export_to_exr, export_to_tiff
import sys

jpg_path = '$jpg'
exr_path = '$EXR_DIR/${filename}_32bit.exr'
tiff_path = '$EXR_DIR/${filename}_16bit.tiff'

metadata = {
    'software': 'StudioFlow FIBO',
    'source_file': '$filename.jpg'
}

export_to_exr(jpg_path, exr_path, bit_depth=32, metadata=metadata)
export_to_tiff(jpg_path, tiff_path, bit_depth=16)

print(f'✓ Exported {exr_path}')
print(f'✓ Exported {tiff_path}')
"
    fi
done

echo ""
echo "✅ Export complete! Files saved to $EXR_DIR"
ls -lh "$EXR_DIR"
