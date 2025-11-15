# 📁 Folder Structure Comparison

## Before vs After: Architecture Changes

---

## 🔧 MICROSERVICES Architecture (Old Default)

```
project-root/
│
├── backend/                        ← SEPARATE ROOT FOLDER
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── routes/
│   │   ├── users.py
│   │   ├── posts.py
│   │   └── auth.py
│   ├── services/
│   │   ├── user_service.py
│   │   └── auth_service.py
│   ├── middleware/
│   │   ├── auth.py
│   │   └── error_handler.py
│   ├── tests/
│   └── Dockerfile
│
├── frontend/                       ← SEPARATE ROOT FOLDER
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   └── Modal.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   └── DashboardPage.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useApi.ts
│   │   ├── services/
│   │   │   └── apiClient.ts
│   │   └── styles/
│   │       └── globals.css
│   ├── tests/
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

### Characteristics:
- ✅ Independent deployment (2 Docker containers)
- ✅ Separate CI/CD pipelines
- ✅ Team autonomy (backend/frontend teams work independently)
- ❌ No shared code (types duplicated)
- ❌ CORS configuration needed
- ❌ More complex setup

---

## 🏗️ MONOLITHIC Architecture (New Default)

```
project-root/
│
├── src/                            ← SINGLE ROOT SOURCE FOLDER
│   │
│   ├── server/                     ← Backend in subfolder
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── post.py
│   │   │   └── comment.py
│   │   ├── routes/
│   │   │   ├── users.py
│   │   │   ├── posts.py
│   │   │   └── auth.py
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   └── auth_service.py
│   │   ├── middleware/
│   │   │   ├── auth.py
│   │   │   └── error_handler.py
│   │   └── utils/
│   │       └── database.py
│   │
│   ├── client/                     ← Frontend in subfolder
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   └── Modal.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   └── DashboardPage.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useApi.ts
│   │   ├── services/
│   │   │   └── apiClient.ts
│   │   └── styles/
│   │       └── globals.css
│   │
│   └── shared/                     ← Shared code between client & server
│       ├── types/
│       │   ├── User.ts
│       │   ├── Post.ts
│       │   └── Comment.ts
│       ├── constants/
│       │   └── apiRoutes.ts
│       └── validators/
│           └── userSchema.ts
│
├── package.json                    ← Single package.json
├── tsconfig.json                   ← Single TypeScript config
├── docker-compose.yml
├── Dockerfile                      ← Single Dockerfile
└── README.md
```

### Characteristics:
- ✅ Shared types (no duplication)
- ✅ Single deployment (1 Docker container)
- ✅ Simpler development (no CORS issues)
- ✅ Single build process
- ✅ Better for full-stack frameworks
- ❌ Less team autonomy

---

## 📊 Side-by-Side Import Examples

### Microservices (Separate Folders)

**Backend imports:**
```python
# backend/routes/users.py
from models.user import User                    # Local import
from services.user_service import UserService   # Local import
```

**Frontend imports:**
```typescript
// frontend/src/pages/HomePage.tsx
import { Button } from '../components/Button';    // Relative import
import { useAuth } from '../hooks/useAuth';       // Relative import
```

**❌ Cannot share types:**
```typescript
// Frontend needs to duplicate types or fetch from API
interface User {  // Duplicated in frontend!
  id: number;
  name: string;
  email: string;
}
```

---

### Monolithic (Unified Folder)

**Backend imports:**
```python
# src/server/routes/users.py
from src.server.models.user import User              # From server/
from src.server.services.user_service import UserService
from src.shared.types import UserSchema              # From shared/! ✅
```

**Frontend imports:**
```typescript
// src/client/pages/HomePage.tsx
import { Button } from '@/client/components/Button';  // Alias import
import { useAuth } from '@/client/hooks/useAuth';
import { User } from '@/shared/types/User';           // Shared types! ✅
```

**✅ Shared types:**
```typescript
// src/shared/types/User.ts
export interface User {
  id: number;
  name: string;
  email: string;
}

// Used by BOTH client and server - no duplication!
```

---

## 🐳 Docker Configuration Comparison

### Microservices (2 Containers)

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend              # ← Separate Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
  
  frontend:
    build: ./frontend             # ← Separate Dockerfile
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://backend:8000
    depends_on:
      - backend
```

