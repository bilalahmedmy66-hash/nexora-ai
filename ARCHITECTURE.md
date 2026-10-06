# ARCHITECTURE

_Status: design only. Nothing below is implemented yet._

## Layers (every feature must implement all of them)

UI -> Frontend logic -> API -> Backend service -> Database, with Permissions, Validation, Error handling, Audit logging, and Tests applied across the stack.

## Repository layout

```text
backend/    FastAPI app, models, services, migrations, tests
frontend/   React + TypeScript app, design system, tests
docs/       Extra design notes
```

## Backend rules

- Routers stay thin; business logic lives in services.
- Every write goes through validation (Pydantic), a permission check, and an audit log entry.
- Schema changes only through Alembic migrations.

## AI layer

- `AIProvider` interface with implementations: Claude, OpenAI, and `MockProvider` (clearly labeled).
- The agent exposes tools that call the same services as the UI, so it obeys the same permissions.
- The UI shows only safe, high-level execution steps (never hidden reasoning).

## Frontend rules

- One design system (`frontend/src/styles/tokens.css`) drives color, type, spacing, radius, and motion.
- Themes: light, dark, system. Accessibility and responsiveness are part of "done".
