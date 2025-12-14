# 🔑 API Key Setup Instructions

## Current Status

❌ **MOCK RENDERING ACTIVE** - Your backend is copying the same sample image for all renders.

## Why Images Look the Same

The backend is using a placeholder function that just copies `example_render.jpg` to the output folder. This is intentional for testing without API access.

## How to Enable Real FIBO Rendering

### Step 1: Get Your HuggingFace API Token

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name (e.g., "StudioFlow FIBO")
4. Select "Read" permissions
5. Copy the token (starts with `hf_`)

### Step 2: Update .env File

Open `e:\StudioFlow\.env` and replace:

```env
HF_API_TOKEN=hf_your_actual_token_here
```

With your real token:

```env
HF_API_TOKEN=hf_AbCdEfGhIjKlMnOpQrStUvWxYz1234567890
```

### Step 3: Request Access to BRIA Model

1. Go to https://huggingface.co/briaai/BRIA-2.3-FAST
2. Click "Request Access" if required
3. Wait for approval (usually instant for public models)

### Step 4: Update Backend to Use FIBO Client

The backend currently has `FIBOClient` implemented but not connected. To enable:

**Option A: Quick Test (Recommended)**
Install required packages:

```bash
cd e:\StudioFlow
pip install torch diffusers transformers pillow
```

**Option B: Full Integration**
Modify `backend/app.py` to use the FIBO client instead of mock rendering.

---

## Current Rendering Flow

```
User clicks "Render"
    ↓
Frontend calls /render
    ↓
Backend: render_with_fibo()
    ↓
Copies example_render.jpg → output/render_xxx.jpg
    ↓
Returns same image every time
```

## Target Rendering Flow (After Setup)

```
User clicks "Render"
    ↓
Frontend calls /render
    ↓
Backend: FIBOClient.generate()
    ↓
Calls HuggingFace API with your token
    ↓
BRIA FIBO generates unique image
    ↓
Returns new image based on prompt
```

---

## Quick Test: Check if Token Works

After adding your token to `.env`, run:

```bash
cd e:\StudioFlow
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Token:', os.getenv('HF_API_TOKEN')[:10] + '...' if os.getenv('HF_API_TOKEN') else 'NOT FOUND')"
```

Should show: `Token: hf_xxxxxxx...`

---

## Files to Modify for Real Rendering

### `backend/app.py` - Replace mock function

Currently at line 115:

```python
def render_with_fibo(scene_json):
    """MVP stub - just copies example_render.jpg"""
    src = os.path.join(SAMPLES_DIR, "example_render.jpg")
    # ... copies file ...
```

**Change to:**

```python
def render_with_fibo(scene_json):
    """Real FIBO rendering"""
    from backend.model_clients.fibo_client import FIBOClient
    from dotenv import load_dotenv

    load_dotenv()
    client = FIBOClient()

    # Extract prompt from scene_json
    prompt = scene_json.get("scene", {}).get("description", "")
    seed = scene_json.get("scene", {}).get("seed", None)

    # Generate with FIBO
    output_path = client.generate({
        "prompt": prompt,
        "seed": seed,
        "num_inference_steps": 30,
        "guidance_scale": 7.5,
        "width": 1024,
        "height": 1024
    })

    return output_path
```

---

## Summary

✅ **What's Working Now:**

- Frontend → Backend communication
- Image generation (mock/placeholder)
- Version history storage
- Image display

❌ **What's NOT Working:**

- Real FIBO API calls (using mock instead)
- Unique images per prompt (all same sample image)
- Your HF token is not configured

📝 **Next Steps:**

1. Get HuggingFace token from https://huggingface.co/settings/tokens
2. Add token to `.env` file
3. Install: `pip install torch diffusers transformers`
4. Modify `render_with_fibo()` to use `FIBOClient`
5. Restart backend server

**Do you want me to automatically update the backend code to use real FIBO rendering?**
