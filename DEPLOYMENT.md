# DEPLOYMENT

_Planning only. Finalized in Phase 8._

- Database: PostgreSQL, migrated with Alembic.
- Backend: containerized FastAPI behind a reverse proxy with HTTPS.
- Frontend: static build served from a CDN or the reverse proxy.
- Config: environment variables only (see `.env.example`).
- Required before go-live: security checklist in SECURITY.md complete, backups configured, tests passing in CI.
