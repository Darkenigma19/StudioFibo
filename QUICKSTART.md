# StudioFlow - Quick Start Guide

**Get StudioFlow running in 5 minutes**

## ✅ Prerequisites Check

Before starting, ensure you have:

- [ ] Python 3.13+ installed (`python --version`)
- [ ] Node.js 20+ installed (`node --version`)
- [ ] pip and npm available
- [ ] Git (optional, for cloning)

## 🚀 Installation Steps

### Option 1: Automated Setup (Recommended)

```bash
cd StudioFlow
bash scripts/setup_dev.sh
```

This will:

1. Create Python virtual environment
2. Install backend dependencies
3. Install frontend dependencies
4. Create necessary directories

### Option 2: Manual Setup

**Backend:**

```bash
cd StudioFlow/backend
pip install -r requirements.txt
```

**Frontend:**

```bash
cd StudioFlow/frontend/StudioFlow
npm install --legacy-peer-deps
```

## 🎯 Running the Application

### Start Backend Server

```bash
# From StudioFlow root directory
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

**Expected output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Application startup complete.
```

### Start Frontend Server

**In a new terminal:**

```bash
cd StudioFlow/frontend/StudioFlow
npm run dev
```

**Expected output:**

```
VITE v7.2.6  ready in 1358 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

## 🌐 Access the Application

Open your browser and navigate to:

- **Frontend UI:** http://localhost:5173
- **Backend API Docs:** http://localhost:8000/docs

## ✨ First Steps

### 1. Translate a Prompt

```
Try: "Product shot of coffee mug, moody lighting, 50mm"
```

Click **Translate → JSON** to see the generated FIBO manifest.

### 2. Edit Parameters

Use the **Parameter Controls** sliders to adjust:

- Focal length (24mm - 200mm)
- Camera pitch/yaw
- Lighting intensity
- Aperture

### 3. Upload ControlNet (Optional)

1. Scroll to **ControlNet Upload**
2. Select image type (sketch, depth, seg, pose)
3. Choose your conditioning image
4. Set strength (0.0 - 1.0)
5. Click **Upload ControlNet**

### 4. Render

Click **Render** to generate the image.
_(Currently uses mock rendering; see below for FIBO model setup)_

### 5. Compare Versions

Use the **Before/After** slider to compare renders side-by-side.

## 📊 API Testing (Optional)

Test the backend directly:

```bash
# Translate prompt
curl -X POST http://127.0.0.1:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Product shot of coffee grinder"}'

# Validate JSON
curl -X POST http://127.0.0.1:8000/validate \
  -H "Content-Type: application/json" \
  -d @samples/product_shot.json

# List versions
curl http://127.0.0.1:8000/versions
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# FIBO Model Configuration
HF_API_TOKEN=your_huggingface_token_here
FIBO_MODEL_ID=briaai/FIBO

# Storage Backend (local or s3)
STORAGE_BACKEND=local

# S3 Configuration (if using S3)
AWS_BUCKET_NAME=your-bucket
AWS_REGION=us-east-1

# ComfyUI (optional)
COMFYUI_URL=http://localhost:8188
```

### Using Real FIBO Model

See [docs/get_fibo.md](../docs/get_fibo.md) for:

1. Requesting FIBO access on HuggingFace
2. Downloading model weights
3. Configuring API tokens
4. Enabling GPU inference

## 🐛 Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'orchestrator'`

**Fix:** Run from StudioFlow root directory, not backend/:

```bash
cd StudioFlow  # Not backend!
python -m uvicorn backend.app:app --reload
```

### Frontend won't install dependencies

**Error:** `ERESOLVE unable to resolve dependency tree`

**Fix:** Use `--legacy-peer-deps` flag:

```bash
npm install --legacy-peer-deps
```

### Port already in use

**Error:** `Address already in use: 8000`

**Fix:** Kill existing process or use different port:

```bash
# Kill process on port 8000 (Windows)
Get-Process | Where-Object {$_.Name -eq "python"} | Stop-Process -Force

# Or use different port
uvicorn backend.app:app --port 8001
```

### Cannot access uploaded images

**Error:** `404 Not Found` for `/uploads/xxx.png`

**Fix:** Ensure static file mounting in `backend/app.py`:

```python
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
```

### CORS errors

**Error:** `Access to fetch blocked by CORS policy`

**Fix:** Backend already configured with permissive CORS. Ensure:

1. Backend is running
2. Frontend is accessing `http://localhost:8000` (not `127.0.0.1`)

## 📦 Docker Deployment (Alternative)

Run entire stack with Docker:

```bash
cd StudioFlow
docker-compose -f infra/docker-compose.yml up
```

Access:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

## 🧪 Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_translator.py -v

# With coverage
pytest tests/ --cov=backend --cov-report=html
```

## 📚 Next Steps

- **Explore samples:** Check `samples/` directory for example JSON manifests
- **Read docs:** See `docs/architecture.md` for system overview
- **ComfyUI integration:** See `docs/comfyui_integration.md` for workflows
- **HDR export:** See `docs/hdr_workflow.md` for professional output
- **Production deployment:** See `infra/aws/deploy.md` for cloud setup

## 🆘 Need Help?

1. Check [docs/file_reference.md](../docs/file_reference.md) for complete project structure
2. Review API docs: http://localhost:8000/docs
3. Examine sample JSONs in `samples/` directory
4. Open GitHub issue with:
   - OS and versions (Python, Node.js)
   - Error message
   - Steps to reproduce

## 🎉 Success Criteria

You know it's working when:

- ✅ Backend responds to http://127.0.0.1:8000/versions
- ✅ Frontend loads at http://localhost:5173
- ✅ Translating a prompt generates valid JSON
- ✅ Rendering creates a new version entry
- ✅ Before/after slider shows images

---

**Happy rendering! 🎨**

For the complete hackathon submission, see `README.md` in the root directory.
