"""
Monitoring and metrics for API performance tracking
"""

import time
from typing import Dict, List
from collections import defaultdict, deque
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Collect and track API metrics
    """
    
    def __init__(self, window_size: int = 1000):
        """
        Initialize metrics collector
        
        Args:
            window_size: Number of recent requests to track
        """
        # Request metrics
        self.request_count = defaultdict(int)
        self.error_count = defaultdict(int)
        self.response_times: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        
        # OpenAI metrics
        self.openai_calls = 0
        self.openai_errors = 0
        self.openai_tokens_used = 0
        self.openai_cost = 0.0
        
        # Cache metrics (updated from cache module)
        self.cache_hits = 0
        self.cache_misses = 0
        
        # System start time
        self.start_time = time.time()
    
    def record_request(self, method: str, path: str, status_code: int, duration: float):
        """Record a request"""
        endpoint = f"{method} {path}"
        
        self.request_count[endpoint] += 1
        self.response_times[endpoint].append(duration)
        
        if status_code >= 400:
            self.error_count[endpoint] += 1
    
    def record_openai_call(self, success: bool, tokens: int = 0, cost: float = 0.0):
        """Record OpenAI API call"""
        self.openai_calls += 1
        
        if not success:
            self.openai_errors += 1
        else:
            self.openai_tokens_used += tokens
            self.openai_cost += cost
    
    def record_cache(self, hit: bool):
        """Record cache hit/miss"""
        if hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
    
    def get_metrics(self) -> Dict:
        """Get current metrics"""
        uptime = time.time() - self.start_time
        
        # Calculate average response times
        avg_response_times = {}
        p95_response_times = {}
        
        for endpoint, times in self.response_times.items():
            if times:
                times_sorted = sorted(times)
                avg_response_times[endpoint] = sum(times) / len(times)
                
                # 95th percentile
                idx = int(len(times_sorted) * 0.95)
                p95_response_times[endpoint] = times_sorted[idx] if idx < len(times_sorted) else times_sorted[-1]
        
        # Calculate rates
        requests_per_second = sum(self.request_count.values()) / uptime if uptime > 0 else 0
        errors_per_second = sum(self.error_count.values()) / uptime if uptime > 0 else 0
        
        # Cache hit rate
        total_cache_requests = self.cache_hits + self.cache_misses
        cache_hit_rate = (self.cache_hits / total_cache_requests * 100) if total_cache_requests > 0 else 0
        
        # Error rate
        total_requests = sum(self.request_count.values())
        total_errors = sum(self.error_count.values())
        error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "system": {
                "uptime_seconds": int(uptime),
                "uptime_formatted": self._format_uptime(uptime)
            },
            "requests": {
                "total": total_requests,
                "by_endpoint": dict(self.request_count),
                "rate_per_second": round(requests_per_second, 2)
            },
            "errors": {
                "total": total_errors,
                "by_endpoint": dict(self.error_count),
                "rate_per_second": round(errors_per_second, 2),
                "error_rate_percent": round(error_rate, 2)
            },
            "performance": {
                "avg_response_time_ms": {k: round(v * 1000, 2) for k, v in avg_response_times.items()},
                "p95_response_time_ms": {k: round(v * 1000, 2) for k, v in p95_response_times.items()}
            },
            "openai": {
                "total_calls": self.openai_calls,
                "errors": self.openai_errors,
                "tokens_used": self.openai_tokens_used,
                "estimated_cost_usd": round(self.openai_cost, 4),
                "success_rate_percent": round((self.openai_calls - self.openai_errors) / self.openai_calls * 100, 2) if self.openai_calls > 0 else 0
            },
            "cache": {
                "hits": self.cache_hits,
                "misses": self.cache_misses,
                "hit_rate_percent": round(cache_hit_rate, 2),
                "total_requests": total_cache_requests
            }
        }
    
    def _format_uptime(self, seconds: float) -> str:
        """Format uptime as human-readable string"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
        
        return " ".join(parts)
    
    def get_health_status(self) -> Dict:
        """Get system health status"""
        metrics = self.get_metrics()
        
        # Determine health based on metrics
        is_healthy = True
        warnings = []
        
        # Check error rate
        error_rate = metrics["errors"]["error_rate_percent"]
        if error_rate > 10:
            is_healthy = False
            warnings.append(f"High error rate: {error_rate}%")
        elif error_rate > 5:
            warnings.append(f"Elevated error rate: {error_rate}%")
        
        # Check OpenAI success rate
        openai_success_rate = metrics["openai"]["success_rate_percent"]
        if self.openai_calls > 0 and openai_success_rate < 90:
            is_healthy = False
            warnings.append(f"Low OpenAI success rate: {openai_success_rate}%")
        
        # Check response times (if > 5 seconds on average)
        for endpoint, avg_time in metrics["performance"]["avg_response_time_ms"].items():
            if avg_time > 5000:
                warnings.append(f"Slow response time for {endpoint}: {avg_time}ms")
        
        return {
            "healthy": is_healthy,
            "status": "healthy" if is_healthy else "degraded",
            "warnings": warnings,
            "metrics_summary": {
                "total_requests": metrics["requests"]["total"],
                "error_rate": f"{error_rate:.2f}%",
                "cache_hit_rate": f"{metrics['cache']['hit_rate_percent']:.2f}%",
                "uptime": metrics["system"]["uptime_formatted"]
            }
        }


# Global metrics collector
metrics = MetricsCollector()


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to collect request metrics
    """
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Record metrics
        metrics.record_request(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=duration
        )
        
        # Add performance headers
        response.headers["X-Response-Time"] = f"{duration * 1000:.2f}ms"
        
        return response
