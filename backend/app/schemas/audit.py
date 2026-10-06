from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    actor_id: int | None
    actor_email: str | None
    action: str
    entity_type: str | None
    entity_id: str | None
    details: dict | None
    ip_address: str | None
