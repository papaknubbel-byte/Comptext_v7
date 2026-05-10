"""
Distributed Cache – Redis-backed high-performance caching for CompText V7.
"""

import os
import json
import logging
from typing import Any, Optional
import redis

log = logging.getLogger("comptext.distributed.cache")

class DistributedCache:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL")
        self._client = None
        self._local_fallback = {}
        
        if self.redis_url:
            try:
                self._client = redis.from_url(self.redis_url, decode_responses=True)
                self._client.ping()
                log.info(f"Connected to Redis at {self.redis_url}")
            except Exception as e:
                log.warning(f"Redis connection failed: {e}. Falling back to local cache.")
                self._client = None

    def get(self, key: str) -> Optional[Any]:
        if self._client:
            val = self._client.get(key)
            return json.loads(val) if val else None
        return self._local_fallback.get(key)

    def set(self, key: str, value: Any, ttl: int = 3600):
        if self._client:
            self._client.set(key, json.dumps(value), ex=ttl)
        else:
            self._local_fallback[key] = value

    def exists(self, key: str) -> bool:
        if self._client:
            return self._client.exists(key) > 0
        return key in self._local_fallback

# Singleton
cache = DistributedCache()
