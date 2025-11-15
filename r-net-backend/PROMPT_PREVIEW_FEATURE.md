# Prompt Preview & Editing Feature

## Overview

This feature allows you to **preview and edit** the AI prompt **before** code generation. This gives you complete control over the instructions sent to the AI, enabling you to:

- Review exactly what prompt will be used
- Customize coding standards and requirements
- Add specific instructions or constraints
- Adjust the level of detail or complexity
- Enforce particular design patterns or architectures

## How It Works

### Workflow

```
1. Request Prompt Preview → 2. Review & Edit → 3. Generate with Custom Prompt
   (POST /prompt/preview)      (Edit locally)     (POST /generate with custom_prompt)
```

## API Endpoints

### 1. Preview Prompt Endpoint

**POST** `/prompt/preview`

Preview the prompt that will be generated based on your project requirements.

**Request Body:**
```json
{
  "description": "Create a todo list application with user authentication",
  "tech_stack": {
    "frontend": "React",
    "backend": "FastAPI",
    "database": "PostgreSQL"
  },
  "project_name": "todo-app"
}
```

**Response:**
```json
{
  "system_prompt": "You are a world-class senior full-stack architect...",
  "user_prompt": "Generate a complete React + FastAPI application...",
  "message": "Prompt generated successfully. You can edit these prompts and use them in the /generate endpoint with 'custom_prompt' field."
}
```

### 2. Generate with Custom Prompt

**POST** `/generate`

Generate code using your edited custom prompt.

**Request Body:**
```json
{
  "image_data": "base64_encoded_image_data",
  "description": "Create a todo list application with user authentication",
  "tech_stack": {
    "frontend": "React",
    "backend": "FastAPI",
    "database": "PostgreSQL"
  },
  "project_name": "todo-app",
  "custom_prompt": "YOUR EDITED SYSTEM PROMPT HERE"
}
```

**Note:** If `custom_prompt` is provided, it will be used instead of the auto-generated prompt.

## Usage Examples

### Example 1: Preview & Edit Workflow

```bash
# Step 1: Get prompt preview
curl -X POST http://127.0.0.1:8000/prompt/preview \
  -H "Content-Type: application/json" \
  -d '{
    "description": "E-commerce platform with cart and checkout",
    "tech_stack": {
      "frontend": "React",
      "backend": "FastAPI",
      "database": "PostgreSQL"
    },
    "project_name": "ecommerce-app"
  }' > prompt.json

# Step 2: Extract and save the system prompt
cat prompt.json | python3 -c "import sys, json; print(json.load(sys.stdin)['system_prompt'])" > system_prompt.txt

# Step 3: Edit the prompt
# Open system_prompt.txt in your editor and make changes
nano system_prompt.txt

# Step 4: Generate with custom prompt
CUSTOM_PROMPT=$(cat system_prompt.txt)
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d "{
    \"image_data\": \"$(base64 -i screenshot.png)\",
    \"description\": \"E-commerce platform with cart and checkout\",
    \"tech_stack\": {
      \"frontend\": \"React\",
      \"backend\": \"FastAPI\",
      \"database\": \"PostgreSQL\"
    },
    \"project_name\": \"ecommerce-app\",
    \"custom_prompt\": \"$CUSTOM_PROMPT\"
  }"
```

### Example 2: Using Python

```python
import requests

# Step 1: Preview prompt
preview_response = requests.post(
    "http://127.0.0.1:8000/prompt/preview",
    json={
        "description": "Social media app with posts and comments",
        "tech_stack": {
            "frontend": "React",
            "backend": "FastAPI",
            "database": "PostgreSQL"
        },
        "project_name": "social-app"
    }
)

prompt_data = preview_response.json()
system_prompt = prompt_data["system_prompt"]

# Step 2: Edit the prompt (add custom requirements)
custom_prompt = system_prompt + """

ADDITIONAL REQUIREMENTS:
- Use TypeScript instead of JavaScript
- Implement dark mode support
- Add comprehensive error handling
- Include unit tests for all components
- Follow Airbnb style guide strictly
"""

# Step 3: Generate with custom prompt
with open("screenshot.png", "rb") as f:
    import base64
    image_data = base64.b64encode(f.read()).decode()

generate_response = requests.post(
    "http://127.0.0.1:8000/generate",
    json={
        "image_data": image_data,
        "description": "Social media app with posts and comments",
        "tech_stack": {
            "frontend": "React",
            "backend": "FastAPI",
            "database": "PostgreSQL"
        },
        "project_name": "social-app",
        "custom_prompt": custom_prompt
    }
)

result = generate_response.json()
print(f"Generated {len(result['files'])} files")
```

### Example 3: Quick Test Script

Run the provided test script:

```bash
cd r-net-backend
python3 test_prompt_preview.py
```

This will:
1. Request a prompt preview
2. Display the prompts (truncated)
3. Save prompts to `/tmp/system_prompt.txt` and `/tmp/user_prompt.txt`
4. Show next steps for editing and using the custom prompt

