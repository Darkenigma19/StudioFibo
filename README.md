# StudioFlow

**JSON-native, production-grade visual pipeline built on Bria FIBO**

StudioFlow converts natural-language briefs into validated FIBO JSON scene manifests, enables precise parameter control (camera, lighting, FOV, materials), accepts multimodal ControlNet inputs (sketch/seg/depth), runs renders, and exports professional HDR assets (OpenEXR / 16-bit TIFF). Everything is reproducible (seed + JSON), versioned, and ready for production teams.

![StudioFlow Demo](docs/demo_screenshot.png)

## 🎯 What StudioFlow Does

1. **Natural Language → JSON Translation**: Convert "Product shot of coffee mug, moody lighting, 50mm" into a complete FIBO scene manifest
2. **JSON-Native Editing**: Every parameter is editable through an interactive JSON tree or friendly sliders
3. **Multimodal ControlNet**: Upload sketches, depth maps, or segmentation masks for composition control
4. **Professional Export**: Generate 32-bit OpenEXR and 16-bit TIFF outputs with ACES tone mapping
5. **Full Reproducibility**: Every render is tied to a seed + JSON manifest stored in version history

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Node.js 20+
- (Optional) Access to Bria FIBO model weights via Hugging Face

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/StudioFlow.git
cd StudioFlow

# Run the setup script
bash scripts/setup_dev.sh

# Or manually:
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend/StudioFlow
npm install --legacy-peer-deps
```

### Running the Application

**Terminal 1 - Backend:**

```bash
cd StudioFlow
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**

```bash
cd StudioFlow/frontend/StudioFlow
npm run dev
```

Open http://localhost:5173 in your browser.

## 📖 Getting FIBO Model Weights

See [docs/get_fibo.md](docs/get_fibo.md) for detailed instructions on:

- Requesting access to Bria FIBO on Hugging Face
- Downloading model weights
- Configuring API tokens

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────┐
│   Frontend  │────▶│  Translator  │────▶│ Orchestrator│────▶│   FIBO   │
│  (React UI) │     │  (NL → JSON) │     │  (Pipeline) │     │  Engine  │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────┘
                                                 │
                                                 ▼
                                          ┌─────────────┐
                                          │   Exporter  │
                                          │ (EXR/TIFF)  │
                                          └─────────────┘
```

See [docs/architecture.md](docs/architecture.md) for detailed component diagrams.

## 📁 Project Structure

```
StudioFlow/
├── README.md                      # This file
├── .env.example                   # Environment template
├── LICENSE                        # MIT License
├── demo_video.mp4                 # 3-minute demo video
│
├── docs/                          # Documentation
│   ├── architecture.md            # System architecture
│   ├── get_fibo.md               # FIBO setup guide
│   ├── comfyui_integration.md    # ComfyUI recipes guide
│   ├── hdr_workflow.md           # HDR export workflow
│   ├── next_steps.md             # Roadmap
│   └── file_reference.md         # Per-file descriptions
│
├── schemas/                       # JSON schemas
│   ├── fibo_schema.json          # FIBO manifest schema
│   └── fibo_schema_examples.md   # Schema field docs
│
├── samples/                       # Example manifests
│   ├── product_shot.json         # Product demo
│   ├── portrait.json             # Portrait demo
│   ├── environment.json          # Environment demo
│   ├── sku_batch_template.json   # Batch processing
│   ├── sku_list.csv              # SKU data
│   └── exr_examples/             # Sample outputs
│
├── comfyui-recipes/              # ComfyUI workflows
│   ├── product_with_sketch.json
│   └── portrait_controlnet.json
│
├── backend/                       # FastAPI backend
│   ├── app.py                    # Main API server
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Container config
│   ├── translator/               # NL → JSON translation
│   ├── orchestrator/             # Pipeline orchestration
│   ├── model_clients/            # FIBO integration
│   ├── storage/                  # File storage
│   └── utils/                    # Validation, export
│
├── frontend/                      # React frontend
│   └── StudioFlow/
│       ├── src/
│       │   ├── App.tsx           # Main UI
│       │   └── components/       # UI components
│       ├── package.json
│       └── vite.config.ts
│
├── scripts/                       # Development scripts
│   ├── setup_dev.sh              # Environment setup
│   ├── render_local.sh           # Local render test
│   └── export_examples.sh        # Generate examples
│
├── tests/                         # Test suite
│   ├── test_translator.py
│   ├── test_schema_validation.py
│   ├── test_orchestrator_smoke.py
│   └── test_export_exr.py
│
└── infra/                         # Deployment configs
    ├── docker-compose.yml
    └── aws/deploy.md
