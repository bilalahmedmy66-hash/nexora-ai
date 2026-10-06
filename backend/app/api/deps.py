from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.permissions import Permission, has_permission
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User

bearer = HTTPBearer(auto_error=False)


def client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = AppError(401, "unauthorized", "Sign in to continue.")
    if creds is None:
        raise unauthorized
    user_id = decode_token(creds.credentials, "access")
    user = db.get(User, user_id) if user_id else None
    if not user or not user.is_active:
        raise unauthorized
    return user


def require_permission(permission: Permission):
    def checker(user: User = Depends(get_current_user)) -> User:
        if not has_permission(user.role, permission):
            raise AppError(403, "forbidden", "You do not have permission to do this.")
        return user

    return checker
