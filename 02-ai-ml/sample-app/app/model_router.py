import re
import logging
from typing import Tuple
from app.models import ComplexityLevel
from config.settings import settings

logger = logging.getLogger(__name__)


class ModelRouter:
    """Classifies request complexity and routes to appropriate model."""

    COMPLEX_KEYWORDS = [
        "compare",
        "contrast",
        "analyze",
        "analyze",
        "design",
        "architect",
        "evaluate",
        "trade-off",
        "tradeoffs",
        "implications",
        "considerations",
        "multi-step",
        "comprehensive",
        "in-depth",
        "detailed analysis",
        "security implications",
        "cost-benefit",
        "pros and cons",
        "advantages and disadvantages",
        "scalability",
        "distributed",
        "microservices",
        "infrastructure",
        "pipeline",
        "architecture",
        "strategy",
        "roadmap",
        "implementation plan",
    ]

    SIMPLE_KEYWORDS = [
        "what is",
        "define",
        "explain in one sentence",
        "how do i",
        "what color",
        "what time",
        "what is the",
        "calculate",
        "what is ",
        "name the",
        "list",
        "true or false",
        "yes or no",
    ]

    def classify_request(self, query: str) -> ComplexityLevel:
        """Classify request complexity based on query characteristics."""
        query_lower = query.lower()
        word_count = len(query.split())

        # Simple: short, factual, low complexity
        if word_count < 15:
            for keyword in self.SIMPLE_KEYWORDS:
                if keyword in query_lower:
                    logger.info(f"Classified as SIMPLE: {query[:50]}...")
                    return ComplexityLevel.SIMPLE

        # Complex: long, technical, multi-step reasoning
        if word_count > 50:
            logger.info(f"ClassIFIED as COMPLEX (long query): {query[:50]}...")
            return ComplexityLevel.COMPLEX

        # Check for complex keywords
        complex_score = sum(
            1 for kw in self.COMPLEX_KEYWORDS if kw in query_lower
        )
        if complex_score >= 2:
            logger.info(f"Classified as COMPLEX (keywords): {query[:50]}...")
            return ComplexityLevel.COMPLEX

        # Check for simple keywords
        simple_score = sum(
            1 for kw in self.SIMPLE_KEYWORDS if kw in query_lower
        )
        if simple_score >= 1 and word_count < 30:
            logger.info(f"Classified as SIMPLE (keywords): {query[:50]}...")
            return ComplexityLevel.SIMPLE

        # Default to normal
        logger.info(f"Classified as NORMAL: {query[:50]}...")
        return ComplexityLevel.NORMAL

    def select_model(
        self, complexity: ComplexityLevel, force_model: str = None
    ) -> str:
        """Select model based on complexity level."""
        if force_model and force_model in settings.model_info:
            return force_model

        model_map = {
            ComplexityLevel.SIMPLE: "gpt-3.5-turbo",
            ComplexityLevel.NORMAL: "gpt-4",
            ComplexityLevel.COMPLEX: "gpt-4",
        }

        selected = model_map.get(complexity, settings.default_model)
        logger.info(f"Selected model: {selected} for complexity: {complexity}")
        return selected

    def get_routing_info(self, query: str) -> Tuple[ComplexityLevel, str, str]:
        """
        Get complete routing information.
        Returns: (complexity, model, reason)
        """
        complexity = self.classify_request(query)
        model = self.select_model(complexity)

        reasons = {
            ComplexityLevel.SIMPLE: "Short query with factual/simple intent",
            ComplexityLevel.NORMAL: "Moderate complexity, standard reasoning",
            ComplexityLevel.COMPLEX: "High complexity, multi-step reasoning",
        }

        return complexity, model, reasons[complexity]

    def estimate_tokens(self, query: str) -> int:
        """Rough token estimate for routing decisions."""
        # Rough estimate: 1 token per 4 characters
        return len(query) // 4


router = ModelRouter()
