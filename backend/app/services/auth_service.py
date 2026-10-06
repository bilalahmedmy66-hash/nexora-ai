from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.security import (
    DUMMY_HASH,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import TokenPair
from app.services import audit_service, user_service


def _tokens(user: User) -> TokenPair:
    return TokenPair(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


def login(db: Session, email: str, password: str, ip: str | None) -> TokenPair:
    user = user_service.get_by_email(db, email)
    # Always run a hash verification so timing does not reveal whether the email exists.
    valid = verify_password(password, user.hashed_password if user else DUMMY_HASH)
    if not user or not valid or not user.is_active:
        audit_service.record(
            db,
            "auth.login_failed",
            actor_email=email.lower(),
            ip=ip,
            details={"reason": "inactive" if user and valid and not user.is_active else "bad_credentials"},
        )
        db.commit()
        raise AppError(401, "invalid_credentials", "Incorrect email or password.")
    user_service.mark_login(db, user)
    audit_service.record(db, "auth.login", actor=user, entity_type="user", entity_id=user.id, ip=ip)
    db.commit()
    return _tokens(user)


def refresh(db: Session, refresh_token: str) -> TokenPair:
    user_id = decode_token(refresh_token, "refresh")
    user = db.get(User, user_id) if user_id else None
    if not user or not user.is_active:
        raise AppError(401, "invalid_token", "Your session has expired. Please sign in again.")
    return _tokens(user)
