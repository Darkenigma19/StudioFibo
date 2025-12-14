from dotenv import load_dotenv
import os
from huggingface_hub import HfApi

# Load environment
load_dotenv()

token = os.getenv('HF_API_TOKEN')

print("=" * 60)
print("HUGGINGFACE TOKEN VALIDATION")
print("=" * 60)

if not token:
    print("✗ NO TOKEN FOUND in .env file")
    exit(1)

print(f"✓ Token found: {token[:10]}...{token[-4:]}")
print(f"✓ Token length: {len(token)} chars")

# Test token validity
try:
    api = HfApi()
    user_info = api.whoami(token=token)
    print("\n✓ TOKEN IS VALID!")
    print(f"  Username: {user_info['name']}")
    print(f"  Account: {user_info.get('type', 'user')}")
    
    # Check access to BRIA model
    print("\n" + "=" * 60)
    print("CHECKING BRIA MODEL ACCESS")
    print("=" * 60)
    
    try:
        model_info = api.model_info("briaai/BRIA-2.3-FAST", token=token)
        print("✓ YOU HAVE ACCESS to briaai/BRIA-2.3-FAST")
        print(f"  Model ID: {model_info.modelId}")
        print(f"  Downloads: {model_info.downloads}")
        print(f"  Gated: {model_info.gated}")
        
    except Exception as e:
        if "401" in str(e) or "403" in str(e):
            print("✗ NO ACCESS to briaai/BRIA-2.3-FAST")
            print("  You need to request access at:")
            print("  https://huggingface.co/briaai/BRIA-2.3-FAST")
            print(f"  Error: {str(e)[:150]}")
        else:
            print(f"✗ Error checking model: {str(e)[:150]}")
    
except Exception as e:
    print("\n✗ TOKEN IS INVALID!")
    print(f"  Error: {str(e)[:150]}")
    exit(1)

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("Your token is working correctly!")
print("Images should render if you have BRIA model access.")
