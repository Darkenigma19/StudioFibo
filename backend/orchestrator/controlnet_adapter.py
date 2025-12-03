import os , uuid ,shutil
from PIL import Image

# Get the backend directory (parent of orchestrator)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload(fileobj, filename):
    """
    fileobj: starlette UploadFile.file-like object or path
    returns relative path from repo root to saved file (for API use)
    """
    ext = os.path.splitext(filename)[1].lower() or ".png"
    out_name = f"upload_{uuid.uuid4().hex[:12]}{ext}"
    out_path = os.path.join(UPLOAD_DIR, out_name)
    # fileobj may be SpooledTemporaryFile or a path
    if hasattr(fileobj,"read"):
        with open(out_path,"wb") as out_file:
            shutil.copyfileobj(fileobj,out_file)
    else:
        # it is a path
        shutil.copyfile(fileobj,out_path)
    # Optically  normalize size for ControlNet models
    try:
        im = Image.open(out_path)
        im = im.convert("RGB")
        im.thumbnail((512,512),Image.LANCZOS)
        im.save(out_path)
    except Exception as e:
        print(f"Warning: could not process image {out_path}: {e}")

    rel = os.path.relpath(out_path,BASE_DIR)
    return f"/{rel.replace(os.path.sep,'/')}"