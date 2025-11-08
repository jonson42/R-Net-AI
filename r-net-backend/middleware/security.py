"""
Security middleware for API authentication and input sanitization
"""

import secrets
from typing import Optional
from fastapi import Request, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

# Security bearer for API key authentication
security = HTTPBearer(auto_error=False)


class APIKeyAuth:
    """
    API Key authentication manager
    """
    
    def __init__(self, api_keys: Optional[list[str]] = None):
        # In production, load from database or secure config
        self.api_keys = set(api_keys or [])
        
        # If no keys provided, generate a default one (dev only)
        if not self.api_keys:
            default_key = "rnet_dev_" + secrets.token_urlsafe(32)
            self.api_keys.add(default_key)
            logger.warning(f"Generated default API key: {default_key}")
    
    def verify_key(self, api_key: str) -> bool:
        """Verify if API key is valid"""
        return api_key in self.api_keys
    
    def generate_key(self) -> str:
        """Generate new API key"""
        new_key = "rnet_" + secrets.token_urlsafe(32)
        self.api_keys.add(new_key)
        return new_key


# Global auth manager
auth_manager = APIKeyAuth()


async def verify_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> str:
    """
    Dependency for API key verification
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not auth_manager.verify_key(credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses
    """
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response


def sanitize_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Trim to max length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove potentially dangerous patterns
    dangerous_patterns = [
        '<script', '</script',
        'javascript:', 'onerror=',
        'onload=', 'onclick=',
    ]
    
    text_lower = text.lower()
    for pattern in dangerous_patterns:
        if pattern in text_lower:
            logger.warning(f"Suspicious pattern detected: {pattern}")
            # Remove the pattern (case-insensitive)
            import re
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    return text


def validate_base64_image(image_data: str) -> bool:
    """
    Validate base64 image data
    """
    import base64
    import re
    
    try:
        # Check if it has data URL prefix
        if image_data.startswith('data:image'):
            # Extract base64 part
            match = re.match(r'data:image/\w+;base64,(.+)', image_data)
            if match:
                image_data = match.group(1)
        
        # Try to decode
        decoded = base64.b64decode(image_data, validate=True)
        
        # Check if it looks like an image (starts with common image headers)
        image_headers = [
            b'\x89PNG',  # PNG
            b'\xFF\xD8\xFF',  # JPEG
            b'GIF87a',  # GIF
            b'GIF89a',  # GIF
            b'RIFF',  # WebP
        ]
        
        return any(decoded.startswith(header) for header in image_headers)
        
    except Exception as e:
        logger.error(f"Invalid base64 image data: {e}")
        return False
