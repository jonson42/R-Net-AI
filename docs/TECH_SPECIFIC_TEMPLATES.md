# Technology-Specific Prompt Templates

## Overview

The R-Net AI system now features **dynamic prompt template selection** based on user's technology stack choices. When you select a frontend framework, backend framework, and database from the UI, the system automatically loads the most appropriate, comprehensive templates for those specific technologies.

## How It Works

### 1. **User Selection Flow**

```
User selects in UI:
├── Frontend: React
├── Backend: FastAPI  
└── Database: PostgreSQL

↓

System automatically loads:
├── React-specific templates (Hooks, TypeScript, Tailwind)
├── FastAPI-specific templates (Pydantic, SQLAlchemy, async)
└── PostgreSQL-specific templates (asyncpg, migrations)
```

### 2. **Template Structure**

Each technology has dedicated templates stored in `services/tech_specific_templates.py`:

```python
FRONTEND_TEMPLATES = {
    "React": {
        "core_instructions": "...",      # React best practices, hooks, routing
        "styling_requirements": "...",    # Tailwind config, component styling
        "dependencies": [...],            # NPM packages with versions
        "dev_dependencies": [...]         # Development tools
    },
    "Vue": { ... },
    "Angular": { ... }
}

BACKEND_TEMPLATES = {
    "FastAPI": {
        "core_instructions": "...",      # FastAPI patterns, Pydantic, async
        "dependencies": [...],            # Python packages with versions
        "dev_dependencies": [...]         # pytest, black, mypy
    },
    "Express": { ... },
    "Django": { ... }
}

DATABASE_TEMPLATES = {
    "PostgreSQL": {
        "connection_example": "...",     # SQLAlchemy async engine setup
        "migration_example": "...",      # Alembic migration pattern
    },
    "MySQL": { ... },
    "MongoDB": { ... }
}
```

### 3. **Automatic Prompt Assembly**

When code generation starts:

```python
# User selects: React + FastAPI + PostgreSQL
tech_stack = TechStack(
    frontend="React",
    backend="FastAPI", 
    database="PostgreSQL"
)

# System automatically builds comprehensive prompt:
complete_prompt = TechSpecificTemplates.build_complete_prompt(
    tech_stack=tech_stack,
    description=user_description,
    project_name=project_name
)

# This prompt includes:
# ✓ React-specific patterns (hooks, TypeScript, Tailwind)
# ✓ FastAPI-specific patterns (Pydantic, async, dependency injection)
# ✓ PostgreSQL connection setup (asyncpg, migrations)
# ✓ Integration guidelines (API calls, auth flow, data flow)
# ✓ Complete dependency lists with exact versions
```

## Technology Templates Available

### Frontend Templates

#### **React** (Default)
- **Core Instructions:**
  - Functional components with hooks (useState, useEffect, useContext)
  - TypeScript with strict mode
  - React Query for server state management
  - React Router v6 with lazy loading
  - Custom hooks (useAuth, useApi, useForm, useDebounce)
  - Context API for global state
  - React Hook Form + Zod validation

- **Styling Requirements:**
  - Complete Tailwind CSS configuration
  - Custom theme (colors, fonts, spacing, shadows)
  - 15-20 fully styled UI components
  - Responsive design (mobile-first)
  - Dark mode support
  - Interactive states (hover, focus, active, disabled)

- **Dependencies:** 
  - react@18.2.0, react-router-dom@6.x, @tanstack/react-query@5.x
  - react-hook-form@7.x, zod@3.x, axios@1.x
  - clsx@2.x, tailwind-merge@2.x, @heroicons/react@2.x

#### **Vue**
- Composition API with `<script setup>`
- Pinia for state management
- Vue Router with lazy loading
- VeeValidate for forms
- Tailwind CSS integration

#### **Angular**
- Standalone components (Angular 17+)
- Reactive forms with validators
- RxJS for reactive programming
- Angular Material or PrimeNG
- HttpInterceptor for auth

### Backend Templates

#### **FastAPI** (Default)
- **Core Instructions:**
  - Async route handlers for I/O operations
  - Pydantic v2 models with Field constraints
  - Dependency injection for DB sessions
  - SQLAlchemy 2.0+ with async support
  - Alembic for database migrations
  - JWT authentication with OAuth2
  - Structured logging with context

