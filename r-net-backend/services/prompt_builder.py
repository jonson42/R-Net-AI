"""
Modular Prompt Builder with Step-by-Step Logic
Breaks down complex prompts into manageable, composable sections
Now with technology-specific template integration
"""

from typing import Dict, List, Optional
from models import TechStack
from services.tech_specific_templates import TechSpecificTemplates


class PromptSection:
    """Base class for prompt sections"""
    
    @staticmethod
    def format_section(title: str, content: str, symbol: str = "═") -> str:
        """Format a section with visual separators"""
        separator = symbol * 79
        return f"\n{separator}\n{title}\n{separator}\n{content}\n"


class ProjectContextBuilder:
    """Builds project context section"""
    
    @staticmethod
    def build(tech_stack: TechStack, project_name: str, app_type: str) -> str:
        """Generate project context with tech stack info"""
        context = f"""Project Name: {project_name}
Application Type: {app_type.upper()}
Technology Stack:
  • Frontend: {tech_stack.frontend.value}
  • Backend: {tech_stack.backend.value}
  • Database: {tech_stack.database.value}"""
        
        return PromptSection.format_section("PROJECT CONTEXT", context)


class ResponseFormatBuilder:
    """Builds JSON response format requirements"""
    
    @staticmethod
    def build() -> str:
        """Generate response format specification"""
        format_spec = """Return ONLY a valid JSON object. No markdown, no explanations outside the JSON.

Structure:
```json
{
  "project_structure": {
    "frontend/": ["src/", "public/", "package.json"],
    "backend/": ["src/", "tests/", "requirements.txt"],
    "database/": ["migrations/", "schema.sql"],
    "docs/": ["API.md", "SETUP.md"]
  },
  "files": [
    {
      "path": "frontend/src/App.tsx",
      "content": "// COMPLETE file content - NO placeholders",
      "description": "Main application component"
    }
  ],
  "dependencies": {
    "frontend": ["react@18.2.0", "react-router-dom@6.x"],
    "backend": ["fastapi==0.104.1", "sqlalchemy==2.0.23"],
    "devDependencies": ["typescript", "pytest"]
  },
  "setup_instructions": [
    "1. Prerequisites: Node.js 18+, Python 3.11+",
    "2. Frontend: cd frontend && npm install && npm run dev",
    "3. Backend: cd backend && pip install -r requirements.txt"
  ]
}
```"""
        
        return PromptSection.format_section(
            "CRITICAL RESPONSE FORMAT (MUST FOLLOW EXACTLY)", 
            format_spec
        )


class CoreRequirementsBuilder:
    """Builds core code generation requirements"""
    
    @staticmethod
    def build() -> str:
        """Generate core requirements section"""
        requirements = """🎯 COMPLETENESS
  ✓ Every file MUST be 100% functional - zero placeholders
  ✓ Include ALL imports, type definitions, and dependencies
  ✓ Generate complete CRUD operations if needed
  ✓ Include error boundaries, loading states, and empty states

⚠️ SYNTAX CORRECTNESS (CRITICAL)
  ✓ ALL generated code MUST have valid syntax
  ✓ Python: Must parse with ast.parse() - no SyntaxError
  ✓ JavaScript/TypeScript: Balanced brackets, proper function syntax
  ✓ JSON: Valid JSON format with proper escaping
  ✓ HTML: Properly nested tags, no unclosed elements
  ✓ CSS: Balanced braces, valid property syntax
  ✓ Double-check syntax before returning - files will be validated

🔒 SECURITY (ESSENTIAL)
  ✓ Input validation using Pydantic/Zod schemas
  ✓ SQL injection prevention (use ORM parameterized queries)
  ✓ Authentication with JWT tokens (httpOnly cookies)
  ✓ CORS configuration for production
  ✓ Password hashing with bcrypt (12 rounds minimum)
  ✓ Rate limiting on authentication endpoints

📦 PRODUCTION READINESS
  ✓ Environment configuration (.env support)
  ✓ Proper logging with log levels (info, warn, error)
  ✓ Health check endpoints
  ✓ Graceful error handling and user-friendly messages
  ✓ Database connection pooling and retry logic
  ✓ Docker support with multi-stage builds"""
        
        return PromptSection.format_section(
            "CODE GENERATION REQUIREMENTS (NON-NEGOTIABLE)", 
            requirements
        )


class StyleRequirementsBuilder:
    """Builds frontend styling requirements"""
    
    @staticmethod
    def build() -> str:
        """Generate styling requirements section"""
        styling = """🎨 MANDATORY STYLING - NO UNSTYLED ELEMENTS
  ✓ Generate complete tailwind.config.js with custom theme
  ✓ Generate globals.css with CSS variables and animations
  ✓ Every component MUST have complete Tailwind classes
  ✓ Include responsive design (sm/md/lg/xl breakpoints)
  ✓ Add interactive states (hover/focus/active/disabled)
  ✓ Include dark mode support

REQUIRED UI COMPONENTS (All fully styled):
  • Button (primary/secondary/outline/ghost/danger variants)
  • Input (with label, error states, icon support)
  • Card, Modal, Dropdown, Tabs
  • Table with pagination
  • Loading states, Toast notifications
  • Form validation with error messages"""
        
        return PromptSection.format_section(
            "🎨 FRONTEND STYLING REQUIREMENTS", 
            styling
        )


