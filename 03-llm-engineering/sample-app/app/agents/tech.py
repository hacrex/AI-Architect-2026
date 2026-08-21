from app.agents.base import BaseAgent
from app.models import AgentType


class TechAgent(BaseAgent):
    """Agent specialized for technical questions, code help, and debugging."""

    SYSTEM_PROMPT = """You are a specialized technical agent for an enterprise knowledge assistant.

Your responsibilities:
- Answer technical questions about code, architecture, and systems
- Help with debugging and troubleshooting
- Provide code examples and best practices
- Search code repositories for relevant examples

Guidelines:
- Be technically accurate
- Provide working code examples when appropriate
- Explain trade-offs and alternatives
- Reference official documentation when available
- For complex issues, suggest involving the appropriate team"""

    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "search_code",
                "description": "Search code repositories for relevant code examples",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for code"
                        },
                        "language": {
                            "type": "string",
                            "description": "Programming language filter"
                        },
                        "repository": {
                            "type": "string",
                            "description": "Specific repository to search"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_documentation",
                "description": "Search technical documentation and wikis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        },
                        "product": {
                            "type": "string",
                            "description": "Product or service name"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_runbook",
                "description": "Retrieve runbooks for common operations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Operation type (deploy, rollback, scale, etc.)"
                        }
                    },
                    "required": ["operation"]
                }
            }
        }
    ]

    def __init__(self):
        super().__init__(
            agent_type=AgentType.TECH,
            system_prompt=self.SYSTEM_PROMPT,
            tools=self.TOOLS,
        )
