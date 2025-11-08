#!/usr/bin/env python3
"""
Simple script to test backend connection
"""
import requests
import json

def test_backend():
    backend_url = "http://127.0.0.1:8000"
    
    print(f"Testing backend at {backend_url}")
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = requests.get(f"{backend_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test root endpoint
        print("\n2. Testing root endpoint...")
        response = requests.get(f"{backend_url}/", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        print("\n✅ Backend is running and responding!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend - is it running?")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

if __name__ == "__main__":
    test_backend()