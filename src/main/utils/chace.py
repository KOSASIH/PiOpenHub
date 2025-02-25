import time
import json
import redis
from functools import wraps
from typing import Any, Callable, Dict, Optional

class Cache:
    def __init__(self, backend: str = 'memory', redis_url: Optional[str] = None):
        self.backend = backend
        self.cache_data: Dict[str, Any] = {}
        
        if self.backend == 'redis':
            if redis_url is None:
                raise ValueError("Redis URL must be provided for Redis backend.")
            self.redis_client = redis.StrictRedis.from_url(redis_url)
        else:
            self.redis_client = None

    def set(self, key: str, value: Any, expiration: Optional[int] = None):
        if self.backend == 'redis':
            self.redis_client.set(key, json.dumps(value), ex=expiration)
        else:
            self.cache_data[key] = (value, time.time() + expiration if expiration else None)

    def get(self, key: str) -> Optional[Any]:
        if self.backend == 'redis':
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        else:
            value, expiration = self.cache_data.get(key, (None, None))
            if expiration and time.time() > expiration:
                self.delete(key)
                return None
            return value

    def delete(self, key: str):
        if self.backend == 'redis':
            self.redis_client.delete(key)
        else:
            if key in self.cache_data:
                del self.cache_data[key]

    def clear(self):
        if self.backend == 'redis':
            self.redis_client.flushdb()
        else:
            self.cache_data.clear()

    def cache(self, expiration: Optional[int] = None):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}:{json.dumps(args)}:{json.dumps(kwargs)}"
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                result = func(*args, **kwargs)
                self.set(cache_key, result, expiration)
                return result
            return wrapper
        return decorator

# Example usage
if __name__ == "__main__":
    # Initialize cache with Redis backend
    cache = Cache(backend='redis', redis_url='redis://localhost:6379')

    @cache.cache(expiration=60)  # Cache results for 60 seconds
    def expensive_function(param1, param2):
        time.sleep(2)  # Simulate a time-consuming operation
        return param1 + param2

    # First call will take time and cache the result
    print(expensive_function(1, 2))  # Output: 3
    # Second call will return the cached result
    print(expensive_function(1, 2))  # Output: 3 (instantaneous)
