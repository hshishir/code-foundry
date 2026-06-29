# Code Foundry

Code Foundry is planned as a modular agent-workflow platform that can eventually take work from idea to spec, code, review, quality gates, Docker images, and Kubernetes/GKE agent execution.

Phase 1 is still deliberately smaller than the long-term platform: it provides the workflow API spine, a server-rendered dashboard, and deterministic fake local agents that prove idea to spec to implementation to review. There are no LLM calls, real agents, auth, background workers, Docker, Kubernetes, GitHub integration, or Alembic migrations yet.

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

## Run the Fake Orchestrator

Advance the oldest eligible feature by one deterministic workflow step:

```bash
uv run code-foundry run-once
```

Advance a specific feature by one deterministic workflow step:

```bash
uv run code-foundry run-feature 1
```

Phase 1 fake agents are local and deterministic:

- `idea` runs the fake designer and writes `.local_workspaces/default/docs/story_<feature_id>.md`
- `spec_ready` runs the fake coder and writes `.local_workspaces/default/artifacts/implementation_<feature_id>.md`
- `implemented` runs the fake reviewer and writes `.local_workspaces/default/artifacts/review_<feature_id>.md`
- `reviewed` and `blocked` are ignored

No LLMs are used yet.

## Run Tests

```bash
uv run pytest
```

Tests use an isolated in-memory SQLite database and cover the Phase 0 health, feature, and session endpoints.
