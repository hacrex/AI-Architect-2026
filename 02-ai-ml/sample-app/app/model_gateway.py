from openai import OpenAI
from typing import AsyncGenerator
from app.models import LLMResponse
from config.settings import settings
import time
import logging

logger = logging.getLogger(__name__)


class ModelGateway:
    """Model gateway with provider abstraction and cost tracking."""

    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.token_usage = {}
        self.cost_by_model = {}
        logger.info("Model Gateway initialized")

    async def generate(
        self,
        query: str,
        context: str,
        model: str = None,
    ) -> LLMResponse:
        """Generate response from specified model."""
        model = model or settings.default_model
        start_time = time.time()

        system_prompt = """You are a helpful AI assistant.
Answer questions clearly and concisely.
If you're unsure, say so."""

        user_message = f"""Context:
{context}

Question: {query}

Answer based on the context above:"""

        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=settings.max_tokens_per_request,
                temperature=0.1,
            )

            latency_ms = (time.time() - start_time) * 1000

            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens

            # Track usage
            self.token_usage[model] = self.token_usage.get(model, 0) + total_tokens

            # Calculate cost
            model_info = settings.model_info.get(model, {})
            input_cost = model_info.get("input_cost", 0.03)
            output_cost = model_info.get("output_cost", 0.06)

            cost = (input_tokens * input_cost / 1000) + (
                output_tokens * output_cost / 1000
            )
            self.cost_by_model[model] = self.cost_by_model.get(model, 0) + cost

            return LLMResponse(
                content=response.choices[0].message.content,
                model_used=model,
                tokens_used=total_tokens,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms,
                finish_reason=response.choices[0].finish_reason or "stop",
                cost_estimate=cost,
            )

        except Exception as e:
            logger.error(f"Model {model} failed: {e}")
            raise

    async def generate_stream(
        self,
        query: str,
        context: str,
        model: str = None,
    ) -> AsyncGenerator[str, None]:
        """Stream response from specified model."""
        model = model or settings.default_model

        system_prompt = """You are a helpful AI assistant.
Answer questions clearly and concisely."""

        user_message = f"""Context:
{context}

Question: {query}

Answer based on the context above:"""

        stream = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=settings.max_tokens_per_request,
            temperature=0.1,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def health_check(self) -> dict:
        """Check gateway health and usage stats."""
        return {
            "status": "healthy",
            "token_usage": self.token_usage,
            "cost_by_model": self.cost_by_model,
            "available_models": list(settings.model_info.keys()),
        }

    def get_usage_summary(self) -> dict:
        """Get usage summary."""
        total_tokens = sum(self.token_usage.values())
        total_cost = sum(self.cost_by_model.values())

        return {
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "tokens_by_model": self.token_usage,
            "cost_by_model": self.cost_by_model,
        }


model_gateway = ModelGateway()
