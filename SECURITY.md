# SECURITY

## Never commit

`.env`, API keys, passwords, tokens, database credentials, private certificates. `.gitignore` excludes these; check `git status` before every commit.

If a secret is committed by mistake: rotate it immediately (removing it from history is not enough).

## Planned controls

| Control | Status |
|---------|--------|
| Password hashing (argon2 or bcrypt) | PLANNED |
| JWT access and refresh tokens | PLANNED |
| Role-based permissions on every endpoint | PLANNED |
| Input validation on every endpoint | PLANNED |
| Audit logging of all writes | PLANNED |
| Rate limiting | PLANNED |
| CORS allowlist | PLANNED |
| Secrets via environment only | IMPLEMENTED (`.env.example` pattern) |
| Dependency scanning | PLANNED |

## Reporting a vulnerability

Open a private security advisory on the GitHub repository, or email bilalahmedmy66@gmail.com.
