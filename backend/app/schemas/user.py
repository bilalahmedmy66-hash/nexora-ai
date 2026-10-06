from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.permissions import Role


def _check_password(v: str) -> str:
    if len(v) < 10:
        raise ValueError("Password must be at least 10 characters.")
    if not any(c.isalpha() for c in v) or not any(c.isdigit() for c in v):
        raise ValueError("Password must contain at least one letter and one number.")
    return v


Password = Annotated[str, Field(max_length=128)]
FullName = Annotated[str, Field(min_length=1, max_length=200)]


class UserCreate(BaseModel):
    email: EmailStr
    full_name: FullName
    password: Password
    role: Role = Role.MEMBER

    _pw = field_validator("password")(_check_password)

    @field_validator("full_name")
    @classmethod
    def _strip_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be blank.")
        return v


class UserUpdate(BaseModel):
    full_name: FullName | None = None
    role: Role | None = None
    is_active: bool | None = None
    password: Password | None = None

    @field_validator("password")
    @classmethod
    def _pw(cls, v: str | None) -> str | None:
        return _check_password(v) if v is not None else v


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    role: Role
    is_active: bool
    created_at: datetime
    last_login_at: datetime | None


class MeOut(UserOut):
    permissions: list[str]
