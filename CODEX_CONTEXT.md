# Code Foundry Codex Context

Use this file as the reusable Codex context prompt when continuing this project on another machine or in a fresh Codex session. Update it after major changes so the next session starts with the right project memory.

## Copy-Paste Prompt

```text
You are helping me work on Code Foundry, a modular agent-workflow platform in the repository named `code-foundry`.

Current project state:
- Phase 0 is complete: FastAPI JSON API for features and sessions.
- Phase 0.5 is complete: polished server-rendered dashboard UI under `app/web/`.
- Phase 1 is complete: deterministic fake local agents and a minimal orchestrator runner.

Core stack:
- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- SQLite for local development
- Pydantic
- Jinja2 templates for the dashboard
- Vanilla JavaScript only
- Handcrafted modular CSS only
- pytest
- uv for dependency management
- `pyproject.toml` and `uv.lock`

Important constraints:
- Do not add LLM calls yet.
- Do not add OpenAI, Anthropic, LangChain, LangGraph, Docker, Kubernetes, GKE, GitHub PR integration, queues, or background workers yet.
- Do not add React, Vue, Svelte, Next.js, Tailwind, Bootstrap, or frontend build tooling.
- Keep the app local, deterministic, modular, and testable.
- Preserve existing API and dashboard behavior unless I explicitly ask to change it.
- Prefer small, boring functions and reuse existing services/enums/models.

Current architecture:
- `app/api/routes/` contains JSON API routes for health, features, and sessions.
- `app/web/` contains the server-rendered dashboard routes, templates, static CSS, and vanilla JS.
- `app/core/enums.py` contains feature/session enums.
- `app/db/` contains SQLAlchemy database setup and models.
- `app/schemas/` contains Pydantic schemas.
- `app/services/` contains feature/session business logic.
- `agents/` contains deterministic fake designer, coder, and reviewer agents.
- `orchestrator/` contains workflow decision logic and CLI runner.
- `workspace/` contains local workspace path helpers.
- `tests/` contains API, dashboard, agent, and workflow tests.

Current workflow behavior:
- Feature statuses: `idea`, `spec_ready`, `implementing`, `implemented`, `reviewed`, `blocked`.
- Session personas: `designer`, `coder`, `reviewer`.
- Session statuses: `pending`, `running`, `completed`, `failed`.
- If a feature is `idea`, the fake designer writes a spec and marks it `spec_ready`.
- If a feature is `spec_ready`, the fake coder writes an implementation artifact and marks it `implemented`.
- If a feature is `implemented`, the fake reviewer writes a review artifact and marks it `reviewed`.
- If a feature is `reviewed` or `blocked`, the orchestrator does nothing.
- `implementing` exists but is intentionally not used yet.

Fake artifacts are written under:
- `.local_workspaces/default/docs/story_<feature_id>.md`
- `.local_workspaces/default/artifacts/implementation_<feature_id>.md`
- `.local_workspaces/default/artifacts/review_<feature_id>.md`

Important commands:
- Install/sync dependencies: `uv sync`
- Run tests: `uv run pytest`
- Run the app/dashboard: `uv run uvicorn app.main:app --reload`
- Open dashboard: `http://127.0.0.1:8000/`
- Run oldest eligible workflow step: `uv run code-foundry run-once`
- Run one workflow step for a feature: `uv run code-foundry run-feature 1`

Recent naming decision:
- The CLI command should be `code-foundry`, matching the repository name.
- Do not refer to the CLI as `agentfoundry`.

When you start work:
1. Inspect the current repo state before editing.
2. Keep JSON API code under `app/api/`.
3. Keep dashboard code under `app/web/`.
4. Keep deterministic agent code under `agents/`.
5. Keep orchestration code under `orchestrator/`.
6. Keep local artifact path behavior under `workspace/`.
7. Run `uv run pytest` after implementation and fix failures.

If I ask for the next phase, propose a small scoped plan first, then implement only that phase.
```

## Maintenance Notes

Update this file when:
- A new phase is completed.
- CLI commands change.
- Data models or statuses change.
- New integrations are intentionally added.
- Project constraints change.
- The README gains important setup or usage details.

Keep the copy-paste prompt factual and concise. It should describe what exists now, not aspirational features that have not been implemented yet.
