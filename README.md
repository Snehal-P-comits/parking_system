# Smart Parking Entry/Exit Logging System

Production-style backend built with FastAPI and SQLite using a modular monolith architecture.

## Stack
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic
- Uvicorn

## Architecture
The system is structured as reusable modules with clear boundaries:
- `app/core`: configuration, constants, database/session setup
- `app/modules/passkey`: reusable passkey component (framework and ORM agnostic)
- `app/modules/vehicle`: vehicle domain model, repository, service, routes
- `app/modules/parking`: parking session model, repository, service, routes
- `app/shared`: cross-cutting validators, exceptions, response contracts, utilities

### Boundary Rules
- Routes are thin and call services only.
- Services hold all business logic and orchestration.
- Repositories hold all database access concerns.
- Shared/passkey components are reusable and loosely coupled.

## Features
- Vehicle Entry:
  - create/update vehicle record
  - generate unique numeric passkey
  - create ACTIVE parking session with entry timestamp
- Vehicle Exit:
  - validate license plate + passkey
  - close active session with exit timestamp
  - transition session status to EXITED
- Queries:
  - list all ACTIVE vehicles/sessions
  - fetch complete parking history

## API Endpoints
- `POST /api/v1/parking/entry`
- `POST /api/v1/parking/exit`
- `GET /api/v1/parking/active`
- `GET /api/v1/parking/history`
- `POST /api/v1/vehicles`

## Run Locally (with uv)
From `parking_system/`:

1) Create virtual environment:
```bash
uv venv
```

2) Install/sync dependencies:
```bash
uv sync
```

3) Start server:
```bash
uv run uvicorn app.main:app --reload
```

Server runs at `http://127.0.0.1:8000`.

## Configuration
Environment variables are loaded via `app/core/config.py`:
- `DATABASE_URL` (default: `sqlite:///./parking.db`)
- `API_PREFIX` (default: `/api/v1`)
- `PASSKEY_LENGTH` (default: `4`)
- `PASSKEY_MAX_RETRIES` (default: `25`)

## Scalability Notes
The current design is intentionally migration-friendly:
- one `Vehicle` can own multiple `ParkingSession` records
- repository contracts isolate ORM/dialect specifics
- passkey module supports future hash strategy and expiry strategy
- service boundaries are ready for future JWT/RBAC, payments, analytics, audit logs, and multi-lot expansion
