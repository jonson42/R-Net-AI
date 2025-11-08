"""
Rate limiting middleware for API protection
"""

import time
from typing import Dict, Tuple
from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimiter:
    """
    Token bucket rate limiter with configurable limits per endpoint
    """
    
    def __init__(self):
        # Storage: {client_id: {endpoint: (tokens, last_update)}}
        self.buckets: Dict[str, Dict[str, Tuple[float, float]]] = defaultdict(dict)
        
        # Rate limits per endpoint (requests per minute)
        self.limits = {
            "/generate": 5,      # 5 generations per minute (expensive)
            "/health": 60,       # 60 health checks per minute
            "default": 30        # 30 requests per minute for other endpoints
        }
        
        # Burst allowance (max tokens)
        self.burst = {
            "/generate": 2,      # Allow burst of 2
            "/health": 10,
            "default": 5
        }
    
    def _get_limit(self, endpoint: str) -> Tuple[int, int]:
        """Get rate limit and burst for endpoint"""
        rate = self.limits.get(endpoint, self.limits["default"])
        burst = self.burst.get(endpoint, self.burst["default"])
        return rate, burst
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier (IP + User-Agent)"""
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")[:50]
        return f"{client_ip}:{user_agent}"
    
    def check_rate_limit(self, request: Request) -> bool:
        """
        Check if request is within rate limit
        Returns True if allowed, False if rate limited
        """
        client_id = self._get_client_id(request)
        endpoint = request.url.path
        current_time = time.time()
        
        # Get rate limit configuration
        rate_per_minute, max_burst = self._get_limit(endpoint)
        
        # Get or initialize bucket
        if endpoint not in self.buckets[client_id]:
            self.buckets[client_id][endpoint] = (max_burst, current_time)
        
        tokens, last_update = self.buckets[client_id][endpoint]
        
        # Calculate token refill (tokens per second)
        time_passed = current_time - last_update
        refill_rate = rate_per_minute / 60.0  # Convert to per-second rate
        tokens = min(max_burst, tokens + time_passed * refill_rate)
        
        # Check if request can proceed
        if tokens >= 1.0:
            # Consume one token
            tokens -= 1.0
            self.buckets[client_id][endpoint] = (tokens, current_time)
            return True
        else:
            # Rate limited
            self.buckets[client_id][endpoint] = (tokens, current_time)
            return False
    
    def get_retry_after(self, request: Request) -> int:
        """Calculate seconds until next request allowed"""
        client_id = self._get_client_id(request)
        endpoint = request.url.path
        
        rate_per_minute, _ = self._get_limit(endpoint)
        
        if endpoint in self.buckets.get(client_id, {}):
            tokens, last_update = self.buckets[client_id][endpoint]
            if tokens < 1.0:
                # Calculate time needed to refill 1 token
                refill_rate = rate_per_minute / 60.0
                time_needed = (1.0 - tokens) / refill_rate
                return int(time_needed) + 1
        
        return 60  # Default: retry after 1 minute
    
    def cleanup_old_entries(self, max_age_seconds: int = 3600):
        """Remove entries older than max_age_seconds (1 hour default)"""
        current_time = time.time()
        
        for client_id in list(self.buckets.keys()):
            for endpoint in list(self.buckets[client_id].keys()):
                _, last_update = self.buckets[client_id][endpoint]
                if current_time - last_update > max_age_seconds:
                    del self.buckets[client_id][endpoint]
            
            # Remove client if no endpoints left
            if not self.buckets[client_id]:
                del self.buckets[client_id]


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for rate limiting
    """
    
    def __init__(self, app, limiter: RateLimiter = None):
        super().__init__(app)
        self.limiter = limiter or RateLimiter()
        self.last_cleanup = time.time()
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for excluded paths
        if request.url.path in ["/", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)
        
        # Periodic cleanup (every 10 minutes)
        if time.time() - self.last_cleanup > 600:
            self.limiter.cleanup_old_entries()
            self.last_cleanup = time.time()
        
        # Check rate limit
        if not self.limiter.check_rate_limit(request):
            retry_after = self.limiter.get_retry_after(request)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please try again in {retry_after} seconds.",
                    "retry_after": retry_after
                },
                headers={"Retry-After": str(retry_after)}
            )
        
        # Add rate limit headers to response
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limiter.limits.get(request.url.path, 30))
        
        return response
