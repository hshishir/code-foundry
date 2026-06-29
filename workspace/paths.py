from pathlib import Path

from app.core.config import settings


def workspace_root(root: Path | str | None = None) -> Path:
    return Path(root or settings.workspace_root)


def docs_dir(root: Path | str | None = None) -> Path:
    return workspace_root(root) / "docs"


def artifacts_dir(root: Path | str | None = None) -> Path:
    return workspace_root(root) / "artifacts"


def story_path(feature_id: int, root: Path | str | None = None) -> Path:
    return docs_dir(root) / f"story_{feature_id}.md"


def implementation_path(feature_id: int, root: Path | str | None = None) -> Path:
    return artifacts_dir(root) / f"implementation_{feature_id}.md"


def review_path(feature_id: int, root: Path | str | None = None) -> Path:
    return artifacts_dir(root) / f"review_{feature_id}.md"


def ensure_workspace(root: Path | str | None = None) -> Path:
    base = workspace_root(root)
    docs_dir(base).mkdir(parents=True, exist_ok=True)
    artifacts_dir(base).mkdir(parents=True, exist_ok=True)
    return base

