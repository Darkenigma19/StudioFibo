# File Reference Guide

Complete reference for every file and folder in the StudioFlow repository. Use this as the canonical map for documentation, onboarding teammates, and submission review.

## Top-level Files

### .gitignore

Ignore node modules, virtualenvs, build artifacts, and secret files so you don't commit unnecessary or sensitive files.

### .gitattributes

Configure Git LFS handling for large assets (EXR/TIFF, sample renders) so repo remains manageable.

### .env.example

Template for environment variables (`HF_API_TOKEN`, `FIBO_MODEL_ID`, `COMFYUI_URL`). Shows which secrets/configs are required while preventing accidental commits.

### LICENSE

Project license (MIT) — required for open-source clarity and judge confidence.

### README.md

The primary project entry point: overview, quickstart, where to get Bria/FIBO weights, how to run, submission text, and pointers to the demo video. **This is what judges will read first.**

### demo_video.mp4

The 3-minute demonstration video for the hackathon submission — shows the end-to-end pipeline and highlights novelty.

## docs/ — Documentation & Guidance

### docs/architecture.md

Component diagrams and explanation of data flow (frontend → agent → orchestrator → model → exporter). Useful for judges who want architecture depth.

### docs/get_fibo.md

Step-by-step instructions for obtaining FIBO weights from Hugging Face and any license/access steps required.

### docs/comfyui_integration.md

How to import and run the ComfyUI recipes included in the repo and how JSON placeholders map to nodes.

### docs/hdr_workflow.md

How to open EXR/TIFF in grading tools, why ACES matters, and recommended workflows for judges/production.

### docs/next_steps.md

Roadmap and extension ideas (replace stubs with real inference, scale performance, add CI renders).

### docs/file_reference.md

**This file** — per-file explanation of the entire repository structure.

## schemas/ — JSON Schemas & Examples

### schemas/fibo_schema.json

The authoritative JSON Schema for all FIBO manifests used by StudioFlow. Enforces required fields, types, and helps UI autocomplete/validation. **Central for reproducibility and correctness.**

### schemas/fibo_schema_examples.md

Human-readable commentary on schema fields, intended values, and example JSON snippets (helps judges & integrators understand fields like `camera`, `lighting`, `controlnet`, `post_process`).

## samples/ — Sample Manifests & Assets

### samples/product_shot.json

A fully populated example manifest (seeded) for the product-shot demo. Judges can paste this into the UI to reproduce outputs.

### samples/portrait.json

Example manifest for a portrait workflow (depth/pose params included).

### samples/environment.json

Example for environmental / scene renders.

### samples/sku_batch_template.json & samples/sku_list.csv

Template and CSV for the batch/template engine demo (generate variants for SKUs). Demonstrates agentic batch generation.

### samples/example_render.jpg

Placeholder sample image used by backend stubs so frontend preview works without GPU/model access.

### samples/exr_examples/

Directory for EXR/TIFF outputs produced by the exporter. Use Git LFS if you commit any sample EXRs.

## comfyui-recipes/ — Reproducible Recipes for ControlNet Integration

### comfyui-recipes/product_with_sketch.json

A templated ComfyUI recipe showing how to feed `controlnet.image_ref` and `strength` into a ControlNet + FIBO inference pipeline. Judges can import it into ComfyUI and supply the same assets to reproduce results.

### comfyui-recipes/portrait_controlnet.json

Variant for portrait workflows (depth + pose guidance). Clear placeholders show what the orchestrator will replace at runtime.

## frontend/ — User Interface (React)

### frontend/StudioFlow/package.json & vite.config.ts

Frontend package manifest and dev server configuration.

### frontend/StudioFlow/src/main.tsx

App bootstrap and client entrypoint that mounts the React app.

### frontend/StudioFlow/src/App.tsx

The main demo page: prompt input, Translate/Render buttons, versions panel, JSON editor, parameter controls, ControlNet panel, and preview (before/after). **This is the judge-facing UI.**

### frontend/StudioFlow/src/components/JsonEditor.tsx

Editable JSON tree (uses `react-json-view`) that lets users edit any field in the FIBO manifest inline — key for demonstrating JSON-native control.

### frontend/StudioFlow/src/components/ParamControls.tsx

Friendly sliders and inputs mapped to common pro parameters (focal length, yaw, key intensity, color palette). Each control edits the JSON manifest; used in the single-parameter disentanglement demo.

### frontend/StudioFlow/src/components/CompareSlider.tsx

The before/after slider component that visually proves an edit only changed one aspect (shows previous render vs current render).

### frontend/StudioFlow/src/components/SketchUploader.tsx

UI for uploading sketches/seg/depth maps to be used as ControlNet guidance. Sends multipart data to the backend.

### frontend/StudioFlow/src/components/ControlNetPanel.tsx

Shows uploaded controlnet mapping, allows setting strength and type, merges controlnet manifest into the scene JSON.

### frontend/StudioFlow/public/

Static files for the frontend (favicon, etc.).

## backend/ — API, Orchestrator, Model Clients

### backend/requirements.txt

Python packages required by the backend (FastAPI, uvicorn, jsonschema, pillow, numpy, etc.). Judges or CI will use this to recreate the environment.

### backend/Dockerfile

Optional containerization for convenience and reproducibility.

### backend/app.py

**Central FastAPI application** and the main orchestrator endpoints:

- `POST /translate` — NL → FIBO JSON translator (rule-based in MVP; swap to LLM wrapper later)
- `POST /validate` — validate arbitrary JSON against `schemas/fibo_schema.json`
- `POST /render` — accept JSON and run render path (calls `render_with_fibo`)
- `POST /upload_controlnet` — accepts multipart file upload and returns a controlnet manifest entry (image_ref + strength)
- `POST /render_controlnet` — render path that honors controlnet entries
- `GET /versions` — list past renders (id, timestamp, image_url, json_preview)