## Common Use Cases

### 1. Enforce Specific Coding Standards

```python
# Get the default prompt
preview = get_prompt_preview(...)

# Add your coding standards
custom = preview["system_prompt"] + """

MANDATORY CODING STANDARDS:
- Use functional components only (no class components)
- All functions must have TypeScript type annotations
- Maximum function length: 50 lines
- Use ESLint with Airbnb config
- Follow BEM naming convention for CSS
"""
```

### 2. Add Security Requirements

```python
custom = preview["system_prompt"] + """

SECURITY REQUIREMENTS:
- Implement JWT authentication with refresh tokens
- Add rate limiting on all endpoints
- Validate and sanitize ALL user inputs
- Use parameterized queries to prevent SQL injection
- Implement CORS properly
- Add security headers (CSP, HSTS, etc.)
"""
```

### 3. Specify Architecture Pattern

```python
custom = preview["system_prompt"] + """

ARCHITECTURE REQUIREMENTS:
- Follow Clean Architecture principles
- Implement Repository pattern for data access
- Use Dependency Injection
- Separate business logic from framework code
- Create clear layers: Presentation → Application → Domain → Infrastructure
"""
```

### 4. Add Testing Requirements

```python
custom = preview["system_prompt"] + """

TESTING REQUIREMENTS:
- Minimum 80% code coverage
- Unit tests for all business logic
- Integration tests for API endpoints
- E2E tests for critical user flows
- Use Jest for frontend, pytest for backend
- Mock external dependencies
"""
```

## Benefits

✅ **Full Control**: See and modify exactly what instructions go to the AI

✅ **Consistency**: Enforce your team's coding standards across all projects

✅ **Customization**: Add specific requirements not covered by default prompts

✅ **Debugging**: Understand why the AI generates code in a certain way

✅ **Learning**: See what makes an effective prompt for code generation

✅ **Quality**: Add quality gates and requirements before generation

## Technical Details

### Prompt Structure

The generated prompt consists of two parts:

1. **System Prompt**: 
   - Sets the AI's role and expertise level
   - Defines response format (JSON structure)
   - Lists code generation requirements
   - Specifies quality standards
   - Includes syntax validation requirements

2. **User Prompt**:
   - Contains project description
   - Lists specific features
   - Defines styling requirements
   - Includes technical specifications

### Custom Prompt Behavior

- If `custom_prompt` is provided, it **replaces** the system prompt
- The user prompt remains the description field
- The custom prompt is logged for debugging
- Syntax validation still applies to generated code

### Logging

When using a custom prompt, the logs will show:

```
INFO - Using custom prompt provided by user
INFO - ================================================================================
INFO - FINAL PROMPT SENT TO OPENAI:
INFO - ================================================================================
INFO - SYSTEM PROMPT:
INFO - YOUR CUSTOM PROMPT HERE...
```

## Testing

### Run the Test Suite

```bash
cd r-net-backend
python3 test_prompt_preview.py
```

### Manual Testing

1. **Test Preview Endpoint**:
```bash
curl -X POST http://127.0.0.1:8000/prompt/preview \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Test app",
    "tech_stack": {"frontend": "React", "backend": "FastAPI", "database": "PostgreSQL"},
    "project_name": "test"
  }' | python3 -m json.tool
```

2. **Test Custom Prompt**:
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": "iVBORw0KG...",
    "description": "Test app",
    "tech_stack": {"frontend": "React", "backend": "FastAPI", "database": "PostgreSQL"},
    "project_name": "test",
    "custom_prompt": "You are an expert. Generate a complete app..."
  }'
```

## API Documentation

Full interactive API documentation available at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Limitations

⚠️ **Custom Prompt Length**: Keep custom prompts under 8000 tokens (approx 32,000 characters)

⚠️ **Response Format**: Ensure your custom prompt instructs the AI to return JSON in the correct format

⚠️ **Cache Bypass**: Custom prompts bypass the cache (each request goes to OpenAI)

⚠️ **Validation**: Syntax validation still applies regardless of custom prompt

## Best Practices

1. **Start with Preview**: Always preview the default prompt first
2. **Incremental Changes**: Make small, targeted edits
3. **Keep Format Instructions**: Don't remove JSON format requirements
4. **Test Iteratively**: Test changes with small projects first
5. **Save Templates**: Save effective custom prompts for reuse
6. **Document Changes**: Keep notes on what customizations work well

## Version

- **Feature**: Prompt Preview & Editing
- **Version**: 1.0.0
- **Backend Version**: 2.0.0+
- **Endpoints**: `/prompt/preview`, `/generate` (with custom_prompt)

---

## Summary

The Prompt Preview & Editing feature gives you complete control over the AI code generation process. Preview the prompt, edit it to match your requirements, and generate code with your custom instructions. This ensures the generated code meets your specific standards and requirements.
