# BUILD_LOG

## 2026-10-06, Phase 0: Git setup
- Verified Git 2.54.0, configured identity, initialized repo on `main`, added `origin` (github.com/bilalahmedmy66-hash/nexora-ai).
- Lesson: run PowerShell commands from `C:\Users\<you>\projects`, not `C:\Windows\System32`.

## 2026-10-06, Phase 1: Foundation
- Added `.gitignore`, `.env.example`, `LICENSE` (MIT).
- Added README, PROJECT_STATE, BUILD_LOG, ARCHITECTURE, SETUP, API, SECURITY, DEPLOYMENT.
- Added design tokens with light, dark, and system themes.
- Decisions: FastAPI + React/TS stack; SQLite in dev, PostgreSQL in prod; AI layer provider-agnostic with a labeled mock.
- Tested: nothing executable yet.
