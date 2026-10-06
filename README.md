# Nexora AI

**The Agentic AI Business Operating System**

CRM + Sales + Customer Service + Marketing + Projects + Automation + Analytics + Knowledge + Integrations + AI Agents, with an AI agent that can operate the platform through natural language.

> **Status:** Phase 1 (Foundation). No application features exist yet. See [PROJECT_STATE.md](PROJECT_STATE.md) for the honest, current status of every module.

## Resuming work (new developer or new Claude session)

1. Clone the repo and read [PROJECT_STATE.md](PROJECT_STATE.md) ("Resume here" section).
2. Read [BUILD_LOG.md](BUILD_LOG.md) for what changed and why.
3. Follow [SETUP.md](SETUP.md) to run the project.
4. Continue from the next unfinished step. Never restart from zero.

## Planned stack

React + TypeScript + Vite, Tailwind, FastAPI, SQLAlchemy + Alembic, SQLite (dev) / PostgreSQL (prod), JWT auth with role-based permissions, provider-agnostic AI layer (Claude, OpenAI, labeled mock).

## Documentation

| File | Purpose |
|------|---------|
| [PROJECT_STATE.md](PROJECT_STATE.md) | Source of truth for progress and what to do next |
| [BUILD_LOG.md](BUILD_LOG.md) | Chronological log of phases and decisions |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design and layering rules |
| [SETUP.md](SETUP.md) | Local setup instructions |
| [API.md](API.md) | API conventions and endpoint reference |
| [SECURITY.md](SECURITY.md) | Security policy and controls |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment plan |

## License

MIT. See [LICENSE](LICENSE).
