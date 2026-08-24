"""Context assembly — combine RAG context, agent results, and prompt."""
import uuid
from datetime import datetime
from typing import Optional


class ContextAssembler:
    """Assemble context from multiple sources into a single prompt."""

    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens

    def assemble(self, query: str, rag_context: dict = None,
                 agent_results: dict = None, system_prompt: str = None) -> dict:
        parts = []
        tokens_used = 0

        sys_prompt = system_prompt or (
            "You are an enterprise AI assistant. Answer based on the provided context. "
            "Always cite sources. If you don't know, say so."
        )
        parts.append({"role": "system", "content": sys_prompt})
        tokens_used += len(sys_prompt.split()) * 1.3

        if rag_context and rag_context.get("context"):
            context_block = (
                "Relevant information from the knowledge base:\n\n"
                f"{rag_context['context']}"
            )
            parts.append({"role": "context", "content": context_block})
            tokens_used += rag_context.get("tokens_used", len(context_block.split()) * 1.3)

        if agent_results and agent_results.get("execution"):
            exec_data = agent_results["execution"]
            if exec_data.get("final_answer"):
                agent_block = f"Agent analysis:\n{exec_data['final_answer']}"
                parts.append({"role": "agent_analysis", "content": agent_block})
                tokens_used += len(agent_block.split()) * 1.3

        user_message = f"Question: {query}"
        parts.append({"role": "user", "content": user_message})
        tokens_used += len(user_message.split()) * 1.3

        sources = []
        if rag_context and rag_context.get("sources"):
            sources.extend(rag_context["sources"])

        prompt_text = "\n\n".join([p["content"] for p in parts])

        return {
            "prompt": prompt_text,
            "messages": parts,
            "sources": sources,
            "estimated_tokens": int(tokens_used),
            "within_budget": int(tokens_used) <= self.max_tokens
        }

    def truncate_to_budget(self, messages: list[dict], max_tokens: int) -> list[dict]:
        total = 0
        result = []
        for msg in reversed(messages):
            msg_tokens = len(msg.get("content", "").split()) * 1.3
            if total + msg_tokens > max_tokens:
                break
            result.insert(0, msg)
            total += msg_tokens
        return result
