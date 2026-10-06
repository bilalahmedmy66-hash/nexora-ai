# API

_No endpoints exist yet._

## Conventions (apply from Phase 2)

- Base path: `/api/v1`
- JSON in and out; Pydantic validation; consistent error shape:

```json
{ "error": { "code": "validation_error", "message": "Human-readable summary", "details": [] } }
```

- Auth: `Authorization: Bearer <JWT>`
- List endpoints: pagination (`page`, `page_size`), sorting (`sort`), filtering by field, and search (`q`).
- Every mutating endpoint checks permissions and writes an audit log entry.

## Endpoint reference

| Method | Path | Status |
|--------|------|--------|
| (none yet) | | |
