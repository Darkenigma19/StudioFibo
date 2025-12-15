import os
import json
import shutil
import uuid
import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from jsonschema import validate, ValidationError
from fastapi import UploadFile, File, Form
from backend.orchestrator.controlnet_adapter import save_upload
from backend.model_clients.fibo_client import FIBOClient
from backend.translator.translator import translate_prompt_to_json, params_to_enhanced_prompt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(os.path.dirname(BASE_DIR), "schemas", "fibo_schema.json")
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")
OUTPUT_DIR = os.path.join(SAMPLES_DIR, "output")
DB_PATH = os.path.join(BASE_DIR, "versions.sqlite")
# Add static mount for uploads (if not already covered by /samples)
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(SCHEMA_PATH, 'r') as f:
    FIBO_SCHEMA = json.load(f)

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS versions (
        id TEXT PRIMARY KEY,
        seed INTEGER,
        timestamp TEXT,
        image_url TEXT,
        json TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

app = FastAPI(title = "StudioFlow - Phase 2 Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/samples", StaticFiles(directory=SAMPLES_DIR), name="samples")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

class NLRequest(BaseModel):
    prompt: str

@app.post("/translate")
async def translate(request: NLRequest):
    """
    Translate natural language prompt to frontend-compatible JSON format.
    Returns parameters matching the frontend RenderParameters interface.
    """
    prompt = request.prompt.strip()
    
    # Use the translator module
    result = translate_prompt_to_json(prompt)
    
    return result

@app.post("/validate")
async def validate_json(payload: dict):
    """
    Validate frontend RenderParameters format.
    Checks for required fields, correct types, and value ranges matching frontend sliders/selects.
    Returns validation status and an enhanced prompt for image generation.
    """
    try:
        # Required fields validation
        required_fields = ["prompt", "focalLength", "yaw", "pitch", "lighting", 
                          "colorPalette", "controlNet", "seed", "resolution", "colorSpace"]
        
        for field in required_fields:
            if field not in payload:
                return {"valid": False, "error": f"Missing required field: {field}"}
        
        # Type validations
        if not isinstance(payload["focalLength"], (int, float)):
            return {"valid": False, "error": "focalLength must be a number"}
        
        if not isinstance(payload["seed"], int):
            return {"valid": False, "error": "seed must be an integer"}
        
        # Range validations (matching frontend sliders)
        if not (12 <= payload["focalLength"] <= 200):
            return {"valid": False, "error": "focalLength must be between 12 and 200"}
        
        if not (-180 <= payload["yaw"] <= 180):
            return {"valid": False, "error": "yaw must be between -180 and 180"}
        
        if not (-90 <= payload["pitch"] <= 90):
            return {"valid": False, "error": "pitch must be between -90 and 90"}
        
        if not (0 <= payload["lighting"] <= 100):
            return {"valid": False, "error": "lighting must be between 0 and 100"}
        
        # Color palette validation (matching frontend select options)
        valid_palettes = ["warm", "cool", "neutral", "cinematic", "vibrant"]
        if payload["colorPalette"] not in valid_palettes:
            return {"valid": False, "error": f"colorPalette must be one of: {', '.join(valid_palettes)}"}
        
        # ControlNet validation
        if "controlNet" in payload:
            cn = payload["controlNet"]
            valid_types = ["none", "sketch", "depth", "canny"]
            if cn.get("type") not in valid_types:
                return {"valid": False, "error": f"controlNet.type must be one of: {', '.join(valid_types)}"}
            
            if "strength" in cn and not (0.0 <= cn["strength"] <= 1.0):
                return {"valid": False, "error": "controlNet.strength must be between 0.0 and 1.0"}
        
        # Color space validation
        valid_color_spaces = ["sRGB", "Adobe RGB", "Display P3"]
        if payload["colorSpace"] not in valid_color_spaces:
            return {"valid": False, "error": f"colorSpace must be one of: {', '.join(valid_color_spaces)}"}
        
        # Generate enhanced prompt from parameters
        enhanced_prompt = params_to_enhanced_prompt(payload)
        
        return {
            "valid": True,
            "enhancedPrompt": enhanced_prompt,
            "message": "Parameters are valid and ready for rendering"
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}

def render_with_fibo(scene_json):
    """
    Real image generation using Stable Diffusion XL via HuggingFace Diffusers.
    Accepts frontend RenderParameters format and converts to enhanced prompt.
    Falls back to mock rendering if SDXL fails to load.
    """
    try:
        # Initialize FIBO client (now using SDXL)
        client = FIBOClient()
        
        # Convert parameters to enhanced prompt for better image generation
        enhanced_prompt = params_to_enhanced_prompt(scene_json)
        seed = scene_json.get("seed", None)
        
        print(f"Original prompt: {scene_json.get('prompt', '')}")
        print(f"Enhanced prompt: {enhanced_prompt}")
        
        # Prepare rendering arguments optimized for SDXL
        render_args = {
            "prompt": enhanced_prompt,  # Use enhanced prompt with all parameters
            "seed": seed,
            "num_inference_steps": 50,  # SDXL works well with 50 steps
            "guidance_scale": 9.0,  # Higher guidance for better quality
            "width": 1024,
            "height": 1024
        }
        
        # Generate image with SDXL
        out_path = client.generate(render_args)
        return out_path
        
    except Exception as e:
        print(f"Warning: SDXL rendering failed: {e}")
        print("Falling back to mock rendering...")
        
        # Fallback to mock rendering
        src = os.path.join(SAMPLES_DIR, "example_render.jpg")
        if not os.path.exists(src):
            raise FileNotFoundError("Sample render image not found.")
        out_name = f"render_{uuid.uuid4().hex[:12]}.jpg"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        shutil.copyfile(src, out_path)
        return out_path
        print("Falling back to mock rendering...")
        
        # Fallback to mock rendering
        src = os.path.join(SAMPLES_DIR, "example_render.jpg")
        if not os.path.exists(src):
            raise FileNotFoundError("Sample render image not found.")
        out_name = f"render_{uuid.uuid4().hex[:12]}.jpg"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        shutil.copyfile(src, out_path)
        return out_path

def render_with_controlnet(scene_json):
    """
    MVP stub for ControlNet rendering.
    In production, this would call ComfyUI or FIBO pipeline with ControlNet.
    """
    src = os.path.join(SAMPLES_DIR, "example_render.jpg")
    if not os.path.exists(src):
        raise FileNotFoundError("Sample render image not found.")
    out_name = f"render_cn_{uuid.uuid4().hex[:12]}.jpg"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    shutil.copyfile(src, out_path)
    return out_path

@app.post("/render")
async def render(scene_json: dict):
    """
    Accepts frontend RenderParameters format and returns an image URL.
    Converts frontend format to SDXL-compatible parameters.
    Saves version metadata to sqlite.
    """
    # Validate required fields
    if "prompt" not in scene_json:
        raise HTTPException(status_code=400, detail="Missing 'prompt' field")
    
    # Extract seed (use existing or generate new)
    seed = scene_json.get("seed", int(datetime.utcnow().timestamp()) % 1000000)

    # Call rendering function with frontend parameters
    try:
        out_path = render_with_fibo(scene_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rendering error: {str(e)}")
    
    # Form public URL path for frontend
    rel_path = os.path.relpath(out_path, BASE_DIR)
    image_url = f"/{rel_path.replace(os.path.sep, '/')}"

    # Save version metadata to sqlite
    vid = uuid.uuid4().hex
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO versions (id, seed, timestamp, image_url, json) VALUES (?, ?, ?, ?, ?)",
              (vid, seed, datetime.utcnow().isoformat(), image_url, json.dumps(scene_json)))
    conn.commit()
    conn.close()

    return {"version_id": vid, "image_url": image_url, "seed": seed}

@app.get("/versions")
async def list_versions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, seed, timestamp, image_url, json FROM versions ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "seed": r[1],
            "timestamp": r[2],
            "image_url": r[3]
        })
    return results

