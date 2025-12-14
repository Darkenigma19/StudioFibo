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
    Simple rule-based translator for Phase 2 MVP.
    This returns a deterministic JSON manifest from the prompt.
    Replace with LLM translator later.
    """
    prompt = request.prompt.strip()
    # Very simple rule-based translation
    focal = 35
    if "50mm" in prompt or "50 mm" in prompt or "50mm," in prompt:
        focal = 50
    if "85mm" in prompt or "85 mm" in prompt or "85mm," in prompt:
        focal = 85

    # checky for "moody" -> darker ambient
    ambient = 0.1 if "moody" in prompt.lower() else 0.2

    json_out = {
        "scene": {"description": prompt, "seed": 12345},
        "camera": {
            "lens": {"focal_length_mm": focal, "aperture": 2.2},
            "position": {"x": 0.0, "y": 0.6, "z": 1.2},
            "rotation": {"pitch": -8, "yaw": 0, "roll": 0},
            "fov_degrees": 45
        },
        "lighting": {
            "key": {"type": "softbox", "intensity": 1.0, "direction": {"x": -0.6, "y": 0.9, "z": -0.8}},
            "rim": {"type": "spot", "intensity": 0.6, "color": "#ffd9b3"},
            "ambient": {"intensity": ambient}
        },
        "controlnet": {"sketch_guidance": {"enabled": False}},
        "post_process": {"export": {"format": "jpg"}}
    }

    try:
        validate(instance=json_out, schema=FIBO_SCHEMA)
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Generated JSON failed schema validation: {e.message}")
    return json_out

@app.post("/validate")
async def validate_json(payload: dict):
    try:
        validate(instance=payload, schema=FIBO_SCHEMA)
        return {"valid": True}
    except ValidationError as e:
        return {"valid": False, "error": e.message}

def render_with_fibo(scene_json):
    """
    Real FIBO rendering using HuggingFace Diffusers.
    Falls back to mock rendering if FIBO client fails to load.
    """
    try:
        # Initialize FIBO client
        client = FIBOClient()
        
        # Extract parameters from scene_json
        prompt = scene_json.get("scene", {}).get("description", "")
        seed = scene_json.get("scene", {}).get("seed", None)
        
        # Prepare rendering arguments
        render_args = {
            "prompt": prompt,
            "seed": seed,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "width": 1024,
            "height": 1024
        }
        
        # Generate image with FIBO
        out_path = client.generate(render_args)
        return out_path
        
    except Exception as e:
        print(f"Warning: FIBO rendering failed: {e}")
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
    Accepts the validated FIBO JSON and returns an image URL.
    Ensures 'scene.seed' exists; uses it for reproducibility
    Saves version metadata to sqlite.
    """
    # Validate schema first
    try:
        validate(instance=scene_json, schema=FIBO_SCHEMA)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"JSON schema validation error: {e.message}")
    
    # Ensure seed
    seed = None
    try:
        seed = scene_json["scene"].get("seed", None)
    except Exception:
        seed =None

    if seed is None:
        # if no seed, assign deterministic seed
        # For demo, use current timestamp truncated
        seed = int(datetime.utcnow().timestamp()) % 1000000
        scene_json.setdefault("scene", {})["seed"] = seed

    # Call rendering function (stub)
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
async def upload_controlnet(file: UploadFile = File(...), kind: str = Form("sketch"), strength: float = Form(0.8)):
    """
    Upload controlnet reference image (sketch/depth/seg). Returns mapped controlnet manifest:
      {
        "controlnet": {
           "type": "sketch",
           "image_ref": "/uploads/xxx.png",
           "strength": 0.8
         }
      }
    """
    # save file
    saved_rel = save_upload(file.file, file.filename)
    # Build controlnet snippet for JSON
    cn = {
        "controlnet": {
            "type": kind,
            "image_ref": saved_rel,
            "strength": float(strength),
            "enabled": True
        }
    }
    return cn

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