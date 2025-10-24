import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from config import settings
from models import (
    CodeGenerationRequest, 
    CodeGenerationResponse, 
    HealthResponse, 
    ErrorResponse,
    GeneratedFile
)
from services.openai_service import openai_service

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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if settings.debug else "An unexpected error occurred"
        ).dict()
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


@app.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate full-stack code from image and description"""
    try:
        logger.info(f"Code generation request for project: {request.project_name}")
        logger.info(f"Tech stack: {request.tech_stack}")
        logger.info(f"Description length: {len(request.description)} characters")
        
        # Validate OpenAI API key
        if not settings.openai_api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OpenAI API key not configured"
            )
        
        # Generate code using OpenAI
        result = await openai_service.generate_code(
            image_data=request.image_data,
            description=request.description,
            tech_stack=request.tech_stack,
            project_name=request.project_name
        )
        
        # Create response
        response = CodeGenerationResponse(
            success=True,
            message=f"Successfully generated {len(result['files'])} files for {request.project_name}",
            project_structure=result["project_structure"],
            files=result["files"],
            dependencies=result["dependencies"],
            setup_instructions=result["setup_instructions"]
        )
        
        logger.info(f"Code generation completed successfully - {len(result['files'])} files generated")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Code generation failed: {e}", exc_info=True)
        
        return CodeGenerationResponse(
            success=False,
            message="Code generation failed",
            error_details=str(e) if settings.debug else "An error occurred during generation"
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "R-Net AI Backend Service",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )