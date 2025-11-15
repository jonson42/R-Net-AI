"""
Chained Code Generation Service
Breaks down large code generation into smaller, manageable prompts
Each step builds upon the previous step's output
"""

import logging
import json
from typing import Dict, List, Any, Optional
from openai import OpenAI

from config import settings
from models import TechStack, GeneratedFile
from services.tech_specific_templates import TechSpecificTemplates

logger = logging.getLogger(__name__)


class ChainedGenerationService:
    """
    Multi-step code generation using chained prompts
    Each step focuses on a specific aspect of the application
    """
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base
        )
        self.tech_templates = TechSpecificTemplates()
    
    def _get_architecture_instructions(self, tech_stack: TechStack) -> str:
        """Get folder structure instructions based on architecture type"""
        from models import ArchitectureType
        
        if tech_stack.architecture == ArchitectureType.MONOLITHIC:
            return """
📁 **MONOLITHIC ARCHITECTURE - Single Unified Folder Structure:**

Use a SINGLE ROOT project structure where backend and frontend coexist:

```
project-root/
├── src/                          # All source code in one place
│   ├── server/                   # Backend code
│   │   ├── main.py or app.ts    # Server entry point
│   │   ├── config.py/config.ts  # Configuration
│   │   ├── models/              # Database models
│   │   ├── routes/ or controllers/
│   │   ├── services/            # Business logic
│   │   ├── middleware/          # Auth, error handling
│   │   └── utils/               # Helpers
│   │
│   ├── client/                   # Frontend code
│   │   ├── components/          # React/Vue/Angular components
│   │   ├── pages/               # Page components
│   │   ├── hooks/               # Custom hooks
│   │   ├── services/            # API client
│   │   ├── styles/              # CSS/SCSS
│   │   └── utils/               # Frontend utilities
│   │
│   └── shared/                   # Shared code between client and server
│       ├── types/               # TypeScript interfaces
│       ├── constants/           # Shared constants
│       └── validators/          # Validation schemas
│
├── public/                       # Static assets
├── prisma/ or migrations/        # Database migrations
├── tests/                        # All tests
├── package.json                  # Single package.json for monorepo
├── tsconfig.json                 # Single TypeScript config
├── .env                          # Single environment file
├── docker-compose.yml
└── README.md

**File Path Examples:**
- Backend API: src/server/routes/users.ts
- Frontend Page: src/client/pages/Dashboard.tsx
- Shared Type: src/shared/types/User.ts
- Database Model: src/server/models/user.model.ts

**NO separate backend/ and frontend/ root folders!**
**Everything under src/ with server/ and client/ subdirectories.**
"""
        else:  # MICROSERVICES
            return """
📁 **MICROSERVICES ARCHITECTURE - Separate Backend & Frontend:**

Use SEPARATE root-level folders for backend and frontend:

```
project-root/
├── backend/                      # Backend microservice
│   ├── main.py or server.ts
│   ├── config.py
│   ├── requirements.txt or package.json
│   ├── models/
│   ├── routes/ or controllers/
│   ├── services/
│   ├── middleware/
│   ├── utils/
│   ├── tests/
│   └── Dockerfile
│
├── frontend/                     # Frontend microservice
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts or next.config.js
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── styles/
│   │   └── utils/
│   ├── public/
│   ├── tests/
│   └── Dockerfile
│
├── docker-compose.yml            # Orchestrates both services
└── README.md

**File Path Examples:**
- Backend API: backend/routes/users.py
- Frontend Page: frontend/src/pages/Dashboard.tsx
- Backend Model: backend/models/user.py
- Frontend Component: frontend/src/components/Button.tsx

**Separate backend/ and frontend/ root folders with independent configs.**
"""
    
    async def generate_code_chained(
        self,
        image_data: str,
        description: str,
        tech_stack: TechStack,
        project_name: str = "generated-app"
    ) -> Dict[str, Any]:
        """
        Generate code using chained prompts strategy
        
        Flow:
        1. Analyze UI and create architecture
        2. Generate database schema
        3. Generate backend API endpoints
        4. Generate frontend components
        5. Generate configuration & deployment files
        6. Combine all results
        """
        
        logger.info(f"Starting chained generation for: {project_name}")
        
        # Step 1: Architecture & Planning
        architecture = await self._step1_analyze_architecture(
            image_data, description, tech_stack, project_name
        )
        logger.info("✓ Step 1/5: Architecture planned")
        
        # Step 2: Database Schema
        database_files = await self._step2_generate_database(
            architecture, tech_stack, description
        )
        logger.info(f"✓ Step 2/5: Database schema generated ({len(database_files)} files)")
        for f in database_files:
            logger.info(f"  - {f.path}")
        
        # Step 3: Backend API
        backend_files = await self._step3_generate_backend(
            architecture, database_files, tech_stack, description
        )
        logger.info(f"✓ Step 3/5: Backend API generated ({len(backend_files)} files)")
        for f in backend_files:
            logger.info(f"  - {f.path}")
        
        # Step 4: Frontend Components
        frontend_files = await self._step4_generate_frontend(
            architecture, backend_files, tech_stack, description, image_data
        )
        logger.info(f"✓ Step 4/5: Frontend components generated ({len(frontend_files)} files)")
        for f in frontend_files:
            logger.info(f"  - {f.path}")
        
        # Step 5: Configuration & Deployment
        config_files = await self._step5_generate_configs(
            architecture, tech_stack, project_name
        )
        logger.info(f"✓ Step 5/5: Configuration files generated ({len(config_files)} files)")
        for f in config_files:
            logger.info(f"  - {f.path}")
        
        # Combine all results
        result = self._combine_results(
            architecture, database_files, backend_files, 
            frontend_files, config_files, tech_stack
        )
        
        logger.info(f"Chained generation completed: {len(result['files'])} files generated")
        return result
    
    async def _step1_analyze_architecture(
        self,
        image_data: str,
        description: str,
        tech_stack: TechStack,
        project_name: str
    ) -> Dict[str, Any]:
        """
        Step 1: Analyze UI mockup and create architecture plan
        """
        
        system_prompt = """You are an expert software architect. Analyze the UI mockup and description to create a comprehensive architecture plan.

Return a JSON object with:
{
  "pages": ["list of pages/routes"],
  "components": ["list of main components"],
  "features": ["list of key features"],
  "api_endpoints": ["list of required API endpoints"],
  "database_tables": ["list of required database tables"],
  "authentication": "yes/no",
  "real_time": "yes/no",
  "file_upload": "yes/no",
  "project_structure": {
    "frontend": ["folder structure"],
    "backend": ["folder structure"]
  }
}"""

        user_prompt = f"""Analyze this UI mockup and create an architecture plan.

**Project**: {project_name}
**Tech Stack**: {tech_stack.frontend}, {tech_stack.backend}, {tech_stack.database}
**Description**: {description}

Create a detailed architecture plan focusing on:
1. All pages/routes needed
2. Main components and their relationships
3. Required API endpoints
4. Database structure
5. Special features (auth, real-time, file uploads)"""

        # Log the prompts
        logger.info("=" * 80)
        logger.info("STEP 1: ARCHITECTURE ANALYSIS")
        logger.info("=" * 80)
        logger.info(f"SYSTEM PROMPT:\n{system_prompt}")
        logger.info("-" * 80)
        logger.info(f"USER PROMPT:\n{user_prompt}")
        logger.info("=" * 80)

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_data}"}
                        }
                    ]
                }
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        # Extract JSON from response
        try:
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            architecture = json.loads(content[json_start:json_end])
        except Exception as e:
            logger.warning(f"Failed to parse architecture JSON: {e}")
            architecture = {
                "pages": ["Home", "Dashboard"],
                "components": ["Header", "Footer", "MainContent"],
                "features": ["CRUD operations"],
                "api_endpoints": ["/api/items"],
                "database_tables": ["items"],
                "authentication": "yes",
                "real_time": "no",
                "file_upload": "no"
            }
        
        return architecture
    
    async def _step2_generate_database(
        self,
        architecture: Dict[str, Any],
        tech_stack: TechStack,
        description: str
    ) -> List[GeneratedFile]:
        """
        Step 2: Generate database schema based on architecture
        """
        
        tables = architecture.get("database_tables", [])
        has_auth = architecture.get("authentication", "no") == "yes"
        
        # Get tech-specific database template
        db_template = self.tech_templates.get_database_template(tech_stack.database.value)
        db_instructions = db_template.get("core_instructions", "")
        
        system_prompt = f"""You are a database expert. Create complete database schema files for {tech_stack.database}.

{db_instructions}

Return ONLY valid JSON:
{{
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "complete file content",
      "description": "file description"
    }}
  ]
}}"""

        user_prompt = f"""Create database schema for these tables: {', '.join(tables)}

**Database**: {tech_stack.database}
**Authentication needed**: {has_auth}
**Requirements**: {description}

Generate complete schema with:
- All necessary tables and relationships
- Proper indexes and constraints
- Foreign keys
- Timestamps
- {'User authentication tables (users, sessions, tokens)' if has_auth else ''}"""

        # Log the prompts
        logger.info("=" * 80)
        logger.info("STEP 2: DATABASE SCHEMA GENERATION")
        logger.info("=" * 80)
        logger.info(f"SYSTEM PROMPT:\n{system_prompt}")
        logger.info("-" * 80)
        logger.info(f"USER PROMPT:\n{user_prompt}")
        logger.info("=" * 80)

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )
        
        return self._parse_files_from_response(response.choices[0].message.content)
    
    async def _step3_generate_backend(
        self,
        architecture: Dict[str, Any],
        database_files: List[GeneratedFile],
        tech_stack: TechStack,
        description: str
    ) -> List[GeneratedFile]:
        """
        Step 3: Generate backend API based on architecture and database
        Split into multiple sub-steps to avoid token limits
        """
        
        endpoints = architecture.get("api_endpoints", [])
        has_auth = architecture.get("authentication", "no") == "yes"
        
        logger.info("=" * 80)
        logger.info("STEP 3: BACKEND API GENERATION (Multi-phase)")
        logger.info("=" * 80)
        
        # Get tech-specific backend template
        backend_template = self.tech_templates.get_backend_template(tech_stack.backend.value)
        backend_instructions = backend_template.get("core_instructions", "")
        
        # Summarize database schema for context
        db_summary = "\n".join([
            f"- {f.path}: {f.description}" 
            for f in database_files[:3]
        ])
        
        all_backend_files = []
        
        # Sub-step 3.1: Generate core setup files (main app, config, requirements)
        logger.info("Step 3.1: Generating core application files...")
        core_files = await self._generate_backend_core(
            tech_stack, backend_instructions, has_auth, description
        )
        all_backend_files.extend(core_files)
        logger.info(f"✓ Generated {len(core_files)} core files")
        
        # Sub-step 3.2: Generate models/schemas
        logger.info("Step 3.2: Generating data models and schemas...")
        model_files = await self._generate_backend_models(
            tech_stack, backend_instructions, database_files, db_summary
        )
        all_backend_files.extend(model_files)
        logger.info(f"✓ Generated {len(model_files)} model files")
        
        # Sub-step 3.3: Generate API routes
        logger.info("Step 3.3: Generating API route handlers...")
        route_files = await self._generate_backend_routes(
            tech_stack, backend_instructions, endpoints, has_auth, description
        )
        all_backend_files.extend(route_files)
        logger.info(f"✓ Generated {len(route_files)} route files")
        
        # Sub-step 3.4: Generate middleware and utilities
        logger.info("Step 3.4: Generating middleware and utilities...")
        util_files = await self._generate_backend_utils(
            tech_stack, backend_instructions, has_auth
        )
        all_backend_files.extend(util_files)
        logger.info(f"✓ Generated {len(util_files)} utility files")
        
        logger.info("=" * 80)
        logger.info(f"Backend generation produced {len(all_backend_files)} total files")
        return all_backend_files
    
    async def _generate_backend_core(
        self,
        tech_stack: TechStack,
        backend_instructions: str,
        has_auth: bool,
        description: str
    ) -> List[GeneratedFile]:
        """Generate core backend files: main app, config, dependencies"""
        
        arch_instructions = self._get_architecture_instructions(tech_stack)
        
        system_prompt = f"""You are a backend expert for {tech_stack.backend}.

{backend_instructions}

{arch_instructions}

**CRITICAL: Follow the folder structure shown above EXACTLY!**

Generate ONLY core application setup files:
1. Main application file (entry point)
2. Configuration file (settings, environment)
3. Dependencies file (requirements.txt, package.json, etc.)

Return ONLY valid JSON:
{{
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "complete file content",
      "description": "file description"
    }}
  ]
}}"""

        # Determine correct file extensions based on backend
        if tech_stack.backend.value == ".NET":
            main_file = "Program.cs"
            config_file = "appsettings.json"
            deps_file = "ProjectName.csproj"
            language = "C#"
        elif tech_stack.backend.value == "Express":
            main_file = "server.js or server.ts"
            config_file = "config.js"
            deps_file = "package.json"
            language = "TypeScript/JavaScript"
        elif tech_stack.backend.value in ["FastAPI", "Flask", "Django"]:
            main_file = "main.py or app.py"
            config_file = "config.py or settings.py"
            deps_file = "requirements.txt"
            language = "Python"
        else:
            main_file = "main file"
            config_file = "config file"
            deps_file = "dependencies file"
            language = tech_stack.backend.value
        
        user_prompt = f"""Create core application files for {tech_stack.backend} using {language}.

**CRITICAL**: ALL code must be in {language}. File extensions must match the language!
- Main file: {main_file}
- Config file: {config_file}
- Dependencies: {deps_file}

**Requirements**:
- {description}
- Authentication: {has_auth}

Generate:
- Main application file with CORS, middleware setup
- Configuration with environment variables
- Dependencies file with all required packages

**DO NOT mix languages! All files must be {language}!**"""

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )
        
        return self._parse_files_from_response(response.choices[0].message.content)
    
    async def _generate_backend_models(
        self,
        tech_stack: TechStack,
        backend_instructions: str,
        database_files: List[GeneratedFile],
        db_summary: str
    ) -> List[GeneratedFile]:
        """Generate data models and schemas"""
        
        arch_instructions = self._get_architecture_instructions(tech_stack)
        
        system_prompt = f"""You are a backend expert for {tech_stack.backend}.

{backend_instructions}

{arch_instructions}

**CRITICAL: Follow the folder structure shown above EXACTLY!**

Generate ONLY data models and schemas:
1. ORM models (database entities)
2. Request/Response schemas (validation)
3. Data transfer objects

Return ONLY valid JSON:
{{
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "complete file content",
      "description": "file description"
    }}
  ]
}}"""

        # Determine language-specific terminology
        if tech_stack.backend.value == ".NET":
            orm_name = "Entity Framework"
            schema_name = "DTOs (Data Transfer Objects)"
            file_ext = ".cs"
            language = "C#"
        elif tech_stack.backend.value == "Express":
            orm_name = "Sequelize or Prisma"
            schema_name = "TypeScript interfaces"
            file_ext = ".ts"
            language = "TypeScript"
        elif tech_stack.backend.value in ["FastAPI", "Flask", "Django"]:
            orm_name = "SQLAlchemy" if tech_stack.backend.value != "Django" else "Django ORM"
            schema_name = "Pydantic models"
            file_ext = ".py"
            language = "Python"
        else:
            orm_name = "ORM"
            schema_name = "schemas"
            file_ext = ""
            language = tech_stack.backend.value
        
        user_prompt = f"""Create data models and schemas using {language}.

**CRITICAL**: ALL code must be in {language} with {file_ext} file extensions!

**Database Schema**:
{db_summary}

Generate:
- {orm_name} models for each database table (files ending with {file_ext})
- {schema_name} for request validation (files ending with {file_ext})
- Response models for API output (files ending with {file_ext})

**DO NOT use Python if backend is {tech_stack.backend.value}!**
**DO NOT mix languages! All files must be {language}!**"""

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )
        
        return self._parse_files_from_response(response.choices[0].message.content)
    
    async def _generate_backend_routes(
        self,
        tech_stack: TechStack,
        backend_instructions: str,
        endpoints: List[str],
        has_auth: bool,
        description: str
    ) -> List[GeneratedFile]:
        """Generate API route handlers"""
        
        arch_instructions = self._get_architecture_instructions(tech_stack)
        
        system_prompt = f"""You are a backend expert for {tech_stack.backend}.

{backend_instructions}

{arch_instructions}

**CRITICAL: Follow the folder structure shown above EXACTLY!**

Generate ONLY API route handlers:
1. Router files with endpoints
2. Request handlers
3. Business logic/services

Return ONLY valid JSON:
{{
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "complete file content",
      "description": "file description"
    }}
  ]
}}"""

        # Determine language-specific terminology
        if tech_stack.backend.value == ".NET":
            router_name = "Controllers"
            file_pattern = "*Controller.cs"
            language = "C#"
            file_ext = ".cs"
        elif tech_stack.backend.value == "Express":
            router_name = "Routes and Controllers"
            file_pattern = "*.routes.ts and *.controller.ts"
            language = "TypeScript"
            file_ext = ".ts"
        elif tech_stack.backend.value == "FastAPI":
            router_name = "APIRouter endpoints"
            file_pattern = "*.py"
            language = "Python"
            file_ext = ".py"
        elif tech_stack.backend.value in ["Flask", "Django"]:
            router_name = "Blueprints" if tech_stack.backend.value == "Flask" else "Views"
            file_pattern = "*.py"
            language = "Python"
            file_ext = ".py"
        else:
            router_name = "Routes"
            file_pattern = "route files"
            language = tech_stack.backend.value
            file_ext = ""
        
        user_prompt = f"""Create API route handlers for these endpoints using {language}: {', '.join(endpoints[:10])}

**CRITICAL**: ALL code must be in {language} with {file_ext} file extensions!
**File pattern**: {file_pattern}

**Requirements**:
- {description}
- Authentication: {has_auth}

Generate:
- {router_name} for each resource (files ending with {file_ext})
- CRUD operations
- Error handling
- {'Protected routes with JWT' if has_auth else 'Public routes'}

**DO NOT use Python if backend is {tech_stack.backend.value}!**
**DO NOT mix languages! All files must be {language} ({file_ext})!**"""

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6
        )
        
        return self._parse_files_from_response(response.choices[0].message.content)
    
    async def _generate_backend_utils(
        self,
        tech_stack: TechStack,
        backend_instructions: str,
        has_auth: bool
    ) -> List[GeneratedFile]:
        """Generate middleware and utility files"""
        
        arch_instructions = self._get_architecture_instructions(tech_stack)
        
        system_prompt = f"""You are a backend expert for {tech_stack.backend}.

{backend_instructions}

{arch_instructions}

**CRITICAL: Follow the folder structure shown above EXACTLY!**

Generate ONLY middleware and utilities:
1. Authentication middleware
2. Error handlers
3. Database utilities
4. Helper functions

Return ONLY valid JSON:
{{
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "complete file content",
      "description": "file description"
    }}
  ]
}}"""

        # Determine language-specific terminology
        if tech_stack.backend.value == ".NET":
            middleware_name = "Middleware classes"
            file_ext = ".cs"
            language = "C#"
        elif tech_stack.backend.value == "Express":
            middleware_name = "Express middleware functions"
            file_ext = ".ts"
            language = "TypeScript"
        elif tech_stack.backend.value in ["FastAPI", "Flask", "Django"]:
            middleware_name = "Middleware functions"
            file_ext = ".py"
            language = "Python"
        else:
            middleware_name = "Middleware"
            file_ext = ""
            language = tech_stack.backend.value
        
        user_prompt = f"""Create middleware and utility files using {language}.

**CRITICAL**: ALL code must be in {language} with {file_ext} file extensions!

**Requirements**:
- Authentication: {has_auth}

Generate:
- {'JWT authentication middleware' if has_auth else 'Basic middleware'} (files ending with {file_ext})
- Global error handler ({file_ext})
- Database connection utilities ({file_ext})
- Logging setup ({file_ext})
- Security utilities - CORS, rate limiting ({file_ext})

**DO NOT use Python if backend is {tech_stack.backend.value}!**
**DO NOT mix languages! All files must be {language} ({file_ext})!**"""

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )
        
        return self._parse_files_from_response(response.choices[0].message.content)
    
    async def _step4_generate_frontend(
        self,
        architecture: Dict[str, Any],
        backend_files: List[GeneratedFile],
        tech_stack: TechStack,
        description: str,
        image_data: str
    ) -> List[GeneratedFile]:
        """
        Step 4: Generate frontend components based on UI mockup and backend API
        Split into multiple sub-steps to avoid token limits
        """
        
        pages = architecture.get("pages", [])
        components = architecture.get("components", [])
        
        logger.info("=" * 80)
        logger.info("STEP 4: FRONTEND COMPONENTS GENERATION (Multi-phase)")
        logger.info("=" * 80)
        
        # Get tech-specific frontend template
        frontend_template = self.tech_templates.get_frontend_template(tech_stack.frontend.value)
        frontend_instructions = frontend_template.get("core_instructions", "")
        
        # Summarize backend API for context
        api_summary = "\n".join([
            f"- {f.path}: {f.description}" 
            for f in backend_files[:5]
        ])
        
        all_frontend_files = []
        
        # Sub-step 4.1: Generate setup files (package.json, tsconfig, vite config)
        logger.info("Step 4.1: Generating project setup files...")
        setup_files = await self._generate_frontend_setup(
            tech_stack, frontend_instructions, description
        )
        all_frontend_files.extend(setup_files)
        logger.info(f"✓ Generated {len(setup_files)} setup files")
        
        # Sub-step 4.2: Generate core app structure (App.tsx, main.tsx, routing)
        logger.info("Step 4.2: Generating core application structure...")
        core_files = await self._generate_frontend_core(
            tech_stack, frontend_instructions, pages, image_data
        )
        all_frontend_files.extend(core_files)
        logger.info(f"✓ Generated {len(core_files)} core files")
        
        # Sub-step 4.3: Generate page components
        logger.info("Step 4.3: Generating page components...")
        page_files = await self._generate_frontend_pages(
            tech_stack, frontend_instructions, pages, api_summary, image_data, description
        )
        all_frontend_files.extend(page_files)
        logger.info(f"✓ Generated {len(page_files)} page files")
        
        # Sub-step 4.4: Generate UI components and utilities
        logger.info("Step 4.4: Generating UI components and utilities...")
        component_files = await self._generate_frontend_components(
            tech_stack, frontend_instructions, components
        )
        all_frontend_files.extend(component_files)
        logger.info(f"✓ Generated {len(component_files)} component files")
        
        logger.info("=" * 80)
        logger.info(f"Frontend generation produced {len(all_frontend_files)} total files")
        return all_frontend_files
    
    async def _generate_frontend_setup(
        self,
        tech_stack: TechStack,
        frontend_instructions: str,
        description: str
    ) -> List[GeneratedFile]:
        """Generate frontend setup files: package.json, tsconfig, build config"""
        
        arch_instructions = self._get_architecture_instructions(tech_stack)
        
        system_prompt = f"""You are a frontend expert for {tech_stack.frontend}.

{frontend_instructions}

{arch_instructions}

**CRITICAL: Follow the folder structure shown above EXACTLY!**

Generate ONLY project setup and configuration files:
1. package.json with dependencies
2. tsconfig.json (TypeScript config)
3. Build tool config (vite.config.ts or next.config.js)
4. Styling config (tailwind.config.js, postcss.config.js)

Return ONLY valid JSON:
{{
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "complete file content",
      "description": "file description"
    }}
  ]
}}"""

        # Determine root folder based on architecture
        from models import ArchitectureType
        root_folder = "" if tech_stack.architecture == ArchitectureType.MONOLITHIC else "frontend/"
        
        user_prompt = f"""Create project setup files for {tech_stack.frontend}.

**CRITICAL FILE PATHS**: All files must start with `{root_folder}` prefix!
Example: `{root_folder}package.json`, `{root_folder}tsconfig.json`

**Requirements**: {description}

Generate:
- {root_folder}package.json with React 18+, TypeScript, Tailwind CSS, React Router, Axios
- {root_folder}tsconfig.json with strict mode
- {root_folder}Vite or Next.js config
- {root_folder}Tailwind CSS config with custom theme
- {root_folder}PostCSS config"""

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )
        
        return self._parse_files_from_response(response.choices[0].message.content)
    
    async def _generate_frontend_core(
        self,
        tech_stack: TechStack,
        frontend_instructions: str,
        pages: List[str],
        image_data: str
    ) -> List[GeneratedFile]:
        """Generate core app files: App.tsx, main.tsx, routing, contexts"""
        
        arch_instructions = self._get_architecture_instructions(tech_stack)
        
        system_prompt = f"""You are a frontend expert for {tech_stack.frontend}.

{frontend_instructions}

{arch_instructions}

**CRITICAL: Follow the folder structure shown above EXACTLY!**

Generate ONLY core application files:
1. main.tsx (entry point)
2. App.tsx (root component with routing)
3. Global contexts (AuthContext, ThemeContext)
4. API service client
5. Global styles

Return ONLY valid JSON:
{{
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "complete file content",
      "description": "file description"
    }}
  ]
}}"""

        # Determine root folder and paths based on architecture
        from models import ArchitectureType
        if tech_stack.architecture == ArchitectureType.MONOLITHIC:
            root_folder = ""
            src_path = "src/"
            main_file = "src/main.tsx"
            app_file = "src/App.tsx"
        else:  # MICROSERVICES
            root_folder = "frontend/"
            src_path = "frontend/src/"
            main_file = "frontend/src/main.tsx"
            app_file = "frontend/src/App.tsx"
        
        user_prompt = f"""Create core application files matching the UI design.

**CRITICAL FILE PATHS**: All files must use this structure:
- Main entry: `{main_file}`
- App root: `{app_file}`
- Contexts: `{src_path}contexts/`
- Services: `{src_path}services/`
- Styles: `{src_path}styles/`

**Pages**: {', '.join(pages)}

Generate:
- {main_file} with ReactDOM.createRoot
- {app_file} with React Router setup for all pages
- {src_path}contexts/AuthContext.tsx for user authentication
- {src_path}services/apiClient.ts with axios and interceptors
- {src_path}styles/globals.css with Tailwind directives"""

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_data}"}
                        }
                    ]
                }
            ],
            temperature=0.6
        )
        
        return self._parse_files_from_response(response.choices[0].message.content)
    
    async def _generate_frontend_pages(
        self,
        tech_stack: TechStack,
        frontend_instructions: str,
        pages: List[str],
        api_summary: str,
        image_data: str,
        description: str
    ) -> List[GeneratedFile]:
        """Generate page components"""
        
        arch_instructions = self._get_architecture_instructions(tech_stack)
        
        system_prompt = f"""You are a frontend expert for {tech_stack.frontend}.

{frontend_instructions}

{arch_instructions}

**CRITICAL: Follow the folder structure shown above EXACTLY!**

Generate ONLY page components matching the UI mockup.

Return ONLY valid JSON:
{{
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "complete file content",
      "description": "file description"
    }}
  ]
}}"""

        # Determine pages folder based on architecture
        from models import ArchitectureType
        if tech_stack.architecture == ArchitectureType.MONOLITHIC:
            pages_folder = "src/client/pages/"
        else:  # MICROSERVICES
            pages_folder = "frontend/src/pages/"
        
        user_prompt = f"""Create page components: {', '.join(pages[:8])}

**CRITICAL FILE PATHS**: All page components must be in `{pages_folder}` folder!
Example: `{pages_folder}Dashboard.tsx`, `{pages_folder}Login.tsx`

**Backend API**:
{api_summary}

**Requirements**: {description}

Generate:
- Page component for each route in `{pages_folder}`
- Data fetching with React hooks
- Loading and error states
- Responsive layout matching mockup
- Form handling where needed"""

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_data}"}
                        }
                    ]
                }
            ],
            temperature=0.6
        )
        
        return self._parse_files_from_response(response.choices[0].message.content)
    
    async def _generate_frontend_components(
        self,
        tech_stack: TechStack,
        frontend_instructions: str,
        components: List[str]
    ) -> List[GeneratedFile]:
        """Generate reusable UI components and utilities"""
        
        arch_instructions = self._get_architecture_instructions(tech_stack)
        
        system_prompt = f"""You are a frontend expert for {tech_stack.frontend}.

{frontend_instructions}

{arch_instructions}

**CRITICAL: Follow the folder structure shown above EXACTLY!**

Generate ONLY reusable UI components and utilities:
1. Layout components (Header, Footer, Sidebar)
2. UI components (Button, Input, Card, Modal, Table)
3. Utility functions
4. Custom hooks

Return ONLY valid JSON:
{{
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "complete file content",
      "description": "file description"
    }}
  ]
}}"""

        # Determine component paths based on architecture
        from models import ArchitectureType
        if tech_stack.architecture == ArchitectureType.MONOLITHIC:
            components_folder = "src/client/components/"
            hooks_folder = "src/client/hooks/"
            utils_folder = "src/client/utils/"
        else:  # MICROSERVICES
            components_folder = "frontend/src/components/"
            hooks_folder = "frontend/src/hooks/"
            utils_folder = "frontend/src/utils/"
        
        user_prompt = f"""Create reusable components: {', '.join(components[:10])}

**CRITICAL FILE PATHS**: Use these folder paths:
- Layout: `{components_folder}layout/` (Header.tsx, Footer.tsx, Sidebar.tsx)
- UI: `{components_folder}ui/` (Button.tsx, Input.tsx, Card.tsx, etc.)
- Hooks: `{hooks_folder}` (useAuth.ts, useApi.ts, useLocalStorage.ts)
- Utils: `{utils_folder}` (cn.ts, formatters.ts, validators.ts)

Generate:
- Layout components in `{components_folder}layout/`
- UI components in `{components_folder}ui/` with TypeScript and Tailwind
- Custom hooks in `{hooks_folder}`
- Utility functions in `{utils_folder}`"""

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6
        )
        
        return self._parse_files_from_response(response.choices[0].message.content)
    
    async def _step5_generate_configs(
        self,
        architecture: Dict[str, Any],
        tech_stack: TechStack,
        project_name: str
    ) -> List[GeneratedFile]:
        """
        Step 5: Generate configuration and deployment files
        """
        
        arch_instructions = self._get_architecture_instructions(tech_stack)
        
        system_prompt = f"""You are a DevOps expert. Create configuration and deployment files.

{arch_instructions}

**CRITICAL: Follow the folder structure shown above EXACTLY!**

Generate:
1. README.md with setup instructions
2. .env.example with all required variables
3. docker-compose.yml
4. Dockerfile(s) in the CORRECT locations based on architecture
5. Package manager files (package.json, requirements.txt, etc.) in the CORRECT locations

Return ONLY valid JSON:
{{
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "complete file content",
      "description": "file description"
    }}
  ]
}}"""

        user_prompt = f"""Create configuration files for {project_name}.

**Tech Stack**: {tech_stack.frontend}, {tech_stack.backend}, {tech_stack.database}
**Features**: {architecture.get('features', [])}

Generate:
- README.md with setup instructions
- Environment configuration (.env.example)
- Docker setup (Dockerfile, docker-compose.yml)
- Dependency files
- CI/CD configuration (optional)"""

        # Log the prompts
        logger.info("=" * 80)
        logger.info("STEP 5: CONFIGURATION FILES GENERATION")
        logger.info("=" * 80)
        logger.info(f"SYSTEM PROMPT:\n{system_prompt}")
        logger.info("-" * 80)
        logger.info(f"USER PROMPT:\n{user_prompt}")
        logger.info("=" * 80)

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )
        
        return self._parse_files_from_response(response.choices[0].message.content)
    
    def _parse_files_from_response(self, content: str) -> List[GeneratedFile]:
        """Parse GeneratedFile objects from LLM response with improved error handling"""
        try:
            # Try to find JSON in response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                logger.error("No JSON found in response")
                logger.error(f"Response content preview: {content[:500]}...")
                return []
            
            json_str = content[json_start:json_end]
            
            # Try to parse JSON
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError as je:
                logger.error(f"JSON decode error: {je}")
                logger.error(f"JSON string preview: {json_str[:1000]}...")
                
                # Try to fix common JSON issues
                # 1. Replace single quotes with double quotes
                json_str = json_str.replace("'", '"')
                
                # 2. Try parsing again
                try:
                    data = json.loads(json_str)
                    logger.info("Successfully parsed JSON after fixing quotes")
                except json.JSONDecodeError:
                    logger.error("Failed to parse JSON even after fixes")
                    return []
            
            files = data.get("files", [])
            
            if not files:
                logger.warning("No files found in parsed JSON")
                logger.warning(f"Data structure: {list(data.keys())}")
                return []
            
            parsed_files = []
            for idx, f in enumerate(files):
                try:
                    file_path = f.get("path", f"unknown_{idx}.txt")
                    file_desc = f.get("description", f"File {idx+1}")
                    
                    parsed_files.append(GeneratedFile(
                        path=file_path,
                        content=f.get("content", ""),
                        description=file_desc
                    ))
                    
                    # Log each generated file
                    logger.info(f"  ✓ Generated: {file_path} - {file_desc}")
                    
                except Exception as e:
                    logger.error(f"Failed to parse file {idx}: {e}")
                    continue
            
            logger.info(f"Successfully parsed {len(parsed_files)} files from response")
            return parsed_files
            
        except Exception as e:
            logger.error(f"Failed to parse files from response: {e}")
            logger.error(f"Response preview: {content[:500]}...")
            return []
    
    def _combine_results(
        self,
        architecture: Dict[str, Any],
        database_files: List[GeneratedFile],
        backend_files: List[GeneratedFile],
        frontend_files: List[GeneratedFile],
        config_files: List[GeneratedFile],
        tech_stack: TechStack
    ) -> Dict[str, Any]:
        """Combine all generation steps into final result"""
        
        all_files = database_files + backend_files + frontend_files + config_files
        
        # Build project structure from architecture
        project_structure = architecture.get("project_structure", {
            "frontend": ["src/", "public/", "package.json"],
            "backend": ["src/", "requirements.txt"],
            "database": ["schema.sql"]
        })
        
        # Extract dependencies
        dependencies = {
            "frontend": self._extract_frontend_deps(tech_stack.frontend),
            "backend": self._extract_backend_deps(tech_stack.backend),
            "database": [tech_stack.database.value]
        }
        
        # Generate setup instructions
        setup_instructions = [
            "# Setup Instructions",
            "",
            "## Prerequisites",
            f"- {tech_stack.frontend} runtime",
            f"- {tech_stack.backend} runtime",
            f"- {tech_stack.database} database",
            "",
            "## Backend Setup",
            "1. Navigate to backend directory",
            "2. Install dependencies",
            "3. Configure environment variables (.env)",
            "4. Run database migrations",
            "5. Start backend server",
            "",
            "## Frontend Setup",
            "1. Navigate to frontend directory",
            "2. Install dependencies",
            "3. Configure API endpoint",
            "4. Start development server",
            "",
            "## Database Setup",
            "1. Create database",
            "2. Run schema/migrations",
            "3. (Optional) Seed initial data",
            "",
            f"## Architecture Overview",
            f"- Pages: {', '.join(architecture.get('pages', []))}",
            f"- API Endpoints: {', '.join(architecture.get('api_endpoints', []))}",
            f"- Authentication: {architecture.get('authentication', 'no')}"
        ]
        
        return {
            "project_structure": project_structure,
            "files": all_files,
            "dependencies": dependencies,
            "setup_instructions": setup_instructions,
            "architecture": architecture
        }
    
    def _extract_frontend_deps(self, frontend: str) -> List[str]:
        """Extract typical dependencies for frontend framework"""
        deps_map = {
            "React": ["react", "react-dom", "axios", "@tailwindcss/forms"],
            "Vue": ["vue", "vue-router", "axios", "tailwindcss"],
            "Angular": ["@angular/core", "@angular/common", "@angular/router"],
            "HTML": ["tailwindcss"]
        }
        return deps_map.get(frontend, [])
    
    def _extract_backend_deps(self, backend: str) -> List[str]:
        """Extract typical dependencies for backend framework"""
        deps_map = {
            "FastAPI": ["fastapi", "uvicorn", "sqlalchemy", "pydantic", "python-jose"],
            "Flask": ["flask", "flask-sqlalchemy", "flask-jwt-extended", "flask-cors"],
            "Express": ["express", "cors", "jsonwebtoken", "bcrypt"],
            "Django": ["django", "djangorestframework", "django-cors-headers"]
        }
        return deps_map.get(backend, [])


# Global service instance
chained_generation_service = ChainedGenerationService()
