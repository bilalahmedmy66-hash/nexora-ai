# BUILD_LOG

## 2026-10-06, Phase 0: Git setup
- Verified Git 2.54.0, configured identity, initialized repo on `main`, added `origin` (github.com/bilalahmedmy66-hash/nexora-ai).
- Lesson: run PowerShell commands from `C:\Users\<you>\projects`, not `C:\Windows\System32`.

## 2026-10-06, Phase 1: Foundation
- Added `.gitignore`, `.env.example`, `LICENSE` (MIT).
- Added README, PROJECT_STATE, BUILD_LOG, ARCHITECTURE, SETUP, API, SECURITY, DEPLOYMENT.
- Added design tokens with light, dark, and system themes.
- Decisions: FastAPI + React/TS stack; SQLite in dev, PostgreSQL in prod; AI layer provider-agnostic with a labeled mock.

## 2026-10-06, Phase 1 pushed
- Repo created on GitHub and Phase 1 pushed (commit 870c3f1, "Initial project architecture").

## 2026-10-06, Phase 2a: Backend auth, users, permissions, audit
- Added FastAPI backend in `backend/` with layered structure: routers (`app/api`), services (`app/services`), models, schemas, core (config, security, permissions, errors).
- Auth: email + password login, argon2 hashing, JWT access (30 min) and refresh (14 days) tokens; token type is checked so a refresh token cannot be used as an access token. Login timing does not reveal whether an email exists.
- Users: admin-managed (no public signup). List supports search, role/status filters, sorting, pagination. Delete is a soft deactivate so audit history stays intact. Admins cannot demote or deactivate themselves, and the last active admin is protected.
- Roles: admin, manager, member, viewer, with a central permission map.
- Audit log: every login, failed login, and user change is recorded in the same transaction as the change. Passwords are never stored in audit details.
- Consistent error shape `{"error": {"code", "message", "details"}}`.
- Alembic migration `0001` creates `users` and `audit_logs`; `alembic check` reports no drift.
- Tests: 29 pytest tests (auth, permissions, users, audit) pass on SQLite. Ruff lint is clean.
- Decision: custom `UTCDateTime` column type so timestamps are timezone-aware UTC on SQLite and PostgreSQL.
