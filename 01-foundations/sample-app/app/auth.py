from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models import User
from typing import Dict

security = HTTPBearer()

MOCK_USERS: Dict[str, User] = {
    "user-001": User(
        id="user-001",
        name="John Doe",
        email="john@company.com",
        roles=["employee"],
        document_permissions=["hr", "engineering", "general"],
    ),
    "user-002": User(
        id="user-002",
        name="Jane Admin",
        email="jane@company.com",
        roles=["admin", "employee"],
        document_permissions=["hr", "engineering", "general", "finance", "legal"],
        is_admin=True,
    ),
    "user-003": User(
        id="user-003",
        name="Bob Limited",
        email="bob@company.com",
        roles=["employee"],
        document_permissions=["general"],
    ),
}


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    token = credentials.credentials

    user = MOCK_USERS.get(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def require_role(role: str):
    async def role_checker(user: User = Depends(get_current_user)):
        if role not in user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role}' required",
            )
        return user
    return role_checker
