"""
Technology-Specific Prompt Templates
Dynamic template selection based on user's tech stack choices
"""

from typing import Dict, List
from models import TechStack


class TechSpecificTemplates:
    """
    Manages technology-specific prompt templates for each framework/language
    Templates are selected dynamically based on user's UI selections
    """
    
    # ==================== FRONTEND TEMPLATES ====================
    
    FRONTEND_TEMPLATES = {
        "React": {
            "core_instructions": """
🔷 REACT-SPECIFIC REQUIREMENTS:

**Project Structure:**
```
frontend/
├── package.json (React 18.2+, React Router 6, TypeScript 5)
├── tsconfig.json (strict: true, jsx: react-jsx)
├── vite.config.ts (or next.config.js for Next.js)
├── tailwind.config.js (COMPLETE custom theme - MANDATORY)
├── postcss.config.js (Tailwind + autoprefixer)
├── src/
│   ├── main.tsx (ReactDOM.createRoot, Router setup)
│   ├── App.tsx (Layout, routing, global providers)
│   ├── styles/
│   │   ├── globals.css (Tailwind directives + custom styles)
│   │   └── theme.ts (design tokens)
│   ├── components/
│   │   ├── ui/ (15-20 reusable styled components)
│   │   ├── layout/ (Header, Sidebar, Footer, MainLayout)
│   │   └── features/ (domain-specific components)
│   ├── pages/ (route components with lazy loading)
│   ├── hooks/ (useAuth, useApi, useLocalStorage, useDebounce, useMediaQuery)
│   ├── contexts/ (AuthContext, ThemeContext, ToastContext)
│   ├── services/ (API client, auth service)
│   ├── types/ (TypeScript interfaces)
│   └── utils/ (validators, formatters, cn utility)
└── public/ (index.html, favicon, assets)
```

**Component Patterns:**
1. Functional components ONLY (no class components)
2. TypeScript with explicit prop types:
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
}

export const Button = ({ variant = 'primary', size = 'md', loading, ...props }: ButtonProps) => {
  // Implementation with cn() utility for class merging
};
```

3. Custom Hooks Pattern:
```typescript
// useAuth.ts
export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  
  const login = async (credentials: LoginCredentials) => { /* ... */ };
  const logout = async () => { /* ... */ };
  const refreshToken = async () => { /* ... */ };
  
  return { user, loading, login, logout, isAuthenticated: !!user };
};

// useApi.ts with React Query
export const useApi = <T,>(endpoint: string, options?: UseQueryOptions) => {
  return useQuery<T>({
    queryKey: [endpoint],
    queryFn: () => apiClient.get(endpoint),
    ...options
  });
};
```

4. Context Pattern for Global State:
```typescript
interface AuthContextType {
  user: User | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  // Implementation
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
```

**Routing Setup:**
```typescript
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { lazy, Suspense } from 'react';

// Lazy load pages
const HomePage = lazy(() => import('./pages/HomePage'));
const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const LoginPage = lazy(() => import('./pages/LoginPage'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageSpinner />}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          } />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

**State Management:**
- Context API for global state (auth, theme, notifications)
- React Query for server state (data fetching, caching, mutations)
- useState/useReducer for local component state
- Optional: Zustand for complex client state

**Form Handling:**
```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters')
});

type LoginFormData = z.infer<typeof loginSchema>;

export const LoginForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema)
  });
  
  const onSubmit = (data: LoginFormData) => { /* ... */ };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input {...register('email')} error={errors.email?.message} />
      <Input type="password" {...register('password')} error={errors.password?.message} />
      <Button type="submit">Login</Button>
    </form>
  );
};
```

**Performance Optimizations:**
```typescript
// Memoize expensive computations
const sortedItems = useMemo(() => items.sort((a, b) => a.name.localeCompare(b.name)), [items]);

// Memoize callbacks to prevent re-renders
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);

// Memoize components
export const ExpensiveComponent = React.memo(({ data }) => {
  // Render logic
});

// Code splitting
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

**Testing:**
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('validates email format', async () => {
    render(<LoginForm />);
    const emailInput = screen.getByLabelText('Email');
    fireEvent.change(emailInput, { target: { value: 'invalid' } });
    fireEvent.submit(screen.getByRole('button'));
    expect(await screen.findByText('Invalid email address')).toBeInTheDocument();
  });
});
```
""",
            "styling_requirements": """
🎨 REACT + TAILWIND CSS STYLING (MANDATORY):

**1. Tailwind Configuration (tailwind.config.js):**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        },
        success: { 50: '#f0fdf4', 500: '#22c55e', 900: '#14532d' },
        warning: { 50: '#fffbeb', 500: '#f59e0b', 900: '#78350f' },
        error: { 50: '#fef2f2', 500: '#ef4444', 900: '#7f1d1d' },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        heading: ['Poppins', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      boxShadow: {
        'soft': '0 2px 8px rgba(0, 0, 0, 0.04)',
        'medium': '0 4px 16px rgba(0, 0, 0, 0.08)',
        'strong': '0 8px 32px rgba(0, 0, 0, 0.12)',
        'inner-soft': 'inset 0 2px 4px rgba(0, 0, 0, 0.06)',
      },
      borderRadius: {
        'sm': '0.25rem',
        'md': '0.375rem',
        'lg': '0.5rem',
        'xl': '0.75rem',
        '2xl': '1rem',
      },
      animation: {
        'fadeIn': 'fadeIn 0.3s ease-out',
        'slideIn': 'slideIn 0.3s ease-out',
        'slideOut': 'slideOut 0.3s ease-out',
        'scaleIn': 'scaleIn 0.2s ease-out',
        'spin-slow': 'spin 3s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        slideOut: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-100%)' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
};
```

**2. Global Styles (src/styles/globals.css):**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --color-primary: 37 99 235;
  --color-secondary: 71 85 105;
  --color-success: 34 197 94;
  --color-warning: 245 158 11;
  --color-error: 239 68 68;
  --radius: 0.5rem;
  --shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

@layer base {
  * {
    @apply border-border;
  }
  
  body {
    @apply bg-gray-50 text-gray-900 antialiased;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
  }
  
  h1 {
    @apply text-4xl font-bold text-gray-900 tracking-tight mb-4;
  }
  
  h2 {
    @apply text-3xl font-semibold text-gray-800 tracking-tight mb-3;
  }
  
  h3 {
    @apply text-2xl font-semibold text-gray-800 mb-2;
  }
  
  p {
    @apply text-base text-gray-600 leading-relaxed;
  }
  
  a {
    @apply text-primary-600 hover:text-primary-700 transition-colors underline-offset-4;
  }
  
  /* Custom scrollbar */
  ::-webkit-scrollbar {
    @apply w-2 h-2;
  }
  
  ::-webkit-scrollbar-track {
    @apply bg-gray-100;
  }
  
  ::-webkit-scrollbar-thumb {
    @apply bg-gray-300 rounded-full hover:bg-gray-400;
  }
}

@layer components {
  .btn {
    @apply inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed;
  }
  
  .btn-primary {
    @apply btn bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500 active:bg-primary-800;
  }
  
  .btn-secondary {
    @apply btn bg-secondary-600 text-white hover:bg-secondary-700 focus:ring-secondary-500;
  }
  
  .input {
    @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors;
  }
  
  .card {
    @apply bg-white rounded-xl shadow-soft p-6 hover:shadow-medium transition-shadow;
  }
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}
```

**3. Utility Function (src/utils/cn.ts):**
```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

**4. Component Styling Examples:**

Button Component:
```typescript
import { cn } from '@/utils/cn';

const buttonVariants = {
  primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
  secondary: 'bg-secondary-600 text-white hover:bg-secondary-700 focus:ring-secondary-500',
  outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-primary-500',
  ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
  danger: 'bg-error-600 text-white hover:bg-error-700 focus:ring-error-500',
};

const buttonSizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
};

export const Button = ({ variant = 'primary', size = 'md', className, ...props }) => (
  <button
    className={cn(
      'inline-flex items-center justify-center font-medium rounded-lg',
      'transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      buttonVariants[variant],
      buttonSizes[size],
      className
    )}
    {...props}
  />
);
```

Card Component:
```typescript
export const Card = ({ children, className, hover = true }) => (
  <div
    className={cn(
      'bg-white rounded-xl shadow-soft p-6',
      hover && 'hover:shadow-medium transition-shadow',
      className
    )}
  >
    {children}
  </div>
);
```
""",
            "dependencies": [
                "react@^18.2.0",
                "react-dom@^18.2.0",
                "react-router-dom@^6.20.0",
                "@tanstack/react-query@^5.14.0",
                "axios@^1.6.0",
                "react-hook-form@^7.49.0",
                "@hookform/resolvers@^3.3.2",
                "zod@^3.22.4",
                "clsx@^2.0.0",
                "tailwind-merge@^2.2.0",
                "@heroicons/react@^2.1.0",
            ],
            "dev_dependencies": [
                "typescript@^5.3.0",
                "@types/react@^18.2.0",
                "@types/react-dom@^18.2.0",
                "@vitejs/plugin-react@^4.2.0",
                "vite@^5.0.0",
                "tailwindcss@^3.4.0",
                "postcss@^8.4.0",
                "autoprefixer@^10.4.0",
                "@testing-library/react@^14.1.0",
                "@testing-library/jest-dom@^6.1.0",
                "vitest@^1.0.0",
                "eslint@^8.55.0",
                "prettier@^3.1.0",
            ]
        },
        
        "Vue": {
            "core_instructions": """
🔷 VUE 3 SPECIFIC REQUIREMENTS:

**Use Composition API with <script setup>:**
```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { User } from '@/types';

const user = ref<User | null>(null);
const isLoading = ref(false);

const fullName = computed(() => 
  user.value ? `${user.value.firstName} ${user.value.lastName}` : ''
);

const fetchUser = async () => {
  isLoading.value = true;
  // Fetch logic
  isLoading.value = false;
};

onMounted(() => {
  fetchUser();
});
</script>

<template>
  <div class="user-card">
    <div v-if="isLoading">Loading...</div>
    <div v-else-if="user">{{ fullName }}</div>
  </div>
</template>

<style scoped>
.user-card {
  @apply bg-white rounded-lg shadow p-4;
}
</style>
```

**Composables (Vue's hooks):**
```typescript
// composables/useAuth.ts
import { ref, computed } from 'vue';
import type { User } from '@/types';

export const useAuth = () => {
  const user = ref<User | null>(null);
  const loading = ref(false);
  
  const login = async (credentials: LoginCredentials) => {
    loading.value = true;
    // Login logic
    loading.value = false;
  };
  
  const isAuthenticated = computed(() => !!user.value);
  
  return { user, loading, login, logout, isAuthenticated };
};
```

**Pinia Store:**
```typescript
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null);
  const isAuthenticated = computed(() => !!user.value);
  
  async function login(credentials: LoginCredentials) {
    // Login logic
  }
  
  return { user, isAuthenticated, login };
});
```

**Vue Router:**
```typescript
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('./pages/Home.vue') },
    { path: '/dashboard', component: () => import('./pages/Dashboard.vue'), meta: { requiresAuth: true } },
  ]
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    next('/login');
  } else {
    next();
  }
});
```
""",
            "styling_requirements": "Use Tailwind CSS with Vue 3, scoped styles in .vue files",
            "dependencies": ["vue@^3.3.0", "vue-router@^4.2.0", "pinia@^2.1.0", "axios@^1.6.0"],
            "dev_dependencies": ["@vitejs/plugin-vue@^4.5.0", "vite@^5.0.0", "typescript@^5.3.0"]
        },
        
        "Angular": {
            "core_instructions": """
🔷 ANGULAR SPECIFIC REQUIREMENTS:

**Standalone Components (Angular 17+):**
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-user-card',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="user-card">
      <h3>{{ user.name }}</h3>
      <p>{{ user.email }}</p>
    </div>
  `,
  styles: [`
    .user-card {
      @apply bg-white rounded-lg shadow p-4;
    }
  `]
})
export class UserCardComponent {
  user = { name: 'John Doe', email: 'john@example.com' };
}
```

**Services with Dependency Injection:**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient) {}
  
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');
  }
}
```

**Reactive Forms:**
```typescript
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
      <input formControlName="email" type="email" />
      <input formControlName="password" type="password" />
      <button type="submit">Login</button>
    </form>
  `
})
export class LoginFormComponent {
  loginForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]]
  });
  
  constructor(private fb: FormBuilder) {}
  
  onSubmit() {
    if (this.loginForm.valid) {
      console.log(this.loginForm.value);
    }
  }
}
```
""",
            "styling_requirements": "Angular Material or Tailwind CSS with Angular",
            "dependencies": ["@angular/core@^17.0.0", "@angular/common@^17.0.0", "@angular/router@^17.0.0", "rxjs@^7.8.0"],
            "dev_dependencies": ["@angular/cli@^17.0.0", "typescript@^5.2.0"]
        }
    }
    
    # ==================== BACKEND TEMPLATES ====================
    
    BACKEND_TEMPLATES = {
        "FastAPI": {
            "core_instructions": """
🔷 FASTAPI SPECIFIC REQUIREMENTS:

**Project Structure:**
```
backend/
├── main.py (FastAPI app initialization)
├── config.py (settings with pydantic-settings)
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── models/ (SQLAlchemy models)
│   │   ├── __init__.py
│   │   ├── base.py (Base model class)
│   │   ├── user.py
│   │   └── entity.py
│   ├── schemas/ (Pydantic schemas)
│   │   ├── __init__.py
│   │   ├── user.py (UserCreate, UserResponse, UserUpdate)
│   │   └── entity.py
│   ├── routers/ (API endpoints)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── entities.py
│   ├── services/ (Business logic)
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── user_service.py
│   ├── repositories/ (Data access)
│   │   ├── __init__.py
│   │   └── user_repository.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py (JWT authentication)
│   │   ├── error_handler.py
│   │   └── rate_limiter.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py (password hashing, JWT)
│   │   ├── database.py (async engine, session)
│   │   └── logger.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_users.py
└── alembic/
    ├── env.py
    └── versions/
```

**Main Application (main.py):**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging

from src.routers import auth, users, entities
from src.utils.database import create_db_and_tables
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logging.info("Starting application...")
    await create_db_and_tables()
    yield
    # Shutdown
    logging.info("Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(entities.router, prefix="/api/v1/entities", tags=["entities"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
```

**Pydantic Schemas:**
```python
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
```

**SQLAlchemy Models:**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**Router with Dependency Injection:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.user import UserCreate, UserResponse, UserUpdate
from src.services.user_service import UserService
from src.utils.database import get_db
from src.middleware.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    return await service.create_user(user_data)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = UserService(db)
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    return await service.list_users(skip=skip, limit=limit)
```

**Service Layer:**
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.utils.security import hash_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        hashed_pwd = hash_password(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_pwd
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
    
    async def get_user(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
```

**Authentication (JWT):**
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Fetch user from database
    return user_id
```

**Testing:**
```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/users/",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data
```
""",
            "dependencies": [
                "fastapi==0.109.0",
                "uvicorn[standard]==0.27.0",
                "sqlalchemy==2.0.25",
                "alembic==1.13.1",
                "pydantic==2.5.3",
                "pydantic-settings==2.1.0",
                "python-jose[cryptography]==3.3.0",
                "passlib[bcrypt]==1.7.4",
                "python-multipart==0.0.6",
                "asyncpg==0.29.0",
                "aiofiles==23.2.1"
            ],
            "dev_dependencies": [
                "pytest==7.4.4",
                "pytest-asyncio==0.23.3",
                "httpx==0.26.0",
                "black==23.12.1",
                "mypy==1.8.0",
                "ruff==0.1.11"
            ]
        },
        
        "Express": {
            "core_instructions": """
🔷 EXPRESS.JS + TYPESCRIPT REQUIREMENTS:

**TypeScript Configuration:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

**Main Server (src/server.ts):**
```typescript
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import morgan from 'morgan';
import rateLimit from 'express-rate-limit';
import { errorHandler } from './middleware/errorHandler';
import authRoutes from './routes/auth';
import userRoutes from './routes/users';

const app = express();

// Middleware
app.use(helmet());
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(',') }));
app.use(express.json());
app.use(morgan('combined'));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100
});
app.use('/api/', limiter);

// Routes
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/users', userRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Error handling
app.use(errorHandler);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

**Controllers:**
```typescript
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/userService';
import { CreateUserDto } from '../dtos/user.dto';

export class UserController {
  private userService: UserService;
  
  constructor() {
    this.userService = new UserService();
  }
  
  createUser = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userData: CreateUserDto = req.body;
      const user = await this.userService.createUser(userData);
      res.status(201).json(user);
    } catch (error) {
      next(error);
    }
  };
  
  getUser = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { id } = req.params;
      const user = await this.userService.getUser(parseInt(id));
      if (!user) {
        return res.status(404).json({ message: 'User not found' });
      }
      res.json(user);
    } catch (error) {
      next(error);
    }
  };
}
```

**Middleware (JWT Authentication):**
```typescript
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

interface JwtPayload {
  userId: number;
  email: string;
}

export const authenticateToken = (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ message: 'Access token required' });
  }
  
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload;
    req.user = payload;
    next();
  } catch (error) {
    return res.status(403).json({ message: 'Invalid token' });
  }
};
```
""",
            "dependencies": [
                "express@^4.18.2",
                "helmet@^7.1.0",
                "cors@^2.8.5",
                "morgan@^1.10.0",
                "express-rate-limit@^7.1.5",
                "jsonwebtoken@^9.0.2",
                "bcrypt@^5.1.1",
                "prisma@^5.7.1",
                "@prisma/client@^5.7.1",
                "zod@^3.22.4",
                "dotenv@^16.3.1"
            ],
            "dev_dependencies": [
                "typescript@^5.3.3",
                "@types/express@^4.17.21",
                "@types/node@^20.10.6",
                "@types/cors@^2.8.17",
                "@types/morgan@^1.9.9",
                "nodemon@^3.0.2",
                "ts-node@^10.9.2"
            ]
        },
        
        "Django": {
            "core_instructions": """
🔷 DJANGO + DRF REQUIREMENTS:

**settings.py:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'apps.users',
    'apps.entities',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # ... other middleware
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}
```

**Models:**
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
```

**Serializers:**
```python
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
```

**ViewSets:**
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserCreateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
```
""",
            "dependencies": [
                "Django==5.0",
                "djangorestframework==3.14.0",
                "django-cors-headers==4.3.1",
                "django-filter==23.5",
                "psycopg2-binary==2.9.9",
                "python-decouple==3.8",
                "celery==5.3.4"
            ],
            "dev_dependencies": ["pytest-django==4.7.0", "black==23.12.1"]
        },
        
        ".NET": {
            "core_instructions": """
🔷 ASP.NET CORE + C# REQUIREMENTS:

**Project Structure:**
```
backend/ or src/server/
├── Program.cs (Application entry point)
├── appsettings.json (Configuration)
├── appsettings.Development.json
├── ProjectName.csproj (Dependencies)
├── Controllers/
│   ├── CarsController.cs
│   ├── AuthController.cs
│   └── UsersController.cs
├── Models/
│   ├── Car.cs
│   ├── User.cs
│   └── ApplicationDbContext.cs
├── DTOs/
│   ├── CarDto.cs
│   ├── UserDto.cs
│   └── LoginDto.cs
├── Services/
│   ├── ICarService.cs
│   ├── CarService.cs
│   ├── IAuthService.cs
│   └── AuthService.cs
├── Repositories/
│   ├── ICarRepository.cs
│   └── CarRepository.cs
├── Middleware/
│   ├── AuthMiddleware.cs
│   └── ErrorHandlingMiddleware.cs
└── Extensions/
    └── ServiceExtensions.cs
```

**Program.cs (Minimal API - .NET 8):**
```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Database
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

// CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll",
        builder => builder
            .AllowAnyOrigin()
            .AllowAnyMethod()
            .AllowAnyHeader());
});

// JWT Authentication
var jwtSettings = builder.Configuration.GetSection("JwtSettings");
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = jwtSettings["Issuer"],
            ValidAudience = jwtSettings["Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(jwtSettings["SecretKey"]))
        };
    });

// Dependency Injection
builder.Services.AddScoped<ICarService, CarService>();
builder.Services.AddScoped<ICarRepository, CarRepository>();
builder.Services.AddScoped<IAuthService, AuthService>();

var app = builder.Build();

// Configure middleware pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("AllowAll");
app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

**Model (Entity Framework Core):**
```csharp
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ProjectName.Models
{
    [Table("cars")]
    public class Car
    {
        [Key]
        [Column("id")]
        public int Id { get; set; }
        
        [Required]
        [StringLength(100)]
        [Column("model")]
        public string Model { get; set; } = string.Empty;
        
        [Required]
        [StringLength(50)]
        [Column("color")]
        public string Color { get; set; } = string.Empty;
        
        [Required]
        [StringLength(50)]
        [Column("version")]
        public string Version { get; set; } = string.Empty;
        
        [Column("user_id")]
        public int UserId { get; set; }
        
        [ForeignKey("UserId")]
        public User User { get; set; } = null!;
        
        [Column("created_at")]
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        
        [Column("updated_at")]
        public DateTime? UpdatedAt { get; set; }
    }
}
```

**DTO (Data Transfer Object):**
```csharp
namespace ProjectName.DTOs
{
    public class CarDto
    {
        public int Id { get; set; }
        public string Model { get; set; } = string.Empty;
        public string Color { get; set; } = string.Empty;
        public string Version { get; set; } = string.Empty;
        public int UserId { get; set; }
        public DateTime CreatedAt { get; set; }
    }
    
    public class CreateCarDto
    {
        [Required]
        [StringLength(100)]
        public string Model { get; set; } = string.Empty;
        
        [Required]
        [StringLength(50)]
        public string Color { get; set; } = string.Empty;
        
        [Required]
        [StringLength(50)]
        public string Version { get; set; } = string.Empty;
    }
    
    public class UpdateCarDto
    {
        [StringLength(100)]
        public string? Model { get; set; }
        
        [StringLength(50)]
        public string? Color { get; set; }
        
        [StringLength(50)]
        public string? Version { get; set; }
    }
}
```

**Controller:**
```csharp
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using ProjectName.DTOs;
using ProjectName.Services;

namespace ProjectName.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class CarsController : ControllerBase
    {
        private readonly ICarService _carService;
        private readonly ILogger<CarsController> _logger;
        
        public CarsController(ICarService carService, ILogger<CarsController> logger)
        {
            _carService = carService;
            _logger = logger;
        }
        
        [HttpGet]
        public async Task<ActionResult<IEnumerable<CarDto>>> GetCars([FromQuery] int page = 1, [FromQuery] int pageSize = 10)
        {
            try
            {
                var cars = await _carService.GetCarsAsync(page, pageSize);
                return Ok(cars);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving cars");
                return StatusCode(500, new { message = "Internal server error" });
            }
        }
        
        [HttpGet("{id}")]
        public async Task<ActionResult<CarDto>> GetCar(int id)
        {
            var car = await _carService.GetCarByIdAsync(id);
            if (car == null)
                return NotFound(new { message = $"Car with ID {id} not found" });
                
            return Ok(car);
        }
        
        [HttpPost]
        public async Task<ActionResult<CarDto>> CreateCar([FromBody] CreateCarDto dto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);
                
            var car = await _carService.CreateCarAsync(dto);
            return CreatedAtAction(nameof(GetCar), new { id = car.Id }, car);
        }
        
        [HttpPut("{id}")]
        public async Task<ActionResult<CarDto>> UpdateCar(int id, [FromBody] UpdateCarDto dto)
        {
            var car = await _carService.UpdateCarAsync(id, dto);
            if (car == null)
                return NotFound(new { message = $"Car with ID {id} not found" });
                
            return Ok(car);
        }
        
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteCar(int id)
        {
            var success = await _carService.DeleteCarAsync(id);
            if (!success)
                return NotFound(new { message = $"Car with ID {id} not found" });
                
            return NoContent();
        }
        
        [HttpGet("search")]
        public async Task<ActionResult<IEnumerable<CarDto>>> SearchCars([FromQuery] string query)
        {
            var cars = await _carService.SearchCarsAsync(query);
            return Ok(cars);
        }
    }
}
```

**Service Layer:**
```csharp
using ProjectName.DTOs;
using ProjectName.Models;
using ProjectName.Repositories;

namespace ProjectName.Services
{
    public interface ICarService
    {
        Task<IEnumerable<CarDto>> GetCarsAsync(int page, int pageSize);
        Task<CarDto?> GetCarByIdAsync(int id);
        Task<CarDto> CreateCarAsync(CreateCarDto dto);
        Task<CarDto?> UpdateCarAsync(int id, UpdateCarDto dto);
        Task<bool> DeleteCarAsync(int id);
        Task<IEnumerable<CarDto>> SearchCarsAsync(string query);
    }
    
    public class CarService : ICarService
    {
        private readonly ICarRepository _repository;
        
        public CarService(ICarRepository repository)
        {
            _repository = repository;
        }
        
        public async Task<IEnumerable<CarDto>> GetCarsAsync(int page, int pageSize)
        {
            var cars = await _repository.GetAllAsync(page, pageSize);
            return cars.Select(MapToDto);
        }
        
        public async Task<CarDto?> GetCarByIdAsync(int id)
        {
            var car = await _repository.GetByIdAsync(id);
            return car == null ? null : MapToDto(car);
        }
        
        public async Task<CarDto> CreateCarAsync(CreateCarDto dto)
        {
            var car = new Car
            {
                Model = dto.Model,
                Color = dto.Color,
                Version = dto.Version,
                CreatedAt = DateTime.UtcNow
            };
            
            var created = await _repository.CreateAsync(car);
            return MapToDto(created);
        }
        
        public async Task<CarDto?> UpdateCarAsync(int id, UpdateCarDto dto)
        {
            var car = await _repository.GetByIdAsync(id);
            if (car == null) return null;
            
            if (!string.IsNullOrEmpty(dto.Model)) car.Model = dto.Model;
            if (!string.IsNullOrEmpty(dto.Color)) car.Color = dto.Color;
            if (!string.IsNullOrEmpty(dto.Version)) car.Version = dto.Version;
            car.UpdatedAt = DateTime.UtcNow;
            
            var updated = await _repository.UpdateAsync(car);
            return MapToDto(updated);
        }
        
        public async Task<bool> DeleteCarAsync(int id)
        {
            return await _repository.DeleteAsync(id);
        }
        
        public async Task<IEnumerable<CarDto>> SearchCarsAsync(string query)
        {
            var cars = await _repository.SearchAsync(query);
            return cars.Select(MapToDto);
        }
        
        private static CarDto MapToDto(Car car) => new CarDto
        {
            Id = car.Id,
            Model = car.Model,
            Color = car.Color,
            Version = car.Version,
            UserId = car.UserId,
            CreatedAt = car.CreatedAt
        };
    }
}
```

**Repository (Entity Framework Core):**
```csharp
using Microsoft.EntityFrameworkCore;
using ProjectName.Models;

namespace ProjectName.Repositories
{
    public interface ICarRepository
    {
        Task<IEnumerable<Car>> GetAllAsync(int page, int pageSize);
        Task<Car?> GetByIdAsync(int id);
        Task<Car> CreateAsync(Car car);
        Task<Car> UpdateAsync(Car car);
        Task<bool> DeleteAsync(int id);
        Task<IEnumerable<Car>> SearchAsync(string query);
    }
    
    public class CarRepository : ICarRepository
    {
        private readonly ApplicationDbContext _context;
        
        public CarRepository(ApplicationDbContext context)
        {
            _context = context;
        }
        
        public async Task<IEnumerable<Car>> GetAllAsync(int page, int pageSize)
        {
            return await _context.Cars
                .OrderByDescending(c => c.CreatedAt)
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();
        }
        
        public async Task<Car?> GetByIdAsync(int id)
        {
            return await _context.Cars.FindAsync(id);
        }
        
        public async Task<Car> CreateAsync(Car car)
        {
            _context.Cars.Add(car);
            await _context.SaveChangesAsync();
            return car;
        }
        
        public async Task<Car> UpdateAsync(Car car)
        {
            _context.Cars.Update(car);
            await _context.SaveChangesAsync();
            return car;
        }
        
        public async Task<bool> DeleteAsync(int id)
        {
            var car = await _context.Cars.FindAsync(id);
            if (car == null) return false;
            
            _context.Cars.Remove(car);
            await _context.SaveChangesAsync();
            return true;
        }
        
        public async Task<IEnumerable<Car>> SearchAsync(string query)
        {
            return await _context.Cars
                .Where(c => c.Model.Contains(query) || c.Color.Contains(query) || c.Version.Contains(query))
                .ToListAsync();
        }
    }
}
```

**appsettings.json:**
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=carmanagement;Username=postgres;Password=password"
  },
  "JwtSettings": {
    "SecretKey": "your-super-secret-key-min-32-characters-long",
    "Issuer": "YourApp",
    "Audience": "YourAppUsers",
    "ExpiryMinutes": 60
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

**ProjectName.csproj:**
```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.0" />
    <PackageReference Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="8.0.0" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
    <PackageReference Include="BCrypt.Net-Next" Version="4.0.3" />
  </ItemGroup>
</Project>
```
""",
            "dependencies": [
                "Microsoft.AspNetCore.Authentication.JwtBearer@8.0.0",
                "Microsoft.EntityFrameworkCore@8.0.0",
                "Microsoft.EntityFrameworkCore.Design@8.0.0",
                "Npgsql.EntityFrameworkCore.PostgreSQL@8.0.0",
                "MySql.EntityFrameworkCore@8.0.0",
                "Swashbuckle.AspNetCore@6.5.0",
                "BCrypt.Net-Next@4.0.3",
                "AutoMapper.Extensions.Microsoft.DependencyInjection@12.0.1",
                "Serilog.AspNetCore@8.0.0"
            ],
            "dev_dependencies": [
                "xunit@2.6.0",
                "Moq@4.20.0",
                "Microsoft.NET.Test.Sdk@17.8.0"
            ]
        }
    }
    
    # ==================== DATABASE TEMPLATES ====================
    
    DATABASE_TEMPLATES = {
        "PostgreSQL": {
            "connection_example": """
# FastAPI with SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session_maker() as session:
        yield session
""",
            "migration_example": """
# Alembic migration
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now())
    )
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade():
    op.drop_table('users')
"""
        },
        
        "MySQL": {
            "connection_example": """
# MySQL Connection
DATABASE_URL = "mysql+aiomysql://user:password@localhost/dbname"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)
""",
            "migration_example": "Similar to PostgreSQL but with MySQL-specific syntax"
        },
        
        "MongoDB": {
            "connection_example": """
# MongoDB with Motor (async)
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.your_database

# Usage in FastAPI
async def get_database():
    return db
""",
            "schema_example": """
# Pydantic models for MongoDB
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    username: str
    
    class Config:
        json_encoders = {ObjectId: str}
"""
        }
    }
    
    # ==================== METHODS ====================
    
    @classmethod
    def get_frontend_template(cls, frontend: str) -> Dict:
        """Get frontend-specific template"""
        return cls.FRONTEND_TEMPLATES.get(frontend, cls.FRONTEND_TEMPLATES["React"])
    
    @classmethod
    def get_backend_template(cls, backend: str) -> Dict:
        """Get backend-specific template"""
        return cls.BACKEND_TEMPLATES.get(backend, cls.BACKEND_TEMPLATES["FastAPI"])
    
    @classmethod
    def get_database_template(cls, database: str) -> Dict:
        """Get database-specific template"""
        return cls.DATABASE_TEMPLATES.get(database, cls.DATABASE_TEMPLATES["PostgreSQL"])
    
    @classmethod
    def build_complete_prompt(
        cls,
        tech_stack: TechStack,
        description: str,
        project_name: str
    ) -> str:
        """
        Build a complete prompt by combining tech-specific templates
        
        Args:
            tech_stack: User's selected technology stack
            description: User's project description
            project_name: Name of the project
            
        Returns:
            Complete assembled prompt with all tech-specific instructions
        """
        frontend_template = cls.get_frontend_template(tech_stack.frontend.value)
        backend_template = cls.get_backend_template(tech_stack.backend.value)
        database_template = cls.get_database_template(tech_stack.database.value)
        
        # Assemble the complete prompt
        complete_prompt = f"""
═══════════════════════════════════════════════════════════════════════════════
TECH STACK-SPECIFIC CODE GENERATION
═══════════════════════════════════════════════════════════════════════════════

Project: {project_name}
Frontend: {tech_stack.frontend.value}
Backend: {tech_stack.backend.value}
Database: {tech_stack.database.value}

User Requirements:
{description}

═══════════════════════════════════════════════════════════════════════════════
FRONTEND FRAMEWORK: {tech_stack.frontend.value.upper()}
═══════════════════════════════════════════════════════════════════════════════

{frontend_template.get('core_instructions', '')}

{frontend_template.get('styling_requirements', '')}

**Required Dependencies:**
{chr(10).join('• ' + dep for dep in frontend_template.get('dependencies', []))}

**Dev Dependencies:**
{chr(10).join('• ' + dep for dep in frontend_template.get('dev_dependencies', []))}

═══════════════════════════════════════════════════════════════════════════════
BACKEND FRAMEWORK: {tech_stack.backend.value.upper()}
═══════════════════════════════════════════════════════════════════════════════

{backend_template.get('core_instructions', '')}

**Required Dependencies:**
{chr(10).join('• ' + dep for dep in backend_template.get('dependencies', []))}

**Dev Dependencies:**
{chr(10).join('• ' + dep for dep in backend_template.get('dev_dependencies', []))}

═══════════════════════════════════════════════════════════════════════════════
DATABASE: {tech_stack.database.value.upper()}
═══════════════════════════════════════════════════════════════════════════════

{database_template.get('connection_example', '')}

{database_template.get('migration_example', '')}

{database_template.get('schema_example', '')}

═══════════════════════════════════════════════════════════════════════════════
INTEGRATION REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════════

1. **API Communication:**
   - Frontend calls Backend via axios/fetch
   - Base URL configuration: process.env.VITE_API_URL or similar
   - Request/response interceptors for auth tokens
   - Error handling and retry logic

2. **Authentication Flow:**
   - Login endpoint returns JWT token
   - Token stored in localStorage/sessionStorage
   - Token included in Authorization header for protected routes
   - Token refresh mechanism before expiration
   - Logout clears token and redirects to login

3. **Data Flow:**
   - Frontend → API request → Backend router → Service layer → Repository → Database
   - Database → Repository → Service → Backend response → Frontend state update

4. **Error Handling:**
   - Backend: Custom exception classes with proper HTTP status codes
   - Frontend: Toast notifications for errors, form validation messages
   - Consistent error response format: {{ "error": "message", "details": [] }}

5. **Environment Configuration:**
   - Frontend .env: VITE_API_URL, VITE_APP_NAME
   - Backend .env: DATABASE_URL, SECRET_KEY, CORS_ORIGINS
   - Different configs for dev/staging/prod

═══════════════════════════════════════════════════════════════════════════════
FINAL CHECKLIST - VERIFY BEFORE RETURNING
═══════════════════════════════════════════════════════════════════════════════

Frontend ({tech_stack.frontend.value}):
☐ package.json with ALL required dependencies
☐ TypeScript configuration (tsconfig.json)
☐ Tailwind config with COMPLETE custom theme
☐ globals.css with CSS variables and animations
☐ 15-20 fully styled UI components (Button, Input, Modal, Card, etc.)
☐ Layout components (Header, Sidebar, Footer)
☐ Page components with routing
☐ Custom hooks (useAuth, useApi, useForm, etc.)
☐ Context providers for global state
☐ API service with axios/fetch client
☐ Form validation with real-time feedback
☐ Responsive design (mobile/tablet/desktop)
☐ Loading states and error boundaries

Backend ({tech_stack.backend.value}):
☐ requirements.txt or package.json with ALL dependencies
☐ Main server file with middleware setup
☐ Database models with relationships
☐ Pydantic/Joi schemas for validation
☐ Router/controller files for each entity
☐ Service layer with business logic
☐ Repository layer for data access
☐ JWT authentication middleware
☐ Error handling middleware
☐ Database migration files
☐ Seed data for testing
☐ Unit and integration tests
☐ API documentation (OpenAPI/Swagger)

Database ({tech_stack.database.value}):
☐ Complete schema with tables and relationships
☐ Indexes on foreign keys and query fields
☐ Unique constraints on business keys
☐ Timestamps (created_at, updated_at)
☐ Migration files (up and down)
☐ Seed data (5-10 records per table)

DevOps:
☐ Dockerfile for frontend (multi-stage build)
☐ Dockerfile for backend (multi-stage build)
☐ docker-compose.yml (all services)
☐ .env.example with all variables documented
☐ README.md with setup instructions
☐ API.md with endpoint documentation

═══════════════════════════════════════════════════════════════════════════════
BEGIN GENERATION - FOLLOW ALL TECH-SPECIFIC REQUIREMENTS ABOVE
═══════════════════════════════════════════════════════════════════════════════
"""
        
        return complete_prompt


# Export
__all__ = ['TechSpecificTemplates']
