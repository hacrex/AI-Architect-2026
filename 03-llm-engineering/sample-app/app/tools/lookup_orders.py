from app.tools.base import BaseTool
from typing import Dict, Any
import json
from datetime import datetime, timedelta
import random


class LookupOrdersTool(BaseTool):
    """Tool for looking up order details."""

    def __init__(self):
        super().__init__(
            name="lookup_order",
            description="Look up order details by order ID"
        )

    async def execute(self, order_id: str) -> str:
        """Look up order details (simulated)."""
        # Simulated order data
        orders = {
            "ORD-001": {
                "order_id": "ORD-001",
                "status": "delivered",
                "items": [{"name": "Laptop", "price": 1299.99, "quantity": 1}],
                "total": 1299.99,
                "order_date": "2024-01-15",
                "delivery_date": "2024-01-20",
                "eligible_for_return": True,
                "return_window_days": 30,
            },
            "ORD-002": {
                "order_id": "ORD-002",
                "status": "in_transit",
                "items": [{"name": "Monitor", "price": 599.99, "quantity": 2}],
                "total": 1199.98,
                "order_date": "2024-02-01",
                "estimated_delivery": "2024-02-10",
                "eligible_for_return": False,
            },
            "ORD-003": {
                "order_id": "ORD-003",
                "status": "processing",
                "items": [{"name": "Keyboard", "price": 149.99, "quantity": 1}],
                "total": 149.99,
                "order_date": "2024-02-05",
                "eligible_for_return": False,
            },
        }

        order = orders.get(order_id)
        if not order:
            return json.dumps({"error": f"Order {order_id} not found"})

        return json.dumps(order)

    def _get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID to look up (e.g., ORD-001)"
                }
            },
            "required": ["order_id"]
        }
