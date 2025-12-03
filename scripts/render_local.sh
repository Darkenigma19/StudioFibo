#!/bin/bash
# Quick local render test script

set -e

echo "🎨 Running local render test..."

# Activate venv
source ../venv/bin/activate 2>/dev/null || . ../venv/Scripts/activate

# Create test JSON
cat > /tmp/test_render.json << 'EOF'
{
  "scene": {
    "description": "Simple product test render",
    "seed": 42
  },
  "camera": {
    "lens": {"focal_length_mm": 50, "aperture": 5.6}
  },
  "lighting": {
    "key": {"type": "softbox", "intensity": 1.0},
    "ambient": {"intensity": 0.5}
  },
  "post_process": {
    "export": {"format": "jpg"}
  }
}
EOF

# Call API
echo "Sending render request..."
curl -X POST http://localhost:8000/render \
  -H "Content-Type: application/json" \
  -d @/tmp/test_render.json \
  | python3 -m json.tool

echo ""
echo "✅ Render complete! Check backend/samples/output/"
