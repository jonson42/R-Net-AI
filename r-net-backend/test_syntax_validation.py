"""
Test script to demonstrate syntax validation
"""

import json
import requests
import time

# Test syntax validation endpoint
def test_syntax_validation():
    print("🧪 Testing Syntax Validation\n")
    print("=" * 60)
    
    # Test 1: Valid Python code
    print("\n1. Testing VALID Python code:")
    valid_python = {
        "path": "test.py",
        "content": """def hello_world():
    print("Hello, World!")
    return True

if __name__ == "__main__":
    hello_world()
""",
        "description": "Simple Python file"
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/validate",
        json=[valid_python]
    )
    result = response.json()
    print(f"   Result: {'✓ PASS' if result.get('success') else '✗ FAIL'}")
    print(f"   Validated: {result.get('validation', {}).get('validated_files', 0)} files")
    print(f"   Errors: {len(result.get('validation', {}).get('errors', []))}")
    time.sleep(0.5)  # Avoid rate limiting
    
    # Test 2: Invalid Python code (syntax error)
    print("\n2. Testing INVALID Python code (missing colon):")
    invalid_python = {
        "path": "bad_test.py",
        "content": """def broken_function()
    print("This is broken")
    return False
""",
        "description": "Broken Python file"
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/validate",
        json=[invalid_python]
    )
    result = response.json()
    print(f"   Result: {'✓ PASS' if result['success'] else '✗ FAIL (expected)'}")
    print(f"   Errors found: {len(result['validation']['errors'])}")
    if result['validation']['errors']:
        print(f"   Error: {result['validation']['errors'][0]['error']}")
    
    # Test 3: Valid JSON
    print("\n3. Testing VALID JSON:")
    valid_json = {
        "path": "config.json",
        "content": '{"name": "test", "version": "1.0.0", "active": true}',
        "description": "Configuration file"
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/validate",
        json=[valid_json]
    )
    result = response.json()
    print(f"   Result: {'✓ PASS' if result.get('success') else '✗ FAIL'}")
    time.sleep(0.5)  # Avoid rate limiting
    
    # Test 4: Invalid JSON
    print("\n4. Testing INVALID JSON (missing quote):")
    invalid_json = {
        "path": "bad_config.json",
        "content": '{"name": "test", "version: "1.0.0"}',
        "description": "Broken JSON file"
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/validate",
        json=[invalid_json]
    )
    result = response.json()
    print(f"   Result: {'✗ FAIL (expected)' if not result.get('success') else '✓ PASS (unexpected)'}")
    if result.get('validation', {}).get('errors'):
        print(f"   Error detected: {result['validation']['errors'][0]['error']}")
    time.sleep(0.5)  # Avoid rate limiting
    
    # Test 5: Valid JavaScript
    print("\n5. Testing VALID JavaScript:")
    valid_js = {
        "path": "app.js",
        "content": """function greet(name) {
    return `Hello, ${name}!`;
}

const result = greet("World");
console.log(result);
""",
        "description": "JavaScript file"
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/validate",
        json=[valid_js]
    )
    result = response.json()
    print(f"   Result: {'✓ PASS' if result.get('success') else '✗ FAIL'}")
    time.sleep(0.5)  # Avoid rate limiting
    
    # Test 6: Invalid JavaScript (unmatched bracket)
    print("\n6. Testing INVALID JavaScript (unmatched bracket):")
    invalid_js = {
        "path": "bad_app.js",
        "content": """function broken() {
    console.log("Missing closing bracket");
""",
        "description": "Broken JavaScript file"
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/validate",
        json=[invalid_js]
    )
    result = response.json()
    print(f"   Result: {'✗ FAIL (expected)' if not result.get('success') else '✓ PASS (unexpected)'}")
    if result.get('validation', {}).get('errors'):
        print(f"   Error: {result['validation']['errors'][0]['error']}")
    time.sleep(0.5)  # Avoid rate limiting
    
    # Test 7: Multiple files with mixed results
    print("\n7. Testing MULTIPLE files (mixed valid/invalid):")
    mixed_files = [
        {
            "path": "good.py",
            "content": "print('This is valid')",
            "description": "Valid Python"
        },
        {
            "path": "bad.py",
            "content": "print('Missing parenthesis'",
            "description": "Invalid Python"
        },
        {
            "path": "config.json",
            "content": '{"status": "ok"}',
            "description": "Valid JSON"
        }
    ]
    
    response = requests.post(
        "http://127.0.0.1:8000/validate",
        json=mixed_files
    )
    result = response.json()
    print(f"   Result: {'✗ FAIL (expected)' if not result.get('success') else '✓ PASS (unexpected)'}")
    print(f"   Total files: {result.get('validation', {}).get('total_files', 0)}")
    print(f"   Validated: {result.get('validation', {}).get('validated_files', 0)}")
    print(f"   Errors: {len(result.get('validation', {}).get('errors', []))}")
    for error in result.get('validation', {}).get('errors', []):
        print(f"      - {error['file']}: {error['error']}")
    
    print("\n" + "=" * 60)
    print("✓ Syntax validation tests completed!\n")


if __name__ == "__main__":
    try:
        test_syntax_validation()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Backend is not running at http://127.0.0.1:8000")
        print("   Start the backend first: cd r-net-backend && python3 main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
