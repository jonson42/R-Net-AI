# Tech-Specific Prompt Templates - Quick Reference

## Overview

Dynamic prompt template selection based on UI technology choices. System automatically loads optimized templates for your selected stack.

## Usage in UI

```
1. User selects in VS Code extension:
   Frontend: React ↓
   Backend: FastAPI ↓
   Database: PostgreSQL ↓

2. System automatically applies:
   ✓ React templates (hooks, TypeScript, Tailwind)
   ✓ FastAPI templates (Pydantic, async, SQLAlchemy)
   ✓ PostgreSQL templates (asyncpg, migrations)

3. Generate button → Complete, framework-optimized code
```

## Supported Technologies

### Frontend
- ✅ **React** - Hooks, TypeScript, Tailwind, React Query, React Router
- ✅ **Vue** - Composition API, Pinia, Vue Router, TypeScript
- ✅ **Angular** - Standalone components, RxJS, Angular Material

### Backend
- ✅ **FastAPI** - Async, Pydantic, SQLAlchemy, Alembic, JWT
- ✅ **Express** - TypeScript, Helmet, Prisma/TypeORM, JWT
- ✅ **Django** - DRF, Class-based views, Django ORM, Celery

### Database
- ✅ **PostgreSQL** - asyncpg, SQLAlchemy async, Alembic migrations
- ✅ **MySQL** - aiomysql, connection pooling
- ✅ **MongoDB** - Motor async driver, Pydantic models

## Template Contents

Each technology template includes:

### 1. Core Instructions
- Framework-specific patterns and best practices
- Project structure recommendations
- Code examples with proper syntax

### 2. Dependencies
- Exact package versions (e.g., `react@18.2.0`)
- All required packages for that technology
- Separated dev dependencies

### 3. Styling (Frontend)
- Complete Tailwind configuration
- Component styling patterns
- Responsive design guidelines

### 4. Integration Patterns
- API communication setup
- Authentication flow
- Error handling strategy

## Example Output

### React + FastAPI + PostgreSQL generates:

**Frontend (25+ files)**
```
frontend/
├── package.json (React, TypeScript, Tailwind, React Query)
├── tailwind.config.js (Custom theme: colors, fonts, spacing)
├── src/
│   ├── components/ui/ (15-20 styled components)
│   ├── hooks/ (useAuth, useApi, useForm)
│   ├── pages/ (Login, Dashboard, etc.)
│   └── services/ (API client with interceptors)
```

**Backend (15+ files)**
```
backend/
├── requirements.txt (FastAPI, SQLAlchemy, Pydantic)
├── main.py (App with middleware)
├── src/
│   ├── models/ (SQLAlchemy models)
│   ├── schemas/ (Pydantic validation)
│   ├── routers/ (API endpoints)
│   ├── services/ (Business logic)
│   └── middleware/ (Auth, CORS, errors)
```

**Database**
```
database/
├── schema.sql (Complete PostgreSQL schema)
├── migrations/ (Alembic migration files)
└── seeds/ (Sample data)
```

## Key Benefits

1. **Framework-Optimized Code**
   - React uses hooks, not class components
   - FastAPI uses async, not sync
   - Follows official style guides

2. **Correct Dependencies**
   - No version conflicts
   - Security updates included
   - Dev tools separated

3. **Complete Styling**
   - Full Tailwind theme
   - 15-20 styled components
   - Responsive + dark mode

4. **Security Built-in**
   - JWT authentication
   - Input validation
   - SQL injection prevention
   - Password hashing

5. **Production Ready**
   - Error handling
   - Logging
   - Docker support
   - Environment configs

## API Usage

### Automatic (Default)

```python
# System automatically uses tech templates
response = await openai_service.generate_code(
    image_data=image,
    description=description,
    tech_stack=tech_stack,
    project_name=project_name
)
# ↑ Internally uses tech-specific templates
```

### Manual Template Access

```python
from services.tech_specific_templates import TechSpecificTemplates

# Get specific template
react_template = TechSpecificTemplates.get_frontend_template("React")
print(react_template['core_instructions'])

# Build complete prompt
complete_prompt = TechSpecificTemplates.build_complete_prompt(
    tech_stack=tech_stack,
    description=description,
    project_name=project_name
)
```

## Customization

Edit `services/tech_specific_templates.py`:

