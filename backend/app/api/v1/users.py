from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.api.deps import client_ip, require_permission
from app.core.permissions import Permission, Role
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import Page
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=Page[UserOut])
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: str | None = Query(None, max_length=100),
    role: Role | None = None,
    is_active: bool | None = None,
    sort: str = "-created_at",
    db: Session = Depends(get_db),
    _: User = Depends(require_permission(Permission.USERS_READ)),
):
    rows, total = user_service.list_users(
        db,
        page=page,
        page_size=page_size,
        q=q,
        role=role.value if role else None,
        is_active=is_active,
        sort=sort,
    )
    return Page[UserOut](items=rows, total=total, page=page, page_size=page_size)


@router.post("", response_model=UserOut, status_code=201)
def create_user(
    body: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    actor: User = Depends(require_permission(Permission.USERS_WRITE)),
):
    return user_service.create_user(db, body, actor, client_ip(request))


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission(Permission.USERS_READ)),
):
    return user_service.get_or_404(db, user_id)


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    body: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    actor: User = Depends(require_permission(Permission.USERS_WRITE)),
):
    user = user_service.get_or_404(db, user_id)
    return user_service.update_user(db, user, body, actor, client_ip(request))


@router.delete("/{user_id}", response_model=UserOut)
def deactivate_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    actor: User = Depends(require_permission(Permission.USERS_WRITE)),
):
    """Deactivates the user (soft delete) so audit history stays intact."""
    user = user_service.get_or_404(db, user_id)
    return user_service.deactivate_user(db, user, actor, client_ip(request))