- **Project Structure:**
  ```
  backend/
  ├── main.py (App initialization, middleware)
  ├── config.py (Pydantic settings)
  ├── requirements.txt
  ├── src/
  │   ├── models/ (SQLAlchemy models)
  │   ├── schemas/ (Pydantic request/response)
  │   ├── routers/ (API endpoints)
  │   ├── services/ (Business logic)
  │   ├── repositories/ (Data access)
  │   ├── middleware/ (Auth, CORS, error handling)
  │   └── utils/ (Security, database, logging)
  └── alembic/ (Database migrations)
  ```

- **Dependencies:**
  - fastapi==0.109.0, uvicorn==0.27.0
  - sqlalchemy==2.0.25, alembic==1.13.1
  - pydantic==2.5.3, pydantic-settings==2.1.0
  - python-jose==3.3.0, passlib==1.7.4

#### **Express**
- TypeScript with strict mode
- Helmet for security headers
- Express-validator for input validation
- Prisma or TypeORM for database
- JWT authentication middleware

#### **Django**
- Django REST Framework
- Class-based views with serializers
- Django ORM with migrations
- Token authentication
- Celery for background tasks

### Database Templates

#### **PostgreSQL** (Default)
- **Connection Example:**
  ```python
  from sqlalchemy.ext.asyncio import create_async_engine
  
  DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
  engine = create_async_engine(DATABASE_URL, echo=True)
  ```

- **Migration Example:**
  ```python
  # Alembic migration
  def upgrade():
      op.create_table(
          'users',
          sa.Column('id', sa.Integer(), primary_key=True),
          sa.Column('email', sa.String(255), unique=True),
          sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
      )
  ```

#### **MySQL**
- MySQL+aiomysql async driver
- Connection pooling setup
- MySQL-specific syntax considerations

#### **MongoDB**
- Motor (async MongoDB driver)
- Pydantic models with ObjectId handling
- Schema-less flexibility with validation

## Example: React + FastAPI + PostgreSQL

When you select this stack, the system generates:

### Frontend Files (React):
- `package.json` - React 18.2, TypeScript, Tailwind, React Query
- `tailwind.config.js` - Complete custom theme (colors, fonts, spacing)
- `src/styles/globals.css` - CSS variables, animations, base styles
- `src/components/ui/Button.tsx` - 5 variants, loading states, icons
- `src/components/ui/Input.tsx` - Label, error states, validation
- `src/components/ui/Modal.tsx` - Backdrop, animations, close button
- `src/hooks/useAuth.ts` - Authentication logic with JWT
- `src/services/api.ts` - Axios client with interceptors
- `src/pages/LoginPage.tsx` - Styled login form with validation

### Backend Files (FastAPI):
- `main.py` - FastAPI app with CORS, Gzip middleware
- `src/models/user.py` - SQLAlchemy User model with timestamps
- `src/schemas/user.py` - Pydantic UserCreate, UserResponse schemas
- `src/routers/users.py` - CRUD endpoints with dependency injection
- `src/services/user_service.py` - Business logic layer
- `src/middleware/auth.py` - JWT authentication with OAuth2
- `src/utils/security.py` - Password hashing with bcrypt
- `alembic/versions/001_initial.py` - Database migration

### Database Files:
- `schema.sql` - PostgreSQL schema with indexes
- `migrations/001_initial_migration.sql` - Alembic-compatible migration
- `seeds/sample_data.sql` - Test data (5-10 users)

### Integration:
- Frontend calls backend via `http://localhost:8000/api/v1`
- JWT tokens stored in localStorage, included in Authorization header
- Error handling with toast notifications
- Consistent API response format: `{ "success": true, "data": {...} }`

## Benefits of Tech-Specific Templates

### 1. **Framework-Optimized Code**
Each template follows the best practices and patterns specific to that technology:
- React: Hooks, not class components
- Vue: Composition API, not Options API
- FastAPI: Async/await, not sync
- Django: Class-based views with DRF

### 2. **Correct Dependencies**
Templates include exact package versions that work together:
- No version conflicts
- Security updates included
- Dev dependencies separated from production

### 3. **Proper Project Structure**
Each framework has its preferred folder structure:
- React: `components/`, `hooks/`, `pages/`, `services/`
- FastAPI: `routers/`, `services/`, `models/`, `schemas/`
- Django: `apps/`, `models.py`, `views.py`, `serializers.py`

### 4. **Complete Styling**
Frontend templates include full Tailwind configurations:
- Custom theme with design tokens
- Responsive breakpoints
- Dark mode support
- Component variants
- Animation keyframes

### 5. **Security by Default**
Templates include security best practices:
- JWT authentication
- Password hashing (bcrypt)
- Input validation (Pydantic/Zod)
- SQL injection prevention (ORM)
- CORS configuration
- Rate limiting

