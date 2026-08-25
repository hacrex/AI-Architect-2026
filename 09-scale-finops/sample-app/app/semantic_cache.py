"""Semantic Cache — meaning-based response reuse to reduce latency and cost."""
import hashlib
import math
import time
from datetime import datetime
from typing import Optional
from app.models import CacheEntry, CacheStats


class SemanticCache:
    """Cache that matches queries by semantic similarity, not exact string match."""

    def __init__(self, similarity_threshold: float = 0.92,
                 max_entries: int = 10000, default_ttl: int = 3600):
        self.similarity_threshold = similarity_threshold
        self.max_entries = max_entries
        self.default_ttl = default_ttl
        self._entries: dict[str, CacheEntry] = {}
        self._hit_count = 0
        self._miss_count = 0

    def _hash_query(self, query: str) -> str:
        return hashlib.sha256(query.lower().strip().encode()).hexdigest()[:16]

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def _compute_embedding(self, query: str) -> list[float]:
        words = query.lower().split()
        embedding = [0.0] * 100
        for i, word in enumerate(words):
            for j, ch in enumerate(word):
                idx = (ord(ch) + i * 7 + j * 13) % 100
                embedding[idx] += 1.0
        norm = math.sqrt(sum(x * x for x in embedding))
        if norm > 0:
            embedding = [x / norm for x in embedding]
        return embedding

    def get(self, query: str) -> Optional[str]:
        query_embedding = self._compute_embedding(query)
        best_match = None
        best_score = 0.0

        for entry in self._entries.values():
            if self._is_expired(entry):
                continue
            score = self._cosine_similarity(query_embedding, entry.embedding)
            if score >= self.similarity_threshold and score > best_score:
                best_score = score
                best_match = entry

        if best_match:
            self._hit_count += 1
            best_match.access_count += 1
            return best_match.response

        self._miss_count += 1
        return None

    def put(self, query: str, response: str, tokens_saved: int = 0) -> CacheEntry:
        key = self._hash_query(query)
        embedding = self._compute_embedding(query)

        if len(self._entries) >= self.max_entries:
            self._evict_lru()

        entry = CacheEntry(
            key=key,
            query_hash=key,
            response=response,
            tokens_saved=tokens_saved,
            ttl_seconds=self.default_ttl,
            embedding=embedding
        )
        self._entries[key] = entry
        return entry

    def invalidate(self, key: str) -> bool:
        if key in self._entries:
            del self._entries[key]
            return True
        return False

    def invalidate_by_pattern(self, pattern: str) -> int:
        to_remove = [k for k, v in self._entries.items()
                     if pattern.lower() in v.query_hash.lower()]
        for k in to_remove:
            del self._entries[k]
        return len(to_remove)

    def clear(self) -> int:
        count = len(self._entries)
        self._entries.clear()
        return count

    def _is_expired(self, entry: CacheEntry) -> bool:
        elapsed = (datetime.utcnow() - entry.created_at).total_seconds()
        return elapsed > entry.ttl_seconds

    def _evict_lru(self):
        if not self._entries:
            return
        lru_key = min(self._entries.keys(),
                      key=lambda k: self._entries[k].access_count)
        del self._entries[lru_key]

    def get_stats(self) -> CacheStats:
        total = self._hit_count + self._miss_count
        hit_rate = (self._hit_count / total * 100) if total > 0 else 0.0
        tokens_saved = sum(e.tokens_saved for e in self._entries.values())
        avg_age = 0.0
        expired = 0
        now = datetime.utcnow()
        for e in self._entries.values():
            age = (now - e.created_at).total_seconds()
            avg_age += age
            if age > e.ttl_seconds:
                expired += 1
        if self._entries:
            avg_age /= len(self._entries)

        return CacheStats(
            total_entries=len(self._entries),
            hit_count=self._hit_count,
            miss_count=self._miss_count,
            hit_rate_pct=round(hit_rate, 2),
            tokens_saved=tokens_saved,
            estimated_savings_usd=round(tokens_saved * 3.0 / 1_000_000, 6),
            avg_age_seconds=round(avg_age, 1),
            expired_entries=expired
        )

    def list_entries(self) -> list[dict]:
        return [
            {
                "key": e.key,
                "response_preview": e.response[:80],
                "tokens_saved": e.tokens_saved,
                "access_count": e.access_count,
                "created_at": e.created_at.isoformat(),
                "ttl_seconds": e.ttl_seconds,
                "expired": self._is_expired(e)
            }
            for e in self._entries.values()
        ]
