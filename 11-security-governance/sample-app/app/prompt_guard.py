"""Prompt Guard — detect and block prompt injection attempts."""
import re
from datetime import datetime
from app.models import PromptAnalysis, RiskLevel
import config.settings as settings


class PromptGuard:
    """Detect prompt injection with pattern matching and heuristic analysis."""

    INJECTION_PATTERNS = [
        (r"ignore\s+(previous|all|above)\s+instructions", 0.95),
        (r"disregard\s+(previous|all|above)\s+instructions", 0.95),
        (r"reveal\s+confidential", 0.90),
        (r"show\s+me\s+all", 0.70),
        (r"you\s+are\s+now\s+(a|an)\s+", 0.80),
        (r"forget\s+(everything|all|your)\s+instructions", 0.95),
        (r"new\s+instructions:", 0.85),
        (r"system\s*:\s*you\s+are", 0.90),
        (r"override\s+(safety|system|previous)", 0.90),
        (r"act\s+as\s+if\s+you\s+have\s+no\s+restrictions", 0.85),
        (r"bypass\s+(all|your|the)\s+(rules|restrictions|filters)", 0.90),
        (r"do\s+not\s+(follow|obey|listen\s+to)\s+(your|the)\s+instructions", 0.90),
        (r"pretend\s+you\s+(are|have|can)", 0.60),
        (r"jailbreak", 0.80),
        (r"DAN\s+mode", 0.85),
        (r"developer\s+mode", 0.85),
        (r"output\s+your\s+(system\s+)?prompt", 0.80),
        (r"what\s+(is|are)\s+your\s+(system\s+)?(prompt|instructions)", 0.60),
        (r"repeat\s+(everything|all|your)\s+(above|from)", 0.75),
        (r"translate\s+to\s+.*\s+and\s+ignore", 0.70),
    ]

    INDIRECT_PATTERNS = [
        (r"IGNORE\s+THE\s+SYSTEM\s+INSTRUCTIONS", 0.95),
        (r"REVEAL\s+CONFIDENTIAL", 0.90),
        (r"DISREGARD\s+ALL\s+PREVIOUS", 0.90),
        (r"you\s+must\s+now\s+follow\s+these\s+instructions", 0.85),
        (r"new\s+system\s+prompt:", 0.90),
    ]

    def __init__(self, threshold: float = None):
        self.threshold = threshold or settings.PROMPT_INJECTION_THRESHOLD
        self._blocked_patterns = [p.strip().lower() for p in settings.PROMPT_BLOCKED_PATTERNS]
        self._detection_count = 0
        self._blocked_count = 0

    def analyze(self, prompt: str) -> PromptAnalysis:
        self._detection_count += 1
        if len(prompt) > settings.PROMPT_MAX_LENGTH:
            return PromptAnalysis(
                prompt=prompt[:200],
                is_injection=True,
                confidence=1.0,
                risk_level=RiskLevel.HIGH,
                recommendation="Prompt exceeds maximum length",
                sanitized_prompt=prompt[:settings.PROMPT_MAX_LENGTH]
            )

        matched = []
        max_confidence = 0.0

        for pattern, confidence in self.INJECTION_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                matched.append(pattern)
                max_confidence = max(max_confidence, confidence)

        for pattern, confidence in self.INDIRECT_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                matched.append(f"indirect:{pattern}")
                max_confidence = max(max_confidence, confidence)

        lower_prompt = prompt.lower()
        for bp in self._blocked_patterns:
            if bp in lower_prompt:
                matched.append(f"blocked_word:{bp}")
                max_confidence = max(max_confidence, 0.85)

        is_injection = max_confidence >= self.threshold
        if is_injection:
            self._blocked_count += 1

        risk_level = RiskLevel.LOW
        if max_confidence >= 0.9:
            risk_level = RiskLevel.CRITICAL
        elif max_confidence >= 0.8:
            risk_level = RiskLevel.HIGH
        elif max_confidence >= 0.6:
            risk_level = RiskLevel.MEDIUM

        recommendation = "Allow" if not is_injection else "Block — prompt injection detected"

        return PromptAnalysis(
            prompt=prompt[:200],
            is_injection=is_injection,
            confidence=round(max_confidence, 4),
            matched_patterns=matched,
            risk_level=risk_level,
            recommendation=recommendation,
            sanitized_prompt=self._sanitize(prompt) if is_injection else prompt
        )

    def _sanitize(self, prompt: str) -> str:
        sanitized = prompt
        for pattern, _ in self.INJECTION_PATTERNS:
            sanitized = re.sub(pattern, "[BLOCKED]", sanitized, flags=re.IGNORECASE)
        for pattern, _ in self.INDIRECT_PATTERNS:
            sanitized = re.sub(pattern, "[BLOCKED]", sanitized, flags=re.IGNORECASE)
        return sanitized

    def get_stats(self) -> dict:
        return {
            "total_analyzed": self._detection_count,
            "total_blocked": self._blocked_count,
            "block_rate_pct": round(
                self._blocked_count / self._detection_count * 100, 1
            ) if self._detection_count > 0 else 0,
            "threshold": self.threshold,
            "blocked_patterns_count": len(self._blocked_patterns)
        }

    def list_patterns(self) -> list[dict]:
        return [
            {"pattern": p, "type": "direct"}
            for p, _ in self.INJECTION_PATTERNS
        ] + [
            {"pattern": p, "type": "indirect"}
            for p, _ in self.INDIRECT_PATTERNS
        ]
