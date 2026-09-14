# MOIL AI — Unified Backend

This is the real M4 backend: authentication, database, mine management,
your original M2 exploration engine, the M3 production module, and the
combined AI recommendation engine — all in one FastAPI app.

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env             # then edit SECRET_KEY inside .env

python seed_demo_user.py         # creates a demo login + the database file

uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.
Interactive docs (auto-generated): `http://127.0.0.1:8000/docs`

## Demo login

```
email:    industrialist@moil.demo
password: demo1234
```

## What changed from your original M2-only backend

- `m2_exploration/` is copied in **completely untouched** — same engine, same
  services, same data. It's now mounted as a router (`routers/exploration.py`)
  instead of running as its own standalone app.
- Every route except `/`, `/health`, `/auth/register`, `/auth/login` now
  requires a Bearer token (login first, then send
  `Authorization: Bearer <token>` on subsequent requests — this is what
  `js/api.js` on the frontend does automatically after login).
- New: `/mines`, `/production/*`, `/ai/recommendations`.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/auth/register` | Create an account |
| POST | `/auth/login` | Log in, get a JWT |
| GET/POST/DELETE | `/mines` | Manage saved mine sites |
| POST | `/exploration/analyze` | Run your M2 engine on a location |
| GET | `/exploration/history/{mine_id}` | Past exploration runs for a mine |
| GET | `/production/history` | Historical monthly production (IBM data) |
| GET | `/production/forecast` | 2026 forecast (Seasonal Naive model) |
| GET | `/production/summary` | KPI dashboard numbers |
| GET | `/production/shortfall` | Forecast vs approved target |
| POST | `/production/target` | Set an approved monthly target |
| GET | `/production/alerts` | Current production/risk alerts |
| POST | `/ai/recommendations` | Combined Exploration + Production AI feed |

## Moving to a real deployment later

1. Swap `DATABASE_URL` in `.env` to a real Postgres instance — no code changes needed.
2. Set a strong `SECRET_KEY` in `.env`.
3. Add your deployed frontend's URL to `EXTRA_CORS_ORIGINS` in `.env`.
4. Deploy this `backend/` folder to any Python host (Render, Railway, a VM, etc.)
   and point the frontend's `js/config.js` `API_BASE_URL` at it.
