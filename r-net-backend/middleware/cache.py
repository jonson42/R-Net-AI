"""
Request/Response caching to reduce OpenAI API calls
"""

import hashlib
import json
import time
from typing import Optional, Dict, Any
from collections import OrderedDict


class LRUCache:
    """
    Simple in-memory LRU cache for request/response caching
    """
    
    def __init__(self, max_size: int = 100, ttl_seconds: int = 3600):
        """
        Initialize cache
        
        Args:
            max_size: Maximum number of cached items
            ttl_seconds: Time-to-live for cached items (1 hour default)
        """
        self.cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def _generate_key(self, image_data: str, description: str, tech_stack: dict) -> str:
        """
        Generate cache key from request parameters
        Uses hash to avoid storing large image data in key
        """
        # Create a deterministic hash
        image_hash = hashlib.sha256(image_data.encode()).hexdigest()[:16]
        tech_str = json.dumps(tech_stack, sort_keys=True)
        
        key_data = f"{image_hash}:{description}:{tech_str}"
        cache_key = hashlib.sha256(key_data.encode()).hexdigest()
        
        return cache_key
    
    def get(self, image_data: str, description: str, tech_stack: dict) -> Optional[Dict[str, Any]]:
        """
        Get cached response if available and not expired
        """
        key = self._generate_key(image_data, description, tech_stack)
        
        if key in self.cache:
            value, timestamp = self.cache[key]
            
            # Check if expired
            if time.time() - timestamp > self.ttl_seconds:
                # Expired - remove it
                del self.cache[key]
                self.misses += 1
                return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.hits += 1
            return value
        
        self.misses += 1
        return None
    
    def set(self, image_data: str, description: str, tech_stack: dict, value: Dict[str, Any]):
        """
        Cache response
        """
        key = self._generate_key(image_data, description, tech_stack)
        
        # Remove oldest if at capacity
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            self.evictions += 1
        
        # Add to cache with timestamp
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """Clear all cached items"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "hit_rate": f"{hit_rate:.2f}%",
            "total_requests": total_requests
        }
    
    def cleanup_expired(self):
        """Remove all expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if current_time - timestamp > self.ttl_seconds
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)


# Global cache instance
cache = LRUCache(max_size=100, ttl_seconds=3600)  # 100 items, 1 hour TTL
