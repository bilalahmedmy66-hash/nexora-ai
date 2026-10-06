from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.user import User


def record(
    db: Session,
    action: str,
    *,
    actor: User | None = None,
    actor_email: str | None = None,
    entity_type: str | None = None,
    entity_id: int | str | None = None,
    details: dict | None = None,
    ip: str | None = None,
) -> AuditLog:
    """Add an audit entry to the session. The caller commits, so the entry is
    saved atomically with the change it describes."""
    entry = AuditLog(
        action=action,
        actor_id=actor.id if actor else None,
        actor_email=actor.email if actor else actor_email,
        entity_type=entity_type,
        entity_id=str(entity_id) if entity_id is not None else None,
        details=details,
        ip_address=ip,
    )
    db.add(entry)
    return entry


def list_logs(
    db: Session,
    *,
    page: int,
    page_size: int,
    action: str | None = None,
    actor_id: int | None = None,
) -> tuple[list[AuditLog], int]:
    q = select(AuditLog)
    if action:
        q = q.where(AuditLog.action == action)
    if actor_id is not None:
        q = q.where(AuditLog.actor_id == actor_id)
    total = db.scalar(select(func.count()).select_from(q.subquery())) or 0
    rows = db.scalars(
        q.order_by(AuditLog.created_at.desc(), AuditLog.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return list(rows), total
