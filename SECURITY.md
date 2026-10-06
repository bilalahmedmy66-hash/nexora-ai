# SECURITY

## Never commit

`.env`, API keys, passwords, tokens, database credentials, private certificates. `.gitignore` excludes these; check `git status` before every commit.

If a secret is committed by mistake: rotate it immediately (removing it from history is not enough).

## Controls

| Control | Status |
|---------|--------|
| Password hashing (argon2) | TESTED |
| Password policy (10+ chars, letter and number) | TESTED |
| JWT access and refresh tokens, type-checked | TESTED |
| Role-based permissions on every endpoint | TESTED |
| Input validation (Pydantic) on every endpoint | TESTED |
| Audit logging of logins and user changes | TESTED |
| No user enumeration on login (same error, similar timing) | TESTED |
| Deactivated users lose access immediately | TESTED |
| Production refuses weak JWT secret | IMPLEMENTED |
| Secrets via environment only | IMPLEMENTED |
| CORS allowlist | IMPLEMENTED (not yet tested) |
| Refresh token revocation / logout | PLANNED |
| Login rate limiting and lockout | PLANNED |
| Security headers, HTTPS enforcement | PLANNED |
| Dependency scanning | PLANNED |

## Reporting a vulnerability

Open a private security advisory on the GitHub repository, or email bilalahmedmy66@gmail.com.
