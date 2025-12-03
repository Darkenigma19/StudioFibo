"""
Render Orchestrator

Builds pipeline arguments and invokes FIBO model or ComfyUI.
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime


class RenderOrchestrator:
    """Coordinates rendering pipeline execution."""
    
    def __init__(self, use_comfyui: bool = False):
        self.use_comfyui = use_comfyui
        
    def prepare_render_args(self, scene_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert FIBO JSON manifest to rendering pipeline arguments.
        
        Args:
            scene_json: Validated FIBO JSON structure
            
        Returns:
            Dict of arguments for the rendering backend
        """
        args = {
            "prompt": scene_json["scene"]["description"],
            "seed": scene_json["scene"].get("seed", int(datetime.utcnow().timestamp()) % 1000000),
            "width": 1024,
            "height": 1024,
            "num_inference_steps": int(os.getenv("DEFAULT_STEPS", "30")),
            "guidance_scale": float(os.getenv("DEFAULT_GUIDANCE_SCALE", "7.5")),
        }
        
        # Map camera parameters
        if "camera" in scene_json:
            focal = scene_json["camera"].get("lens", {}).get("focal_length_mm", 50)
            # Adjust CFG based on focal length
            args["guidance_scale"] = self._focal_to_cfg(focal)
            
        # Map lighting to prompt modifiers
        if "lighting" in scene_json:
            ambient = scene_json["lighting"].get("ambient", {}).get("intensity", 0.5)
            if ambient < 0.3:
                args["prompt"] += ", dramatic moody lighting"
            elif ambient > 0.7:
                args["prompt"] += ", bright even lighting"
                
        # Add ControlNet args if enabled
        if scene_json.get("controlnet", {}).get("enabled"):
            args["controlnet_image"] = scene_json["controlnet"]["image_ref"]
            args["controlnet_strength"] = scene_json["controlnet"].get("strength", 0.8)
            args["controlnet_type"] = scene_json["controlnet"].get("type", "sketch")
            
        return args
    
    def _focal_to_cfg(self, focal_length: int) -> float:
        """
        Convert focal length to CFG scale.
        Wider lenses (lower mm) = more creative (lower CFG).
        """
        if focal_length < 35:
            return 6.0  # Wide, more freedom
        elif focal_length < 70:
            return 7.5  # Standard
        else:
            return 9.0  # Telephoto, more controlled
    
    def invoke_render(self, render_args: Dict[str, Any]) -> str:
        """
        Execute the render using configured backend.
        
        Args:
            render_args: Prepared rendering arguments
            
        Returns:
            Path to rendered output image
        """
        if self.use_comfyui:
            return self._render_with_comfyui(render_args)
        else:
            return self._render_with_fibo(render_args)
    
    def _render_with_fibo(self, args: Dict[str, Any]) -> str:
        """Render using direct FIBO/Diffusers pipeline."""
        from model_clients.fibo_client import FIBOClient
        
        client = FIBOClient()
        return client.generate(args)
    
    def _render_with_comfyui(self, args: Dict[str, Any]) -> str:
        """Render using ComfyUI workflow."""
        import requests
        
        comfyui_url = os.getenv("COMFYUI_URL", "http://localhost:8188")
        # TODO: Load recipe, map args, submit to ComfyUI API
        raise NotImplementedError("ComfyUI integration pending")
