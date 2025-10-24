# R-Net AI Backend API Documentation

The R-Net AI backend provides a RESTful API for AI-powered full-stack code generation. This service processes UI mockups and natural language descriptions to generate complete application code.

## Base URL
```
http://127.0.0.1:8000
```

## Authentication
Currently, the API doesn't require authentication for client requests. OpenAI API key is configured server-side via environment variables.

## API Endpoints

### Health Check
```http
GET /health
```

Check the health status of the backend service and OpenAI connection.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "openai_connected": true
}
```

**Status Codes:**
- `200` - Service is healthy
- `503` - Service is unhealthy

---

### Root Information
```http
GET /
```

Get basic service information and available endpoints.

**Response:**
```json
{
  "message": "R-Net AI Backend Service",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### Generate Code
```http
POST /generate
```

Generate full-stack application code from UI mockup and description.

**Request Body:**
```json
{
  "image_data": "base64_encoded_image_string",
  "description": "Detailed application requirements...",
  "tech_stack": {
    "frontend": "React",
    "backend": "FastAPI", 
    "database": "PostgreSQL"
  },
  "project_name": "my-awesome-app"
}
```

**Request Fields:**
- `image_data` (string, required): Base64 encoded image data (PNG, JPG, WebP)
- `description` (string, required): Detailed application description (min 10 chars)
- `tech_stack` (object, required): Technology stack selection
  - `frontend` (string): Frontend framework
  - `backend` (string): Backend framework  
  - `database` (string): Database technology
- `project_name` (string, optional): Project name (default: "generated-app")

**Supported Tech Stack Options:**

*Frontend:*
- React
- Angular
- HTML
- Vue
- Svelte

*Backend:*
- FastAPI
- Flask
- .NET
- Express
- Django

*Database:*
- PostgreSQL
- MySQL
- MongoDB
- SQLite
- Redis

**Success Response (200):**
```json
{
  "success": true,
  "message": "Successfully generated 15 files for my-awesome-app",
  "project_structure": {
    "frontend/": ["src/", "public/", "package.json"],
    "backend/": ["src/", "main.py", "requirements.txt"],
    "database/": ["schema.sql", "migrations/"]
  },
  "files": [
    {
      "path": "frontend/src/App.tsx",
      "content": "import React from 'react';\n\nfunction App() {\n  return (\n    <div className=\"App\">\n      <h1>My Awesome App</h1>\n    </div>\n  );\n}\n\nexport default App;",
      "description": "Main React application component"
    }
  ],
  "dependencies": {
    "frontend": ["react", "react-dom", "@types/react"],
    "backend": ["fastapi", "uvicorn", "sqlalchemy"],
    "database": []
  },
  "setup_instructions": [
    "1. Install Node.js and Python",
    "2. Run npm install in frontend/",
    "3. Install backend dependencies: pip install -r requirements.txt",
    "4. Configure database connection",
    "5. Run backend: uvicorn main:app --reload",
    "6. Run frontend: npm start"
  ]
}
```

**Error Response (200 with success: false):**
```json
{
  "success": false,
  "message": "Code generation failed",
  "project_structure": {},
  "files": [],
  "dependencies": {},
  "setup_instructions": [],
  "error_details": "OpenAI API rate limit exceeded. Please try again later."
}
```

**Validation Error Response (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "description"],
      "msg": "ensure this value has at least 10 characters",
      "type": "value_error.any_str.min_length",
      "ctx": {"limit_value": 10}
    }
  ]
}
```

**Service Unavailable (503):**
```json
{
  "error": "OpenAI API key not configured",
  "detail": "Backend service requires valid OpenAI API key"
}
```

---

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes and detailed error messages.

### Common Error Scenarios

#### 1. Invalid Image Data
```json
{
  "success": false,
  "error_details": "Invalid image data: cannot identify image file"
}
```

#### 2. Image Too Large
```json
{
  "success": false, 
  "error_details": "Image size exceeds 5242880 bytes"
}
```

#### 3. OpenAI API Errors
```json
{
  "success": false,
  "error_details": "OpenAI API authentication failed. Please check your API key."
}
```

#### 4. Rate Limiting
```json
{
  "success": false,
  "error_details": "OpenAI API rate limit exceeded. Please try again later."
}
```

#### 5. Short Description
```json
{
  "success": false,
  "error_details": "Description must be at least 10 characters long"
}
```

---

## Rate Limits

The API implements retry logic for OpenAI API calls with exponential backoff:
- Maximum 3 retry attempts
- Exponential backoff: 2^retry_count seconds
- Automatic handling of rate limit errors

---

## File Upload Limits

- **Maximum file size**: 5MB (5,242,880 bytes)
- **Supported formats**: PNG, JPG, JPEG, GIF, WebP
- **Image processing**: Automatic resizing if larger than 2048x2048
- **Format conversion**: Automatic conversion to PNG for API compatibility

---

## Example Usage

### cURL Example
```bash
# Generate code for a React/FastAPI/PostgreSQL app
curl -X POST "http://127.0.0.1:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
    "description": "A task management application with user authentication, CRUD operations for tasks, real-time updates, and responsive design. Include login/register pages, dashboard with task statistics, task creation/editing forms, and proper error handling.",
    "tech_stack": {
      "frontend": "React",
      "backend": "FastAPI", 
      "database": "PostgreSQL"
    },
    "project_name": "task-manager"
  }'
```

### Python Example
```python
import requests
import base64

# Read image file
with open("mockup.png", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode()

# API request
response = requests.post("http://127.0.0.1:8000/generate", json={
    "image_data": image_data,
    "description": "A comprehensive task management application...",
    "tech_stack": {
        "frontend": "React",
        "backend": "FastAPI",
        "database": "PostgreSQL"
    },
    "project_name": "my-task-app"
})

result = response.json()
if result["success"]:
    print(f"Generated {len(result['files'])} files")
    for file in result["files"]:
        print(f"- {file['path']}: {file['description']}")
else:
    print(f"Generation failed: {result.get('error_details', 'Unknown error')}")
```

### JavaScript Example
```javascript
// Convert image to base64
const fileToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result.split(',')[1]);
    reader.onerror = error => reject(error);
  });
};

// Generate code
const generateCode = async (imageFile, description) => {
  try {
    const imageData = await fileToBase64(imageFile);
    
    const response = await fetch('http://127.0.0.1:8000/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image_data: imageData,
        description: description,
        tech_stack: {
          frontend: 'React',
          backend: 'FastAPI',
          database: 'PostgreSQL'
        },
        project_name: 'my-app'
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      console.log(`Generated ${result.files.length} files`);
      return result;
    } else {
      throw new Error(result.error_details || 'Generation failed');
    }
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
```

---

## Interactive API Documentation

The backend provides interactive API documentation using Swagger UI:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

These interfaces allow you to:
- Explore all available endpoints
- View request/response schemas
- Test API calls directly from the browser
- Download OpenAPI specification

---

## Development and Testing

### Local Development
```bash
# Start development server with auto-reload
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Start with debug logging
LOG_LEVEL=DEBUG uvicorn main:app --reload
```

### Health Monitoring  
```bash
# Check service health
curl http://127.0.0.1:8000/health

# Expected response
{"status":"healthy","version":"1.0.0","openai_connected":true}
```

### Configuration
Set environment variables in `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4-vision-preview
MAX_TOKENS=4096
TEMPERATURE=0.7
MAX_FILE_SIZE=5242880
HOST=127.0.0.1
PORT=8000
DEBUG=True
```

---

For more detailed technical information, see the [OpenAPI documentation](http://127.0.0.1:8000/docs) when the service is running.