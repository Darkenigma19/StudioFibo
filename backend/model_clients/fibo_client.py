"""
FIBO Client - HuggingFace Diffusers Wrapper

Handles direct inference with Stable Diffusion XL model for image generation.
"""

import os
import uuid
from typing import Dict, Any
from pathlib import Path


class FIBOClient:
    """Client for Stable Diffusion XL model inference via HuggingFace Diffusers."""
    
    def __init__(self):
        # Use Stable Diffusion XL instead of BRIA
        self.model_id = os.getenv("FIBO_MODEL_ID", "stabilityai/stable-diffusion-xl-base-1.0")
        self.hf_token = os.getenv("HF_API_TOKEN")
        self.pipeline = None
        self.output_dir = Path(__file__).parent.parent / "samples" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_pipeline(self):
        """Lazy load the diffusion pipeline."""
        if self.pipeline is not None:
            return
            
        try:
            from diffusers import StableDiffusionXLPipeline
            import torch
            
            print(f"Loading Stable Diffusion XL model: {self.model_id}")
            self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16,
                use_auth_token=self.hf_token if self.hf_token else None
            )
            
            # Enable optimizations
            if torch.cuda.is_available():
                print("Using CUDA GPU for inference")
                self.pipeline = self.pipeline.to("cuda")
                self.pipeline.enable_attention_slicing()
            else:
                # CPU fallback
                print("Using CPU for inference (this will be slow)")
                self.pipeline = self.pipeline.to("cpu")
                
            print("Model loaded successfully!")
                
        except Exception as e:
            print(f"Warning: Could not load Stable Diffusion XL pipeline: {e}")
            print("Falling back to mock rendering")
            self.pipeline = None
    
    def generate(self, args: Dict[str, Any]) -> str:
        """
        Generate image using Stable Diffusion XL model.
        
        Args:
            args: Rendering arguments (prompt, seed, steps, etc.)
            
        Returns:
            Path to generated image file
        """
        self._load_pipeline()
        
        if self.pipeline is None:
            # Fallback: copy example image
            return self._mock_generate(args)
        
        print(f"Generating image with prompt: {args['prompt'][:50]}...")
        
        # Run inference with SDXL parameters
        image = self.pipeline(
            prompt=args["prompt"],
            num_inference_steps=args.get("num_inference_steps", 50),  # SDXL works well with 50 steps
            guidance_scale=args.get("guidance_scale", 9.0),  # Higher guidance for better quality
            width=args.get("width", 1024),
            height=args.get("height", 1024),
            generator=self._get_generator(args.get("seed")),
        ).images[0]
        
        # Save output
        output_name = f"render_{uuid.uuid4().hex[:12]}.jpg"
        output_path = self.output_dir / output_name
        image.save(output_path, "JPEG", quality=95)
        
        print(f"Image saved to: {output_path}")
        return str(output_path)
    
    def _get_generator(self, seed: int = None):
        """Create torch Generator with seed."""
        try:
            import torch
            generator = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu")
            if seed is not None:
                generator.manual_seed(seed)
            return generator
        except:
            return None
    
    def _mock_generate(self, args: Dict[str, Any]) -> str:
        """Fallback mock rendering (copies example image)."""
        import shutil
        
        example_path = self.output_dir.parent / "example_render.jpg"
        output_name = f"render_{uuid.uuid4().hex[:12]}.jpg"
        output_path = self.output_dir / output_name
        
        if example_path.exists():
            shutil.copy(example_path, output_path)
        else:
            # Create placeholder
            from PIL import Image
            img = Image.new('RGB', (1024, 1024), color='#4a5568')
            img.save(output_path, 'JPEG')
        
        return str(output_path)
