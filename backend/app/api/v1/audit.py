from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.permissions import Permission
from app.db.session import get_db
from app.models.user import User
from app.schemas.audit import AuditLogOut
from app.schemas.common import Page
from app.services import audit_service

router = APIRouter(prefix="/audit-logs", tags=["audit"])


@router.get("", response_model=Page[AuditLogOut])
def list_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    action: str | None = Query(None, max_length=100),
    actor_id: int | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission(Permission.AUDIT_READ)),
):
    rows, total = audit_service.list_logs(
        db, page=page, page_size=page_size, action=action, actor_id=actor_id
    )
    return Page[AuditLogOut](items=rows, total=total, page=page, page_size=page_size)
