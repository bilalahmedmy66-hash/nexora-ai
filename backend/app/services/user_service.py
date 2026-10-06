from datetime import UTC, datetime

from sqlalchemy import asc, desc, func, or_, select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.permissions import Role
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services import audit_service

SORTABLE = {
    "created_at": User.created_at,
    "email": User.email,
    "full_name": User.full_name,
    "role": User.role,
    "last_login_at": User.last_login_at,
}


def get_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.lower()))


def get_or_404(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if not user:
        raise AppError(404, "user_not_found", "User not found.")
    return user


def list_users(
    db: Session,
    *,
    page: int,
    page_size: int,
    q: str | None,
    role: str | None,
    is_active: bool | None,
    sort: str,
) -> tuple[list[User], int]:
    stmt = select(User)
    if q:
        like = f"%{q.lower()}%"
        stmt = stmt.where(or_(func.lower(User.email).like(like), func.lower(User.full_name).like(like)))
    if role:
        stmt = stmt.where(User.role == role)
    if is_active is not None:
        stmt = stmt.where(User.is_active == is_active)

    desc_order = sort.startswith("-")
    column = SORTABLE.get(sort.lstrip("-"))
    if column is None:
        raise AppError(
            422,
            "invalid_sort",
            f"Sort must be one of: {', '.join(SORTABLE)} (prefix with - for descending).",
        )
    stmt = stmt.order_by(desc(column) if desc_order else asc(column), User.id)

    total = db.scalar(select(func.count()).select_from(stmt.order_by(None).subquery())) or 0
    rows = db.scalars(stmt.offset((page - 1) * page_size).limit(page_size)).all()
    return list(rows), total


def create_user(db: Session, data: UserCreate, actor: User | None, ip: str | None = None) -> User:
    email = data.email.lower()
    if get_by_email(db, email):
        raise AppError(409, "email_taken", "A user with this email already exists.")
    user = User(
        email=email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        role=data.role.value,
    )
    db.add(user)
    db.flush()
    audit_service.record(
        db,
        "user.created",
        actor=actor,
        entity_type="user",
        entity_id=user.id,
        details={"email": email, "role": user.role},
        ip=ip,
    )
    db.commit()
    return user


def update_user(db: Session, user: User, data: UserUpdate, actor: User, ip: str | None = None) -> User:
    changes: dict = {}
    if data.full_name is not None and data.full_name.strip() != user.full_name:
        changes["full_name"] = data.full_name.strip()
    if data.role is not None and data.role.value != user.role:
        changes["role"] = data.role.value
    if data.is_active is not None and data.is_active != user.is_active:
        changes["is_active"] = data.is_active

    if user.id == actor.id and ("role" in changes or changes.get("is_active") is False):
        raise AppError(
            400,
            "cannot_modify_self",
            "You cannot change your own role or deactivate yourself.",
        )

    # Never leave the system without an active admin.
    removing_admin = (
        user.role == Role.ADMIN.value
        and user.is_active
        and (changes.get("role", user.role) != Role.ADMIN.value or changes.get("is_active") is False)
    )
    if removing_admin and _active_admin_count(db) <= 1:
        raise AppError(400, "last_admin", "At least one active admin is required.")

    for field, value in changes.items():
        setattr(user, field, value)
    audit_details = dict(changes)
    if data.password is not None:
        user.hashed_password = hash_password(data.password)
        audit_details["password"] = "reset"

    if audit_details:
        audit_service.record(
            db,
            "user.updated",
            actor=actor,
            entity_type="user",
            entity_id=user.id,
            details=audit_details,
            ip=ip,
        )
    db.commit()
    return user


def deactivate_user(db: Session, user: User, actor: User, ip: str | None = None) -> User:
    if user.id == actor.id:
        raise AppError(
            400,
            "cannot_modify_self",
            "You cannot change your own role or deactivate yourself.",
        )
    if user.role == Role.ADMIN.value and user.is_active and _active_admin_count(db) <= 1:
        raise AppError(400, "last_admin", "At least one active admin is required.")
    if user.is_active:
        user.is_active = False
        audit_service.record(
            db,
            "user.deactivated",
            actor=actor,
            entity_type="user",
            entity_id=user.id,
            ip=ip,
        )
        db.commit()
    return user


def mark_login(db: Session, user: User) -> None:
    user.last_login_at = datetime.now(UTC)


def _active_admin_count(db: Session) -> int:
    return (
        db.scalar(
            select(func.count())
            .select_from(User)
            .where(User.role == Role.ADMIN.value, User.is_active.is_(True))
        )
        or 0
    )
