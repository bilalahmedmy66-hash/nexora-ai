from datetime import UTC, datetime, timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

from app.core.config import get_settings

_hasher = PasswordHasher()
# Used to keep login timing similar when the email does not exist.
DUMMY_HASH = _hasher.hash("not-a-real-password")


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return _hasher.verify(hashed, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def _create_token(subject: str, token_type: str, expires: timedelta) -> str:
    s = get_settings()
    now = datetime.now(UTC)
    payload = {"sub": subject, "type": token_type, "iat": now, "exp": now + expires}
    return jwt.encode(payload, s.jwt_secret, algorithm=s.jwt_algorithm)


def create_access_token(user_id: int) -> str:
    return _create_token(
        str(user_id),
        "access",
        timedelta(minutes=get_settings().access_token_expire_minutes),
    )


def create_refresh_token(user_id: int) -> str:
    return _create_token(
        str(user_id),
        "refresh",
        timedelta(days=get_settings().refresh_token_expire_days),
    )


def decode_token(token: str, expected_type: str) -> int | None:
    """Return the user id if the token is valid and of the expected type, else None."""
    s = get_settings()
    try:
        payload = jwt.decode(token, s.jwt_secret, algorithms=[s.jwt_algorithm])
    except jwt.PyJWTError:
        return None
    if payload.get("type") != expected_type:
        return None
    try:
        return int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        return None
