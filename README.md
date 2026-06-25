# Code Foundry

Code Foundry is planned as a modular agent-workflow platform that can eventually take work from idea to spec, code, review, quality gates, Docker images, and Kubernetes/GKE agent execution.

Phase 0 plus UI is deliberately smaller than the long-term platform: it provides the workflow API spine for features and sessions plus a server-rendered dashboard. There are no LLM calls, real agents, auth, background workers, Docker, Kubernetes, GitHub integration, or Alembic migrations yet.

## Requirements

- Python 3.12
- uv

## Setup

Create and populate the virtual environment:

```bash
uv sync
```

`uv sync` creates a local `.venv` when needed and installs the runtime and development dependencies from `pyproject.toml` and `uv.lock`.

## Run the App

```bash
uv run uvicorn app.main:app --reload
```

Open the dashboard at:

```text
http://127.0.0.1:8000/
```

The dashboard is built with FastAPI, Jinja2 templates, vanilla JavaScript, and handcrafted CSS under `app/web/`.

The API exposes:

- `GET /health`
- `POST /features`
- `GET /features`
- `GET /features/{feature_id}`
- `PATCH /features/{feature_id}/status`
- `POST /sessions`
- `GET /sessions`
- `GET /sessions/{session_id}`
- `PATCH /sessions/{session_id}/status`

## Run Tests

```bash
uv run pytest
```

Tests use an isolated in-memory SQLite database and cover the Phase 0 health, feature, and session endpoints.
