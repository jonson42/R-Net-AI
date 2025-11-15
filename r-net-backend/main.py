import logging
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from config import settings
from models import (
    CodeGenerationRequest, 
    CodeGenerationResponse, 
    HealthResponse, 
    ErrorResponse,
    GeneratedFile,
    PromptPreviewRequest,
    PromptPreviewResponse
)
from services.openai_service import openai_service
from services.syntax_validator import syntax_validator
from services.chained_generation_service import chained_generation_service

# Import middleware
from middleware.security import SecurityHeadersMiddleware, verify_api_key, sanitize_input, validate_base64_image
from middleware.metrics import MetricsMiddleware, metrics
from middleware.cache import cache
from middleware.exceptions import (
    AppException, ValidationException, AuthenticationException,
    ErrorCode, ErrorDetail
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting R-Net AI Backend Service...")
    
    # Test OpenAI connection on startup
    if settings.openai_api_key:
        is_connected = await openai_service.test_connection()
        if is_connected:
            logger.info("✓ OpenAI API connection successful")
        else:
            logger.warning("✗ OpenAI API connection failed - check your API key")
    else:
        logger.warning("⚠ OpenAI API key not configured")
    
    yield
    
    logger.info("Shutting down R-Net AI Backend Service...")


# Create FastAPI app
app = FastAPI(
    title="R-Net AI Backend",
    description="Backend service for AI-powered full-stack code generation",
    version="1.0.0",
    lifespan=lifespan
)

# Add custom middleware (order matters - first added = outermost)
app.add_middleware(MetricsMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    """Handle custom application exceptions"""
    logger.error(f"Application exception: {exc.message} [{exc.error_code}]")
    
    error_detail = ErrorDetail(
        error=exc.__class__.__name__,
        error_code=exc.error_code.value,
        message=exc.message,
        details=exc.details if settings.debug else None,
        timestamp=datetime.utcnow().isoformat() + "Z",
        path=str(request.url.path)
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_detail.dict(exclude_none=True)
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    error_detail = ErrorDetail(
        error="Internal Server Error",
        error_code=ErrorCode.INTERNAL_ERROR.value,
        message=str(exc) if settings.debug else "An unexpected error occurred",
        timestamp=datetime.utcnow().isoformat() + "Z",
        path=str(request.url.path)
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_detail.dict(exclude_none=True)
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        openai_connected = False
        if settings.openai_api_key:
            openai_connected = await openai_service.test_connection()
        
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            openai_connected=openai_connected
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )


@app.post("/prompt/preview", response_model=PromptPreviewResponse)
async def preview_prompt(request: PromptPreviewRequest):
    """
    Preview the prompt that will be sent to OpenAI before generation.
    This allows users to review and potentially edit the prompt.
    """
    try:
        logger.info(f"Prompt preview request for project: {request.project_name}")
        
        # Sanitize description input
        description = sanitize_input(request.description)
        
        # Generate the prompts
        system_prompt, user_prompt = await openai_service.preview_prompts(
            description=description,
            tech_stack=request.tech_stack,
            project_name=request.project_name
        )
        
        logger.info("Prompt preview generated successfully")
        
        return PromptPreviewResponse(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            message="Prompt generated successfully. You can edit these prompts and use them in the /generate endpoint with 'custom_prompt' field."
        )
        
    except Exception as e:
        logger.error(f"Prompt preview failed: {e}", exc_info=True)
        raise AppException(
            "Prompt preview failed",
            ErrorCode.INTERNAL_ERROR,
            500,
            {"error": str(e)}
        )


@app.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(
    request: CodeGenerationRequest
    # Authentication disabled - open API access
):
    """Generate full-stack code from image and description"""
    try:
        logger.info(f"Code generation request for project: {request.project_name}")
        logger.info(f"Tech stack: {request.tech_stack}")
        logger.info(f"Description length: {len(request.description)} characters")
        
        # Validate OpenAI API key
        if not settings.openai_api_key:
            raise AuthenticationException(
                "OpenAI API key not configured",
                ErrorCode.MISSING_API_KEY
            )
        
        # Sanitize description input
        description = sanitize_input(request.description)
        
        # Validate image data
        if not validate_base64_image(request.image_data):
            raise ValidationException(
                "Invalid image format. Supported formats: png, jpg, jpeg, gif, webp",
                ErrorCode.INVALID_IMAGE
            )
        
        # Check cache first
        tech_stack_dict = request.tech_stack.dict()
        cached_result = cache.get(request.image_data, description, tech_stack_dict)
        
        if cached_result:
            logger.info(f"Cache hit for project: {request.project_name}")
            metrics.record_cache(hit=True)
            
            return CodeGenerationResponse(
                success=True,
                message=f"Successfully generated {len(cached_result['files'])} files for {request.project_name} (from cache)",
                project_structure=cached_result["project_structure"],
                files=cached_result["files"],
                dependencies=cached_result["dependencies"],
                setup_instructions=cached_result["setup_instructions"]
            )
        
        metrics.record_cache(hit=False)
        
        # Generate code using OpenAI
        try:
            result = await openai_service.generate_code(
                image_data=request.image_data,
                description=description,
                tech_stack=request.tech_stack,
                project_name=request.project_name,
                custom_prompt=request.custom_prompt
            )
            
            # Record successful OpenAI call
            metrics.record_openai_call(success=True, tokens=4096, cost=0.08)
            
        except Exception as openai_error:
            # Record failed OpenAI call
            metrics.record_openai_call(success=False)
            raise
        
        # Validate syntax of generated files
        logger.info("Validating syntax of generated files...")
        validation_result = syntax_validator.validate_files(result["files"])
        
        if not validation_result["valid"]:
            # Log syntax errors but continue (non-blocking)
            logger.warning(f"Syntax validation found {len(validation_result['errors'])} errors")
            for error in validation_result["errors"]:
                logger.warning(f"  - {error['file']}: {error['error']}")
            
            # Add validation info to setup instructions
            result["setup_instructions"].insert(0, 
                f"⚠️ Note: {len(validation_result['errors'])} files have syntax warnings. Review before running."
            )
        else:
            logger.info(f"✓ All {validation_result['validated_files']} files passed syntax validation")
            result["setup_instructions"].insert(0, 
                f"✓ All generated files passed syntax validation ({validation_result['validated_files']} files checked)"
            )
        
        # Cache the result
        cache.set(request.image_data, description, tech_stack_dict, result)
        
        # Create response
        response = CodeGenerationResponse(
            success=True,
            message=f"Successfully generated {len(result['files'])} files for {request.project_name} "
                   f"({validation_result['validated_files']} files validated)",
            project_structure=result["project_structure"],
            files=result["files"],
            dependencies=result["dependencies"],
            setup_instructions=result["setup_instructions"]
        )
        
        logger.info(f"Code generation completed successfully - {len(result['files'])} files generated, "
                   f"{validation_result['validated_files']} validated")
        return response
        
    except (ValidationException, AuthenticationException) as e:
        # Re-raise custom exceptions
        raise
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise ValidationException(str(e), ErrorCode.INVALID_INPUT)
    except Exception as e:
        logger.error(f"Code generation failed: {e}", exc_info=True)
        raise AppException(
            "Code generation failed",
            ErrorCode.GENERATION_FAILED,
            500,
            {"error": str(e) if settings.debug else None}
        )


@app.get("/metrics")
async def get_metrics():
    """Get API metrics (authentication disabled)"""
    return metrics.get_metrics()


@app.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics (authentication disabled)"""
    return cache.get_stats()


@app.post("/cache/clear")
async def clear_cache():
    """Clear cache (authentication disabled)"""
    cache.clear()
    return {"message": "Cache cleared successfully"}


@app.post("/validate")
async def validate_code(files: List[GeneratedFile]):
    """
    Validate syntax of code files
    Useful for testing or re-validating existing code
    """
    try:
        validation_result = syntax_validator.validate_files(files)
        return {
            "success": validation_result["valid"],
            "validation": validation_result
        }
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise AppException(
            "Validation failed",
            ErrorCode.INTERNAL_ERROR,
            500,
            {"error": str(e)}
        )


@app.post("/generate/chained", response_model=CodeGenerationResponse)
async def generate_code_chained(request: CodeGenerationRequest):
    """
    Generate code using chained prompts strategy (multi-step approach)
    
    This endpoint breaks down code generation into 5 steps:
    1. Analyze architecture
    2. Generate database schema
    3. Generate backend API (using database context)
    4. Generate frontend (using backend API context)
    5. Generate configs & deployment files
    
    Each step uses the output from previous steps as context, resulting in more
    coherent and complete code generation.
    
    Better for: Complex applications, large projects
    Trade-off: Takes longer but produces more integrated results
    """
    try:
        logger.info(f"Chained code generation request for project: {request.project_name}")
        
        # Validate OpenAI API key
        if not settings.openai_api_key:
            raise AuthenticationException(
                "OpenAI API key not configured",
                ErrorCode.MISSING_API_KEY
            )
        
        # Sanitize description input
        description = sanitize_input(request.description)
        
        # Validate image data
        if not validate_base64_image(request.image_data):
            raise ValidationException(
                "Invalid image format. Supported formats: png, jpg, jpeg, gif, webp",
                ErrorCode.INVALID_IMAGE
            )
        
        # Generate code using chained strategy
        try:
            result = await chained_generation_service.generate_code_chained(
                image_data=request.image_data,
                description=description,
                tech_stack=request.tech_stack,
                project_name=request.project_name
            )
            
            # Record successful OpenAI calls (5 calls for 5 steps)
            metrics.record_openai_call(success=True, tokens=10000, cost=0.20)
            
        except Exception as openai_error:
            metrics.record_openai_call(success=False)
            raise
        
        # Validate syntax of generated files
        logger.info("Validating syntax of generated files...")
        validation_result = syntax_validator.validate_files(result["files"])
        
        if not validation_result["valid"]:
            logger.warning(f"Syntax validation found {len(validation_result['errors'])} errors")
            for error in validation_result["errors"]:
                logger.warning(f"  - {error['file']}: {error['error']}")
            
            result["setup_instructions"].insert(0, 
                f"⚠️ Note: {len(validation_result['errors'])} files have syntax warnings. Review before running."
            )
        else:
            logger.info(f"✓ All {validation_result['validated_files']} files passed syntax validation")
            result["setup_instructions"].insert(0, 
                f"✓ All generated files passed syntax validation ({validation_result['validated_files']} files checked)"
            )
        
        # Create response
        response = CodeGenerationResponse(
            success=True,
            message=f"Successfully generated {len(result['files'])} files for {request.project_name} using chained prompts "
                   f"({validation_result['validated_files']} files validated)",
            project_structure=result["project_structure"],
            files=result["files"],
            dependencies=result["dependencies"],
            setup_instructions=result["setup_instructions"]
        )
        
        logger.info(f"Chained code generation completed - {len(result['files'])} files generated")
        return response
        
    except (ValidationException, AuthenticationException) as e:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise ValidationException(str(e), ErrorCode.INVALID_INPUT)
    except Exception as e:
        logger.error(f"Chained code generation failed: {e}", exc_info=True)
        raise AppException(
            "Code generation failed",
            ErrorCode.GENERATION_FAILED,
            500,
            {"error": str(e) if settings.debug else None}
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "R-Net AI Backend Service",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics",
        "authentication": "disabled",
        "features": [
            "Request caching",
            "Syntax validation",
            "Prompt preview & editing",
            "Security headers",
            "Performance monitoring",
            "Open API access",
            "Chained prompt generation"
        ],
        "endpoints": {
            "single_prompt": "/generate",
            "chained_prompts": "/generate/chained",
            "preview": "/prompt/preview"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )