from pathlib import Path

from sqlalchemy.orm import Session

from agents.base import AgentResult, FakeAgent
from app.core.enums import FeatureStatus, SessionPersona
from app.db.models import Feature
from app.services import features as feature_service
from workspace.paths import ensure_workspace, story_path


class FakeDesigner(FakeAgent):
    persona = SessionPersona.DESIGNER

    def run(
        self,
        db: Session,
        feature: Feature,
        workspace_root: Path | str | None = None,
    ) -> AgentResult:
        ensure_workspace(workspace_root)
        session = self.create_running_session(db, feature)
        output_path = story_path(feature.id, workspace_root)
        output_path.write_text(
            "\n".join(
                [
                    f"# Story {feature.id}: {feature.title}",
                    "",
                    f"Feature ID: {feature.id}",
                    "",
                    "## Description",
                    feature.description,
                    "",
                    "## Acceptance Criteria",
                    "- Placeholder: define deterministic acceptance criteria.",
                    "",
                    "## Implementation Notes",
                    "- Placeholder: document constraints for the fake coder.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        feature_service.update_feature_status(db, feature, FeatureStatus.SPEC_READY)
        self.complete_session(
            db,
            session,
            f"Fake designer wrote spec to {output_path}",
        )
        return AgentResult(
            persona=self.persona,
            feature_id=feature.id,
            artifact_path=output_path,
            summary=f"designer advanced feature {feature.id} to spec_ready",
        )

