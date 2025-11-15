# 🔗 Chained Prompt Generation Guide

## Overview

The **Chained Prompt Generation** feature breaks down large code generation tasks into smaller, manageable steps. Each step builds upon the previous step's output, creating more coherent and integrated code.

## Why Use Chained Prompts?

### Traditional Single Prompt Issues:
- ❌ **Context limit**: Single prompts can hit token limits
- ❌ **Less coherent**: Everything generated at once without cross-referencing
- ❌ **Generic results**: No step-by-step refinement
- ❌ **Harder to debug**: If one part fails, everything fails

### Chained Prompts Benefits:
- ✅ **Better context management**: Each step focuses on one aspect
- ✅ **More integrated**: Later steps use earlier outputs as context
- ✅ **Higher quality**: Progressive refinement
- ✅ **Resilient**: If one step fails, others can still succeed
- ✅ **Scalable**: Can handle very complex projects

## How It Works

### 5-Step Generation Flow

```
┌─────────────────────────────────────────────────────┐
│ Step 1: Architecture Analysis                       │
│ Input: UI mockup + description                      │
│ Output: Architecture plan (pages, APIs, tables)     │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ Step 2: Database Schema                             │
│ Input: Architecture plan                            │
│ Output: Database files (schema, migrations)         │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ Step 3: Backend API                                 │
│ Input: Architecture + Database schema               │
│ Output: Backend files (routes, controllers, auth)   │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ Step 4: Frontend Components                         │
│ Input: Architecture + Backend API + UI mockup       │
│ Output: Frontend files (pages, components, styles)  │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ Step 5: Configuration & Deployment                  │
│ Input: Complete architecture                        │
│ Output: Config files (README, Docker, .env)         │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ Final Result: Combined & Validated                  │
│ All files merged + syntax validation                │
└─────────────────────────────────────────────────────┘
```

## API Usage

### Endpoint

```
POST /generate/chained
```

### Request Body

Same as regular `/generate` endpoint:

```json
{
  "image_data": "base64_encoded_image",
  "description": "Detailed project description",
  "tech_stack": {
    "frontend": "React",
    "backend": "FastAPI",
    "database": "PostgreSQL"
  },
  "project_name": "my-awesome-app"
}
```

### Response

Same structure as `/generate`:

```json
{
  "success": true,
  "message": "Successfully generated 25 files using chained prompts",
  "project_structure": {...},
  "files": [...],
  "dependencies": {...},
  "setup_instructions": [...]
}
```

## Step-by-Step Details

### Step 1: Architecture Analysis

**Purpose**: Understand the overall system design

**Input**:
- UI mockup image
- Project description
- Tech stack

**Output**:
```json
{
  "pages": ["Home", "Dashboard", "Profile", "Settings"],
  "components": ["Header", "Sidebar", "Card", "Modal"],
  "features": ["User authentication", "CRUD operations", "Real-time updates"],
  "api_endpoints": ["/api/auth/login", "/api/users", "/api/items"],
  "database_tables": ["users", "items", "sessions"],
  "authentication": "yes",
  "real_time": "yes",
  "file_upload": "no"
}
```

**What it does**:
- Analyzes UI mockup to identify pages and components
- Plans API endpoints needed
- Determines database structure
- Identifies special features (auth, real-time, etc.)

---

### Step 2: Database Schema Generation

**Purpose**: Create database structure

**Input**:
- Architecture plan from Step 1
- List of tables needed
- Authentication requirements

**Output**: Database files
```
database/
├── schema.sql              # Main schema
├── migrations/
│   └── 001_initial.sql    # Migration files
└── models.py              # ORM models (if applicable)
```

**What it does**:
- Creates tables with proper relationships
- Adds indexes and constraints
- Generates authentication tables if needed
- Creates migration files

**Context used**: Uses table names and relationships from architecture

---

### Step 3: Backend API Generation

**Purpose**: Create backend API implementation

**Input**:
- Architecture plan (API endpoints)
- Database schema from Step 2
- Tech stack specifications

