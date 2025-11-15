# Architecture Type Configuration Guide 🏗️

## Overview

The R-Net AI Code Generator now supports **TWO architecture patterns** for project structure:

1. **Monolithic Architecture** (Default) - Single unified folder structure
2. **Microservices Architecture** - Separate backend/ and frontend/ folders

You can now choose which architecture pattern to use when generating code!

---

## 🎯 Architecture Types

### 1. Monolithic Architecture (Default)

**Best for:**
- Single-team projects
- Next.js, Nuxt.js, ASP.NET MVC, Django full-stack apps
- Shared TypeScript types between client and server
- Simpler deployment (one Docker container)
- Monorepo workflows

**Folder Structure:**
```
project-root/
├── src/
│   ├── server/              # Backend code
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── middleware/
│   │
│   ├── client/              # Frontend code
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── styles/
│   │
│   └── shared/              # Shared code
│       ├── types/           # TypeScript interfaces
│       └── constants/
│
├── package.json             # Single package.json
├── tsconfig.json
├── docker-compose.yml
└── README.md
```

**Example File Paths:**
- Backend API: `src/server/routes/users.ts`
- Frontend Page: `src/client/pages/Dashboard.tsx`
- Shared Type: `src/shared/types/User.ts`
- Database Model: `src/server/models/user.model.ts`

**Advantages:**
- ✅ Easier to share code (types, utilities, constants)
- ✅ Single build process and deployment
- ✅ Simplified dependency management (one package.json)
- ✅ Better for full-stack frameworks (Next.js, Remix, SvelteKit)
- ✅ Faster local development (no CORS issues)

---

### 2. Microservices Architecture

**Best for:**
- Multi-team projects (separate backend/frontend teams)
- Independent scaling requirements
- Different tech stacks (Python backend + React frontend)
- Separate deployment pipelines
- Microservices/containerized environments

**Folder Structure:**
```
project-root/
├── backend/                 # Backend microservice
│   ├── main.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── tests/
│   └── Dockerfile
│
├── frontend/                # Frontend microservice
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── styles/
│   ├── tests/
│   └── Dockerfile
│
├── docker-compose.yml       # Orchestrates both services
└── README.md
```

**Example File Paths:**
- Backend API: `backend/routes/users.py`
- Frontend Page: `frontend/src/pages/Dashboard.tsx`
- Backend Model: `backend/models/user.py`
- Frontend Component: `frontend/src/components/Button.tsx`

**Advantages:**
- ✅ Independent deployment and scaling
- ✅ Team autonomy (backend/frontend teams work independently)
- ✅ Technology flexibility (different languages/frameworks)
- ✅ Easier to version APIs independently
- ✅ Standard microservices pattern

---

## 📝 How to Use

### API Request

Add the `architecture` field to your `tech_stack` object:

```json
{
  "image_data": "base64_encoded_image...",
  "description": "A task management app with authentication",
  "tech_stack": {
    "frontend": "React",
    "backend": "FastAPI",
    "database": "PostgreSQL",
    "architecture": "monolithic"  // or "microservices"
  },
  "project_name": "task-manager"
}
```

### Architecture Field Options

```typescript
architecture: "monolithic" | "microservices"
```

**Default:** If you don't specify `architecture`, it defaults to **`monolithic`**.

---

## 🔄 Examples

### Example 1: Monolithic Next.js App

```json
{
  "tech_stack": {
    "frontend": "React",
    "backend": "Express",
    "database": "PostgreSQL",
    "architecture": "monolithic"
  }
}
```

**Generated Structure:**
```
src/
├── server/
│   ├── server.ts          # Express server
│   ├── routes/
│   └── middleware/
├── client/
│   ├── App.tsx            # React app
│   ├── pages/
│   └── components/
└── shared/
    └── types/
```

---

### Example 2: Microservices with Python + React

```json
{
  "tech_stack": {
    "frontend": "React",
    "backend": "FastAPI",
    "database": "PostgreSQL",
    "architecture": "microservices"
  }
}
```

**Generated Structure:**
```
backend/
├── main.py
├── requirements.txt
├── models/
└── routes/

frontend/
├── package.json
├── src/
│   ├── App.tsx
│   ├── components/
│   └── pages/
```

---

### Example 3: Django Full-Stack (Monolithic)

```json
{
  "tech_stack": {
    "frontend": "React",
    "backend": "Django",
    "database": "PostgreSQL",
    "architecture": "monolithic"
  }
}
```

**Generated Structure:**
```
src/
├── server/
│   ├── manage.py
│   ├── settings.py
│   ├── apps/
│   └── templates/
└── client/
    ├── components/
    └── pages/
```

---

## 🎨 Framework-Specific Recommendations

### Monolithic Architecture (Recommended for):