```

See [docs/file_reference.md](docs/file_reference.md) for detailed per-file documentation.

## 🎨 Key Features

### 1. Natural Language Translation

```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Product shot of coffee grinder, moody lighting, 85mm"}'
```

### 2. JSON-Native Control

Edit any parameter through the interactive JSON tree or parameter sliders. Every change updates the manifest instantly.

### 3. ControlNet Support

Upload sketches, depth maps, or segmentation masks:

```bash
curl -X POST http://localhost:8000/upload_controlnet \
  -F "file=@sketch.png" \
  -F "kind=sketch" \
  -F "strength=0.8"
```

### 4. Professional Export

Generate HDR outputs with ACES tone mapping:

```python
from backend.utils.export_exr import export_to_exr, apply_tone_mapping

# Export float32 image
export_to_exr(image_array, "output.exr")

# Create display version
display = apply_tone_mapping(image_array, method="aces")
```

### 5. Version History

Every render is saved with its exact JSON manifest and seed for perfect reproducibility.

## 🔧 API Endpoints

| Endpoint             | Method | Description                     |
| -------------------- | ------ | ------------------------------- |
| `/translate`         | POST   | Convert NL prompt to FIBO JSON  |
| `/validate`          | POST   | Validate JSON against schema    |
| `/render`            | POST   | Execute standard render         |
| `/render_controlnet` | POST   | Render with ControlNet guidance |
| `/upload_controlnet` | POST   | Upload ControlNet reference     |
| `/versions`          | GET    | List render history             |

See API documentation: http://localhost:8000/docs

## 🎥 Demo Video

[demo_video.mp4](demo_video.mp4) - 3-minute walkthrough showing:

- Natural language input → JSON generation
- Parameter tweaking (focal length, lighting intensity)
- Before/after comparison slider
- ControlNet sketch upload
- EXR/TIFF export workflow

## 📊 Reproducibility

Every render includes:

- **Seed**: Integer for deterministic generation
- **JSON Manifest**: Complete scene description
- **Timestamp**: ISO 8601 format
- **Version ID**: Unique identifier

Example:

```json
{
  "version_id": "a3f2b9c1",
  "seed": 12345,
  "timestamp": "2025-12-02T10:30:00Z",
  "image_url": "/samples/output/render_a3f2b9c1.jpg",
  "manifest": {
    /* full FIBO JSON */
  }
}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/test_translator.py -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html
```

## 🐳 Docker Deployment

```bash
# Build and run with docker-compose
docker-compose -f infra/docker-compose.yml up

# Or build individually
docker build -t studioflow-backend -f backend/Dockerfile .
docker run -p 8000:8000 studioflow-backend
```

## 🚀 Production Deployment

See [infra/aws/deploy.md](infra/aws/deploy.md) for:

- AWS ECS/Fargate deployment
- S3 storage configuration
- CloudWatch monitoring
- Cost optimization strategies

## 🔮 Roadmap

See [docs/next_steps.md](docs/next_steps.md) for planned features:

- [ ] Real-time FIBO inference integration
- [ ] Batch processing UI
- [ ] Advanced ControlNet composition
- [ ] Cloud rendering queue
- [ ] Blender/Maya plugin export

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Bria AI** for the FIBO foundation model
- **Hugging Face** for model hosting and diffusers library
- **ComfyUI** community for workflow inspiration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built for the Bria FIBO Hackathon 2025**

Demonstrating JSON-native control, professional asset export, and production-ready architecture for next-generation visual content creation.
