"""
Enhanced error handling with specific error codes and better messages
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel


class ErrorCode(str, Enum):
    """Standardized error codes"""
    
    # Validation errors (4000-4099)
    INVALID_INPUT = "ERR_4000"
    INVALID_IMAGE = "ERR_4001"
    INVALID_TECH_STACK = "ERR_4002"
    DESCRIPTION_TOO_SHORT = "ERR_4003"
    IMAGE_TOO_LARGE = "ERR_4004"
    UNSUPPORTED_FORMAT = "ERR_4005"
    
    # Authentication errors (4100-4199)
    MISSING_API_KEY = "ERR_4100"
    INVALID_API_KEY = "ERR_4101"
    API_KEY_EXPIRED = "ERR_4102"
    
    # Rate limiting errors (4290-4299)
    RATE_LIMIT_EXCEEDED = "ERR_4290"
    QUOTA_EXCEEDED = "ERR_4291"
    
    # OpenAI errors (5000-5099)
    OPENAI_CONNECTION_FAILED = "ERR_5000"
    OPENAI_AUTH_FAILED = "ERR_5001"
    OPENAI_RATE_LIMIT = "ERR_5002"
    OPENAI_TIMEOUT = "ERR_5003"
    OPENAI_INVALID_RESPONSE = "ERR_5004"
    
    # Code generation errors (5100-5199)
    GENERATION_FAILED = "ERR_5100"
    PARSING_FAILED = "ERR_5101"
    INCOMPLETE_GENERATION = "ERR_5102"
    
    # System errors (5900-5999)
    INTERNAL_ERROR = "ERR_5900"
    SERVICE_UNAVAILABLE = "ERR_5901"
    CONFIGURATION_ERROR = "ERR_5902"


class AppException(Exception):
    """Base application exception with error code"""
    
    def __init__(
        self, 
        message: str, 
        error_code: ErrorCode,
        status_code: int = 500,
        details: Optional[dict] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(AppException):
    """Validation error"""
    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.INVALID_INPUT, details: Optional[dict] = None):
        super().__init__(message, error_code, 400, details)


class AuthenticationException(AppException):
    """Authentication error"""
    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.MISSING_API_KEY, details: Optional[dict] = None):
        super().__init__(message, error_code, 401, details)


class RateLimitException(AppException):
    """Rate limit error"""
    def __init__(self, message: str, retry_after: int, details: Optional[dict] = None):
        merged_details = details or {}
        merged_details["retry_after"] = retry_after
        super().__init__(
            message, 
            ErrorCode.RATE_LIMIT_EXCEEDED, 
            429, 
            merged_details
        )


class OpenAIException(AppException):
    """OpenAI service error"""
    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.OPENAI_CONNECTION_FAILED, details: Optional[dict] = None):
        super().__init__(message, error_code, 503, details)


class CodeGenerationException(AppException):
    """Code generation error"""
    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.GENERATION_FAILED, details: Optional[dict] = None):
        super().__init__(message, error_code, 500, details)


class ErrorDetail(BaseModel):
    """Detailed error response"""
    error: str
    error_code: str
    message: str
    details: Optional[dict] = None
    timestamp: str
    path: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Validation Error",
                "error_code": "ERR_4001",
                "message": "Invalid image format. Supported formats: png, jpg, jpeg, gif, webp",
                "details": {"format": "bmp", "max_size": "5MB"},
                "timestamp": "2025-11-08T10:30:00Z",
                "path": "/generate"
            }
        }