class FrameworkSpecificBuilder:
    """Builds framework-specific requirements using tech-specific templates"""
    
    @staticmethod
    def build(tech_stack: TechStack) -> str:
        """
        Build framework-specific requirements from templates
        Uses TechSpecificTemplates for detailed, comprehensive instructions
        """
        # Get templates for selected technologies
        frontend_template = TechSpecificTemplates.get_frontend_template(tech_stack.frontend.value)
        backend_template = TechSpecificTemplates.get_backend_template(tech_stack.backend.value)
        database_template = TechSpecificTemplates.get_database_template(tech_stack.database.value)
        
        # Assemble comprehensive requirements
        content = f"FRONTEND ({tech_stack.frontend.value}):\n"
        content += frontend_template.get('core_instructions', '')
        content += "\n\n"
        content += frontend_template.get('styling_requirements', '')
        
        content += f"\n\nBACKEND ({tech_stack.backend.value}):\n"
        content += backend_template.get('core_instructions', '')
        
        content += f"\n\nDATABASE ({tech_stack.database.value}):\n"
        content += database_template.get('connection_example', '')
        
        return PromptSection.format_section(
            "TECHNOLOGY-SPECIFIC REQUIREMENTS (FROM TEMPLATES)", 
            content
        )


class TestingRequirementsBuilder:
    """Builds testing requirements"""
    
    @staticmethod
    def build() -> str:
        """Generate testing requirements"""
        testing = """✓ Frontend: Unit tests with Vitest/Jest and React Testing Library
✓ Backend: Unit tests with pytest and 80%+ coverage
✓ Integration tests for API endpoints
✓ Test fixtures and mocks for external dependencies
✓ Test both success and error scenarios"""
        
        return PromptSection.format_section("TESTING REQUIREMENTS", testing)


class DocumentationBuilder:
    """Builds documentation requirements"""
    
    @staticmethod
    def build() -> str:
        """Generate documentation requirements"""
        docs = """✓ README.md with setup instructions, architecture overview, screenshots
✓ API.md with endpoint documentation (request/response examples)
✓ ARCHITECTURE.md explaining project structure and design decisions
✓ Inline code comments for complex logic only
✓ JSDoc/docstrings for public functions"""
        
        return PromptSection.format_section("DOCUMENTATION REQUIREMENTS", docs)


class OutputChecklistBuilder:
    """Builds output validation checklist"""
    
    @staticmethod
    def build() -> str:
        """Generate output checklist"""
        checklist = """Before returning, verify:
  □ All files are complete (no TODOs or placeholders)
  □ All imports and dependencies are included
  □ Security measures implemented (auth, validation, CORS)
  □ Error handling in place for all API calls
  □ Responsive design with mobile-first approach
  □ All UI components have complete Tailwind styling
  □ tailwind.config.js and globals.css generated
  □ Database models with relationships defined
  □ Tests included for critical functionality
  □ Documentation files created (README, API docs)
  □ Environment configuration (.env.example)
  □ Docker support (Dockerfile, docker-compose.yml)"""
        
        return PromptSection.format_section("OUTPUT VALIDATION CHECKLIST", checklist)


