# SETUP

## Prerequisites (Windows)

- Git, Python 3.12+ (3.13 works), Node.js 20+ (needed from Phase 2b)

## Clone

```powershell
cd $HOME\projects
git clone https://github.com/bilalahmedmy66-hash/nexora-ai.git
cd nexora-ai
```

## Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-dev.txt

# Environment file lives in the repo root and is never committed
copy ..\.env.example ..\.env

# Create the database tables
.\.venv\Scripts\python -m alembic upgrade head

# Create your first admin (you will be prompted for a password)
.\.venv\Scripts\python -m app.cli create-admin --email you@example.com --name "Your Name"

# Run the API
.\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs to try the API. Click **Authorize** after logging in via `/auth/login` and pasting the `access_token`.

## Run the tests

```powershell
cd backend
.\.venv\Scripts\python -m pytest -q
```

## Notes

- If you prefer activating the virtual environment: `.\.venv\Scripts\Activate.ps1`. If PowerShell blocks it, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use the explicit `.\.venv\Scripts\python` form above.
- The local database file `backend/nexora.db` is git-ignored.
- In production, `JWT_SECRET` must be a random string of 32+ characters or the server refuses to start.

## Frontend

Coming in Phase 2b.

## Frontend

Open a **second** PowerShell window (the backend keeps running in the first one):

```powershell
cd $HOME\projects\nexora-ai\frontend
npm install
npm run dev
```

Open http://localhost:5173 and sign in with your admin account. The dev server forwards `/api` calls to the backend on port 8000, so the backend must be running.

Other commands: `npm test` (run the frontend tests), `npm run build` (type-check and production build), `npm run preview`.
