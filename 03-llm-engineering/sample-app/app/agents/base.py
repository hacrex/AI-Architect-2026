from openai import OpenAI
from typing import List, Dict, Any, Optional
from app.models import AgentResponse, ToolCall, AgentType
from config.settings import settings
import time
import logging

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all agents with shared functionality."""

    def __init__(self, agent_type: AgentType, system_prompt: str, tools: List[Dict] = None):
        self.agent_type = agent_type
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.agent_model_override.get(agent_type.value, settings.default_model)
        self.tool_registry = {}

    def register_tool(self, tool_name: str, tool_func):
        """Register a callable tool for this agent."""
        self.tool_registry[tool_name] = tool_func

    async def process(self, query: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process a query and return response with any tool calls."""
        start_time = time.time()
        messages = self._build_messages(query, context)
        tool_calls_made = []

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools if self.tools else None,
                tool_choice="auto" if self.tools else None,
                max_tokens=settings.max_tokens_per_request,
                temperature=settings.temperature,
            )

            assistant_message = response.choices[0].message

            # Handle tool calls
            if assistant_message.tool_calls:
                messages.append(assistant_message)

                for tool_call in assistant_message.tool_calls:
                    tool_result = await self._execute_tool(
                        tool_call.function.name,
                        tool_call.function.arguments
                    )
                    tool_calls_made.append(ToolCall(
                        tool_name=tool_call.function.name,
                        arguments=tool_call.function.arguments,
                        result=tool_result,
                    ))
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result,
                    })

                # Get final response after tool use
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=settings.max_tokens_per_request,
                    temperature=settings.temperature,
                )
                content = final_response.choices[0].message.content
                tokens = response.usage.total_tokens + final_response.usage.total_tokens
            else:
                content = assistant_message.content
                tokens = response.usage.total_tokens

            return AgentResponse(
                agent=self.agent_type.value,
                content=content,
                tool_calls=tool_calls_made,
                model_used=self.model,
                tokens_used=tokens,
                latency_ms=round((time.time() - start_time) * 1000, 2),
            )

        except Exception as e:
            logger.error(f"Agent {self.agent_type.value} failed: {e}")
            return AgentResponse(
                agent=self.agent_type.value,
                content=f"I encountered an error processing your request: {str(e)}",
                tool_calls=[],
                model_used=self.model,
                tokens_used=0,
                latency_ms=round((time.time() - start_time) * 1000, 2),
            )

    async def _execute_tool(self, tool_name: str, arguments: str) -> str:
        """Execute a registered tool."""
        import json

        if tool_name not in self.tool_registry:
            return f"Error: Tool '{tool_name}' not found"

        try:
            args = json.loads(arguments)
            result = await self.tool_registry[tool_name](**args)
            return str(result)
        except Exception as e:
            return f"Error executing tool: {str(e)}"

    def _build_messages(self, query: str, context: Dict[str, Any] = None) -> List[Dict]:
        """Build message array for API call."""
        messages = [{"role": "system", "content": self.system_prompt}]

        if context and "history" in context:
            messages.extend(context["history"])

        messages.append({"role": "user", "content": query})
        return messages

    def get_info(self) -> Dict[str, Any]:
        """Return agent metadata."""
        return {
            "name": self.agent_type.value,
            "description": self.system_prompt[:100] + "...",
            "tools": list(self.tool_registry.keys()),
            "model": self.model,
        }