class StepByStepPromptBuilder:
    """
    Main orchestrator for building prompts step by step
    """
    
    @staticmethod
    def build_system_prompt(
        tech_stack: TechStack,
        project_name: str,
        app_type: str = "general",
        include_styling: bool = True,
        include_testing: bool = True,
        include_docs: bool = True
    ) -> str:
        """
        Build system prompt step by step with configurable sections
        
        Args:
            tech_stack: Technology stack configuration
            project_name: Name of the project
            app_type: Type of application
            include_styling: Include detailed styling requirements
            include_testing: Include testing requirements
            include_docs: Include documentation requirements
        """
        
        # Step 1: Role and expertise
        prompt = """You are a world-class senior full-stack architect with 15+ years of experience building production-ready applications. Your expertise spans modern web technologies, security, performance optimization, and clean architecture.
"""
        
        # Step 2: Project context
        prompt += ProjectContextBuilder.build(tech_stack, project_name, app_type)
        
        # Step 3: Response format
        prompt += ResponseFormatBuilder.build()
        
        # Step 4: Core requirements
        prompt += CoreRequirementsBuilder.build()
        
        # Step 5: Styling requirements (optional)
        if include_styling:
            prompt += StyleRequirementsBuilder.build()
        
        # Step 6: Framework-specific practices
        prompt += FrameworkSpecificBuilder.build(tech_stack)
        
        # Step 7: Testing requirements (optional)
        if include_testing:
            prompt += TestingRequirementsBuilder.build()
        
        # Step 8: Documentation requirements (optional)
        if include_docs:
            prompt += DocumentationBuilder.build()
        
        # Step 9: Output checklist
        prompt += OutputChecklistBuilder.build()
        
        # Step 10: Final instruction
        prompt += "\n\n🚀 BEGIN GENERATION - Output only valid JSON with complete, production-ready code.\n"
        
        return prompt
    
    @staticmethod
    def build_user_prompt(
        description: str,
        tech_stack: TechStack,
        features: Optional[List[str]] = None,
        styling_emphasis: bool = True
    ) -> str:
        """
        Build user prompt with feature requirements
        
        Args:
            description: Project description
            tech_stack: Technology stack
            features: Optional list of specific features
            styling_emphasis: Emphasize styling in output
        """
        
        prompt = f"""Generate a complete {tech_stack.frontend.value} + {tech_stack.backend.value} application.

PROJECT DESCRIPTION:
{description}
"""
        
        if features:
            prompt += "\n\nREQUIRED FEATURES:\n"
            for i, feature in enumerate(features, 1):
                prompt += f"{i}. {feature}\n"
        
        if styling_emphasis:
            prompt += """
⚠️ CRITICAL - STYLING REQUIREMENTS:
• Generate tailwind.config.js with custom theme (colors, fonts, spacing)
• Generate globals.css with CSS variables and animations
• Every component MUST have complete Tailwind classes
• Include all UI components: Button, Input, Card, Modal, Table, etc.
• Add responsive design (mobile-first with breakpoints)
• Include interactive states (hover/focus/active)
"""
        
        prompt += f"""
DELIVERABLES:
• 20-30 complete files with full implementation
• Complete frontend with styled components
• Complete backend with API endpoints
• Database models and migrations
• Authentication system
• Error handling and validation
• Docker deployment files
• Documentation (README, API docs)

Technology Stack:
• Frontend: {tech_stack.frontend.value}
• Backend: {tech_stack.backend.value}
• Database: {tech_stack.database.value}

Return complete, production-ready code with NO placeholders or TODOs.
"""
        
        return prompt


class QuickPromptBuilder:
    """Quick builder for simple use cases"""
    
    @staticmethod
    def minimal(tech_stack: TechStack, project_name: str, description: str) -> tuple[str, str]:
        """
        Build minimal prompts for quick generation
        Returns: (system_prompt, user_prompt)
        """
        
        system_prompt = StepByStepPromptBuilder.build_system_prompt(
            tech_stack=tech_stack,
            project_name=project_name,
            app_type="general",
            include_styling=False,
            include_testing=False,
            include_docs=False
        )
        
        user_prompt = f"Generate a {tech_stack.frontend.value} + {tech_stack.backend.value} application: {description}"
        
        return system_prompt, user_prompt
    
    @staticmethod
    def full_featured(
        tech_stack: TechStack, 
        project_name: str, 
        description: str,
        features: List[str]
    ) -> tuple[str, str]:
        """
        Build comprehensive prompts with all features
        Returns: (system_prompt, user_prompt)
        """
        
        system_prompt = StepByStepPromptBuilder.build_system_prompt(
            tech_stack=tech_stack,
            project_name=project_name,
            app_type="general",
            include_styling=True,
            include_testing=True,
            include_docs=True
        )
        
        user_prompt = StepByStepPromptBuilder.build_user_prompt(
            description=description,
            tech_stack=tech_stack,
            features=features,
            styling_emphasis=True
        )
        
        return system_prompt, user_prompt
    
    @staticmethod
    def tech_template_based(
        tech_stack: TechStack,
        project_name: str,
        description: str
    ) -> tuple[str, str]:
        """
        Build prompts using technology-specific templates
        This method provides the most comprehensive, framework-specific guidance
        
        Returns: (system_prompt, user_prompt)
        """
        
        # Use the tech-specific template builder for complete prompts
        complete_prompt = TechSpecificTemplates.build_complete_prompt(
            tech_stack=tech_stack,
            description=description,
            project_name=project_name
        )
        
        # For tech-template-based approach, we combine everything into system prompt
        system_prompt = f"""You are a world-class senior full-stack architect and developer with 15+ years of experience.
Your expertise spans modern web technologies, security best practices, and clean architecture.

{complete_prompt}

CRITICAL: Follow ALL technology-specific requirements exactly as specified above.
Every framework has specific patterns that must be followed for production-quality code.
"""
        
        # Simple user prompt since all details are in system prompt
        user_prompt = f"""Generate a complete, production-ready application based on the requirements above.

Project: {project_name}
Stack: {tech_stack.frontend.value} + {tech_stack.backend.value} + {tech_stack.database.value}

Description: {description}

Return complete code following the exact patterns and structures specified in the system prompt.
"""
        
        return system_prompt, user_prompt
