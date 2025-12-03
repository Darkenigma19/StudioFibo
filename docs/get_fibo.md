# Getting FIBO Model Weights

## Prerequisites

1. **Hugging Face Account**: Create an account at [huggingface.co](https://huggingface.co)
2. **FIBO Access**: Request access to the BRIA-2.3-FAST model

## Step-by-Step Guide

### 1. Request Model Access

Visit the BRIA AI model page:

- Model ID: `briaai/BRIA-2.3-FAST`
- URL: https://huggingface.co/briaai/BRIA-2.3-FAST

Click **"Request Access"** and fill out the form.

### 2. Generate Access Token

Once approved:

1. Go to Settings → Access Tokens
2. Click **"New token"**
3. Name: `studioflow-fibo`
4. Type: **Read**
5. Copy the token (starts with `hf_...`)

### 3. Configure StudioFlow

Add your token to `.env`:

```bash
cp .env.example .env
```

Edit `.env`:

```
HF_TOKEN=hf_your_actual_token_here
MODEL_ID=briaai/BRIA-2.3-FAST
```

### 4. Download Model (Optional)

For offline usage:

```bash
python -c "from huggingface_hub import snapshot_download; snapshot_download('briaai/BRIA-2.3-FAST', use_auth_token='YOUR_TOKEN')"
```

Models are cached in: `~/.cache/huggingface/hub/`

## Using the Model

### Option 1: Auto-Download (Recommended)

StudioFlow will automatically download model weights on first use:

```python
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
    "briaai/BRIA-2.3-FAST",
    use_auth_token=os.getenv("HF_TOKEN")
)
```

### Option 2: Local Path

If pre-downloaded:

```python
pipe = StableDiffusionPipeline.from_pretrained(
    "/path/to/local/model",
    local_files_only=True
)
```

## Troubleshooting

### Access Denied

- Ensure you've been granted access to the model
- Wait 10-15 minutes after approval
- Check token has **read** permissions

### Download Fails

- Check internet connection
- Verify HF_TOKEN in .env
- Ensure sufficient disk space (~10GB)

### CUDA Out of Memory

- Reduce resolution in `.env`: `MAX_RESOLUTION=1024`
- Enable model offloading:

```python
pipe.enable_model_cpu_offload()
```

## Model Specifications

- **Size**: ~5-8 GB
- **Architecture**: Stable Diffusion variant
- **Optimal Resolution**: 1024x1024
- **License**: Check Bria AI terms
