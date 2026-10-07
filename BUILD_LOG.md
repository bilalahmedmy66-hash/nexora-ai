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

## 2026-10-06, Phase 2a verified and pushed
- 29 backend tests pass on Windows, Python 3.13. Pushed as commit bfecd42. Admin account created locally; password rotated; real JWT/app secrets set in local `.env`.

## 2026-10-06, Phase 2b: Frontend shell
- Added `frontend/` (React 19, TypeScript, Vite, React Router). No UI framework; styling uses `tokens.css` plus `app.css`.
- Login with automatic token refresh on 401; protected routes; sign out.
- App shell: collapsible sidebar (remembered), breadcrumbs, command palette (Ctrl/Cmd+K), light/dark/system theme (remembered), mobile drawer, skip link, visible focus.
- Users page: search (debounced), role filter, pagination, skeleton loading, empty and error states, create/edit dialogs with field-level errors, deactivate confirmation. Buttons only appear if the user has the permission.
- Dev server proxies `/api` to `http://localhost:8000`, so no CORS setup is needed in development.
- Verified: `npm run build` passes (type-check + production build); dev server serves the app and proxies a real login to the backend.

## 2026-10-07, Phase 2b verified
- Added 18 Vitest tests: API client (refresh-on-401, failed refresh signs out, error shape, network error), theme, command palette, routing and sign-in.
- Walked the app through in headless Chromium against the real backend: redirect to sign-in, wrong-password message, sign-in, Users list (26 users, 10 per page), Ctrl+K palette, session survives reload, dark theme, mobile drawer layout. No unexpected console errors.
- Fixes: Sign in button label now centered; Manrope font is bundled via @fontsource-variable/manrope (previously fell back to the system font); type errors in tests caught by `npm run build`, which also type-checks tests.
- Not yet covered: Users create/edit/deactivate dialogs, Firefox/Safari, screen-reader testing.
