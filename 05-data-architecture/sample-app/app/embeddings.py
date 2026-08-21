"""Embedding generation for documents."""
import hashlib
import time
from typing import Optional


class EmbeddingCache:
    """Simple in-memory cache for embeddings."""
    
    def __init__(self):
        self._cache: dict[str, list[float]] = {}
        self._ttl: dict[str, float] = {}
    
    def get(self, text: str) -> Optional[list[float]]:
        key = hashlib.md5(text.encode()).hexdigest()
        if key in self._cache:
            if time.time() - self._ttl[key] < 3600:
                return self._cache[key]
            else:
                del self._cache[key]
                del self._ttl[key]
        return None
    
    def set(self, text: str, embedding: list[float]):
        key = hashlib.md5(text.encode()).hexdigest()
        self._cache[key] = embedding
        self._ttl[key] = time.time()
    
    def clear(self):
        self._cache.clear()
        self._ttl.clear()


cache = EmbeddingCache()


class EmbeddingProvider:
    """Base class for embedding providers."""
    
    def embed(self, text: str) -> list[float]:
        raise NotImplementedError
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(text) for text in texts]


class MockEmbeddingProvider(EmbeddingProvider):
    """Mock embedding provider for testing."""
    
    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions
    
    def embed(self, text: str) -> list[float]:
        import random
        random.seed(hash(text) % (2**32))
        return [random.uniform(-1, 1) for _ in range(self.dimensions)]


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider."""
    
    def __init__(self, model: str = "text-embedding-ada-002"):
        self.model = model
        try:
            import openai
            self.client = openai.OpenAI()
        except ImportError:
            raise ImportError("openai package required for OpenAI embeddings")
    
    def embed(self, text: str) -> list[float]:
        cached = cache.get(text)
        if cached:
            return cached
        
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        embedding = response.data[0].embedding
        cache.set(text, embedding)
        return embedding
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        cached_results = []
        uncached_texts = []
        uncached_indices = []
        
        for i, text in enumerate(texts):
            cached = cache.get(text)
            if cached:
                cached_results.append((i, cached))
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
        
        if uncached_texts:
            response = self.client.embeddings.create(
                input=uncached_texts,
                model=self.model
            )
            for j, embedding_data in enumerate(response.data):
                text = uncached_texts[j]
                embedding = embedding_data.embedding
                cache.set(text, embedding)
                cached_results.append((uncached_indices[j], embedding))
        
        cached_results.sort(key=lambda x: x[0])
        return [embedding for _, embedding in cached_results]


def get_embedding_provider(provider: str = "mock", **kwargs) -> EmbeddingProvider:
    """
    Get an embedding provider instance.
    
    Args:
        provider: Provider name (mock, openai)
        **kwargs: Provider-specific arguments
        
    Returns:
        EmbeddingProvider instance
    """
    if provider == "mock":
        return MockEmbeddingProvider(**kwargs)
    elif provider == "openai":
        return OpenAIEmbeddingProvider(**kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider}")
