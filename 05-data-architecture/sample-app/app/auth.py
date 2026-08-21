"""Authentication and authorization for data access."""
from typing import Optional


class UserContext:
    """User context for authorization."""
    
    def __init__(
        self,
        user_id: str,
        department: str,
        clearance: str = "internal",
        roles: Optional[list[str]] = None
    ):
        self.user_id = user_id
        self.department = department
        self.clearance = clearance
        self.roles = roles or []
    
    def has_role(self, role: str) -> bool:
        return role in self.roles
    
    def is_admin(self) -> bool:
        return "admin" in self.roles or self.clearance == "admin"


class PermissionChecker:
    """Check document-level permissions."""
    
    CLASSIFICATION_LEVELS = {
        "public": 0,
        "internal": 1,
        "confidential": 2,
        "restricted": 3,
    }
    
    def has_permission(self, user_context: UserContext, document_metadata: dict) -> bool:
        """
        Check if user has access to a document.
        
        Args:
            user_context: User context
            document_metadata: Document metadata
            
        Returns:
            True if user has access
        """
        if user_context.is_admin():
            return True
        
        doc_classification = document_metadata.get("classification", "internal")
        doc_department = document_metadata.get("department", "unknown")
        
        user_level = self.CLASSIFICATION_LEVELS.get(user_context.clearance, 1)
        doc_level = self.CLASSIFICATION_LEVELS.get(doc_classification, 1)
        
        if user_level < doc_level:
            return False
        
        if doc_classification == "restricted":
            allowed_users = document_metadata.get("viewers", [])
            if user_context.user_id not in allowed_users:
                return False
        
        if doc_department not in [user_context.department, "shared"]:
            if doc_classification in ["confidential", "restricted"]:
                allowed_departments = document_metadata.get("allowed_departments", [])
                if user_context.department not in allowed_departments:
                    return False
        
        return True
    
    def filter_chunks(
        self,
        chunks: list[dict],
        user_context: UserContext
    ) -> list[dict]:
        """
        Filter chunks based on user permissions.
        
        Args:
            chunks: List of chunks with metadata
            user_context: User context
            
        Returns:
            Filtered list of chunks
        """
        return [
            chunk for chunk in chunks
            if self.has_permission(user_context, chunk.get("metadata", {}))
        ]


USERS = {
    "alice@company.com": UserContext(
        user_id="alice@company.com",
        department="engineering",
        clearance="internal",
        roles=["engineer"]
    ),
    "bob@company.com": UserContext(
        user_id="bob@company.com",
        department="hr",
        clearance="internal",
        roles=["hr-specialist"]
    ),
    "carol@company.com": UserContext(
        user_id="carol@company.com",
        department="security",
        clearance="confidential",
        roles=["security-analyst"]
    ),
    "admin@company.com": UserContext(
        user_id="admin@company.com",
        department="admin",
        clearance="admin",
        roles=["admin"]
    ),
}


def get_user_context(user_id: str) -> Optional[UserContext]:
    """
    Get user context by user ID.
    
    Args:
        user_id: User identifier
        
    Returns:
        UserContext or None
    """
    return USERS.get(user_id)
