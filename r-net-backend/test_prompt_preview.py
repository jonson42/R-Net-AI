#!/usr/bin/env python3
"""
Test script for Prompt Preview & Editing feature
Demonstrates the workflow:
1. Preview the generated prompt
2. Edit it if needed
3. Use the edited prompt for code generation
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_prompt_preview():
    """Test the prompt preview endpoint"""
    print("\n" + "=" * 80)
    print("🧪 Testing Prompt Preview Feature")
    print("=" * 80)
    
    # Step 1: Preview the prompt
    print("\n📋 Step 1: Requesting prompt preview...")
    
    preview_request = {
        "description": "Create a simple todo list application with user authentication",
        "tech_stack": {
            "frontend": "React",
            "backend": "FastAPI",
            "database": "PostgreSQL"
        },
        "project_name": "todo-app"
    }
    
    response = requests.post(
        f"{BASE_URL}/prompt/preview",
        json=preview_request
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✓ Prompt preview generated successfully!")
        print(f"\n📄 Message: {result['message']}")
        
        # Show preview of prompts (truncated for readability)
        print("\n" + "-" * 80)
        print("SYSTEM PROMPT (first 500 chars):")
        print("-" * 80)
        print(result['system_prompt'][:500] + "...")
        
        print("\n" + "-" * 80)
        print("USER PROMPT (first 500 chars):")
        print("-" * 80)
        print(result['user_prompt'][:500] + "...")
        
        print("\n" + "=" * 80)
        print("✅ Prompt Preview Test PASSED")
        print("=" * 80)
        
        # Save prompts for potential editing
        with open('/tmp/system_prompt.txt', 'w') as f:
            f.write(result['system_prompt'])
        with open('/tmp/user_prompt.txt', 'w') as f:
            f.write(result['user_prompt'])
        
        print("\n💾 Prompts saved to:")
        print("   - /tmp/system_prompt.txt")
        print("   - /tmp/user_prompt.txt")
        print("\n📝 You can now edit these files and use them in /generate endpoint")
        
        return result['system_prompt']
    else:
        print(f"✗ Failed: {response.status_code}")
        print(f"Error: {response.text}")
        return None


def demonstrate_workflow():
    """Demonstrate the complete workflow"""
    print("\n" + "=" * 80)
    print("📚 PROMPT PREVIEW & EDITING WORKFLOW")
    print("=" * 80)
    
    print("""
    This feature allows you to:
    
    1. Preview the AI prompt BEFORE generation
       POST /prompt/preview
       {
         "description": "Your project description",
         "tech_stack": {...},
         "project_name": "my-app"
       }
    
    2. Edit the prompt if needed
       - Modify the returned system_prompt
       - Add specific instructions
       - Change coding standards
       - Adjust requirements
    
    3. Generate code with your custom prompt
       POST /generate
       {
         "image_data": "base64...",
         "description": "Your project description",
         "tech_stack": {...},
         "project_name": "my-app",
         "custom_prompt": "Your edited system prompt here"
       }
    """)
    
    print("\n" + "=" * 80)
    print("Running live test...")
    print("=" * 80)
    
    # Test the preview endpoint
    custom_prompt = test_prompt_preview()
    
    if custom_prompt:
        print("\n" + "=" * 80)
        print("💡 NEXT STEPS:")
        print("=" * 80)
        print("""
        1. Edit the saved prompts in /tmp/system_prompt.txt
        2. Use the edited prompt in your /generate request:
        
           curl -X POST http://127.0.0.1:8000/generate \\
             -H "Content-Type: application/json" \\
             -d '{
               "image_data": "your_base64_image",
               "description": "Your project description",
               "tech_stack": {
                 "frontend": "React",
                 "backend": "FastAPI",
                 "database": "PostgreSQL"
               },
               "project_name": "my-app",
               "custom_prompt": "YOUR EDITED PROMPT HERE"
             }'
        
        3. The AI will use YOUR custom prompt instead of the default
        """)


if __name__ == "__main__":
    try:
        demonstrate_workflow()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Backend is not running at http://127.0.0.1:8000")
        print("   Start the backend first: cd r-net-backend && python3 main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
