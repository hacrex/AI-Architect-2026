from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """Base class for all tools with shared functionality."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Execute the tool and return result as string."""
        pass

    def get_schema(self) -> Dict[str, Any]:
        """Return tool schema for function calling."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self._get_parameters_schema(),
            }
        }

    @abstractmethod
    def _get_parameters_schema(self) -> Dict[str, Any]:
        """Return parameters schema for this tool."""
        pass

    def _get_cache_key(self, **kwargs) -> str:
        """Generate cache key from arguments."""
        return str(sorted(kwargs.items()))

    def _check_cache(self, **kwargs) -> Optional[str]:
        """Check if result is cached."""
        key = self._get_cache_key(**kwargs)
        if key in self._cache:
            import time
            cached_time, cached_result = self._cache[key]
            if time.time() - cached_time < self._cache_ttl:
                logger.debug(f"Cache hit for {self.name}")
                return cached_result
        return None

    def _set_cache(self, result: str, **kwargs):
        """Cache a result."""
        import time
        key = self._get_cache_key(**kwargs)
        self._cache[key] = (time.time(), result)
