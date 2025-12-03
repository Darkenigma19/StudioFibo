# StudioFlow Architecture

## System Overview

StudioFlow is a three-tier architecture connecting natural language inputs to FIBO rendering outputs:

```
┌─────────────────┐
│  Natural Lang   │
│     Prompt      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Translator    │ ← LLM/Rule-based NL→JSON
│    (Backend)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  JSON Schema    │ ← Validated FIBO manifest
│   Validation    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Orchestrator   │ ← Maps JSON → Pipeline args
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FIBO Engine    │ ← HuggingFace Diffusers
│  (Bria AI)      │   or ComfyUI integration
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Rendered Image │
│   + Metadata    │
└─────────────────┘
```

## Component Flow

### 1. Frontend (React + TypeScript)

- **PromptInput**: Natural language text area
- **JsonEditor**: Real-time JSON editor with schema validation
- **ParamControls**: Sliders for camera/lighting parameters
- **RenderPreview**: Image gallery with before/after comparison
- **BatchUploader**: CSV-based batch SKU processing

### 2. Backend (FastAPI)

#### Translator Module

- Converts natural language → structured JSON
- Uses LLM wrapper (GPT/Claude) or rule-based mapping
- Validates against JSON schema

#### Orchestrator Module

- Maps JSON manifest → rendering pipeline arguments
- Handles ControlNet integration
- Manages batch processing

#### Model Clients

- **fibo_client.py**: Direct HuggingFace Diffusers integration
- **comfyui_adapter**: ComfyUI workflow mapping

#### Storage

- SQLite for version history
- S3/Local file system for images
- EXR/TIFF export with metadata

### 3. Data Flow

```
User Input → Translator → Validator → Orchestrator → FIBO → Storage → UI
     ↑                                                              │
     └──────────────────── Feedback Loop ────────────────────────┘
```

## Key Design Decisions

### JSON Schema as Single Source of Truth

- All components validate against `fibo_schema.json`
- Enables version control and backward compatibility
- Frontend autocomplete from schema

### Modular Orchestrator

- Swappable backends (HF Diffusers, ComfyUI, etc.)
- ControlNet as optional enhancement
- Batch processing through same pipeline

### Version Control

- Every render stored with:
  - Input JSON
  - Seed for reproducibility
  - Timestamp
  - Generated image URL

## Scalability Considerations

- **Async rendering**: FastAPI async endpoints
- **Queue system**: Ready for Celery/Redis integration
- **CDN integration**: S3 with CloudFront
- **Horizontal scaling**: Stateless API design
