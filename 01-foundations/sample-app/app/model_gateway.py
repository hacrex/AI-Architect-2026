from openai import OpenAI
from typing import AsyncGenerator
from app.models import LLMResponse
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class ModelGateway:
    """Model gateway with provider fallback and cost tracking."""

    def __init__(self):
        self.primary_client = OpenAI(api_key=settings.openai_api_key)
        self.fallback_client = OpenAI(api_key=settings.openai_api_key)
        self.token_usage = {"primary": 0, "fallback": 0}
        logger.info("Model Gateway initialized")

    async def generate(
        self,
        query: str,
        context: str,
        model: str = None,
    ) -> LLMResponse:
        model = model or settings.default_model

        system_prompt = """You are a helpful enterprise knowledge assistant.
Answer questions based ONLY on the provided context.
If the context doesn't contain the answer, say "I don't have enough information to answer this question."
Always cite the source document when providing an answer."""

        user_message = f"""Context:
{context}

Question: {query}

Answer based on the context above:"""

        try:
            response = self.primary_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=settings.max_tokens_per_request,
                temperature=0.1,
            )

            self.token_usage["primary"] += response.usage.total_tokens

            return LLMResponse(
                content=response.choices[0].message.content,
                model_used=model,
                tokens_used=response.usage.total_tokens,
                finish_reason=response.choices[0].finish_reason,
            )

        except Exception as e:
            logger.warning(f"Primary model failed: {e}, attempting fallback")
            return await self._fallback_generate(query, context)

    async def _fallback_generate(
        self,
        query: str,
        context: str,
    ) -> LLMResponse:
        model = settings.fallback_model

        system_prompt = """You are a helpful enterprise knowledge assistant.
Answer questions based ONLY on the provided context.
If the context doesn't contain the answer, say "I don't have enough information to answer this question." """

        user_message = f"""Context:
{context}

Question: {query}

Answer based on the context above:"""

        response = self.fallback_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=settings.max_tokens_per_request,
            temperature=0.1,
        )

        self.token_usage["fallback"] += response.usage.total_tokens

        return LLMResponse(
            content=response.choices[0].message.content,
            model_used=model,
            tokens_used=response.usage.total_tokens,
            finish_reason=response.choices[0].finish_reason,
        )

    async def generate_stream(
        self,
        query: str,
        context: str,
        model: str = None,
    ) -> AsyncGenerator[str, None]:
        model = model or settings.default_model

        system_prompt = """You are a helpful enterprise knowledge assistant.
Answer questions based ONLY on the provided context."""

        user_message = f"""Context:
{context}

Question: {query}

Answer based on the context above:"""

        stream = self.primary_client.chat.completions.create(
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
        return {
            "status": "healthy",
            "token_usage": self.token_usage,
            "primary_model": settings.default_model,
            "fallback_model": settings.fallback_model,
        }
