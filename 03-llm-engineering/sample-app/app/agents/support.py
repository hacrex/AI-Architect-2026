from app.agents.base import BaseAgent
from app.models import AgentType


class SupportAgent(BaseAgent):
    """Agent specialized for general support questions, policies, and how-to guides."""

    SYSTEM_PROMPT = """You are a helpful support agent for an enterprise knowledge assistant.

Your responsibilities:
- Answer questions about company policies (leave, remote work, expenses)
- Provide how-to guides for common tasks
- Help users understand company procedures

Guidelines:
- Always cite the source document when providing an answer
- If you don't know the answer, say so clearly
- Be concise but thorough
- Use a professional, helpful tone"""

    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "search_documents",
                "description": "Search internal company documents for relevant information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        },
                        "category": {
                            "type": "string",
                            "enum": ["hr", "policies", "general", "onboarding"],
                            "description": "Document category to search"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_faq",
                "description": "Retrieve frequently asked questions and answers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "FAQ topic"
                        }
                    },
                    "required": ["topic"]
                }
            }
        }
    ]

    def __init__(self):
        super().__init__(
            agent_type=AgentType.SUPPORT,
            system_prompt=self.SYSTEM_PROMPT,
            tools=self.TOOLS,
        )
