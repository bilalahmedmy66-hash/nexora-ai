# PROJECT_STATE

_Last updated: 2026-10-07 (Phase 2b verified)_

## Resume here

**Current phase:** Phase 2b (Frontend: login, app shell, Users admin) complete once committed.
**Next step:** Phase 3, CRM core: Leads first, full stack (model + migration, API with validation/permissions/audit, list with search/filter/sort/pagination, create/edit/delete, notes, tasks, activity history, tests, UI), then Contacts, Accounts, Opportunities. Also add a Playwright smoke test and cover the Users dialogs with tests when convenient.

A fresh session should: clone the repo, read this file and BUILD_LOG.md, follow SETUP.md to run the backend and tests, then start the "Next step" above.

## Status legend

PLANNED, IN DEVELOPMENT, IMPLEMENTED, TESTED, PRODUCTION READY

Mocks and placeholders must be labeled MOCK in this file and in code.

## Module status

| Module | Status | Notes |
|--------|--------|-------|
| Repo hygiene (.gitignore, .env.example, LICENSE) | IMPLEMENTED | |
| Documentation set | IMPLEMENTED | Keep updated every phase |
| Design tokens (light/dark/system) | IMPLEMENTED | Used by the frontend (`frontend/src/styles/tokens.css`) |
| Backend scaffold (FastAPI, SQLAlchemy 2, Alembic) | TESTED | 29 automated tests on SQLite; not yet run on PostgreSQL |
| Auth: login, refresh, /me (JWT, argon2) | TESTED | No token revocation or rate limiting yet |
| Users API: list/search/filter/sort/paginate, create, edit, deactivate, admin password reset | TESTED | |
| Roles and permissions (admin, manager, member, viewer) | TESTED | Permission map in `app/core/permissions.py` |
| Audit logging (logins, failed logins, user changes) | TESTED | Read via `GET /api/v1/audit-logs` (admin only) |
| Database migrations | TESTED | `0001` creates users and audit_logs |
| CLI: create-admin | IMPLEMENTED | Interactive password prompt; not covered by automated tests |
| Frontend app (React, TypeScript, Vite) | TESTED | 18 Vitest tests (API client, theme, command palette, routing and sign-in); production build passes; walked through in headless Chromium against the real backend |
| App shell: collapsible sidebar, breadcrumbs, command palette (Ctrl+K), light/dark/system theme, responsive drawer | TESTED | Verified: sign-in redirect, command palette, session survives reload, dark theme, mobile layout. Not tested in Firefox or Safari |
| Login page | TESTED | Wrong password, success, and redirect covered |
| Users admin UI (search, role filter, pagination, create, edit, deactivate) | IMPLEMENTED | List rendering verified in a browser against 26 real users. Create, edit and deactivate dialogs are NOT yet covered by automated tests or a browser walkthrough |
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
- Frontend has not been accessibility-audited (keyboard use and labels are built in, but untested with a screen reader).
- Sidebar icons are simple text symbols; a proper icon system is still to do.
- No Audit log screen yet (the API exists).
- Several simultaneous expired requests each try to refresh the session; they are not yet merged into one refresh.
- Tokens are kept in browser localStorage (simple, but readable by any XSS bug); revisit with httpOnly cookies before production.
- Dashboard is a status page, not business widgets (those need CRM data first).
- Not tested against PostgreSQL.
