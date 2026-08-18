import time
import logging
from typing import List, Optional
from app.models import (
    LLMResponse,
    ComparisonResult,
    ComplexityLevel,
    BenchmarkResult,
    BenchmarkSummary,
)
from app.model_gateway import model_gateway
from app.model_router import router
from config.settings import settings

logger = logging.getLogger(__name__)


class ModelComparator:
    """Compare model responses side-by-side with metrics."""

    def __init__(self):
        self.benchmark_prompts = {
            "simple": [
                "What is 2 + 2?",
                "What color is the sky?",
                "Define API in one sentence.",
                "What is the capital of France?",
                "How many days are in a week?",
            ],
            "normal": [
                "Explain the difference between REST and GraphQL.",
                "What are three best practices for API design?",
                "Summarize microservices architecture.",
                "What is the purpose of a load balancer?",
                "Explain the concept of CI/CD.",
            ],
            "complex": [
                "Compare horizontal vs vertical scaling for a cloud-native application handling 10,000 requests per second. Consider cost, latency, and operational complexity.",
                "Design a data pipeline architecture for real-time analytics on 5TB of daily event data. Explain your technology choices and trade-offs.",
                "Analyze the security implications of using LLMs in an enterprise setting. What are the risks, mitigations, and architectural patterns to address them?",
                "Evaluate the trade-offs between microservices and monolithic architecture for a startup with 5 engineers building a B2B SaaS platform.",
                "Design a disaster recovery strategy for a multi-region deployment serving 1M+ users with 99.99% availability requirements.",
            ],
            "all": [],
        }
        # Merge all categories
        for category, prompts in self.benchmark_prompts.items():
            if category != "all":
                self.benchmark_prompts["all"].extend(prompts)

    async def compare(
        self,
        query: str,
        models: List[str],
        metrics: List[str],
    ) -> ComparisonResult:
        """Compare response from multiple models."""
        results = []

        for model_id in models:
            start_time = time.time()

            try:
                response = await model_gateway.generate(
                    query=query,
                    context="",
                    model=model_id,
                )

                latency_ms = (time.time() - start_time) * 1000
                response.latency_ms = latency_ms

                results.append(response)

            except Exception as e:
                logger.error(f"Model {model_id} failed: {e}")
                # Create error response
                error_response = LLMResponse(
                    content=f"Error: {str(e)}",
                    model_used=model_id,
                    tokens_used=0,
                    input_tokens=0,
                    output_tokens=0,
                    latency_ms=(time.time() - start_time) * 1000,
                    finish_reason="error",
                    cost_estimate=0.0,
                )
                results.append(error_response)

        # Get routing decision
        complexity, _, _ = router.get_routing_info(query)

        # Generate recommendation
        recommendation = self._generate_recommendation(results, complexity)

        return ComparisonResult(
            query=query,
            results=results,
            routing_decision=complexity,
            recommendation=recommendation,
        )

    def _generate_recommendation(
        self, results: List[LLMResponse], complexity: ComplexityLevel
    ) -> str:
        """Generate recommendation based on comparison results."""
        if not results:
            return "No results to compare"

        # Find best model by different criteria
        fastest = min(results, key=lambda r: r.latency_ms)
        cheapest = min(results, key=lambda r: r.cost_estimate)

        # For quality, we'd need human evaluation or a judge model
        # For now, use a simple heuristic based on response length and tokens
        best_quality = max(results, key=lambda r: r.tokens_used)

        recommendation_parts = [
            f"Complexity: {complexity.value}",
            f"Fastest: {fastest.model_used} ({fastest.latency_ms:.0f}ms)",
            f"Cheapest: {cheapest.model_used} (${cheapest.cost_estimate:.4f})",
            f"Most Detailed: {best_quality.model_used} ({best_quality.tokens_used} tokens)",
        ]

        # Add routing recommendation
        if complexity == ComplexityLevel.SIMPLE:
            recommendation_parts.append(
                "Recommendation: Use the simpler/faster model for this request type"
            )
        elif complexity == ComplexityLevel.COMPLEX:
            recommendation_parts.append(
                "Recommendation: Use the more capable model for quality"
            )
        else:
            recommendation_parts.append(
                "Recommendation: Either model is acceptable, consider cost vs quality"
            )

        return " | ".join(recommendation_parts)

    async def run_benchmark(
        self,
        models: List[str],
        category: str = "all",
        iterations: int = 3,
    ) -> List[BenchmarkResult]:
        """Run benchmark suite against models."""
        prompts = self.benchmark_prompts.get(
            category, self.benchmark_prompts["all"]
        )

        results = []

        for prompt in prompts:
            for model_id in models:
                # Run multiple iterations
                for i in range(iterations):
                    start_time = time.time()

                    try:
                        response = await model_gateway.generate(
                            query=prompt,
                            context="",
                            model=model_id,
                        )

                        latency_ms = (time.time() - start_time) * 1000

                        # Determine category
                        prompt_category = self._categorize_prompt(prompt)

                        result = BenchmarkResult(
                            prompt=prompt[:100] + "..."
                            if len(prompt) > 100
                            else prompt,
                            category=prompt_category,
                            model=model_id,
                            response=response.content[:200] + "..."
                            if len(response.content) > 200
                            else response.content,
                            latency_ms=latency_ms,
                            input_tokens=response.input_tokens,
                            output_tokens=response.output_tokens,
                            cost_estimate=response.cost_estimate,
                        )
                        results.append(result)

                    except Exception as e:
                        logger.error(
                            f"Benchmark failed for {model_id}: {e}"
                        )

        return results

    def _categorize_prompt(self, prompt: str) -> str:
        """Categorize a prompt based on characteristics."""
        word_count = len(prompt.split())

        if word_count < 15:
            return "simple"
        elif word_count > 50:
            return "complex"
        else:
            return "normal"

    def calculate_benchmark_summary(
        self, results: List[BenchmarkResult], model: str
    ) -> BenchmarkSummary:
        """Calculate summary statistics for a model."""
        model_results = [r for r in results if r.model == model]

        if not model_results:
            return BenchmarkSummary(
                model=model,
                total_prompts=0,
                avg_latency_ms=0,
                total_input_tokens=0,
                total_output_tokens=0,
                total_cost=0,
            )

        return BenchmarkSummary(
            model=model,
            total_prompts=len(model_results),
            avg_latency_ms=sum(r.latency_ms for r in model_results)
            / len(model_results),
            total_input_tokens=sum(r.input_tokens for r in model_results),
            total_output_tokens=sum(r.output_tokens for r in model_results),
            total_cost=sum(r.cost_estimate for r in model_results),
        )


comparator = ModelComparator()