This file glues together validation, storage, model calls (or stubs), and versioning.

### backend/translator/translator.py

The NL → JSON translator module. In Phase 1 it contains a deterministic rule-based translator for speed/reproducibility; later it will wrap the Bria LLM translator or your own LLM call to produce more sophisticated JSON manifests.

### backend/translator/templates/

Jinja templates or mapping rules for generating JSON manifests from structured inputs.

### backend/orchestrator/render_orchestrator.py

The layer that takes validated JSON, translates it into pipeline arguments (seed, controlnet maps, width/height, color depth), and calls the model client or ComfyUI. Collates outputs and triggers post-processing.

### backend/orchestrator/controlnet_adapter.py

Maps uploaded images + JSON keys into the exact controlnet node inputs your pipeline/ComfyUI expects. Responsible for saving uploaded files and returning a JSON snippet like:

```json
{
  "controlnet": {
    "type": "sketch",
    "image_ref": "/backend/uploads/...",
    "strength": 0.8,
    "enabled": true
  }
}
```

### backend/model_clients/fibo_client.py

The wrapper that interacts with Bria/FIBO model. Responsibilities:

- Construct the diffusers/Bria pipeline inputs from the FIBO JSON (seed, prompt, controlnet maps)
- Call the model (local or HF Hub) and return either an image file path or a float32 numpy image (H×W×3) when HDR is supported
- Handle batching and minor retries

_(For hack demo you can stub this to copy a sample image; for final submission, this is where real inference hooks live.)_

### backend/storage/store.py

Simple wrapper around local filesystem or S3-compatible storage to save renders, EXR/TIFF outputs, and manage URLs returned to frontend.

### backend/storage/versions.sqlite

SQLite DB (created at runtime) that stores versions: `id`, `seed`, `timestamp`, `image_url`, and JSON manifest. Enables reproducibility and version browsing in the UI.

### backend/utils/validate_json.py

Helper function that wraps `jsonschema.validate()` and returns friendly error messages for the frontend.

### backend/utils/export_exr.py

The HDR exporter and tone-mapping utilities:

- Save float32 arrays to OpenEXR when available
- Provide 16-bit TIFF fallback and 8-bit preview generation
- Tone mapping functions: ACES approximation and Reinhard

Used by orchestrator after model inference to produce pro assets.

## scripts/ — Helper Dev Scripts

### scripts/setup_dev.sh

Bootstraps a dev environment: create venv, install backend deps, install frontend deps. Useful for teammates and judges wishing to reproduce the environment.

### scripts/render_local.sh

Quick script that runs a single low-res render (calls `app.py` endpoints) for CI or local smoke tests.

### scripts/export_examples.sh

Calls `export_exr.py` on an example float file or on the last rendered result to produce EXR/TIFF outputs used in the submission.

## tests/ — Unit & Smoke Tests

### tests/test_translator.py

Unit tests for the NL→JSON translator ensuring popular prompt templates produce valid manifests.

### tests/test_schema_validation.py

Ensures sample JSONs validate against `schemas/fibo_schema.json`.

### tests/test_orchestrator_smoke.py

Smoke tests that call `/render` and check that a file is written and a DB version entry is created.

### tests/test_export_exr.py

Tests the EXR/TIFF exporter on a synthetic float array so CI verifies the exporter works across environments.

## infra/ — Optional Deployment Helpers

### infra/docker-compose.yml

Compose file to run frontend, backend, and optionally ComfyUI for demo machines.

### infra/aws/deploy.md

Notes and scripts for deploying the stack to a cloud provider (S3 for storage, Cloud Run or ECS for compute).

## .github/workflows/ — CI / Smoke Checks

### .github/workflows/ci.yml

Lint + unit tests + schema validation run on PRs so repo health is visible to judges.

### .github/workflows/smoke-render.yml

Optional: spin a tiny container that runs a low-res render using stubbed model and ensures endpoints are healthy; useful to demonstrate reproducibility.

---

## How Each File Contributes to Project Goals

### Reproducibility

`schemas/*`, `samples/*`, `versions.sqlite`, `README.md`, and stored JSON manifests provide the exact inputs for a render so judges can reproduce results deterministically.

### Demonstrability

`frontend/*`, `demo_video.mp4`, `comfyui-recipes/*` create the show-stopping UI & playback judges want to see (prompt → JSON → render → tweak → before/after).

### Novelty & Technical Depth

`export_exr.py` (HDR export), `controlnet_adapter.py` (multimodal composition lock), `model_clients/fibo_client.py` (integration with Bria FIBO) show the technical maturity judges prize.

### Production-readiness

`orchestrator/*`, `storage/store.py`, `infra/*`, and `docs/*` explain how to scale and integrate StudioFlow into real pipelines (ecommerce photography, marketing, VFX).

### Reliability for the Hack

Stubs in `app.py` and `render_with_controlnet` let you demo without heavy GPU resources while providing clear hooks to swap in the real FIBO pipeline later.

---

## Final Note

Put this file reference in your documentation and link it from README.md. It helps judges and contributors quickly understand the repo and speeds code review.

During the demo:

- Open `samples/product_shot.json` to show reproducibility
- Open `frontend/src/App.tsx` to demonstrate the UI flow
- Open `comfyui-recipes/product_with_sketch.json` to show ComfyUI integration
- Open `samples/exr_examples/` to show pro assets

As you replace stubs with real FIBO inference, update `backend/model_clients/fibo_client.py` and note the commit in README.md for reproducibility.
