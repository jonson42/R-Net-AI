# Tech-Specific Template Integration

## Overview
The chained generation service now dynamically selects prompts based on the user's technology stack choices (Frontend, Backend, Database).

## How It Works

### 1. User Selection Flow
```
User selects in UI:
├── Frontend: React / Vue / Angular / Next.js / Svelte
├── Backend: FastAPI / Express / Django / NestJS / Flask / Spring Boot
└── Database: PostgreSQL / MySQL / MongoDB / SQLite
```

### 2. Template Selection Process

When a user initiates code generation, the system:

1. **Receives tech stack** from UI (`TechStack` model)
2. **Loads tech-specific templates** from `tech_specific_templates.py`
3. **Applies templates** to each generation step
4. **Generates optimized code** for the selected technologies

### 3. Integration Points

#### Step 2: Database Schema Generation
```python
# Get tech-specific database template
db_template = self.tech_templates.get_database_prompt(
    tech_stack.database.value,  # e.g., "PostgreSQL"
    tables,                      # List of tables from architecture
    has_auth                     # Boolean: needs authentication?
)

# Template is injected into system prompt
system_prompt = f"""You are a database expert for {tech_stack.database}.

{db_template}  # 🎯 Tech-specific instructions here

Return ONLY valid JSON:
{{"files": [...]}}"""
```

#### Step 3: Backend API Generation
```python
# Get tech-specific backend template
backend_template = self.tech_templates.get_backend_prompt(
    tech_stack.backend.value,   # e.g., "FastAPI"
    endpoints,                   # List of API endpoints
    has_auth                     # Boolean: needs authentication?
)

# Template provides framework-specific patterns
system_prompt = f"""You are a backend expert for {tech_stack.backend}.

{backend_template}  # 🎯 FastAPI-specific patterns, folder structure, etc.

Create complete backend with:
1. Main application file
2. API routes
..."""
```

#### Step 4: Frontend Components Generation
```python
# Get tech-specific frontend template
frontend_template = self.tech_templates.get_frontend_prompt(
    tech_stack.frontend.value,  # e.g., "React"
    pages,                       # List of pages
    components                   # List of components
)

# Template provides React-specific patterns
system_prompt = f"""You are a frontend expert for {tech_stack.frontend}.

{frontend_template}  # 🎯 React hooks, TypeScript, component patterns

Generate complete frontend with:
1. Page components
2. Reusable UI components
..."""
```

## Template Examples

### Frontend Templates (React)
- **Project Structure**: `frontend/src/components/`, `hooks/`, `contexts/`
- **Component Patterns**: Functional components with TypeScript
- **State Management**: React hooks (`useState`, `useEffect`, `useContext`)
- **Styling**: Tailwind CSS with custom theme
- **API Integration**: Axios with interceptors
- **Routing**: React Router v6

### Backend Templates (FastAPI)
- **Project Structure**: `backend/app/routers/`, `services/`, `models/`
- **API Patterns**: Async route handlers with dependency injection
- **Authentication**: JWT with `python-jose`, OAuth2 password flow
- **Database**: SQLAlchemy ORM with async support
- **Validation**: Pydantic models for request/response
- **Documentation**: Automatic OpenAPI/Swagger

### Database Templates (PostgreSQL)
- **Schema Files**: SQL migrations with `psycopg2` or SQLAlchemy
- **Tables**: Proper indexes, foreign keys, constraints
- **Authentication**: `users`, `sessions`, `tokens` tables
- **Data Types**: JSON columns for flexible data
- **Performance**: Indexes on frequently queried columns

## Benefits

### 1. Technology-Optimized Code
- **Before**: Generic code that works but not idiomatic
- **After**: Framework-specific patterns and best practices

### 2. Consistent Project Structure
- **Before**: Random folder organization
- **After**: Industry-standard structure for each framework

### 3. Complete Dependencies
- **Before**: Missing packages, incomplete setup
- **After**: All required dependencies with correct versions

### 4. Better Integration
- **Before**: Components don't connect well
- **After**: Frontend knows exact backend API structure

## Example: React + FastAPI + PostgreSQL

### User Selects:
```json
{
  "frontend": "React",
  "backend": "FastAPI",
  "database": "PostgreSQL"
}
```

### System Generates:

#### Frontend (React Template Applied)
```
frontend/
├── package.json (React 18, TypeScript, Vite, Tailwind)
├── tsconfig.json (strict mode, jsx: react-jsx)
├── src/
│   ├── components/
│   │   ├── ui/Button.tsx (Tailwind + variants)
│   │   ├── ui/Input.tsx
│   │   └── layout/Header.tsx
│   ├── hooks/useAuth.ts (JWT handling)
│   ├── services/apiClient.ts (Axios + interceptors)
│   └── pages/Dashboard.tsx (React Router)
```

#### Backend (FastAPI Template Applied)
```
backend/
├── requirements.txt (FastAPI, SQLAlchemy, pydantic, python-jose)
├── app/
│   ├── main.py (FastAPI app with CORS)
│   ├── routers/auth.py (JWT endpoints)
│   ├── models/user.py (SQLAlchemy models)
│   ├── schemas/user.py (Pydantic schemas)
│   └── dependencies.py (get_db, get_current_user)
```

#### Database (PostgreSQL Template Applied)
```
database/
├── migrations/001_initial.sql
├── schema.sql (CREATE TABLE with indexes)
└── seed.sql (sample data)
```

## Configuration

No configuration needed! The system automatically:
1. Reads user's tech stack selection
2. Loads appropriate templates
3. Generates optimized code

## Logging

All template selections are logged:
```
2025-11-14 14:21:05 - INFO - Step 2/5: Database schema (PostgreSQL template)
2025-11-14 14:21:30 - INFO - Step 3/5: Backend API (FastAPI template)
2025-11-14 14:21:55 - INFO - Step 4/5: Frontend (React template)
```

## Template Coverage

### Supported Frontends:
- ✅ React (TypeScript + Vite + Tailwind)
- ✅ Vue (Composition API + TypeScript)
- ✅ Angular (Standalone components)
- ✅ Next.js (App Router + Server Components)
- ✅ Svelte (SvelteKit + TypeScript)

### Supported Backends:
- ✅ FastAPI (Async + SQLAlchemy + Pydantic)
- ✅ Express (TypeScript + Prisma)
- ✅ Django (Django REST Framework)
- ✅ NestJS (TypeScript + TypeORM)
- ✅ Flask (Blueprints + SQLAlchemy)
- ✅ Spring Boot (Java 17 + Spring Data JPA)

### Supported Databases:
- ✅ PostgreSQL (Advanced features: JSON, indexes)
- ✅ MySQL (InnoDB engine, proper constraints)
- ✅ MongoDB (Document schemas, indexes)
- ✅ SQLite (Embedded, migrations)

## Next Steps

1. **Test with different combinations**: Try React + Express + MongoDB
2. **Review generated code**: Check if it matches your expectations
3. **Customize templates**: Edit `tech_specific_templates.py` if needed
4. **Add new technologies**: Follow the template pattern to add support

## File Locations

- **Template Definitions**: `r-net-backend/services/tech_specific_templates.py`
- **Integration Logic**: `r-net-backend/services/chained_generation_service.py`
- **Prompt Logs**: `r-net-backend/logs/app.log`
