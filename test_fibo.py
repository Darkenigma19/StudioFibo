"""
Test script to verify FIBO integration
"""
import os
from dotenv import load_dotenv
from backend.model_clients.fibo_client import FIBOClient

# Load environment variables
load_dotenv()

def test_fibo_setup():
    print("=" * 50)
    print("FIBO Integration Test")
    print("=" * 50)
    
    # Check environment variables
    hf_token = os.getenv("HF_API_TOKEN")
    model_id = os.getenv("FIBO_MODEL_ID", "briaai/BRIA-2.3-FAST")
    
    print("\n1. Environment Variables:")
    print(f"   HF_API_TOKEN: {'✓ SET' if hf_token and hf_token.startswith('hf_') else '✗ NOT SET (using placeholder)'}")
    print(f"   FIBO_MODEL_ID: {model_id}")
    
    # Initialize client
    print("\n2. Initializing FIBO Client...")
    try:
        client = FIBOClient()
        print("   ✓ Client initialized")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    
    # Test generation
    print("\n3. Testing Image Generation...")
    print("   Using MOCK mode (copying example_render.jpg)")
    print("   To use REAL FIBO:")
    print("   - Add your HuggingFace token to .env")
    print("   - Token must start with 'hf_'")
    print("   - Get token from: https://huggingface.co/settings/tokens")
    
    try:
        test_args = {
            "prompt": "A beautiful sunset over mountains",
            "seed": 42,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "width": 1024,
            "height": 1024
        }
        
        output_path = client.generate(test_args)
        print(f"\n   ✓ Image generated: {output_path}")
        
        if os.path.exists(output_path):
            print(f"   ✓ File exists ({os.path.getsize(output_path)} bytes)")
        else:
            print(f"   ✗ File not found")
            
    except Exception as e:
        print(f"   ✗ Generation failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("=" * 50)
    
    if not hf_token or not hf_token.startswith('hf_'):
        print("\n⚠️  IMPORTANT: Currently using MOCK rendering")
        print("   Update .env with your real HuggingFace token to enable FIBO")
    
    return True

if __name__ == "__main__":
    test_fibo_setup()