@app.post("/upload_controlnet")
async def upload_controlnet(file: UploadFile = File(...), image_type: str = Form("sketch")):
    """
    Upload controlnet reference image (sketch/depth/canny).
    Returns path to uploaded image for frontend ControlNet panel.
    Validates type matches frontend options: none, sketch, depth, canny.
    """
    # Validate image type matches frontend options
    valid_types = ["sketch", "depth", "canny"]
    if image_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"image_type must be one of: {', '.join(valid_types)}")
    
    # Save file
    saved_rel = save_upload(file.file, file.filename)
    
    # Return format matching frontend expectations
    return {
        "path": saved_rel,
        "filename": file.filename,
        "type": image_type
    }

@app.post("/render_controlnet")
async def render_controlnet(scene_json: dict):
    # scene_json should include controlnet.* fields
    # validate as usual
    try:
        validate(instance=scene_json, schema=FIBO_SCHEMA)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"JSON validation failed: {e}")

    # Here we would translate scene_json.controlnet -> ComfyUI or FIBO pipeline args
    # For Phase3 demo: we call render_with_controlnet which either calls ComfyUI API or emulates effect.
    try:
        out_path = render_with_controlnet(scene_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ControlNet render failed: {e}")
    
    rel_path = os.path.relpath(out_path, BASE_DIR)
    image_url = f"/{rel_path.replace(os.path.sep, '/')}"
    # Save version metadata to sqlite
    vid = uuid.uuid4().hex
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    seed = scene_json.get("scene", {}).get("seed", int(datetime.utcnow().timestamp()) % 100000)
    c.execute("INSERT INTO versions (id, seed, timestamp, image_url, json) VALUES (?, ?, ?, ?, ?);",
              (vid, seed, datetime.utcnow().isoformat(), image_url, json.dumps(scene_json)))
    conn.commit()
    conn.close()
    return {"version_id": vid, "image_url": image_url, "seed": seed}