**Output**: Backend files
```
backend/
├── main.py                 # Entry point
├── routes/
│   ├── auth.py            # Auth routes
│   ├── users.py           # User routes
│   └── items.py           # Item routes
├── services/
│   └── auth_service.py    # Business logic
├── models/
│   └── schemas.py         # Pydantic models
└── middleware/
    └── auth.py            # JWT middleware
```

**What it does**:
- Implements API endpoints from architecture
- Creates database integration using schema
- Adds authentication middleware
- Implements error handling and validation

**Context used**: 
- Endpoints list from Step 1
- Database tables and relationships from Step 2
- Knows what tables exist and their structure

---

### Step 4: Frontend Components Generation

**Purpose**: Create UI matching mockup

**Input**:
- Architecture plan (pages, components)
- Backend API structure from Step 3
- Original UI mockup
- Tech stack specifications

**Output**: Frontend files
```
frontend/
├── src/
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Dashboard.jsx
│   │   └── Profile.jsx
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   └── Card.jsx
│   ├── services/
│   │   └── api.js         # API integration
│   ├── hooks/
│   │   └── useAuth.js     # Custom hooks
│   └── styles/
│       └── tailwind.css
└── package.json
```

**What it does**:
- Creates pages from architecture
- Builds reusable components
- Integrates with backend API (knows exact endpoints)
- Implements state management
- Adds styling to match mockup

**Context used**:
- Page list from Step 1
- API endpoints from Step 3 (knows exactly what to call)
- UI mockup image for styling reference

---

### Step 5: Configuration & Deployment

**Purpose**: Add deployment and documentation

**Input**:
- Complete architecture
- Tech stack info
- All features being used

**Output**: Configuration files
```
├── README.md              # Setup guide
├── .env.example           # Environment template
├── docker-compose.yml     # Docker setup
├── Dockerfile            # Container definition
├── requirements.txt       # Python deps
└── package.json          # Node deps
```

**What it does**:
- Creates comprehensive README
- Generates environment configuration
- Sets up Docker deployment
- Documents all dependencies
- Adds setup instructions

**Context used**: Everything from previous steps

---

## Comparison: Single vs Chained

### Single Prompt (`/generate`)

```
✅ Faster (1 API call)
✅ Simpler
✅ Good for small projects
❌ Limited context
❌ Less integrated results
❌ Can hit token limits
```

**Best for:**
- Simple projects (< 10 files)
- Prototypes
- Quick demos
- Single-page applications

### Chained Prompts (`/generate/chained`)

```
✅ Better quality
✅ More integrated code
✅ Handles large projects
✅ Progressive refinement
✅ Each step references previous
❌ Slower (5 API calls)
❌ More complex
```

**Best for:**
- Complex applications (15-30+ files)
- Production-ready code
- Multi-page applications
- Projects with authentication
- Full-stack applications

## Example Usage

### cURL

```bash
curl -X POST http://localhost:8000/generate/chained \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFc...",
    "description": "E-commerce platform with user authentication, product catalog, shopping cart, and payment integration. Users can browse products, add to cart, and checkout securely.",
    "tech_stack": {
      "frontend": "React",
      "backend": "FastAPI",
      "database": "PostgreSQL"
    },
    "project_name": "my-ecommerce"
  }'
```

### Python

```python
import requests
import base64

# Read and encode image
with open("mockup.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:8000/generate/chained",
    json={
        "image_data": image_data,
        "description": "Task management app with drag-and-drop kanban board, real-time collaboration, and user authentication",
        "tech_stack": {
            "frontend": "React",
            "backend": "FastAPI",
            "database": "PostgreSQL"
        },
        "project_name": "task-manager"
    }
)

result = response.json()
print(f"Generated {len(result['files'])} files")
```

### JavaScript

