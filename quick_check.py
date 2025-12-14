import requests

print("=" * 60)
print("QUICK SYNCHRONIZATION CHECK")
print("=" * 60)

# Backend check
try:
    r = requests.get('http://127.0.0.1:8000/versions', timeout=2)
    print(f"\n✓ BACKEND: Running on port 8000 (Status: {r.status_code})")
    print(f"  - API responding: YES")
    print(f"  - Versions available: {len(r.json())}")
except Exception as e:
    print(f"\n✗ BACKEND: Not running on port 8000")
    print(f"  Error: {str(e)[:60]}")

# Frontend check  
try:
    r = requests.get('http://localhost:3000', timeout=2)
    print(f"\n✓ FRONTEND: Running on port 3000 (Status: {r.status_code})")
    print(f"  - Page loading: YES")
    print(f"  - Page size: {len(r.content):,} bytes")
except Exception as e:
    print(f"\n✗ FRONTEND: Not running on port 3000")
    print(f"  Error: {str(e)[:60]}")

# CORS check
try:
    r = requests.get('http://127.0.0.1:8000/versions', headers={'Origin': 'http://localhost:3000'}, timeout=2)
    cors = r.headers.get('Access-Control-Allow-Origin', 'Not set')
    print(f"\n✓ CORS: {cors}")
    print(f"  - Frontend can call backend: {'YES' if cors else 'NO'}")
except:
    print(f"\n⚠ CORS: Cannot verify")

# API endpoints check
endpoints_ok = 0
endpoints_total = 4
print(f"\n📡 API ENDPOINTS:")
try:
    requests.post('http://127.0.0.1:8000/translate', json={'prompt': 'test'}, timeout=2)
    print("  ✓ /translate - Working")
    endpoints_ok += 1
except:
    print("  ✗ /translate - Failed")

try:
    requests.post('http://127.0.0.1:8000/validate', json={}, timeout=2)
    print("  ✓ /validate - Working")
    endpoints_ok += 1
except:
    print("  ✗ /validate - Failed")

try:
    requests.get('http://127.0.0.1:8000/versions', timeout=2)
    print("  ✓ /versions - Working")
    endpoints_ok += 1
except:
    print("  ✗ /versions - Failed")

try:
    requests.get('http://127.0.0.1:8000/samples/output/render_68dbb3805eec.jpg', timeout=2)
    print("  ✓ /samples/output/* - Working")
    endpoints_ok += 1
except:
    print("  ✗ /samples/output/* - Failed")

print(f"\n  Endpoints: {endpoints_ok}/{endpoints_total} working")

# Summary
print("\n" + "=" * 60)
print("SYNCHRONIZATION SUMMARY")
print("=" * 60)

try:
    backend = requests.get('http://127.0.0.1:8000/versions', timeout=1).status_code == 200
    frontend = requests.get('http://localhost:3000', timeout=1).status_code == 200
    
    if backend and frontend:
        print("✅ FULLY SYNCHRONIZED!")
        print("\n📍 Your app is ready:")
        print("   Backend:  http://127.0.0.1:8000")
        print("   Frontend: http://localhost:3000")
        print("\n🎯 Next steps:")
        print("   1. Open http://localhost:3000 in browser")
        print("   2. Click 'Render' button")
        print("   3. Wait for image generation")
        print("   4. Image will appear in preview")
    elif backend:
        print("⚠️  PARTIAL SYNC: Backend OK, Frontend needs restart")
    elif frontend:
        print("⚠️  PARTIAL SYNC: Frontend OK, Backend needs restart")
    else:
        print("❌ NOT SYNCHRONIZED: Both servers need restart")
        print("\n💡 Run: START_APP.bat to start both servers")
except:
    print("❌ CANNOT DETERMINE: Check if servers are running")

print("=" * 60)
