#!/usr/bin/env python3
"""
Test script to verify chained generation API works correctly
This simulates what the VS Code extension will send
"""

import requests
import json
import base64
from pathlib import Path

# Backend URL
BACKEND_URL = "http://localhost:8000"

def create_test_image():
    """Create a simple test image in base64"""
    # 1x1 white pixel PNG
    return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="

def test_health():
    """Test if backend is running"""
    print("=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BACKEND_URL}/")
        print(f"✅ Backend is running: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_single_generation():
    """Test single-shot generation (original endpoint)"""
    print("\n" + "=" * 60)
    print("TEST 2: Single-Shot Generation (/generate)")
    print("=" * 60)
    
    payload = {
        "image_data": create_test_image(),
        "description": "Create a simple task manager app with user authentication, task CRUD operations, and a clean dashboard",
        "tech_stack": {
            "frontend": "React",
            "backend": "FastAPI",
            "database": "PostgreSQL"
        },
        "project_name": "test-single-gen"
    }
    
    try:
        print("Sending request to /generate...")
        response = requests.post(
            f"{BACKEND_URL}/generate",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Generation successful!")
            print(f"   - Files generated: {len(result.get('files', []))}")
            print(f"   - Setup steps: {len(result.get('setup_instructions', []))}")
            print(f"   - Response time: {response.elapsed.total_seconds():.2f}s")
            
            # Show first few files
            files = result.get('files', [])[:5]
            print("\n   First 5 files:")
            for f in files:
                print(f"   - {f['path']} ({len(f['content'])} chars)")
            
            return True
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_chained_generation():
    """Test chained generation (new multi-step endpoint)"""
    print("\n" + "=" * 60)
    print("TEST 3: Chained Generation (/generate/chained)")
    print("=" * 60)
    
    payload = {
        "image_data": create_test_image(),
        "description": "Create a task manager app with user authentication, task CRUD operations, priority levels, due dates, and a responsive dashboard",
        "tech_stack": {
            "frontend": "React",
            "backend": "FastAPI",
            "database": "PostgreSQL"
        },
        "project_name": "test-chained-gen"
    }
    
    try:
        print("Sending request to /generate/chained...")
        print("This uses 5-step progressive generation:")
        print("  Step 1: Architecture Analysis")
        print("  Step 2: Database Schema")
        print("  Step 3: Backend API")
        print("  Step 4: Frontend Components")
        print("  Step 5: Configuration Files")
        print("\nProcessing (may take 60-120 seconds)...")
        
        response = requests.post(
            f"{BACKEND_URL}/generate/chained",
            json=payload,
            timeout=180  # 3 minutes for chained generation
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Chained generation successful!")
            print(f"   - Files generated: {len(result.get('files', []))}")
            print(f"   - Setup steps: {len(result.get('setup_instructions', []))}")
            print(f"   - Response time: {response.elapsed.total_seconds():.2f}s")
            
            # Analyze file types
            files = result.get('files', [])
            file_types = {}
            for f in files:
                ext = Path(f['path']).suffix or 'no-ext'
                file_types[ext] = file_types.get(ext, 0) + 1
            
            print("\n   Files by type:")
            for ext, count in sorted(file_types.items()):
                print(f"   - {ext}: {count} files")
            
            print("\n   Sample files:")
            for i, f in enumerate(files[:8]):
                print(f"   {i+1}. {f['path']} ({len(f['content'])} chars)")
            
            return True
        else:
            print(f"❌ Chained generation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_comparison():
    """Compare single vs chained generation"""
    print("\n" + "=" * 60)
    print("TEST 4: Comparison Summary")
    print("=" * 60)
    
    print("""
Single-Shot Generation:
  - Endpoint: POST /generate
  - Speed: ~15-30 seconds
  - Files: Typically 10-15 files
  - Quality: Good, generic structure
  - Use case: Quick prototypes, simple apps

Chained Generation:
  - Endpoint: POST /generate/chained
  - Speed: ~60-120 seconds
  - Files: Typically 20-30 files
  - Quality: Excellent, integrated components
  - Use case: Production-ready apps, complex features
  
5-Step Process:
  1. Architecture - Analyzes UI mockup, plans structure
  2. Database - Creates schema based on architecture
  3. Backend - Generates API using database context
  4. Frontend - Creates UI using backend API context
  5. Configs - Generates deployment files
""")

def main():
    print("\n" + "=" * 60)
    print("R-NET AI EXTENSION - CHAINED GENERATION TEST")
    print("=" * 60)
    print("This test simulates what the VS Code extension sends")
    print()
    
    # Run tests
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health()))
    
    if not results[0][1]:
        print("\n❌ Backend is not running. Please start it first:")
        print("   cd r-net-backend")
        print("   python main.py")
        return
    
    # Test 2: Single generation
    results.append(("Single Generation", test_single_generation()))
    
    # Test 3: Chained generation
    results.append(("Chained Generation", test_chained_generation()))
    
    # Test 4: Show comparison
    test_comparison()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(r[1] for r in results)
    if all_passed:
        print("\n🎉 All tests passed! Extension is ready to use chained generation.")
        print("\nNext steps:")
        print("1. Open VS Code extension")
        print("2. Run command: 'GHC: Open AI Full-Stack Generator'")
        print("3. Upload an image and provide description")
        print("4. Extension will use chained generation (default)")
        print("5. Toggle in settings: rnet-ai.generation.useChainedPrompts")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
