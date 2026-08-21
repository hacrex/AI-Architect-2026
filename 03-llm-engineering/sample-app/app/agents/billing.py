from app.agents.base import BaseAgent
from app.models import AgentType


class BillingAgent(BaseAgent):
    """Agent specialized for billing inquiries, order status, and refunds."""

    SYSTEM_PROMPT = """You are a specialized billing agent for an enterprise knowledge assistant.

Your responsibilities:
- Answer questions about billing and payments
- Look up order status and history
- Explain refund and return policies
- Process refund requests (with appropriate approvals)

Guidelines:
- Always verify the user's identity before sharing account details
- Be precise with financial information
- Explain charges clearly
- Escalate complex billing disputes to human agents
- Never process refunds without proper authorization"""

    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "lookup_order",
                "description": "Look up order details by order ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The order ID to look up"
                        }
                    },
                    "required": ["order_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_account_balance",
                "description": "Get account balance and recent transactions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The account ID"
                        }
                    },
                    "required": ["account_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "check_refund_eligibility",
                "description": "Check if an order is eligible for refund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The order ID to check"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for refund request"
                        }
                    },
                    "required": ["order_id", "reason"]
                }
            }
        }
    ]

    def __init__(self):
        super().__init__(
            agent_type=AgentType.BILLING,
            system_prompt=self.SYSTEM_PROMPT,
            tools=self.TOOLS,
        )