---

### Monolithic (1 Container)

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .                      # ← Single Dockerfile at root
    ports:
      - "3000:3000"               # Single port for full-stack
    environment:
      - DATABASE_URL=postgresql://...
```

```dockerfile
# Dockerfile (at root)
FROM node:20 AS build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build                 # Builds both client and server

FROM node:20-slim
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY package*.json ./
RUN npm install --production

EXPOSE 3000
CMD ["node", "dist/server/main.js"]
```

---

## 📝 File Path Examples

### Example 1: User Model

**Microservices:**
```
backend/models/user.py
frontend/src/types/User.ts (duplicated!)
```

**Monolithic:**
```
src/server/models/user.py
src/shared/types/User.ts (shared by both!)
```

---

### Example 2: Authentication

**Microservices:**
```
backend/routes/auth.py
backend/middleware/auth.py
frontend/src/services/authService.ts
frontend/src/hooks/useAuth.ts
```

**Monolithic:**
```
src/server/routes/auth.py
src/server/middleware/auth.py
src/client/services/authService.ts
src/client/hooks/useAuth.ts
src/shared/types/AuthToken.ts (shared!)
```

---

### Example 3: API Routes

**Microservices:**
```typescript
// frontend/src/services/apiClient.ts
const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8000';
// Must handle CORS, different origins
```

**Monolithic:**
```typescript
// src/client/services/apiClient.ts
const API_BASE_URL = '/api';  // Same origin, no CORS!
```

---

## 🎯 When to Use Each

### Use Monolithic 🏗️ When:

| Scenario | Why? |
|----------|------|
| **Next.js / Remix / SvelteKit** | These frameworks are built for monolithic architecture |
| **Single team (1-5 devs)** | Simpler collaboration, shared codebase |
| **Shared TypeScript types** | Frontend and backend use same interfaces |
| **Rapid prototyping** | Faster development, single build process |
| **Startup / MVP** | Lower operational complexity |
| **Same language** | TypeScript full-stack (Node.js + React) |

---

### Use Microservices 🔧 When:

| Scenario | Why? |
|----------|------|
| **Large teams (5+ devs)** | Backend and frontend teams work independently |
| **Different languages** | Python backend + React frontend |
| **Independent scaling** | Backend needs more resources than frontend |
| **Separate deployments** | Deploy backend and frontend independently |
| **Enterprise** | Established DevOps pipelines |
| **Polyglot architecture** | Mix of languages (Python, Go, Java, etc.) |

---

## 📊 Decision Matrix

| Criteria | Monolithic | Microservices |
|----------|------------|---------------|
| **Folder Structure** | `src/server`, `src/client`, `src/shared` | `backend/`, `frontend/` |
| **Deployment** | 1 Docker container | 2+ Docker containers |
| **Build Process** | Single build | Separate builds |
| **Code Sharing** | Easy (shared folder) | Hard (API contracts only) |
| **CORS** | Not needed (same origin) | Required (different origins) |
| **Team Size** | 1-5 developers | 5+ developers |
| **Complexity** | Low | High |
| **Development Speed** | Faster | Slower |

---

## 🚀 Migration Path

### Microservices → Monolithic

```bash
# Create unified structure
mkdir -p src/server src/client src/shared

# Move backend
mv backend/* src/server/

# Move frontend
mv frontend/src/* src/client/

# Extract shared types
# Move common interfaces to src/shared/types/

# Update imports
# Change relative paths to alias paths (@/server, @/client, @/shared)
```

---

### Monolithic → Microservices

```bash
# Create separate folders
mkdir backend frontend

# Extract backend
mv src/server/* backend/

# Extract frontend
mv src/client/* frontend/src/

# Duplicate shared types
# Copy src/shared/types to both backend and frontend

# Update imports
# Remove shared folder references, duplicate types
```

---

## ✅ Summary

| Architecture | Structure | Best For |
|--------------|-----------|----------|
| **Monolithic** (Default) | `src/server + src/client + src/shared` | Small teams, single language, rapid development |
| **Microservices** | `backend/ + frontend/` | Large teams, polyglot, independent scaling |

**Your system now supports BOTH**, with **Monolithic as the default**! 🎉