```javascript
const fs = require('fs');

// Read and encode image
const imageBuffer = fs.readFileSync('mockup.png');
const imageData = imageBuffer.toString('base64');

fetch('http://localhost:8000/generate/chained', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    image_data: imageData,
    description: "Social media dashboard with real-time notifications, post creation, and analytics",
    tech_stack: {
      frontend: "React",
      backend: "FastAPI",
      database: "PostgreSQL"
    },
    project_name: "social-dashboard"
  })
})
.then(res => res.json())
.then(data => console.log(`Generated ${data.files.length} files`));
```

## Performance Considerations

### Timing

| Aspect | Single Prompt | Chained Prompts |
|--------|--------------|-----------------|
| API Calls | 1 | 5 |
| Total Time | 10-20 seconds | 40-60 seconds |
| Token Usage | ~4,000 tokens | ~10,000 tokens |
| Cost (GPT-4) | ~$0.08 | ~$0.20 |

### When to Use Each

**Use Single Prompt when:**
- ⏱️ Speed is critical
- 💰 Cost is a concern
- 🎯 Project is simple (< 10 files)
- 🚀 Prototyping quickly

**Use Chained Prompts when:**
- 🏆 Quality is priority
- 🏗️ Complex architecture
- 🔗 Need integrated components
- 📦 Production-ready code

## Tips for Best Results

### 1. **Detailed Descriptions**
```
❌ "Make a blog"
✅ "Blog platform with user authentication, post creation with markdown editor, 
    comments system, and admin dashboard for content moderation"
```

### 2. **Clear UI Mockups**
- Use high-resolution images
- Label important sections
- Include multiple pages if complex

### 3. **Specify Features**
```json
{
  "description": "E-commerce app with:
    - User authentication (JWT)
    - Product catalog with search/filter
    - Shopping cart with local storage
    - Stripe payment integration
    - Order history and tracking
    - Admin panel for product management"
}
```

### 4. **Choose Right Tech Stack**
- Match your expertise
- Consider project requirements
- Think about deployment

## Troubleshooting

### Issue: Step fails midway
**Solution**: Check logs to see which step failed. The service is resilient - earlier steps' outputs are still available.

### Issue: Files don't integrate well
**Solution**: This shouldn't happen with chained approach, but if it does, provide more detailed description.

### Issue: Too slow
**Solution**: Use single prompt (`/generate`) for smaller projects, or increase timeout settings.

### Issue: Syntax errors
**Solution**: All files are validated. Check the setup_instructions for warnings.

## Advanced: Customizing the Chain

You can modify `services/chained_generation_service.py` to:

1. **Add more steps**:
   ```python
   # Step 6: Generate tests
   test_files = await self._step6_generate_tests(...)
   ```

2. **Change step order**:
   ```python
   # Generate frontend before backend
   frontend_files = await self._step3_generate_frontend(...)
   backend_files = await self._step4_generate_backend(...)
   ```

3. **Adjust prompts**:
   - Modify system prompts for each step
   - Add more context between steps
   - Change temperature for creativity

4. **Parallel steps**:
   ```python
   # Run independent steps in parallel
   import asyncio
   database_task = self._step2_generate_database(...)
   config_task = self._step5_generate_configs(...)
   await asyncio.gather(database_task, config_task)
   ```

## Monitoring

Check logs to see progress:

```
INFO:root:Starting chained generation for: my-app
INFO:root:✓ Step 1/5: Architecture planned
INFO:root:✓ Step 2/5: Database schema generated
INFO:root:✓ Step 3/5: Backend API generated
INFO:root:✓ Step 4/5: Frontend components generated
INFO:root:✓ Step 5/5: Configuration files generated
INFO:root:Chained generation completed: 23 files generated
```

## Summary

The chained prompt approach provides:
- 🎯 **Better architecture** - Planned before implementation
- 🔗 **Integrated code** - Components reference each other correctly
- 📊 **Higher quality** - Each step refined
- 🏗️ **Scalability** - Handles complex projects
- 🛠️ **Maintainability** - Clear separation of concerns

Try it today at `/generate/chained`! 🚀
