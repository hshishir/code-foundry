from pathlib import Path

from sqlalchemy.orm import Session

from agents.base import AgentResult, FakeAgent
from app.core.enums import FeatureStatus, SessionPersona
from app.db.models import Feature
from app.services import features as feature_service
from workspace.paths import ensure_workspace, implementation_path, story_path


class FakeCoder(FakeAgent):
    persona = SessionPersona.CODER

    def run(
        self,
        db: Session,
        feature: Feature,
        workspace_root: Path | str | None = None,
    ) -> AgentResult:
        ensure_workspace(workspace_root)
        session = self.create_running_session(db, feature)
        spec_path = story_path(feature.id, workspace_root)
        spec_note = (
            f"Read spec at {spec_path}"
            if spec_path.exists()
            else f"Spec not found at {spec_path}"
        )
        output_path = implementation_path(feature.id, workspace_root)
        output_path.write_text(
            "\n".join(
                [
                    f"# Implementation {feature.id}: {feature.title}",
                    "",
                    f"Feature ID: {feature.id}",
                    "",
                    "## Summary",
                    "A deterministic fake implementation artifact was produced.",
                    "",
                    "## Spec Reference",
                    spec_note,
                    "",
                ]
            ),
            encoding="utf-8",
        )
        feature_service.update_feature_status(db, feature, FeatureStatus.IMPLEMENTED)
        self.complete_session(
            db,
            session,
            f"Fake coder wrote implementation to {output_path}",
        )
        return AgentResult(
            persona=self.persona,
            feature_id=feature.id,
            artifact_path=output_path,
            summary=f"coder advanced feature {feature.id} to implemented",
        )