| Framework | Why? |
|-----------|------|
| **Next.js** | Built for monolithic (API routes + pages in one project) |
| **Nuxt.js** | Same as Next.js, designed for unified structure |
| **SvelteKit** | Full-stack framework with unified routing |
| **Remix** | Server-side rendering with unified folder structure |
| **ASP.NET MVC** | Traditional monolithic architecture |
| **Django** | Full-stack framework with templates |
| **Laravel** | PHP full-stack with Blade templates |

### Microservices Architecture (Recommended for):

| Stack | Why? |
|-------|------|
| **React + FastAPI** | Separate concerns, different languages |
| **Vue + Django REST** | Independent deployment, separate teams |
| **Angular + Express** | Large teams, independent scaling |
| **React + .NET Core** | Enterprise, separate CI/CD pipelines |

---

## 🚀 Migration Between Architectures

If you need to convert between architectures:

### Monolithic → Microservices

Move files:
```bash
# Extract backend
mv src/server/* backend/
mv src/shared/types backend/types

# Extract frontend  
mv src/client/* frontend/src/
mv src/shared/constants frontend/src/constants

# Update imports
# backend/ imports from backend/types
# frontend/ imports types via API responses (no shared code)
```

### Microservices → Monolithic

Merge folders:
```bash
# Create unified structure
mkdir -p src/server src/client src/shared

# Move backend
mv backend/* src/server/

# Move frontend
mv frontend/src/* src/client/

# Extract shared types to src/shared/
```

---

## 🐳 Docker Configuration

### Monolithic (Single Container)

```dockerfile
# Dockerfile
FROM node:20 AS build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:20-slim
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY package*.json ./
RUN npm install --production

EXPOSE 3000
CMD ["node", "dist/server/main.js"]
```

### Microservices (Separate Containers)

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://backend:8000
```

---

## 🔧 Configuration in Code

### Backend Check

```python
# In chained_generation_service.py
from models import ArchitectureType

if tech_stack.architecture == ArchitectureType.MONOLITHIC:
    # Generate: src/server/main.py
    pass
else:
    # Generate: backend/main.py
    pass
```

### Frontend Check

```typescript
// In extension
interface TechStack {
  frontend: string;
  backend: string;
  database: string;
  architecture: 'monolithic' | 'microservices'; // Default: 'monolithic'
}
```

---

## ✅ Best Practices

### For Monolithic:
1. **Shared types:** Use `src/shared/types/` for TypeScript interfaces
2. **Single package.json:** Manage all dependencies in one file
3. **Unified config:** One tsconfig.json, one ESLint config
4. **Relative imports:** `import { User } from '@/shared/types/User'`
5. **Single build:** One Dockerfile, one deployment

### For Microservices:
1. **API contracts:** Document API with OpenAPI/Swagger
2. **Independent versioning:** Semantic versioning for each service
3. **CORS configuration:** Backend must allow frontend origin
4. **Separate dependencies:** backend/requirements.txt, frontend/package.json
5. **Health checks:** Each service has `/health` endpoint

---

## 📊 Decision Matrix

| Criteria | Monolithic | Microservices |
|----------|------------|---------------|
| Team Size | 1-5 developers | 5+ developers |
| Deployment Frequency | Weekly/Monthly | Multiple times daily |
| Scaling Needs | Vertical (single instance) | Horizontal (multiple instances) |
| Tech Stack | Same language/framework | Different languages |
| Shared Code | Extensive (types, utils) | Minimal (API contracts) |
| Development Speed | Faster (simpler) | Slower (more coordination) |
| Operational Complexity | Low | High |

---

## 🆘 Troubleshooting

### Issue: Files generated in wrong folders

**Solution:** Check your request includes the correct `architecture` value:

```json
{
  "tech_stack": {
    "architecture": "monolithic"  // ← Make sure this is set!
  }
}
```

### Issue: CORS errors in monolithic setup

**Solution:** Configure backend to run on same origin as frontend (e.g., Next.js API routes)

### Issue: Import errors between client/server in monolithic

**Solution:** Configure TypeScript path aliases:

```json
{
  "compilerOptions": {
    "paths": {
      "@/server/*": ["./src/server/*"],
      "@/client/*": ["./src/client/*"],
      "@/shared/*": ["./src/shared/*"]
    }
  }
}
```

---

## 🎯 Summary

- **Default:** Monolithic (single `src/` folder with `server/` and `client/`)
- **Alternative:** Microservices (separate `backend/` and `frontend/` root folders)
- **Configure via:** `tech_stack.architecture` field in API request
- **Monolithic = Simpler, faster, better for small teams**
- **Microservices = Scalable, flexible, better for large teams**

Choose the architecture that fits your team size, deployment requirements, and scaling needs! 🚀
