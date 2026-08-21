from openai import OpenAI
from typing import List, Dict, Any, Tuple
from app.models import AgentType, QueryRequest
from app.agents import SupportAgent, BillingAgent, TechAgent
from config.settings import settings
import logging
import json

logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrates multiple agents based on query intent."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.agents = {
            AgentType.SUPPORT: SupportAgent(),
            AgentType.BILLING: BillingAgent(),
            AgentType.TECH: TechAgent(),
        }
        self.classification_prompt = """Classify the following user query into one of these categories:
- support: General questions, policies, how-to guides, company procedures
- billing: Billing inquiries, order status, refunds, payments
- tech: Technical questions, code help, debugging, system architecture

Return ONLY the category name (support, billing, or tech). No explanation needed.

Query: {query}"""

    def _classify_query(self, query: str) -> AgentType:
        """Classify query to determine which agent should handle it."""
        try:
            response = self.client.chat.completions.create(
                model=settings.default_model,
                messages=[
                    {"role": "user", "content": self.classification_prompt.format(query=query)}
                ],
                max_tokens=20,
                temperature=0.0,
            )

            category = response.choices[0].message.content.strip().lower()

            if category in ["support", "billing", "tech"]:
                return AgentType(category)
            return AgentType.SUPPORT

        except Exception as e:
            logger.error(f"Classification failed: {e}")
            return AgentType.SUPPORT

    def _detect_multi_agent_need(self, query: str) -> Tuple[bool, List[str]]:
        """Detect if query requires multiple agents."""
        keywords = {
            "order": "billing",
            "refund": "billing",
            "return": "billing",
            "code": "tech",
            "debug": "tech",
            "deploy": "tech",
            "policy": "support",
            "how to": "support",
        }

        detected = set()
        query_lower = query.lower()

        for keyword, agent in keywords.items():
            if keyword in query_lower:
                detected.add(agent)

        return len(detected) > 1, list(detected)

    def _create_plan(self, agents_needed: List[str], query: str) -> List[str]:
        """Create an orchestration plan."""
        plan = [f"1. Classify query intent"]

        if len(agents_needed) > 1:
            plan.append(f"2. Route to multiple agents: {', '.join(agents_needed)}")
            plan.append(f"3. Combine responses from all agents")
            plan.append(f"4. Synthesize final answer")
        else:
            agent = agents_needed[0] if agents_needed else "support"
            plan.append(f"2. Route to {agent} agent")
            plan.append(f"3. Generate response")

        return plan

    async def process(self, request: QueryRequest) -> Dict[str, Any]:
        """Process a query through the orchestrator."""
        import time
        start_time = time.time()

        # Check if multi-agent handling is needed
        needs_multi, agents_needed = self._detect_multi_agent_need(request.query)

        if needs_multi:
            plan = self._create_plan(agents_needed, request.query)

            # Process with multiple agents
            responses = []
            total_tokens = 0

            for agent_name in agents_needed:
                agent_type = AgentType(agent_name)
                agent = self.agents[agent_type]
                response = await agent.process(request.query, request.context)
                responses.append(response)
                total_tokens += response.tokens_used

            # Synthesize responses
            combined_content = "\n\n".join([
                f"**{r.agent.title()} Agent:**\n{r.content}"
                for r in responses
            ])

            return {
                "answer": combined_content,
                "agents_used": agents_needed,
                "orchestration_plan": plan,
                "tool_calls": [tc for r in responses for tc in r.tool_calls],
                "tokens_used": total_tokens,
                "latency_ms": round((time.time() - start_time) * 1000, 2),
            }
        else:
            # Single agent processing
            agent_type = self._classify_query(request.query)
            agent = self.agents[agent_type]
            response = await agent.process(request.query, request.context)
            plan = self._create_plan([agent_type.value], request.query)

            return {
                "answer": response.content,
                "agents_used": [agent_type.value],
                "orchestration_plan": plan,
                "tool_calls": response.tool_calls,
                "tokens_used": response.tokens_used,
                "latency_ms": round((time.time() - start_time) * 1000, 2),
            }

    def get_agent_info(self) -> List[Dict[str, Any]]:
        """Get information about all agents."""
        return [agent.get_info() for agent in self.agents.values()]
