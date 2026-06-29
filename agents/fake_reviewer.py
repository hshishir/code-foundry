from pathlib import Path

from sqlalchemy.orm import Session

from agents.base import AgentResult, FakeAgent
from app.core.enums import FeatureStatus, SessionPersona
from app.db.models import Feature
from app.services import features as feature_service
from workspace.paths import ensure_workspace, implementation_path, review_path


class FakeReviewer(FakeAgent):
    persona = SessionPersona.REVIEWER

    def run(
        self,
        db: Session,
        feature: Feature,
        workspace_root: Path | str | None = None,
    ) -> AgentResult:
        ensure_workspace(workspace_root)
        session = self.create_running_session(db, feature)
        source_path = implementation_path(feature.id, workspace_root)
        source_note = (
            f"Reviewed implementation at {source_path}"
            if source_path.exists()
            else f"Implementation artifact not found at {source_path}"
        )
        output_path = review_path(feature.id, workspace_root)
        output_path.write_text(
            "\n".join(
                [
                    f"# Review {feature.id}: {feature.title}",
                    "",
                    f"Feature ID: {feature.id}",
                    "",
                    "Decision: approved",
                    "",
                    "## Notes",
                    source_note,
                    "- Deterministic fake reviewer approves this artifact.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        feature_service.update_feature_status(db, feature, FeatureStatus.REVIEWED)
        self.complete_session(
            db,
            session,
            f"Fake reviewer wrote review to {output_path}",
        )
        return AgentResult(
            persona=self.persona,
            feature_id=feature.id,
            artifact_path=output_path,
            summary=f"reviewer advanced feature {feature.id} to reviewed",
        )