## Extending Templates

To add a new technology template:

### 1. Add Template Definition

```python
# In services/tech_specific_templates.py

FRONTEND_TEMPLATES["Svelte"] = {
    "core_instructions": """
    🔷 SVELTE SPECIFIC REQUIREMENTS:
    
    • Use Svelte 4+ with TypeScript
    • SvelteKit for routing and SSR
    • Stores for state management ($: reactive declarations)
    • Form validation with custom stores
    • Tailwind CSS for styling
    """,
    "styling_requirements": "Svelte-specific Tailwind setup",
    "dependencies": [
        "svelte@^4.0.0",
        "@sveltejs/kit@^1.0.0",
        "typescript@^5.0.0"
    ],
    "dev_dependencies": ["vite@^5.0.0", "vitest@^1.0.0"]
}
```

### 2. Update Models (if needed)

```python
# In models.py

class Frontend(str, Enum):
    REACT = "React"
    VUE = "Vue"
    ANGULAR = "Angular"
    SVELTE = "Svelte"  # Add new option
```

### 3. Update Extension UI

```typescript
// In r-net-extension/src/generator-webview.html

<select id="frontend">
  <option value="React">React</option>
  <option value="Vue">Vue</option>
  <option value="Angular">Angular</option>
  <option value="Svelte">Svelte</option>
</select>
```

## Usage in Code

### Direct Template Access

```python
from services.tech_specific_templates import TechSpecificTemplates

# Get specific template
react_template = TechSpecificTemplates.get_frontend_template("React")
print(react_template['core_instructions'])
print(react_template['dependencies'])

# Get complete prompt
from models import TechStack

tech_stack = TechStack(
    frontend="React",
    backend="FastAPI",
    database="PostgreSQL"
)

complete_prompt = TechSpecificTemplates.build_complete_prompt(
    tech_stack=tech_stack,
    description="Build a task management app",
    project_name="taskmaster"
)
```

### Integrated Usage (Automatic)

The system automatically uses tech-specific templates when you call:

```python
# In openai_service.py
system_prompt, user_prompt = QuickPromptBuilder.tech_template_based(
    tech_stack=tech_stack,
    project_name=project_name,
    description=description
)
# ↑ This internally calls TechSpecificTemplates.build_complete_prompt()
```

## Configuration

All templates are configurable through `tech_specific_templates.py`:

```python
# Customize template content
FRONTEND_TEMPLATES["React"]["core_instructions"] = "Your custom React instructions"

# Add more dependencies
FRONTEND_TEMPLATES["React"]["dependencies"].append("framer-motion@^10.0.0")

# Modify styling requirements
FRONTEND_TEMPLATES["React"]["styling_requirements"] = "Your custom styling guide"
```

## Template Validation

Templates are automatically validated when loaded:

```python
# Each template must have required keys
required_keys = ["core_instructions", "dependencies"]

for template_name, template in FRONTEND_TEMPLATES.items():
    assert all(key in template for key in required_keys), \
        f"Template {template_name} missing required keys"
```

## Best Practices

1. **Keep Templates Updated:** Update dependency versions quarterly
2. **Test Each Stack Combination:** Verify React+FastAPI+PostgreSQL works together
3. **Follow Framework Conventions:** Use official style guides as reference
4. **Include Examples:** Show actual code patterns in instructions
5. **Specify Versions:** Always include exact or range versions for dependencies
6. **Add Comments:** Explain why certain patterns are recommended

## Migration from Old System

If you have existing prompts:

```python
# Old way (generic)
system_prompt = PromptTemplateEngine.create_enhanced_system_prompt(
    tech_stack, project_name, app_type
)

# New way (tech-specific)
system_prompt, user_prompt = QuickPromptBuilder.tech_template_based(
    tech_stack, project_name, description
)
```

The new system provides:
- ✅ 3x more detailed instructions per technology
- ✅ Framework-specific code examples
- ✅ Exact dependency versions
- ✅ Complete project structures
- ✅ Integration guidelines

## Summary

The tech-specific template system ensures that every generated project follows the best practices and patterns for the exact technologies chosen by the user. This results in:

- **Higher Quality Code:** Framework-optimized patterns
- **Better Integration:** Technologies work together seamlessly
- **Fewer Errors:** Correct dependencies and syntax
- **Production Ready:** Security and performance built-in
- **Maintainable:** Follows community standards

The templates are completely customizable and extensible, allowing you to add new frameworks or modify existing ones to match your team's preferences.
