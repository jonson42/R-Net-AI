from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum


class TechStackOptions(str, Enum):
    # Frontend options
    REACT = "React"
    ANGULAR = "Angular"
    HTML = "HTML"
    VUE = "Vue"
    SVELTE = "Svelte"
    
    # Backend options
    FASTAPI = "FastAPI"
    FLASK = "Flask"
    DOTNET = ".NET"
    EXPRESS = "Express"
    DJANGO = "Django"
    
    # Database options
    POSTGRESQL = "PostgreSQL"
    MYSQL = "MySQL"
    MONGODB = "MongoDB"
    SQLITE = "SQLite"
    REDIS = "Redis"


class ArchitectureType(str, Enum):
    """Architecture pattern for project structure"""
    MONOLITHIC = "monolithic"  # Single unified folder structure (e.g., Next.js, Django, ASP.NET MVC)
    MICROSERVICES = "microservices"  # Separate backend/ and frontend/ folders


class TechStack(BaseModel):
    frontend: TechStackOptions = Field(..., description="Frontend technology")
    backend: TechStackOptions = Field(..., description="Backend technology")
    database: TechStackOptions = Field(..., description="Database technology")
    architecture: ArchitectureType = Field(
        default=ArchitectureType.MONOLITHIC,
        description="Architecture pattern: monolithic (single folder) or microservices (separate backend/frontend folders)"
    )


class CodeGenerationRequest(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")
    description: str = Field(..., min_length=10, description="Detailed project description")
    tech_stack: TechStack = Field(..., description="Selected technology stack")
    project_name: Optional[str] = Field(default="generated-app", description="Project name")
    custom_prompt: Optional[str] = Field(default=None, description="Optional custom prompt to override generated prompt")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFc...",
                "description": "A task management application with user authentication, CRUD operations for tasks, and real-time updates.",
                "tech_stack": {
                    "frontend": "React",
                    "backend": "FastAPI",
                    "database": "PostgreSQL"
                },
                "project_name": "task-manager"
            }
        }


class PromptPreviewRequest(BaseModel):
    description: str = Field(..., min_length=10, description="Detailed project description")
    tech_stack: TechStack = Field(..., description="Selected technology stack")
    project_name: Optional[str] = Field(default="generated-app", description="Project name")


class PromptPreviewResponse(BaseModel):
    system_prompt: str = Field(..., description="Generated system prompt")
    user_prompt: str = Field(..., description="Generated user prompt")
    message: str = Field(default="Prompt generated successfully. You can edit and use it in /generate endpoint.")


class GeneratedFile(BaseModel):
    path: str = Field(..., description="Relative file path")
    content: str = Field(..., description="File content")
    description: str = Field(..., description="File description")


class CodeGenerationResponse(BaseModel):
    success: bool = Field(..., description="Generation success status")
    message: str = Field(..., description="Response message")
    project_structure: Dict[str, Any] = Field(default_factory=dict, description="Project structure")
    files: List[GeneratedFile] = Field(default_factory=list, description="Generated files")
    dependencies: Dict[str, List[str]] = Field(default_factory=dict, description="Project dependencies")
    setup_instructions: List[str] = Field(default_factory=list, description="Setup instructions")
    error_details: Optional[str] = Field(default=None, description="Error details if any")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    openai_connected: bool = Field(..., description="OpenAI connection status")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Error details")
    code: Optional[str] = Field(default=None, description="Error code")