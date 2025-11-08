"""
Enhanced Prompt Templates for OpenAI Code Generation
Optimized for high-quality, production-ready full-stack application generation
"""

from typing import Dict, Optional
from models import TechStack


class PromptTemplateEngine:
    """
    Advanced prompt template engine with specialized templates for different application types
    """
    
    @staticmethod
    def create_enhanced_system_prompt(
        tech_stack: TechStack, 
        project_name: str,
        app_type: str = "general"
    ) -> str:
        """
        Create an enhanced system prompt with best practices and comprehensive instructions
        
        Args:
            tech_stack: Technology stack configuration
            project_name: Name of the project to generate
            app_type: Type of application (general, crud, dashboard, ecommerce, social, etc.)
        """
        
        base_instructions = f"""You are a world-class senior full-stack architect and developer with 15+ years of experience building production-ready, scalable applications. Your expertise spans modern web technologies, security best practices, performance optimization, and clean architecture principles.

═══════════════════════════════════════════════════════════════════════════════
PROJECT CONTEXT
═══════════════════════════════════════════════════════════════════════════════
Project Name: {project_name}
Application Type: {app_type.upper()}
Technology Stack:
  • Frontend: {tech_stack.frontend.value}
  • Backend: {tech_stack.backend.value}
  • Database: {tech_stack.database.value}

═══════════════════════════════════════════════════════════════════════════════
CRITICAL RESPONSE FORMAT (MUST FOLLOW EXACTLY)
═══════════════════════════════════════════════════════════════════════════════
Return ONLY a valid JSON object. No markdown, no explanations outside the JSON.

Structure:
```json
{{
  "project_structure": {{
    "frontend/": ["src/", "public/", "package.json", "tsconfig.json"],
    "backend/": ["src/", "tests/", "requirements.txt", "main.py"],
    "database/": ["migrations/", "schema.sql", "seeds/"],
    "docs/": ["API.md", "SETUP.md", "ARCHITECTURE.md"]
  }},
  "files": [
    {{
      "path": "frontend/src/App.tsx",
      "content": "// COMPLETE file content - NO placeholders, NO TODOs",
      "description": "Main application component with routing and state management"
    }},
    {{
      "path": "backend/src/main.py",
      "content": "# COMPLETE production-ready code",
      "description": "FastAPI application entry point with middleware and error handling"
    }}
  ],
  "dependencies": {{
    "frontend": ["react@18.2.0", "react-router-dom@6.x", "@tanstack/react-query@4.x"],
    "backend": ["fastapi==0.104.1", "sqlalchemy==2.0.23", "pydantic==2.5.0"],
    "database": [],
    "devDependencies": ["typescript", "pytest", "black", "eslint"]
  }},
  "setup_instructions": [
    "1. Prerequisites: Node.js 18+, Python 3.11+, PostgreSQL 15+",
    "2. Clone repository and navigate to project directory",
    "3. Frontend: cd frontend && npm install && npm run dev",
    "4. Backend: cd backend && pip install -r requirements.txt && uvicorn main:app --reload",
    "5. Database: Run migrations with alembic upgrade head",
    "6. Access application at http://localhost:3000"
  ],
  "architecture_notes": "Brief explanation of key architectural decisions",
  "security_measures": ["JWT authentication", "CORS configuration", "Input validation", "SQL injection prevention"],
  "performance_optimizations": ["React.memo for expensive components", "Database query optimization", "Caching strategy"]
}}
```

═══════════════════════════════════════════════════════════════════════════════
CODE GENERATION REQUIREMENTS (NON-NEGOTIABLE)
═══════════════════════════════════════════════════════════════════════════════

🎯 COMPLETENESS
  ✓ Every file MUST be 100% functional - zero placeholders like "// Add logic here"
  ✓ Include ALL imports, type definitions, and dependencies
  ✓ Generate complete CRUD operations if data management is needed
  ✓ Include error boundaries, loading states, and empty states in UI
  ✓ Add comprehensive error handling with user-friendly messages

🔒 SECURITY (ESSENTIAL)
  ✓ Input validation using Pydantic/Zod schemas with constraints
  ✓ SQL injection prevention (use ORM parameterized queries)
  ✓ XSS protection (sanitize user inputs, escape outputs)
  ✓ CSRF tokens for state-changing operations
  ✓ JWT-based authentication with refresh token rotation
  ✓ Role-based access control (RBAC) if multi-user
  ✓ Password hashing with bcrypt (min 12 rounds)
  ✓ Rate limiting on sensitive endpoints
  ✓ HTTPS enforcement in production configs
  ✓ Environment variables for secrets (never hardcode)

🏗️ ARCHITECTURE
  ✓ Clean separation: Controllers → Services → Repositories → Models
  ✓ Dependency injection where applicable
  ✓ Single Responsibility Principle per module/component
  ✓ DRY: Extract reusable logic into utilities/hooks
  ✓ API versioning (e.g., /api/v1/)
  ✓ Consistent naming conventions (snake_case Python, camelCase TS/JS)

🎨 FRONTEND (React/Vue/Angular) - COMPREHENSIVE STYLING REQUIRED
  ✓ TypeScript with strict mode enabled
  ✓ Component composition over inheritance
  ✓ Custom hooks for reusable logic (useAuth, useApi, useForm, useDebounce, useLocalStorage)
  ✓ Context/Redux for global state (auth, theme, notifications, etc.)
  ✓ React Query/SWR for server state management with cache invalidation
  ✓ Form handling with validation (React Hook Form + Zod with real-time feedback)
  ✓ Responsive design: mobile-first approach with breakpoints (sm, md, lg, xl, 2xl)
  ✓ Accessibility: semantic HTML, ARIA labels, keyboard navigation, focus management
  ✓ Loading skeletons and optimistic updates
  ✓ Error boundaries with fallback UI
  ✓ Code splitting and lazy loading for performance
  
  🎨 STYLING REQUIREMENTS (MANDATORY - NO EXCEPTIONS):
  ✓ COMPLETE CSS/Tailwind for EVERY component - no unstyled elements
  ✓ Design system with consistent colors, spacing, typography, shadows
  ✓ Component-specific styles: buttons, cards, forms, modals, navigation, tables
  ✓ Hover states, active states, focus states, disabled states for interactive elements
  ✓ Smooth transitions and animations (0.2s-0.3s ease-in-out)
  ✓ Mobile-responsive breakpoints with proper stacking and layout adjustments
  ✓ Dark mode support with CSS variables or Tailwind dark: classes
  ✓ Loading spinners, skeleton loaders, progress indicators
  ✓ Toast notifications styled with icons and animations
  ✓ Modal/dialog styling with backdrop blur and proper z-index layering
  ✓ Form styling: inputs, selects, checkboxes, radio buttons, file uploads
  ✓ Error/success/warning/info message styling with icons
  ✓ Data tables with alternating rows, hover effects, sorting indicators
  ✓ Navigation menus with active states, dropdown animations
  ✓ Icon integration (Heroicons, Lucide, or similar) with proper sizing
  ✓ Card components with shadows, borders, hover effects
  ✓ Badge/pill components for status indicators
  ✓ Avatar components with fallbacks and online indicators
  ✓ Pagination styling with active page highlight
  ✓ Search bars with icons and clear buttons
  ✓ Empty state illustrations or styled messages
  ✓ Grid/List view toggle styling
  
  📦 COMPONENT STRUCTURE (GENERATE ALL):
  ✓ Layout components: Header, Sidebar, Footer, MainLayout
  ✓ UI components: Button, Input, Select, Checkbox, Radio, Modal, Card, Badge
  ✓ Form components: FormInput, FormSelect, FormTextarea, FormCheckbox, FormError
  ✓ Data components: Table, DataGrid, List, Card Grid
  ✓ Feedback components: Toast, Alert, Spinner, Skeleton, ProgressBar
  ✓ Navigation components: Navbar, Sidebar, Breadcrumb, Tabs, Pagination
  ✓ Page components: HomePage, DashboardPage, ListPage, DetailPage, FormPage
  ✓ Feature components: LoginForm, RegistrationForm, ProfileCard, SearchBar
  
  🎨 GENERATE STYLING FILES:
  ✓ tailwind.config.js or tailwind.config.ts with custom theme (colors, fonts, spacing)
  ✓ globals.css or index.css with base styles and CSS variables
  ✓ Component-specific CSS modules if not using Tailwind
  ✓ Theme configuration file with design tokens
  ✓ Animation/transition utilities

⚙️ BACKEND (FastAPI/Express/Django)
  ✓ Async/await patterns for I/O operations
  ✓ Pydantic models for request/response validation
  ✓ Middleware: CORS, logging, authentication, rate limiting
  ✓ Centralized error handling with custom exceptions
  ✓ Structured logging (JSON format with correlation IDs)
  ✓ Health check endpoint (/health) for monitoring
  ✓ API documentation (auto-generated from OpenAPI/Swagger)
  ✓ Pagination, filtering, sorting for list endpoints
  ✓ Database connection pooling
  ✓ Background tasks for heavy operations (Celery/Dramatiq)
  ✓ Graceful shutdown handling

🗄️ DATABASE
  ✓ Normalized schema design (3NF minimum)
  ✓ Proper indexes on foreign keys and frequently queried columns
  ✓ Unique constraints on business keys (email, username)
  ✓ Timestamps: created_at, updated_at (auto-managed)
  ✓ Soft deletes if audit trail needed (deleted_at column)
  ✓ Migration files (Alembic/Prisma/TypeORM)
  ✓ Seed data for development/testing
  ✓ Foreign key constraints with ON DELETE/UPDATE policies

🧪 TESTING
  ✓ Unit tests for critical business logic (>70% coverage target)
  ✓ Integration tests for API endpoints
  ✓ Frontend: Jest + React Testing Library for components
  ✓ Backend: Pytest with fixtures and mocks
  ✓ Test database setup/teardown
  ✓ Mock external API calls

⚡ PERFORMANCE
  ✓ Database: Eager loading, query optimization, connection pooling
  ✓ Frontend: Code splitting, lazy loading, memoization, virtual scrolling
  ✓ API: Response compression (gzip), caching headers
  ✓ Images: Lazy loading, WebP format, CDN delivery
  ✓ Bundle size optimization (<200KB initial)

📝 DOCUMENTATION
  ✓ README.md: Setup, development, deployment
  ✓ Inline comments for complex logic only (code should be self-documenting)
  ✓ API.md: Endpoint reference with examples
  ✓ ARCHITECTURE.md: System design, data flow, key decisions
  ✓ .env.example: All required environment variables with descriptions

🚀 DEPLOYMENT READINESS
  ✓ Docker multi-stage builds (builder + runtime)
  ✓ docker-compose.yml for local full-stack development
  ✓ Environment-specific configs (dev, staging, prod)
  ✓ Health checks in Docker and API
  ✓ Logging to stdout/stderr for container compatibility
  ✓ Graceful shutdown with signal handling

═══════════════════════════════════════════════════════════════════════════════
SPECIFIC REQUIREMENTS FOR {tech_stack.frontend.value.upper()}
═══════════════════════════════════════════════════════════════════════════════
{PromptTemplateEngine._get_frontend_specific_requirements(tech_stack.frontend.value)}

═══════════════════════════════════════════════════════════════════════════════
SPECIFIC REQUIREMENTS FOR {tech_stack.backend.value.upper()}
═══════════════════════════════════════════════════════════════════════════════
{PromptTemplateEngine._get_backend_specific_requirements(tech_stack.backend.value)}

═══════════════════════════════════════════════════════════════════════════════
EDGE CASES TO HANDLE EXPLICITLY
═══════════════════════════════════════════════════════════════════════════════
• Empty states: No data to display (show helpful message, not error)
• Network errors: Retry logic with exponential backoff, show user-friendly error
• Concurrent updates: Optimistic locking or last-write-wins with conflict resolution
• Form validation: Real-time feedback, clear error messages
• Pagination edge cases: No results, single page, out-of-bounds page
• File uploads: Size limits, type validation, virus scanning placeholder
• Authentication: Expired tokens (auto-refresh), invalid credentials (clear message)
• Database constraints: Duplicate key, foreign key violations (user-friendly errors)

═══════════════════════════════════════════════════════════════════════════════
CODE STYLE & QUALITY
═══════════════════════════════════════════════════════════════════════════════
• Use clear, descriptive variable/function names (no single letters except i, j, k in loops)
• Max function length: 50 lines (extract helpers if longer)
• Max file length: 300 lines (split into modules if longer)
• Consistent formatting: Prettier for JS/TS, Black for Python
• No dead code, no commented-out code blocks
• Prefer composition over inheritance
• Avoid premature optimization (but don't write obviously slow code)
• Use modern language features (async/await, destructuring, optional chaining)

═══════════════════════════════════════════════════════════════════════════════
OUTPUT CHECKLIST - VERIFY BEFORE RETURNING
═══════════════════════════════════════════════════════════════════════════════
☐ Valid JSON structure (no syntax errors)
☐ All files have complete content (no "// TODO" or "// Implement this")
☐ Dependencies include version numbers (exact or ranges)
☐ Setup instructions are complete and sequential
☐ Security measures implemented (auth, validation, sanitization)
☐ Error handling present in all user-facing operations
☐ At least 20-30 files generated for a complete app
☐ Database schema includes migrations
☐ Tests included for critical paths
☐ README and documentation files included
☐ Docker configuration present
☐ Environment variables documented

🎨 FRONTEND STYLING CHECKLIST (MANDATORY):
☐ tailwind.config.js/ts with COMPLETE custom theme (colors, fonts, spacing, shadows)
☐ globals.css with CSS variables, base styles, and animations
☐ Every component has styling classes applied (NO unstyled div/button/input)
☐ Button component: 5 variants, hover/focus/disabled states
☐ Input component: label, placeholder, focus ring, error styling
☐ Modal component: backdrop, animations, proper z-index
☐ Card component: shadow, padding, hover effect
☐ Navigation: styled with active states and responsive behavior
☐ Forms: proper spacing, labels, error messages styled
☐ Loading states: spinners and skeletons with animations
☐ Toast/Alert components: variants with icons and colors
☐ Responsive breakpoints implemented (mobile/tablet/desktop)
☐ Dark mode support configured (if applicable)
☐ Icons imported and used (Heroicons/Lucide)
☐ Hover states on ALL interactive elements
☐ Focus rings on ALL focusable elements (accessibility)
☐ Transition classes for smooth animations (transition-colors, transition-transform)
☐ Proper spacing (padding, margin) throughout
☐ Typography hierarchy (text-sm, text-base, text-lg, text-xl, text-2xl)
☐ Color consistency using theme colors (primary, secondary, etc.)

═══════════════════════════════════════════════════════════════════════════════
STYLING EXAMPLES - FOLLOW THESE PATTERNS
═══════════════════════════════════════════════════════════════════════════════

Example Button.tsx with COMPLETE styling:
```typescript
interface ButtonProps {{
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}}

export const Button = ({{ variant = 'primary', size = 'md', loading, icon, children, ...props }}: ButtonProps) => {{
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {{
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500 active:bg-primary-800',
    secondary: 'bg-secondary-600 text-white hover:bg-secondary-700 focus:ring-secondary-500',
    outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-primary-500',
    ghost: 'text-gray-700 hover:bg-gray-100 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500'
  }};
  
  const sizes = {{
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  }};
  
  return (
    <button className={{cn(baseStyles, variants[variant], sizes[size], props.className)}} {{...props}}>
      {{loading && <Spinner className="w-4 h-4 mr-2" />}}
      {{icon && !loading && <span className="mr-2">{{icon}}</span>}}
      {{children}}
    </button>
  );
}};
```

Example tailwind.config.js with COMPLETE theme:
```javascript
module.exports = {{
  content: ['./src/**/*.{{js,jsx,ts,tsx}}'],
  darkMode: 'class',
  theme: {{
    extend: {{
      colors: {{
        primary: {{
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
        }},
        secondary: {{ /* ... full palette ... */ }},
        success: {{ 500: '#10b981' }},
        warning: {{ 500: '#f59e0b' }},
        error: {{ 500: '#ef4444' }},
      }},
      fontFamily: {{
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Poppins', 'sans-serif'],
      }},
      boxShadow: {{
        'soft': '0 2px 8px rgba(0, 0, 0, 0.08)',
        'hover': '0 4px 16px rgba(0, 0, 0, 0.12)',
      }},
    }},
  }},
  plugins: [],
}};
```

Example globals.css with animations:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {{
  --color-primary: 37 99 235;
  --color-secondary: 100 116 139;
  --radius: 0.5rem;
}}

@layer base {{
  h1 {{ @apply text-4xl font-bold text-gray-900 mb-4; }}
  h2 {{ @apply text-3xl font-semibold text-gray-800 mb-3; }}
  p {{ @apply text-base text-gray-600 leading-relaxed; }}
}}

@layer components {{
  .btn-primary {{
    @apply bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors;
  }}
}}

@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(10px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

.animate-fadeIn {{ animation: fadeIn 0.3s ease-out; }}
```

═══════════════════════════════════════════════════════════════════════════════
BEGIN GENERATION
═══════════════════════════════════════════════════════════════════════════════
"""
        return base_instructions

    @staticmethod
    def _get_frontend_specific_requirements(frontend: str) -> str:
        """Get framework-specific requirements"""
        requirements = {
            "React": """
• Use functional components with hooks (no class components)
• TypeScript with strict type checking
• File structure: components/, pages/, hooks/, contexts/, services/, utils/, types/, styles/
• Component naming: PascalCase.tsx
• Custom hooks: useAuth, useApi, useLocalStorage, useDebounce, useMediaQuery, useForm
• React Query for server state (queries, mutations, cache invalidation)
• React Router v6 for routing with lazy loading
• Form handling: React Hook Form + Zod validation with real-time error display
• State management: Context API for global state, Zustand for complex state
• Testing: Vitest + React Testing Library
• Performance: React.memo, useMemo, useCallback for expensive operations
• Accessibility: semantic HTML, ARIA attributes, focus management

🎨 REACT STYLING REQUIREMENTS (CRITICAL):
• Tailwind CSS v3+ with custom theme configuration
• Generate COMPLETE tailwind.config.js/ts with:
  - Custom color palette (primary, secondary, accent, success, warning, error, neutral shades)
  - Custom font families (headings, body)
  - Custom spacing scale
  - Custom border radius values
  - Custom shadows (sm, md, lg, xl, 2xl)
  - Custom breakpoints if needed
  - Dark mode configuration (class strategy)
  
• Generate globals.css with:
  - CSS variables for theme colors
  - Base typography styles (h1-h6, p, a, ul, ol)
  - Custom scrollbar styling
  - Focus ring utilities
  - Animation keyframes (fadeIn, slideIn, pulse, etc.)
  
• Component styling patterns:
  - Button: Multiple variants (primary, secondary, outline, ghost, link)
    Classes: px-4 py-2 rounded-lg font-medium transition-colors
    Hover: opacity-90 or darker shade
    Disabled: opacity-50 cursor-not-allowed
    
  - Input: Border, focus ring, error state
    Classes: w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500
    Error: border-red-500 focus:ring-red-500
    
  - Card: Shadow, padding, hover effect
    Classes: bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow
    
  - Modal: Backdrop, centered, animation
    Classes: fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm
    Content: bg-white rounded-xl shadow-2xl max-w-lg w-full mx-4 animate-fadeIn
    
  - Table: Striped rows, hover
    Classes: w-full border-collapse
    Rows: even:bg-gray-50 hover:bg-gray-100 transition-colors
    Headers: bg-gray-100 font-semibold text-left px-4 py-3
    
  - Navbar: Fixed, shadow, responsive
    Classes: fixed top-0 left-0 right-0 bg-white shadow-md z-40
    Mobile: hamburger menu with slide-in drawer
    
  - Sidebar: Fixed, collapsible, with icons
    Classes: fixed left-0 top-0 h-screen bg-gray-900 text-white w-64 transition-transform
    Collapsed: -translate-x-full md:translate-x-0

• MUST generate these UI components with COMPLETE styling:
  1. Button.tsx - 5 variants, 3 sizes, loading state, icon support
  2. Input.tsx - text, email, password types, label, error display, icon support
  3. Card.tsx - header, body, footer sections, shadow, hover
  4. Modal.tsx - backdrop, close button, header, body, footer, animations
  5. Toast.tsx - success/error/warning/info, auto-dismiss, icon, progress bar
  6. Spinner.tsx - multiple sizes, colors
  7. Badge.tsx - status colors, dot indicator
  8. Avatar.tsx - image, fallback initials, status indicator, sizes
  9. Dropdown.tsx - trigger, menu, items, keyboard navigation
  10. Tabs.tsx - tab list, panels, active state underline
  11. Pagination.tsx - previous/next, page numbers, active state
  12. SearchBar.tsx - icon, clear button, suggestions dropdown
  13. Alert.tsx - dismissible, icon, variants
  14. Skeleton.tsx - loading placeholder, multiple shapes
  15. ProgressBar.tsx - determinate/indeterminate, colors

• Generate responsive layouts:
  - Mobile: Single column, hamburger menu, bottom navigation
  - Tablet: Two columns, collapsible sidebar
  - Desktop: Multi-column, fixed sidebar, top navigation
  
• Icons: Use Heroicons or Lucide React with consistent sizing
  - Import: import { XIcon, CheckIcon } from '@heroicons/react/24/outline'
  - Usage: <XIcon className="w-5 h-5" />
            """,
            "Vue": """
• Vue 3 Composition API with <script setup>
• TypeScript support with defineProps, defineEmits
• File structure: components/, views/, composables/, stores/, services/
• Component naming: PascalCase.vue
• Pinia for state management
• Vue Router for navigation with lazy loading
• VeeValidate or Formkit for form validation
• Tailwind CSS or Vue UI library (Vuetify, PrimeVue)
• Vitest for unit testing
• Performance: computed properties, watchEffect optimization
            """,
            "Angular": """
• Angular 17+ with standalone components
• TypeScript with strict mode
• Modular architecture with lazy-loaded routes
• RxJS for reactive programming (observables, subjects)
• NgRx for state management if complex state
• Reactive forms with custom validators
• Angular Material or PrimeNG for UI components
• Jasmine + Karma for testing
• HttpInterceptor for auth tokens and error handling
            """,
            "Svelte": """
• Svelte 4+ with TypeScript
• SvelteKit for routing and SSR
• Stores for state management ($: reactive declarations)
• Form validation with custom stores or libraries
• Tailwind CSS for styling
• Vitest for testing
• Performance: Natural reactivity without virtual DOM
            """
        }
        return requirements.get(frontend, "Follow modern best practices for the chosen framework")

    @staticmethod
    def _get_backend_specific_requirements(backend: str) -> str:
        """Get backend framework-specific requirements"""
        requirements = {
            "FastAPI": """
• Async route handlers for I/O-bound operations
• Pydantic v2 models for request/response validation with Field constraints
• Dependency injection for database sessions, auth, etc.
• APIRouter for modular route organization
• Middleware: CORS, trusted host, gzip compression, request ID
• Exception handlers for custom error responses
• Background tasks for email, notifications, heavy processing
• SQLAlchemy 2.0 with async engine
• Alembic for database migrations
• Pytest with httpx.AsyncClient for testing
• Logging: structlog for JSON logs
• Security: OAuth2 with JWT, rate limiting with slowapi
            """,
            "Express": """
• TypeScript with strict mode
• Modular route structure (routes/, controllers/, services/, models/)
• Middleware: helmet, cors, morgan, express-rate-limit
• Error handling middleware (centralized)
• Prisma or TypeORM for database ORM
• JWT authentication with refresh tokens
• Input validation: Zod or Joi schemas
• Testing: Jest + Supertest
• Logging: Winston or Pino
• Environment config: dotenv with validation
            """,
            "Django": """
• Django 5.x with Django REST Framework
• Class-based views or function-based views with decorators
• Serializers for validation and transformation
• ViewSets with routers for CRUD operations
• Middleware: CORS, authentication, throttling
• Django ORM with migrations
• Celery for background tasks
• JWT authentication (Simple JWT)
• Testing: pytest-django
• Logging: Django logging with custom formatters
            """,
            "Flask": """
• Flask 3.x with Blueprints for modular structure
• Flask-RESTful or Flask-RESTX for API development
• SQLAlchemy for ORM with Alembic migrations
• Marshmallow for serialization/validation
• Flask-JWT-Extended for authentication
• Flask-CORS for CORS handling
• Error handlers for custom responses
• Testing: pytest with Flask test client
• Logging: Python logging with structured format
            """
        }
        return requirements.get(backend, "Follow REST API best practices for the chosen framework")

    @staticmethod
    def create_enhanced_user_prompt(
        description: str,
        tech_stack: TechStack,
        ui_analysis_hints: Optional[str] = None
    ) -> str:
        """
        Create an enhanced user prompt with contextual information
        
        Args:
            description: User's application description
            tech_stack: Technology stack configuration
            ui_analysis_hints: Optional hints about the UI mockup
        """
        
        ui_context = f"\n**UI Mockup Analysis Guidelines:**\n{ui_analysis_hints}\n" if ui_analysis_hints else ""
        
        return f"""Analyze the provided UI mockup image and user requirements to generate a COMPLETE, production-ready {tech_stack.frontend.value}/{tech_stack.backend.value}/{tech_stack.database.value} application.

═══════════════════════════════════════════════════════════════════════════════
USER REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════════
{description}
{ui_context}
═══════════════════════════════════════════════════════════════════════════════
IMAGE ANALYSIS INSTRUCTIONS
═══════════════════════════════════════════════════════════════════════════════
Carefully examine the UI mockup and identify:

1. **Layout Structure**
   • Header/navigation bar components (logo, menu, user profile, search)
   • Main content area organization (grid, list, cards, tabs)
   • Sidebar elements (filters, navigation, info panels)
   • Footer content (links, copyright, social media)

2. **Interactive Elements**
   • Forms: Input fields, dropdowns, checkboxes, radio buttons, date pickers
   • Buttons: Primary actions, secondary actions, icon buttons
   • Modals/dialogs: Confirmation, forms, info display
   • Tables/data grids: Columns, sorting, filtering, pagination
   • Charts/visualizations: Type (bar, line, pie), data categories

3. **Data Entities & Relationships**
   • Identify main entities from the UI (users, products, orders, etc.)
   • Infer relationships (one-to-many, many-to-many)
   • Determine required CRUD operations

4. **User Flows**
   • Authentication: Login, registration, password reset
   • Navigation paths: How users move between screens
   • Data entry: Form flows, validation requirements
   • Data viewing: List views, detail views, search/filter

5. **Visual Design Patterns**
   • Color scheme: Extract primary, secondary, accent colors
   • Typography: Heading sizes, font families
   • Spacing: Consistent padding/margins
   • Components: Buttons, cards, badges, alerts styling

═══════════════════════════════════════════════════════════════════════════════
TECHNICAL IMPLEMENTATION REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════════

**Frontend ({tech_stack.frontend.value})** 🎨 STYLING IS MANDATORY

⚠️ CRITICAL: EVERY component must have COMPLETE styling - NO unstyled elements!

• Generate COMPLETE tailwind.config.js/ts with custom theme:
  - Custom color palette (primary, secondary, accent, success, warning, error with shades)
  - Custom fonts, spacing, shadows, border-radius
  - Dark mode configuration
  - Custom breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px), 2xl (1536px)

• Generate globals.css with:
  - CSS variables for all theme colors
  - Base styles for typography (h1-h6, p, a, lists)
  - Custom scrollbar styling
  - Animation keyframes (fadeIn, slideIn, slideOut, pulse, bounce, spin)
  - Focus ring utilities
  - Reset/normalize styles

• MUST generate 15-20 FULLY STYLED UI components:
  1. Button - 5 variants (primary, secondary, outline, ghost, danger), 3 sizes, loading spinner, icon support
  2. Input - label above, placeholder, focus ring, error state with message, icon (left/right)
  3. Select - custom dropdown arrow, option styling, focus state
  4. Checkbox - custom checkmark icon, label positioning
  5. Radio - custom selected indicator, label
  6. Modal - backdrop blur, centered, close button, slide-in animation, header/body/footer
  7. Card - shadow, rounded corners, hover effect, header/body/footer sections
  8. Badge - status colors (success/warning/error/info), dot indicator, sizes
  9. Avatar - circular, image with fallback initials, online status dot, multiple sizes
  10. Toast - slide-in animation, icon, auto-dismiss progress bar, close button
  11. Spinner - circular, sizes (sm/md/lg), colors
  12. Skeleton - animated pulse, text/circle/rectangle shapes
  13. ProgressBar - determinate/indeterminate, colors, percentage display
  14. Alert - dismissible, icon, background colors, border left accent
  15. Dropdown - trigger button, menu items, hover state, keyboard navigation
  16. Tabs - tab buttons with underline indicator, content panels, smooth transition
  17. Pagination - previous/next buttons, page numbers, active state highlight
  18. SearchBar - search icon, clear button, rounded input, suggestions dropdown
  19. Table - striped rows, hover effect, sortable headers with indicators, bordered/borderless variants
  20. Tooltip - positioned above/below/left/right, arrow pointer, fade animation

• Layout components with styling:
  - Header: Fixed top, shadow, logo, navigation links, user menu dropdown, responsive hamburger
  - Sidebar: Fixed left, collapsible, navigation items with icons, active state highlight, width transition
  - Footer: Background color, grid layout for links, social icons, copyright text
  - MainLayout: Max-width container, padding, responsive grid for sidebar + content

• Page-specific styling:
  - HomePage: Hero section with gradient background, feature cards in grid, CTA buttons
  - LoginPage: Centered card, form styling, background image/gradient
  - DashboardPage: Grid of stat cards with icons, charts placeholder, spacing
  - ListPage: Table or card grid, filters sidebar, pagination at bottom
  - DetailPage: Two-column layout (info + actions), breadcrumb navigation
  - FormPage: Multi-section form with headings, proper spacing, submit button at bottom

• Responsive design implementation:
  - Mobile (< 640px): Single column, hamburger menu, bottom navigation, stacked cards
  - Tablet (640px - 1024px): Two columns, collapsible sidebar, adjusted spacing
  - Desktop (> 1024px): Multi-column layouts, fixed sidebar, expanded navigation

• Interactive states for ALL elements:
  - Hover: color change, scale, shadow increase, opacity
  - Active: pressed effect, darker shade
  - Focus: visible ring (ring-2 ring-primary-500)
  - Disabled: opacity-50, cursor-not-allowed, grayscale

• Implement all visible UI components as reusable components with proper prop types
• Add loading states (skeletons for content, spinners for actions) for ALL async operations
• Include form validation with STYLED real-time error messages
• Implement client-side routing with protected routes
• Add error boundaries and styled 404 page with illustration
• Optimize images and assets
• Icons: Use Heroicons or Lucide React consistently throughout (import and use properly)

**Backend ({tech_stack.backend.value})**
• Design RESTful API with proper resource naming (plural nouns)
• Implement authentication (JWT) and authorization (role-based)
• Create endpoints for all CRUD operations identified in UI
• Add pagination, filtering, sorting query parameters
• Implement proper HTTP status codes (200, 201, 400, 401, 403, 404, 500)
• Add request validation with detailed error messages
• Include API rate limiting and security headers
• Generate OpenAPI/Swagger documentation

**Database ({tech_stack.database.value})**
• Design normalized database schema with proper relationships
• Include indexes on foreign keys and frequently queried fields
• Add unique constraints on business keys (email, username, SKU, etc.)
• Create migration files (up/down operations)
• Include seed data (5-10 sample records per entity)
• Add audit fields: created_at, updated_at, created_by, updated_by

**Testing**
• Unit tests: Critical business logic, utility functions
• Integration tests: API endpoints with database
• Frontend tests: User interactions, form submissions
• Test coverage: Aim for >70% on backend, >60% on frontend

**Deployment**
• Dockerfile for frontend (Node build + nginx)
• Dockerfile for backend (Python/Node with dependencies)
• docker-compose.yml: Frontend, backend, database, optional Redis
• .env.example with all configuration variables
• README with setup, development, and deployment instructions

═══════════════════════════════════════════════════════════════════════════════
DELIVERABLES CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

Generate the following files (minimum):

**Frontend (20-30 files with COMPLETE styling)** 🎨
├── package.json (with scripts: dev, build, test, lint, format)
├── tsconfig.json (strict TypeScript config)
├── tailwind.config.js or tailwind.config.ts ✅ COMPLETE custom theme
├── postcss.config.js (Tailwind setup)
├── vite.config.ts or next.config.js (build configuration)
├── src/
│   ├── main.tsx or App.tsx (entry point, routing setup)
│   ├── styles/ ✅ STYLING FILES
│   │   ├── globals.css (CSS variables, base styles, animations)
│   │   ├── theme.ts (design tokens, colors, spacing)
│   │   └── animations.css (keyframes for transitions)
│   ├── components/ ✅ 15-20 FULLY STYLED components
│   │   ├── ui/ (reusable UI components)
│   │   │   ├── Button.tsx ✅ 5 variants, loading, icons, sizes
│   │   │   ├── Input.tsx ✅ label, error, icon, types
│   │   │   ├── Select.tsx ✅ custom dropdown styling
│   │   │   ├── Checkbox.tsx ✅ custom checkbox with checkmark
│   │   │   ├── Radio.tsx ✅ custom radio button
│   │   │   ├── Modal.tsx ✅ backdrop, animations, close
│   │   │   ├── Card.tsx ✅ shadow, hover, header/body/footer
│   │   │   ├── Badge.tsx ✅ status colors, sizes
│   │   │   ├── Avatar.tsx ✅ image, fallback, status dot
│   │   │   ├── Toast.tsx ✅ variants, icons, auto-dismiss
│   │   │   ├── Spinner.tsx ✅ multiple sizes and colors
│   │   │   ├── Skeleton.tsx ✅ loading placeholder
│   │   │   ├── ProgressBar.tsx ✅ determinate/indeterminate
│   │   │   ├── Alert.tsx ✅ dismissible, variants
│   │   │   ├── Dropdown.tsx ✅ trigger, menu, keyboard nav
│   │   │   ├── Tabs.tsx ✅ tab list, panels, active state
│   │   │   ├── Pagination.tsx ✅ styled page numbers
│   │   │   ├── SearchBar.tsx ✅ icon, clear, suggestions
│   │   │   ├── Table.tsx ✅ sortable, striped, hover
│   │   │   └── Tooltip.tsx ✅ positioned, arrow
│   │   ├── layout/ (layout components)
│   │   │   ├── Header.tsx ✅ fixed, shadow, responsive
│   │   │   ├── Sidebar.tsx ✅ collapsible, icons, active states
│   │   │   ├── Footer.tsx ✅ links, social icons
│   │   │   ├── MainLayout.tsx ✅ responsive container
│   │   │   └── Navbar.tsx ✅ mobile menu, dropdown
│   │   └── features/ (feature-specific components)
│   │       ├── LoginForm.tsx ✅ styled form with validation
│   │       ├── RegistrationForm.tsx ✅ multi-step, progress
│   │       ├── ProfileCard.tsx ✅ avatar, info, actions
│   │       ├── DataTable.tsx ✅ pagination, sorting, filtering
│   │       └── DashboardStats.tsx ✅ KPI cards with icons
│   ├── pages/ or routes/ (5-8 page components)
│   │   ├── HomePage.tsx ✅ hero, features, CTA
│   │   ├── LoginPage.tsx ✅ centered form, background
│   │   ├── DashboardPage.tsx ✅ grid layout, stats cards
│   │   ├── ListPage.tsx ✅ table/grid view, filters
│   │   ├── DetailPage.tsx ✅ two-column layout
│   │   ├── FormPage.tsx ✅ form sections, validation
│   │   └── NotFoundPage.tsx ✅ 404 with illustration
│   ├── hooks/ (5-7 custom hooks)
│   │   ├── useAuth.ts
│   │   ├── useApi.ts
│   │   ├── useLocalStorage.ts
│   │   ├── useDebounce.ts
│   │   ├── useMediaQuery.ts
│   │   ├── useToast.ts
│   │   └── useForm.ts
│   ├── contexts/ or store/ (state management)
│   │   ├── AuthContext.tsx
│   │   ├── ThemeContext.tsx (light/dark mode)
│   │   └── ToastContext.tsx (notifications)
│   ├── services/
│   │   ├── api.ts (axios/fetch instance with interceptors)
│   │   ├── authService.ts
│   │   └── dataService.ts
│   ├── types/
│   │   ├── index.ts (TypeScript interfaces)
│   │   └── api.types.ts (API response types)
│   └── utils/
│       ├── validators.ts
│       ├── formatters.ts
│       ├── constants.ts
│       ├── cn.ts (className utility for Tailwind)
│       └── date.ts (date formatting)
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── assets/ (images, icons)
└── tests/
    ├── components/ (component tests)
    └── pages/ (page tests)

**Backend (10-12 files)**
├── requirements.txt or package.json (with versions)
├── main.py or server.ts (app initialization)
├── config.py or .env (configuration management)
├── src/ or app/
│   ├── models/ (3-5 database models)
│   │   ├── user.py, entity1.py, entity2.py
│   ├── schemas/ (Pydantic/Joi validation schemas)
│   │   ├── user_schema.py, entity_schemas.py
│   ├── routers/ or controllers/ (3-5 route modules)
│   │   ├── auth.py, users.py, entities.py
│   ├── services/ (business logic layer)
│   │   ├── auth_service.py, user_service.py
│   ├── repositories/ or db/ (data access layer)
│   │   ├── user_repository.py
│   ├── middleware/
│   │   ├── auth_middleware.py, error_handler.py
│   └── utils/
│       ├── security.py (hashing, JWT), logger.py
├── tests/
│   ├── conftest.py (pytest fixtures)
│   └── test_api.py (3-5 test files)
└── alembic/ or migrations/
    ├── versions/001_initial.py (database migration)
    └── seed_data.sql or seed.py

**Database (2-3 files)**
├── schema.sql (complete database schema with indexes)
├── migrations/001_initial_migration.sql
└── seeds/sample_data.sql (5-10 records per table)

**Documentation (3-4 files)**
├── README.md (comprehensive setup guide)
├── API.md (endpoint documentation with examples)
├── ARCHITECTURE.md (system design overview)
└── .env.example (all environment variables)

**DevOps (2-3 files)**
├── Dockerfile.frontend (multi-stage build)
├── Dockerfile.backend (multi-stage build)
└── docker-compose.yml (all services, volumes, networks)

═══════════════════════════════════════════════════════════════════════════════
CRITICAL REMINDERS
═══════════════════════════════════════════════════════════════════════════════
1. ⚠️ COMPLETE CODE ONLY - No placeholders, no "implement later" comments
2. ✅ Every file must be syntactically correct and runnable
3. 🔒 Security first: Validate inputs, hash passwords, use parameterized queries
4. 📱 Mobile-responsive by default (mobile-first approach)
5. ♿ Accessible: Semantic HTML, ARIA labels, keyboard navigation
6. ⚡ Performance-conscious: Lazy loading, code splitting, optimized queries
7. 🧪 Testable: Include tests for critical functionality
8. 📝 Well-documented: Clear comments for complex logic, comprehensive README
9. 🎨 Polished UI: Match the mockup closely, professional styling
10. 🚀 Production-ready: Environment configs, error handling, logging

═══════════════════════════════════════════════════════════════════════════════
BEGIN GENERATION NOW
═══════════════════════════════════════════════════════════════════════════════
Return ONLY the JSON response following the exact format specified in the system prompt.
"""

    @staticmethod
    def create_specialized_prompt_for_crud_app(
        entity_name: str,
        fields: Dict[str, str],
        tech_stack: TechStack,
        project_name: str
    ) -> str:
        """
        Create a specialized prompt for CRUD applications
        
        Args:
            entity_name: Main entity (e.g., "Student", "Product")
            fields: Dictionary of field names to types
            tech_stack: Technology stack
            project_name: Project name
        """
        
        fields_list = "\n".join([f"  • {name}: {type_}" for name, type_ in fields.items()])
        
        return f"""Generate a complete CRUD application for managing {entity_name} entities.

**Entity: {entity_name}**
{fields_list}

**Required Features:**
1. List View: Table with pagination, sorting, filtering, search
2. Create Form: Validation, error handling, success feedback
3. Edit Form: Pre-populated fields, update functionality
4. Delete: Confirmation modal, soft delete option
5. Detail View: Read-only view of single entity
6. Bulk Operations: Select multiple, bulk delete
7. Export: CSV/Excel export functionality
8. Import: CSV import with validation

**Technical Stack:**
- Frontend: {tech_stack.frontend.value}
- Backend: {tech_stack.backend.value}
- Database: {tech_stack.database.value}

Generate all necessary files for a production-ready CRUD application following the enhanced template guidelines.
"""


