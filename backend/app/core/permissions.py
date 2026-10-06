"""Role-based permissions. Roles are stored on the user; permissions are defined here.

Add new permission strings as modules are built (e.g. "leads:write").
"""

from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    VIEWER = "viewer"


class Permission(StrEnum):
    USERS_READ = "users:read"
    USERS_WRITE = "users:write"
    AUDIT_READ = "audit:read"


ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.ADMIN: frozenset(Permission),
    Role.MANAGER: frozenset({Permission.USERS_READ}),
    Role.MEMBER: frozenset(),
    Role.VIEWER: frozenset(),
}


def has_permission(role: str, permission: Permission) -> bool:
    try:
        return permission in ROLE_PERMISSIONS[Role(role)]
    except ValueError:
        return False


def permissions_for(role: str) -> list[str]:
    try:
        return sorted(p.value for p in ROLE_PERMISSIONS[Role(role)])
    except ValueError:
        return []
