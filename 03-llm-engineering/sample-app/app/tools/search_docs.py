from app.tools.base import BaseTool
from typing import Dict, Any
import json


class SearchDocsTool(BaseTool):
    """Tool for searching internal company documents."""

    def __init__(self):
        super().__init__(
            name="search_documents",
            description="Search internal company documents for relevant information"
        )
        # Sample knowledge base (in production, this would be a vector DB)
        self.documents = {
            "leave": [
                {"title": "Leave Policy", "content": "Employees are entitled to 20 days annual leave, 10 days sick leave, and 5 personal days per year.", "category": "hr"},
                {"title": "Leave Request Process", "content": "Submit leave requests through the HR portal at least 2 weeks in advance for planned leave.", "category": "hr"},
            ],
            "remote": [
                {"title": "Remote Work Policy", "content": "Hybrid work model: 3 days in office, 2 days remote. Fully remote requires VP approval.", "category": "policies"},
            ],
            "expenses": [
                {"title": "Expense Policy", "content": "Expenses under $100 need manager approval. Over $100 need director approval. Submit within 30 days.", "category": "policies"},
            ],
            "onboarding": [
                {"title": "Onboarding Checklist", "content": "Day 1: IT setup, badge, welcome kit. Week 1: Team introductions, training sessions.", "category": "onboarding"},
            ],
        }

    async def execute(self, query: str, category: str = None) -> str:
        """Search documents and return relevant results."""
        results = []
        query_lower = query.lower()

        for key, docs in self.documents.items():
            for doc in docs:
                if category and doc["category"] != category:
                    continue
                if any(word in doc["content"].lower() or word in doc["title"].lower()
                       for word in query_lower.split()):
                    results.append(doc)

        if not results:
            return json.dumps({"results": [], "message": "No relevant documents found"})

        return json.dumps({"results": results[:5], "count": len(results)})

    def _get_parameters_schema(self) -> Dict[str, Any]:
        return {
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