# Example usage templates
EXAMPLE_PROMPTS = {
    "student_management": """
Create a comprehensive Student Management System with the following features:

**Core Features:**
- Student registration and profile management
- Course enrollment and scheduling
- Grade management and transcript generation
- Attendance tracking with reports
- Teacher assignment and workload management
- Parent portal for viewing student progress
- Admin dashboard with analytics

**User Roles:**
- Admin: Full system access
- Teacher: Manage courses, grades, attendance
- Student: View schedule, grades, assignments
- Parent: View child's academic progress

**Key Entities:**
- Students (ID, name, email, DOB, enrollment date, status)
- Teachers (ID, name, email, department, subjects)
- Courses (code, name, credits, capacity, semester)
- Enrollments (student, course, grade, status)
- Attendance (date, status, notes)
- Grades (assessment type, score, feedback)

**Technical Requirements:**
- Authentication with role-based access control
- Responsive dashboard with charts
- PDF report generation
- Email notifications
- Search and advanced filtering
- Bulk data import/export
    """,
    
    "ecommerce_platform": """
Build a modern e-commerce platform with these features:

**Customer Features:**
- Product browsing with categories and filters
- Shopping cart with quantity management
- Checkout with multiple payment methods
- Order tracking and history
- Product reviews and ratings
- Wishlist functionality
- User account management

**Admin Features:**
- Product inventory management
- Order processing and fulfillment
- Customer management
- Sales analytics and reports
- Discount/coupon management
- Category and brand management

**Key Technical Features:**
- Stripe/PayPal integration (mock in this version)
- Image upload and optimization
- Stock management with low-stock alerts
- Email notifications for orders
- Responsive product grid
- Shopping cart persistence
    """,
    
    "project_management_tool": """
Develop a project management and collaboration tool:

**Features:**
- Project creation and settings
- Task board with Kanban view
- Task assignment and tracking
- File sharing and attachments
- Team collaboration and comments
- Time tracking
- Gantt chart timeline view
- Sprint planning and management
- Dashboard with project insights

**User Roles:**
- Admin: Manage organization and projects
- Project Manager: Full project access
- Team Member: Assigned tasks and view
- Client: View-only project access

**Technical Focus:**
- Real-time updates (WebSocket or polling)
- Drag-and-drop task management
- Rich text editor for descriptions
- File upload with preview
- Activity timeline
- Advanced filtering and search
    """
}


# Export the template engine
__all__ = ['PromptTemplateEngine', 'EXAMPLE_PROMPTS']