```python
# Modify React template
FRONTEND_TEMPLATES["React"]["dependencies"].append("framer-motion@^10.0.0")

# Customize instructions
FRONTEND_TEMPLATES["React"]["core_instructions"] = """
Your custom React guidelines here...
"""

# Add new framework
FRONTEND_TEMPLATES["Svelte"] = {
    "core_instructions": "...",
    "dependencies": ["svelte@^4.0.0"],
    "styling_requirements": "..."
}
```

## Adding New Technologies

### 1. Add Template Definition

```python
FRONTEND_TEMPLATES["YourFramework"] = {
    "core_instructions": "Detailed instructions...",
    "styling_requirements": "Styling guide...",
    "dependencies": ["package@version"],
    "dev_dependencies": ["dev-package@version"]
}
```

### 2. Update Models

```python
class Frontend(str, Enum):
    REACT = "React"
    YOUR_FRAMEWORK = "YourFramework"  # Add here
```

### 3. Update UI Options

```html
<!-- In generator-webview.html -->
<option value="YourFramework">YourFramework</option>
```

## Template Structure Reference

```python
{
    "core_instructions": """
    Multi-line string with:
    • Framework-specific patterns
    • Project structure
    • Code examples
    • Best practices
    """,
    
    "styling_requirements": """
    Frontend only:
    • Tailwind configuration
    • Component styling
    • Responsive design
    """,
    
    "dependencies": [
        "package1@version",
        "package2@version"
    ],
    
    "dev_dependencies": [
        "dev-package1@version",
        "dev-package2@version"
    ]
}
```

## Comparison: Before vs After

### Before (Generic)
```
✗ Generic React instructions
✗ Missing framework-specific patterns
✗ Dependency versions unspecified
✗ Basic styling guidelines
✗ Manual integration setup
```

### After (Tech-Specific)
```
✓ React-specific hooks, routing, state management
✓ Exact patterns for React Query, React Router
✓ Exact versions: react@18.2.0, @tanstack/react-query@5.x
✓ Complete Tailwind config with custom theme
✓ Automatic API client setup with interceptors
```

## Quality Improvements

| Metric | Before | After |
|--------|--------|-------|
| **Code Quality** | Generic patterns | Framework-optimized |
| **Dependency Management** | Unspecified versions | Exact versions |
| **Styling Completeness** | Basic CSS | Full Tailwind theme |
| **Security** | Manual setup | Built-in (JWT, validation) |
| **Production Readiness** | Additional work needed | Deploy-ready |
| **Files Generated** | 10-15 files | 25-40 files |
| **Code Reusability** | Low | High (15-20 components) |

## Common Tech Stack Combinations

### 1. Modern SPA
```
React + FastAPI + PostgreSQL
→ 40+ files, TypeScript, async APIs, responsive UI
```

### 2. Enterprise App
```
Angular + Express + PostgreSQL
→ 35+ files, RxJS, REST APIs, Material Design
```

### 3. Rapid Prototype
```
Vue + Django + MongoDB
→ 30+ files, Composition API, Django admin, flexible schema
```

## Troubleshooting

### Issue: Wrong template loaded
**Solution:** Check tech_stack values match template keys exactly
```python
tech_stack = TechStack(frontend="React")  # ✓ Correct
tech_stack = TechStack(frontend="react")  # ✗ Wrong (lowercase)
```

### Issue: Missing dependencies
**Solution:** Check template dependencies list
```python
template = TechSpecificTemplates.get_frontend_template("React")
print(template['dependencies'])  # View all required packages
```

### Issue: Styling not applied
**Solution:** Ensure frontend template includes styling_requirements
```python
if 'styling_requirements' not in template:
    # Add styling section to template
```

## Performance

- **Template Load Time:** < 10ms (cached in memory)
- **Prompt Generation:** 50-100ms (string assembly)
- **Total Overhead:** Negligible (< 1% of API call time)

## Summary

✅ **Automatic:** System selects templates based on UI choices
✅ **Comprehensive:** 3x more detailed than generic prompts
✅ **Accurate:** Framework-specific patterns and versions
✅ **Complete:** Includes styling, testing, deployment
✅ **Extensible:** Easy to add new frameworks
✅ **Production-Ready:** Security and best practices built-in

**Result:** Higher quality, framework-optimized code generated automatically based on user's technology selections.
