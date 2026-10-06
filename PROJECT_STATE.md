# PROJECT_STATE

_Last updated: 2026-10-06 (Phase 2a: backend auth)_

## Resume here

**Current phase:** Phase 2a (Backend auth, users, permissions, audit log) complete once committed.
**Next step:** Phase 2b, the frontend: Vite + React + TypeScript app, wire in `frontend/src/styles/tokens.css`, build the app shell (collapsible sidebar, breadcrumbs, command palette, light/dark/system theme switch), login page, and a Users admin page that talks to the API.

A fresh session should: clone the repo, read this file and BUILD_LOG.md, follow SETUP.md to run the backend and tests, then start the "Next step" above.

## Status legend

PLANNED, IN DEVELOPMENT, IMPLEMENTED, TESTED, PRODUCTION READY

Mocks and placeholders must be labeled MOCK in this file and in code.

## Module status

| Module | Status | Notes |
|--------|--------|-------|
| Repo hygiene (.gitignore, .env.example, LICENSE) | IMPLEMENTED | |
| Documentation set | IMPLEMENTED | Keep updated every phase |
| Design tokens (light/dark/system) | IMPLEMENTED | Not yet wired into an app or visually tested |
| Backend scaffold (FastAPI, SQLAlchemy 2, Alembic) | TESTED | 29 automated tests on SQLite; not yet run on PostgreSQL |
| Auth: login, refresh, /me (JWT, argon2) | TESTED | No token revocation or rate limiting yet |
| Users API: list/search/filter/sort/paginate, create, edit, deactivate, admin password reset | TESTED | |
| Roles and permissions (admin, manager, member, viewer) | TESTED | Permission map in `app/core/permissions.py` |
| Audit logging (logins, failed logins, user changes) | TESTED | Read via `GET /api/v1/audit-logs` (admin only) |
| Database migrations | TESTED | `0001` creates users and audit_logs |
| CLI: create-admin | IMPLEMENTED | Interactive password prompt; not covered by automated tests |
| Frontend app and app shell | PLANNED | Phase 2b |
| Login and Users admin UI | PLANNED | Phase 2b |
| CRM: Leads | PLANNED | Phase 3 |
| CRM: Contacts, Accounts, Opportunities | PLANNED | Phase 3 |
| AI provider layer | PLANNED | Phase 4 (mock provider first) |
| Agent orchestration + progress UI | PLANNED | Phase 4 |
| Workflows, tasks, Kanban | PLANNED | Phase 5 |
| Service, Marketing, Projects | PLANNED | Phase 6 |
| Dashboard and analytics | PLANNED | Phase 7 |
| Security hardening, deployment | PLANNED | Phase 8 |

## Known gaps

- Refresh tokens cannot be revoked (logout is client-side only until a token store is added).
- No login rate limiting or account lockout yet.
- No frontend; the API can be explored at `/docs` when the server runs.
- Not tested against PostgreSQL.
