# API

Base path: `/api/v1`. Interactive docs: `http://localhost:8000/docs` while the server runs.

## Conventions

- JSON in and out. Auth: `Authorization: Bearer <access_token>`.
- Errors always look like:

```json
{ "error": { "code": "validation_error", "message": "The request data is invalid.", "details": [{ "field": "email", "message": "..." }] } }
```

- Lists return `{ "items": [], "total": 0, "page": 1, "page_size": 20 }`.
- Timestamps are ISO 8601 in UTC.
- Every mutating endpoint checks permissions and writes an audit log entry.

## Endpoints

| Method | Path | Permission | Status |
|--------|------|------------|--------|
| GET | `/health` | public | TESTED |
| POST | `/auth/login` | public | TESTED |
| POST | `/auth/refresh` | refresh token | TESTED |
| GET | `/auth/me` | signed in | TESTED |
| GET | `/users` | `users:read` | TESTED |
| POST | `/users` | `users:write` | TESTED |
| GET | `/users/{id}` | `users:read` | TESTED |
| PATCH | `/users/{id}` | `users:write` | TESTED |
| DELETE | `/users/{id}` | `users:write` (deactivates) | TESTED |
| GET | `/audit-logs` | `audit:read` | TESTED |

## Query parameters

`GET /users`: `page`, `page_size` (max 100), `q` (name or email), `role`, `is_active`, `sort` (`created_at`, `email`, `full_name`, `role`, `last_login_at`; prefix `-` for descending, default `-created_at`).

`GET /audit-logs`: `page`, `page_size` (max 200), `action`, `actor_id`.

## Error codes

`validation_error` (422), `invalid_credentials` (401), `unauthorized` (401), `invalid_token` (401), `forbidden` (403), `user_not_found` (404), `email_taken` (409), `cannot_modify_self` (400), `last_admin` (400), `invalid_sort` (422), `internal_error` (500).

## Roles

| Role | Permissions |
|------|-------------|
| admin | users:read, users:write, audit:read |
| manager | users:read |
| member | none yet |
| viewer | none yet |
