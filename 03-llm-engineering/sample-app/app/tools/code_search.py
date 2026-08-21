from app.tools.base import BaseTool
from typing import Dict, Any
import json


class CodeSearchTool(BaseTool):
    """Tool for searching code repositories."""

    def __init__(self):
        super().__init__(
            name="search_code",
            description="Search code repositories for relevant code examples"
        )
        # Sample code snippets (in production, this would query a code search API)
        self.code_samples = {
            "authentication": [
                {
                    "file": "app/auth.py",
                    "language": "python",
                    "snippet": "def verify_token(token: str) -> dict:\\n    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])\\n    return payload",
                    "description": "JWT token verification function"
                },
            ],
            "rate_limit": [
                {
                    "file": "app/middleware.py",
                    "language": "python",
                    "snippet": "class RateLimiter:\\n    def __init__(self, max_requests: int, window_seconds: int):\\n        self.max_requests = max_requests\\n        self.window = window_seconds",
                    "description": "Rate limiter implementation"
                },
            ],
            "database": [
                {
                    "file": "app/db.py",
                    "language": "python",
                    "snippet": "async def get_user(user_id: str) -> User:\\n    return await db.users.find_one({'id': user_id})",
                    "description": "Database query function"
                },
            ],
        }

    async def execute(self, query: str, language: str = None, repository: str = None) -> str:
        """Search code and return relevant results."""
        results = []
        query_lower = query.lower()

        for key, snippets in self.code_samples.items():
            for snippet in snippets:
                if language and snippet["language"] != language:
                    continue
                if any(word in snippet["description"].lower() or word in snippet["file"].lower()
                       for word in query_lower.split()):
                    results.append(snippet)

        if not results:
            return json.dumps({"results": [], "message": "No relevant code found"})

        return json.dumps({"results": results[:5], "count": len(results)})

    def _get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for code"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language filter (e.g., python, javascript)"
                },
                "repository": {
                    "type": "string",
                    "description": "Specific repository to search"
                }
            },
            "required": ["query"]
        }
